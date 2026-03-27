#! /usr/local/bin/python3
"""Tests for the tableio_ods_odfdo module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Optional

from odfdo import Cell, Document, Element, Table
from odfdo.body import Spreadsheet
from odfdo.style import Style
from pytest import CaptureFixture

from tableio.tableio import FileAccess
from tableio.tableio_ods_odfdo import TableIOOdsOdfdo
from tableio.value_type import get_checked_type

from .check_capsys import check_capsys
from .spreadsheet_test_helper import \
    run_box_write_removes_overlapping_filtered_range, \
    run_read_formula_uses_cached_value, \
    run_read_formula_without_cached_value, \
    run_round_trip_dictdata_in_box, \
    run_round_trip_sequential_list_reads, \
    run_table_width_is_widen_only_with_cap, \
    run_update_default_write_starts_after_last_used_row, \
    run_write_dictdata_applies_first_row_format, \
    run_write_fmtdictdata_applies_first_row_format, \
    run_write_formatted_listdata_applies_formatting_and_filter, \
    run_write_multiple_filtered_ranges_keeps_all_ranges, \
    run_write_row_formatted_dictdata_applies_formatting


def _load_document(file_path: Path) -> tuple[Document, Table]:
    """Load one ODS document and return its first table."""
    document = Document(file_path)
    table = document.body.get_table(position=0)
    assert isinstance(table, Table)
    return document, table


def _cell_style_properties(
        document: Document,
        table: Table,
        row: int,
        column: int) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return table-cell and text properties for one styled cell."""
    cell = table.get_cell((column, row), clone=False)
    assert cell.style is not None
    style = document.get_style('table-cell', cell.style)
    assert style is not None
    table_props = get_checked_type(style, Style).get_properties(
        'table-cell') or {}
    text_props = get_checked_type(style, Style).get_properties('text') or {}
    return table_props, text_props


def _filtered_database_ranges(document: Document) -> list[Element]:
    """Return filtered ODS database ranges."""
    spreadsheet = get_checked_type(document.body, Spreadsheet)
    return spreadsheet.get_elements(
        'descendant::table:database-ranges/table:database-range')


def _database_range_addresses(document: Document) -> list[str]:
    """Return target addresses of the ODS database ranges."""
    ret: list[str] = []
    for database_range in _filtered_database_ranges(document):
        address = database_range.get_attribute_string(
            'table:target-range-address')
        assert address is not None
        ret.append(str(address))
    return ret


def _default_table_cell_language(document: Document) -> tuple[str, str]:
    """Return the default ODS table-cell language and country."""
    for style in document.styles.default_styles:
        if style.family != 'table-cell':
            continue
        props = style.get_properties('text') or {}
        language = props.get('fo:language')
        country = props.get('fo:country')
        assert isinstance(language, str)
        assert isinstance(country, str)
        return language, country
    raise AssertionError('Default table-cell style missing.')


def _column_width_cm(document: Document, table: Table,
                     column: int) -> Optional[float]:
    """Return one column width in centimetres from the saved style."""
    odf_column = table.get_column(column)
    if odf_column.style is None:
        return None
    style = document.get_style('table-column', odf_column.style)
    assert style is not None
    properties = get_checked_type(style, Style).get_properties(
        'table-column') or {}
    width_text = properties.get('style:column-width')
    if width_text is None:
        return None
    assert isinstance(width_text, str)
    assert width_text.endswith('cm')
    return float(width_text[:-2])


def _create_formula_document(file_path: Path,
                             cached_value: Optional[int] = None) -> None:
    """Create one ODS file with a formula cell and optional cached value."""
    document = Document('spreadsheet')
    document.body.clear()
    table = Table('Sheet1')
    document.body.append(table)
    table.set_cell((0, 0), Cell(cached_value, formula='of:=1+2'),
                   clone=False)
    table.set_value((1, 0), 'x')
    document.save(file_path)


def _create_update_document(file_path: Path) -> None:
    """Create the starting ODS file used by the UPDATE mode test."""
    document = Document('spreadsheet')
    document.body.clear()
    table = Table('Sheet1')
    document.body.append(table)
    table.set_value((0, 0), 'old')
    table.set_value((1, 0), 'row')
    document.save(file_path)


def _inspect_updated_document(file_path: Path) -> None:
    """Check the ODS file produced by the shared UPDATE mode case."""
    _, table = _load_document(file_path)
    assert table.get_value((0, 0)) == 'old'
    assert table.get_value((1, 0)) == 'row'
    assert table.get_value((0, 1)) is None
    assert table.get_value((1, 1)) is None
    assert table.get_value((0, 2)) == 'new'
    assert table.get_value((1, 2)) == 'row'


def _inspect_formatted_document(file_path: Path) -> None:
    """Check formatting and filtered-range metadata in one ODS file."""
    document, table = _load_document(file_path)
    assert str(table.name) == 'Sheet1'
    assert _database_range_addresses(document) == ['Sheet1.A1:Sheet1.B2']
    _, text_props = _cell_style_properties(document, table, 0, 0)
    table_props, text_props_row = _cell_style_properties(
        document, table, 1, 0)
    assert text_props['fo:font-weight'] == 'bold'
    assert text_props_row['fo:font-style'] == 'italic'
    assert table_props['fo:background-color'] == '#ffff00'


def _inspect_multiple_filters_document(file_path: Path) -> None:
    """Check that sequential filtered writes remain separate ranges."""
    document, table = _load_document(file_path)
    assert str(table.name) == 'Sheet1'
    assert sorted(_database_range_addresses(document)) == [
        'Sheet1.A1:Sheet1.B2',
        'Sheet1.A4:Sheet1.B5'
    ]


def _inspect_table_width_cap_document(file_path: Path) -> None:
    """Check that repeated boxed writes do not shrink the widened column."""
    document, table = _load_document(file_path)
    assert table.get_value((0, 1)) == 'y'
    assert _column_width_cm(document, table, 0) == 12.50


def _inspect_rewrite_box_document(file_path: Path) -> None:
    """Check that overwriting a box removes stale filter metadata."""
    document, _ = _load_document(file_path)
    assert _filtered_database_ranges(document) == []


def _inspect_row_formatted_document(file_path: Path) -> None:
    """Check row formatting copied from FmtDictRow writes."""
    document, table = _load_document(file_path)
    assert str(table.name) == 'Sheet1'
    assert _database_range_addresses(document) == ['Sheet1.A1:Sheet1.B3']
    row2_table_props, row2_text_props = _cell_style_properties(
        document, table, 1, 0)
    row3_table_props, row3_text_props = _cell_style_properties(
        document, table, 2, 0)
    assert row2_text_props['fo:font-weight'] == 'bold'
    assert row2_table_props['fo:background-color'] == '#c6efce'
    assert row3_text_props['fo:font-style'] == 'italic'
    assert row3_table_props['fo:background-color'] == '#ffc7ce'


def _inspect_dict_header_fmt_document(file_path: Path) -> None:
    """Check header formatting produced by dict-data writes."""
    document, table = _load_document(file_path)
    assert table.get_value((0, 0)) == 'name'
    assert table.get_value((1, 0)) == 'active'
    header_table_props, header_text_props = _cell_style_properties(
        document, table, 0, 0)
    assert header_text_props['fo:font-weight'] == 'bold'
    assert header_table_props['fo:background-color'] == '#ffff00'
    assert table.get_cell((0, 1), clone=False).style is None


def _inspect_fmtdict_header_fmt_document(file_path: Path) -> None:
    """Check header and row formatting separation in fmtdict writes."""
    document, table = _load_document(file_path)
    _, header_text_props = _cell_style_properties(document, table, 0, 0)
    data_table_props, data_text_props = _cell_style_properties(
        document, table, 1, 0)
    assert header_text_props['fo:font-weight'] == 'bold'
    assert data_text_props['fo:font-style'] == 'italic'
    assert data_table_props['fo:background-color'] == '#c6efce'


def test_ods_round_trip_sequential_list_reads(
        capsys: CaptureFixture[str]) -> None:
    """Two list sections can be written and then read back sequentially."""
    run_round_trip_sequential_list_reads(TableIOOdsOdfdo, capsys)


def test_ods_round_trip_dictdata_in_box(
        capsys: CaptureFixture[str]) -> None:
    """Dict data can be written into and read back from a box."""
    run_round_trip_dictdata_in_box(TableIOOdsOdfdo, capsys)


def test_ods_update_default_write_starts_after_last_used_row(
        capsys: CaptureFixture[str]) -> None:
    """UPDATE mode appends after the used area with a blank row separator."""
    run_update_default_write_starts_after_last_used_row(
        TableIOOdsOdfdo, '.ods', _create_update_document,
        _inspect_updated_document, capsys)


def test_ods_write_formatted_listdata_applies_formatting_and_filter(
        capsys: CaptureFixture[str]) -> None:
    """Per-cell formatting and one filtered range are written."""
    run_write_formatted_listdata_applies_formatting_and_filter(
        TableIOOdsOdfdo, '.ods', _inspect_formatted_document, capsys)


def test_ods_write_multiple_filtered_ranges_keeps_all_ranges(
        capsys: CaptureFixture[str]) -> None:
    """Sequential filtered writes are kept as separate named ranges."""
    run_write_multiple_filtered_ranges_keeps_all_ranges(
        TableIOOdsOdfdo, '.ods', _inspect_multiple_filters_document,
        capsys)


def test_ods_table_width_is_widen_only_with_cap(
        capsys: CaptureFixture[str]) -> None:
    """Box rewrites keep an already widened column width."""
    run_table_width_is_widen_only_with_cap(
        TableIOOdsOdfdo, '.ods', _inspect_table_width_cap_document,
        capsys)


def test_ods_box_write_removes_overlapping_filtered_range(
        capsys: CaptureFixture[str]) -> None:
    """Rewriting a boxed area removes stale overlapping filter metadata."""
    run_box_write_removes_overlapping_filtered_range(
        TableIOOdsOdfdo, '.ods', _inspect_rewrite_box_document,
        capsys)


def test_ods_write_row_formatted_dictdata_applies_formatting(
        capsys: CaptureFixture[str]) -> None:
    """Row formatting for dict rows is copied to each written cell."""
    run_write_row_formatted_dictdata_applies_formatting(
        TableIOOdsOdfdo, '.ods', _inspect_row_formatted_document,
        capsys)


def test_ods_write_dictdata_applies_first_row_format(
        capsys: CaptureFixture[str]) -> None:
    """Dict header cells can be formatted with first_row_format."""
    run_write_dictdata_applies_first_row_format(
        TableIOOdsOdfdo, '.ods', _inspect_dict_header_fmt_document,
        capsys)


def test_ods_write_fmtdictdata_applies_first_row_format(
        capsys: CaptureFixture[str]) -> None:
    """Formatted dict writes keep header and row formatting separate."""
    run_write_fmtdictdata_applies_first_row_format(
        TableIOOdsOdfdo, '.ods', _inspect_fmtdict_header_fmt_document,
        capsys)


def test_ods_read_formula_uses_cached_value(
        capsys: CaptureFixture[str]) -> None:
    """A formula cell is read as its cached value."""
    run_read_formula_uses_cached_value(
        TableIOOdsOdfdo, '.ods', _create_formula_document, 3, capsys)


def test_ods_read_formula_without_cached_value_returns_none(
        capsys: CaptureFixture[str]) -> None:
    """A formula without a cached result is read as None."""
    run_read_formula_without_cached_value(
        TableIOOdsOdfdo, '.ods', _create_formula_document, capsys)


def test_ods_default_lang_uses_mformat_convention(
        capsys: CaptureFixture[str]) -> None:
    """CREATE mode sets the default ODS document language to en-UK."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'default_lang'
        with TableIOOdsOdfdo(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_listdata([['left', 'right']])
        document, _ = _load_document(Path(temp_dir) / 'default_lang.ods')
        assert document.meta.language == 'en-UK'
        assert _default_table_cell_language(document) == ('en', 'UK')
    check_capsys(capsys)


def test_ods_accepts_explicit_lang(
        capsys: CaptureFixture[str]) -> None:
    """CREATE mode stores an explicit RFC3066 document language."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'explicit_lang'
        with TableIOOdsOdfdo(file_name, FileAccess.CREATE,
                             lang='sv-SE') as table_io:
            table_io.write_table_listdata([['left', 'right']])
        document, _ = _load_document(Path(temp_dir) / 'explicit_lang.ods')
        assert document.meta.language == 'sv-SE'
        assert _default_table_cell_language(document) == ('sv', 'SE')
    check_capsys(capsys)


def test_ods_rejects_invalid_lang(
        capsys: CaptureFixture[str]) -> None:
    """Invalid non-RFC3066 language strings are rejected."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'bad_lang'
        try:
            TableIOOdsOdfdo(file_name, FileAccess.CREATE, lang='sv_SE')
        except TypeError as err:
            assert 'RFC3066' in str(err)
        else:
            raise AssertionError('Expected TypeError for invalid lang.')
    check_capsys(capsys)


def test_ods_description_advertises_lang_optional_arg(
        capsys: CaptureFixture[str]) -> None:
    """The factory metadata advertises the ODS lang optional argument."""
    description = TableIOOdsOdfdo.get_description()
    assert description.optional_args == ['lang']
    check_capsys(capsys)
