#! /usr/local/bin/python3
"""Tests for the tableio_ods_odfdo module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Optional, cast
import pytest
from odfdo import Cell, Document, Element, Table
from odfdo.body import Spreadsheet
from odfdo.style import Style
from openxml_audit import OdfValidator  # type: ignore[import-untyped]
from pytest import CaptureFixture
from tableio.capability import CAP_IMPLEMENTED
from tableio.tableio import FileAccess
from tableio.tableio_ods_odfdo import TableIOOdsOdfdo
from tableio.value_type import Fmt, get_checked_type
from .check_capsys import check_capsys
from .spreadsheet_test_helper import \
    run_bordered_workbook_is_validator_clean, \
    run_box_rewrite_clears_old_borders, \
    run_boxed_table_partial_overwrite_raises, \
    run_box_write_removes_overlapping_filtered_range, \
    run_find_value_and_write_cells, \
    run_multi_sheet_heading_state_is_per_sheet, \
    run_multi_sheet_read_only_create_raises, \
    run_multi_sheet_read_positions_are_per_sheet, \
    run_multi_sheet_update_uses_selected_sheet_write_position, \
    run_multi_sheet_write_positions_are_per_sheet, \
    run_open_rejects_second_open, \
    run_read_formula_uses_cached_value, \
    run_read_formula_without_cached_value, \
    run_round_trip_dictdata_in_box, \
    run_round_trip_sequential_list_reads, \
    run_select_missing_sheet_without_create_raises_key_error, \
    run_table_width_is_widen_only_with_cap, \
    run_update_default_write_starts_after_last_used_row, \
    run_write_dictdata_applies_first_row_format, \
    run_write_fmtdictdata_applies_first_row_format, \
    run_write_formatted_listdata_applies_formatting_and_filter, \
    run_write_table_listdata_applies_borders, \
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


def _cell_border_properties(
        document: Document,
        table: Table,
        row: int,
        column: int) -> tuple[Optional[str], Optional[str], Optional[str],
                              Optional[str]]:
    """Return one cell border tuple as top-right-bottom-left."""
    cell = table.get_cell((column, row), clone=False)
    if cell.style is None:
        return None, None, None, None
    style = document.get_style('table-cell', cell.style)
    assert style is not None
    table_props = get_checked_type(style, Style).get_properties(
        'table-cell') or {}
    return (cast(Optional[str], table_props.get('fo:border-top')),
            cast(Optional[str], table_props.get('fo:border-right')),
            cast(Optional[str], table_props.get('fo:border-bottom')),
            cast(Optional[str], table_props.get('fo:border-left')))


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


def _inspect_find_and_write_cells_document(file_path: Path) -> None:
    """Check exact cell writes after finding one row in the table."""
    document, table = _load_document(file_path)
    assert table.get_value((1, 3)) == 'Bob'
    assert table.get_value((2, 3)) is True
    bob_table_props, _ = _cell_style_properties(document, table, 3, 1)
    active_table_props, _ = _cell_style_properties(document, table, 3, 2)
    assert bob_table_props['fo:background-color'] == '#ffff00'
    assert active_table_props['fo:background-color'] == '#ffff00'


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


def _inspect_bordered_document(file_path: Path) -> None:
    """Check that one ODS file stores the requested table borders."""
    document, table = _load_document(file_path)
    thick = '1.75pt solid #000000'
    thin = '0.75pt solid #000000'
    assert _cell_border_properties(document, table, 0, 0) == (
        thick, thin, thin, thick)
    assert _cell_border_properties(document, table, 0, 1) == (
        thick, thick, thin, thin)
    assert _cell_border_properties(document, table, 1, 0) == (
        thin, thin, thick, thick)
    assert _cell_border_properties(document, table, 1, 1) == (
        thin, thick, thick, thin)


def _inspect_box_rewrite_clears_borders_document(file_path: Path) -> None:
    """Check that boxed rewrites clear stale ODS borders."""
    document, table = _load_document(file_path)
    for row_index in range(2):
        for column_index in range(2):
            assert _cell_border_properties(
                document, table, row_index, column_index) == (
                    None, None, None, None)


def test_ods_get_capabilities_support_borders(
        capsys: CaptureFixture[str]) -> None:
    """The ODS backend reports border writing as supported."""
    assert TableIOOdsOdfdo.get_capabilities().can_write_borders == \
        CAP_IMPLEMENTED
    check_capsys(capsys)


def test_ods_written_workbook_is_validator_clean() -> None:
    """Plain `.ods` output is normalized to validator-clean package XML."""
    with TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / 'validator_clean.ods'
        with TableIOOdsOdfdo(file_path, FileAccess.CREATE) as table_io:
            table_io.write_table_listdata([['left', 'right']])
        result = OdfValidator().validate(file_path)
        assert result.is_valid


def test_ods_bordered_workbook_is_validator_clean() -> None:
    """Bordered `.ods` output remains validator clean."""
    run_bordered_workbook_is_validator_clean(
        TableIOOdsOdfdo, '.ods',
        lambda file_path: OdfValidator().validate(file_path).is_valid)


def _make_database_range(name: Optional[str], display_buttons: str,
                         address: str) -> Element:
    """Create one ODS database-range element for tests."""
    database_range = Element.from_tag('table:database-range')
    if name is not None:
        database_range.set_attribute('table:name', name)
    database_range.set_attribute('table:display-filter-buttons',
                                 display_buttons)
    database_range.set_attribute('table:target-range-address', address)
    return database_range


class ExposedTableIOOdsOdfdo(TableIOOdsOdfdo):
    """ODS test double exposing protected helpers through public wrappers."""

    @classmethod
    def split_rfc3066_language(cls, lang: str) -> tuple[str, str]:
        """Expose the RFC3066 splitting helper for tests."""
        return cls._split_rfc3066_language(lang)

    @classmethod
    def quote_table_name(cls, table_name: str) -> str:
        """Expose the table-name quoting helper for tests."""
        return cls._quoted_table_name(table_name)

    @classmethod
    def split_range_endpoint(cls, endpoint: str) -> tuple[str, str]:
        """Expose the range-endpoint parsing helper for tests."""
        return cls._split_range_endpoint(endpoint)

    @classmethod
    def cell_ref_to_position(cls, cell_ref: str) -> tuple[int, int]:
        """Expose the A1 parsing helper for tests."""
        return cls._cell_ref_to_position(cell_ref)

    @classmethod
    def database_range_bounds(
            cls, database_range: Element) -> tuple[str, tuple[int, int,
                                                              int, int]]:
        """Expose the database-range parser for tests."""
        return cls._database_range_bounds(database_range)

    def database_range_container(self) -> Element:
        """Expose the database-range container helper for tests."""
        return self._database_range_container()

    def spreadsheet_body(self) -> Spreadsheet:
        """Expose the spreadsheet-body helper for tests."""
        return self._spreadsheet_body()

    def filtered_range_infos(self) -> list[tuple[str, tuple[int, int,
                                                            int, int]]]:
        """Expose filtered-range discovery for tests."""
        return self._filtered_range_infos()

    def current_column_width(self, column: int) -> Optional[float]:
        """Expose current-column-width lookup for tests."""
        return self._current_column_width(column)

    @classmethod
    def column_width_from_text(cls, width: str) -> Optional[float]:
        """Expose the column-width parser for tests."""
        return cls._column_width_from_text(width)

    def cell_style_name(self, fmt: Fmt) -> str:
        """Expose the cell-style cache helper for tests."""
        return self._cell_style_name(fmt)


def test_ods_round_trip_sequential_list_reads(
        capsys: CaptureFixture[str]) -> None:
    """Two list sections can be written and then read back sequentially."""
    run_round_trip_sequential_list_reads(TableIOOdsOdfdo, capsys)


def test_ods_round_trip_dictdata_in_box(
        capsys: CaptureFixture[str]) -> None:
    """Dict data can be written into and read back from a box."""
    run_round_trip_dictdata_in_box(TableIOOdsOdfdo, capsys)


def test_ods_multi_sheet_write_positions_are_per_sheet(
        capsys: CaptureFixture[str]) -> None:
    """Sequential writes keep an independent default position per sheet."""
    run_multi_sheet_write_positions_are_per_sheet(
        TableIOOdsOdfdo, capsys)


def test_ods_multi_sheet_read_positions_are_per_sheet(
        capsys: CaptureFixture[str]) -> None:
    """Sequential reads resume independently when switching sheets."""
    run_multi_sheet_read_positions_are_per_sheet(
        TableIOOdsOdfdo, capsys)


def test_ods_multi_sheet_heading_state_is_per_sheet(
        capsys: CaptureFixture[str]) -> None:
    """Each sheet tracks whether a default heading level was used before."""
    run_multi_sheet_heading_state_is_per_sheet(
        TableIOOdsOdfdo, capsys)


def test_ods_multi_sheet_read_only_create_raises(
        capsys: CaptureFixture[str]) -> None:
    """READ mode can select an existing sheet but cannot create one."""
    run_multi_sheet_read_only_create_raises(
        TableIOOdsOdfdo, capsys)


def test_ods_update_default_write_starts_after_last_used_row(
        capsys: CaptureFixture[str]) -> None:
    """UPDATE mode appends after the used area with a blank row separator."""
    run_update_default_write_starts_after_last_used_row(
        TableIOOdsOdfdo, '.ods', _create_update_document,
        _inspect_updated_document, capsys)


def test_ods_multi_sheet_update_uses_selected_sheet_write_position(
        capsys: CaptureFixture[str]) -> None:
    """UPDATE mode appends using the selected sheet's used area."""
    run_multi_sheet_update_uses_selected_sheet_write_position(
        TableIOOdsOdfdo, capsys)


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


def test_ods_find_value_and_write_cells(
        capsys: CaptureFixture[str]) -> None:
    """Found cell ranges can be read and updated without moving cursors."""
    run_find_value_and_write_cells(
        TableIOOdsOdfdo, '.ods',
        _inspect_find_and_write_cells_document, capsys)


def test_ods_boxed_table_partial_overwrite_raises(
        capsys: CaptureFixture[str]) -> None:
    """Boxed table writes reject overlaps that leave part of a table behind."""
    run_boxed_table_partial_overwrite_raises(TableIOOdsOdfdo, capsys)


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


def test_ods_write_table_listdata_applies_borders(
        capsys: CaptureFixture[str]) -> None:
    """Writes the requested table borders to saved ODS cells."""
    run_write_table_listdata_applies_borders(
        TableIOOdsOdfdo, '.ods', _inspect_bordered_document, capsys)


def test_ods_box_rewrite_clears_old_borders(
        capsys: CaptureFixture[str]) -> None:
    """Rewriting the same boxed area clears any stale ODS borders."""
    run_box_rewrite_clears_old_borders(
        TableIOOdsOdfdo, '.ods',
        _inspect_box_rewrite_clears_borders_document, capsys)


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


def test_ods_open_rejects_second_open(
        capsys: CaptureFixture[str]) -> None:
    """Opening the same ODS object twice raises RuntimeError."""
    run_open_rejects_second_open(TableIOOdsOdfdo, capsys)


def test_ods_open_update_creates_default_table_when_document_has_none(
        capsys: CaptureFixture[str]) -> None:
    """Opening a table-less ODS file creates the default first table."""
    with TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / 'empty_tables.ods'
        document = Document('spreadsheet')
        document.body.clear()
        document.save(file_path)
        with TableIOOdsOdfdo(
                Path(temp_dir) / 'empty_tables',
                FileAccess.UPDATE) as table_io:
            assert table_io.list_sheets() == ['Sheet1']
            assert table_io.current_sheet_name() == 'Sheet1'
    check_capsys(capsys)


def test_ods_split_rfc3066_language_without_country(
        capsys: CaptureFixture[str]) -> None:
    """A plain language code is split with an empty country part."""
    assert ExposedTableIOOdsOdfdo.split_rfc3066_language('sv') == ('sv', '')
    check_capsys(capsys)


def test_ods_select_missing_sheet_without_create_raises_key_error(
        capsys: CaptureFixture[str]) -> None:
    """Selecting a missing sheet without create=True raises KeyError."""
    run_select_missing_sheet_without_create_raises_key_error(
        TableIOOdsOdfdo, capsys)


def test_ods_quoted_table_name_quotes_non_identifier_names(
        capsys: CaptureFixture[str]) -> None:
    """Names containing spaces are quoted for ODF range addresses."""
    assert ExposedTableIOOdsOdfdo.quote_table_name('Quarter 1') == \
        "'Quarter 1'"
    check_capsys(capsys)


def test_ods_split_range_endpoint_rejects_malformed_quoted_endpoint(
        capsys: CaptureFixture[str]) -> None:
    """Quoted range endpoints must include the closing quote and dot."""
    with pytest.raises(ValueError, match='Invalid endpoint'):
        ExposedTableIOOdsOdfdo.split_range_endpoint("'Sheet1.A1")
    check_capsys(capsys)


def test_ods_split_range_endpoint_accepts_quoted_table_name(
        capsys: CaptureFixture[str]) -> None:
    """Quoted range endpoints preserve the table name and cell reference."""
    assert ExposedTableIOOdsOdfdo.split_range_endpoint(
        "'Quarter 1'.B3") == ('Quarter 1', 'B3')
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('cell_ref', 'match'),
    [
        pytest.param('A1B', 'Invalid cell reference', id='alpha-after-row'),
        pytest.param('A-1', 'Invalid cell reference', id='invalid-character'),
        pytest.param('A', 'Invalid cell reference', id='missing-row')
    ]
)
def test_ods_cell_ref_to_position_rejects_invalid_references(
        cell_ref: str, match: str,
        capsys: CaptureFixture[str]) -> None:
    """Malformed A1 references are rejected."""
    with pytest.raises(ValueError, match=match):
        ExposedTableIOOdsOdfdo.cell_ref_to_position(cell_ref)
    check_capsys(capsys)


def test_ods_database_range_bounds_handles_single_cell_and_errors(
        capsys: CaptureFixture[str]) -> None:
    """database_range_bounds parses single cells and rejects bad metadata."""
    single_cell = Element.from_tag('table:database-range')
    single_cell.set_attribute('table:target-range-address', 'Sheet1.C3')
    assert ExposedTableIOOdsOdfdo.database_range_bounds(single_cell) == (
        'Sheet1',
        (2, 2, 3, 3)
    )
    missing_address = Element.from_tag('table:database-range')
    with pytest.raises(ValueError, match='Missing target range address'):
        ExposedTableIOOdsOdfdo.database_range_bounds(missing_address)
    multi_table = Element.from_tag('table:database-range')
    multi_table.set_attribute('table:target-range-address',
                              'Sheet1.A1:Sheet2.B2')
    with pytest.raises(ValueError, match='spans several tables'):
        ExposedTableIOOdsOdfdo.database_range_bounds(multi_table)
    check_capsys(capsys)


def test_ods_filtered_range_infos_ignores_non_matching_range_metadata(
        capsys: CaptureFixture[str]) -> None:
    """Only filtered ranges for the active table are returned."""
    with TemporaryDirectory() as temp_dir:
        with ExposedTableIOOdsOdfdo(
                Path(temp_dir) / 'filter_infos',
                FileAccess.CREATE) as opened:
            table_io = cast(ExposedTableIOOdsOdfdo, opened)
            container = table_io.database_range_container()
            container.append(_make_database_range(
                None, 'true', 'Sheet1.A1:Sheet1.B2'))
            container.append(_make_database_range(
                'SkipDisplay', 'false', 'Sheet1.A1:Sheet1.B2'))
            container.append(_make_database_range(
                'SkipTable', 'true', 'Other.A1:Other.B2'))
            container.append(_make_database_range(
                'DbFilter', 'true', 'Sheet1.C1:Sheet1.D2'))
            body = table_io.spreadsheet_body()
            body.set_named_range('SkipUsage', (0, 0, 1, 1), 'Sheet1',
                                 usage='print-range')
            body.set_named_range('SkipNamedTable', (0, 0, 1, 1), 'Other',
                                 usage='filter')
            body.set_named_range('NamedFilter', (0, 0, 1, 1), 'Sheet1',
                                 usage='filter')
            assert dict(table_io.filtered_range_infos()) == {
                'DbFilter': (0, 2, 2, 4),
                'NamedFilter': (0, 0, 2, 2)
            }
    check_capsys(capsys)


def test_ods_column_width_from_text_rejects_invalid_values(
        capsys: CaptureFixture[str]) -> None:
    """Non-centimetre widths and invalid numbers are rejected."""
    assert ExposedTableIOOdsOdfdo.column_width_from_text('12pt') is None
    assert ExposedTableIOOdsOdfdo.column_width_from_text('abccm') is None
    check_capsys(capsys)


def test_ods_current_column_width_handles_missing_style_information(
        monkeypatch: pytest.MonkeyPatch,
        capsys: CaptureFixture[str]) -> None:
    """current_column_width returns None when style metadata is incomplete."""
    with TemporaryDirectory() as temp_dir:
        with ExposedTableIOOdsOdfdo(
                Path(temp_dir) / 'width_info',
                FileAccess.CREATE) as opened:
            table_io = cast(ExposedTableIOOdsOdfdo, opened)
            assert table_io.table is not None
            assert table_io.document is not None
            column = table_io.table.get_column(0)
            column.style = 'missing_style'
            table_io.table.set_column(0, column)
            monkeypatch.setattr(table_io.document, 'get_style',
                                lambda family, name: None)
            assert table_io.current_column_width(0) is None
            no_props_style = Style('table-column', name='no_props')
            monkeypatch.setattr(no_props_style, 'get_properties',
                                lambda area: None)
            column.style = 'no_props'
            table_io.table.set_column(0, column)
            monkeypatch.setattr(table_io.document, 'get_style',
                                lambda family, name: no_props_style)
            assert table_io.current_column_width(0) is None
            no_width_style = Style('table-column', name='no_width')
            no_width_style.set_properties(
                {'style:use-optimal-column-width': 'true'},
                area='table-column')
            column.style = 'no_width'
            table_io.table.set_column(0, column)
            monkeypatch.setattr(table_io.document, 'get_style',
                                lambda family, name: no_width_style)
            assert table_io.current_column_width(0) is None
    check_capsys(capsys)


def test_ods_cell_style_name_handles_plain_default_format(
        capsys: CaptureFixture[str]) -> None:
    """The style cache also works for an unformatted default cell."""
    with TemporaryDirectory() as temp_dir:
        with ExposedTableIOOdsOdfdo(
                Path(temp_dir) / 'plain_style',
                FileAccess.CREATE) as opened:
            table_io = cast(ExposedTableIOOdsOdfdo, opened)
            assert table_io.document is not None
            style_name = table_io.cell_style_name(Fmt())
            assert table_io.cell_style_name(Fmt()) == style_name
            style = table_io.document.get_style('table-cell', style_name)
            assert isinstance(style, Style)
    check_capsys(capsys)


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
