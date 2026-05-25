#! /usr/local/bin/python3
"""Tests for the tableio_excel_openpyxl module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from tempfile import TemporaryDirectory
from functools import partial
from typing import Callable, cast
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from openxml_audit import OpenXmlValidator  # type: ignore[import-untyped]
import pytest
from pytest import CaptureFixture
from tableio import tableio_excel_openpyxl
from tableio.tableio import FileAccess
from tableio.tableio_excel_openpyxl import TableIOExcelOpenPyXL
from .check_capsys import check_capsys
from .excel_test_file_helper import create_formula_workbook, \
    create_update_workbook, inspect_find_and_write_cells_workbook as \
    inspect_find_and_write_cells_workbook_common, \
    inspect_updated_workbook
from .excel_inspect_helper import inspect_bordered_workbook, \
    inspect_box_rewrite_clears_borders_workbook, \
    inspect_dict_header_fmt_workbook, inspect_fmtdict_header_fmt_workbook, \
    inspect_formatted_workbook, inspect_multiple_filters_workbook, \
    inspect_normalized_headers, inspect_rewrite_box_workbook, \
    inspect_row_formatted_workbook, inspect_table_width_cap_workbook, \
    inspect_table_width_heading_workbook
from .spreadsheet_test_helper import \
    run_bordered_workbook_is_validator_clean, \
    run_box_rewrite_clears_borders, \
    run_box_partial_overwrite, \
    run_box_removes_filter, \
    run_close_removes_temp_file_on_rewrite_failure, \
    run_find_value_and_write_cells, \
    run_multi_sheet_heading_state_is_per_sheet, \
    run_multi_sheet_read_only_create_raises, \
    run_multi_sheet_read_positions_are_per_sheet, \
    run_multi_sheet_update_uses_selected_sheet_write_position, \
    run_multi_sheet_write_positions_are_per_sheet, \
    run_open_rejects_second_open, \
    run_read_formula_cached, \
    run_read_formula_no_cache, \
    run_round_trip_dictdata_in_box, \
    run_sequential_list_reads, \
    run_select_missing_sheet_without_create_raises_key_error, \
    run_table_width_content, \
    run_table_width_widen_cap, \
    run_update_default_write_starts_after_last_used_row, \
    run_dictdata_header_format, \
    run_write_fmtdictdata_applies_first_row_format, \
    run_write_formatted_listdata_applies_formatting_and_filter, \
    run_listdata_applies_borders, \
    run_multi_filtered_ranges, \
    run_write_row_formatted_dictdata_applies_formatting


def _inspect_find_and_write_cells_workbook(file_path: Path) -> None:
    """Check exact cell writes after finding one row in the worksheet."""
    inspect_find_and_write_cells_workbook_common(file_path,
                                                 expect_highlight=True)


def _shared_string_count(root: ET.Element) -> int:
    """Return the number of shared strings in a parsed XML root."""
    namespace = (
        '{http://schemas.openxmlformats.org/'
        'spreadsheetml/2006/main}'
    )
    return len(root.findall(f'{namespace}si'))


def _existing_content_types_xml() -> bytes:
    """Return content types XML that already has shared strings."""
    return (
        b'<Types xmlns="http://schemas.openxmlformats.org/package/2006/'
        b'content-types"><Override PartName="/xl/sharedStrings.xml" '
        b'ContentType="application/vnd.openxmlformats-officedocument.'
        b'spreadsheetml.sharedStrings+xml"/></Types>'
    )


def _existing_workbook_rels_xml() -> bytes:
    """Return workbook relationships XML with shared strings already set."""
    return (
        b'<Relationships xmlns="http://schemas.openxmlformats.org/'
        b'package/2006/relationships"><Relationship Id="rId1" '
        b'Type="http://schemas.openxmlformats.org/officeDocument/2006/'
        b'relationships/sharedStrings" Target="sharedStrings.xml"/>'
        b'</Relationships>'
    )


def _shared_strings_xml() -> bytes:
    """Return one shared strings XML document."""
    return (
        b'<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/'
        b'2006/main"><si><t>old</t></si></sst>'
    )


def test_excel_round_trip_sequential_list_reads(
        capsys: CaptureFixture[str]) -> None:
    """Two list sections can be written and then read back sequentially."""
    run_sequential_list_reads(TableIOExcelOpenPyXL, capsys)


def test_excel_dictdata_roundtrip(capsys: CaptureFixture[str]) -> None:
    """Dict data can be written into and read back from a box."""
    run_round_trip_dictdata_in_box(TableIOExcelOpenPyXL, capsys)


def test_excel_multi_sheet_write_positions_are_per_sheet(
        capsys: CaptureFixture[str]) -> None:
    """Sequential writes keep an independent default position per sheet."""
    run_multi_sheet_write_positions_are_per_sheet(TableIOExcelOpenPyXL, capsys)


def test_excel_multi_sheet_read_positions_are_per_sheet(
        capsys: CaptureFixture[str]) -> None:
    """Sequential reads resume independently when switching sheets."""
    run_multi_sheet_read_positions_are_per_sheet(TableIOExcelOpenPyXL, capsys)


def test_excel_multi_sheet_heading_state_is_per_sheet(
        capsys: CaptureFixture[str]) -> None:
    """Each sheet tracks whether a default heading level was used before."""
    run_multi_sheet_heading_state_is_per_sheet(TableIOExcelOpenPyXL, capsys)


def test_excel_multi_sheet_read_only_create_raises(
        capsys: CaptureFixture[str]) -> None:
    """READ mode can select an existing sheet but cannot create one."""
    run_multi_sheet_read_only_create_raises(TableIOExcelOpenPyXL, capsys)


def test_excel_update_default_write_starts_after_last_used_row(
        capsys: CaptureFixture[str]) -> None:
    """UPDATE mode appends after the used area with a blank row separator."""
    run_update_default_write_starts_after_last_used_row(
        TableIOExcelOpenPyXL, '.xlsx', create_update_workbook,
        inspect_updated_workbook, capsys)


def test_excel_multi_sheet_update_uses_selected_sheet_write_position(
        capsys: CaptureFixture[str]) -> None:
    """UPDATE mode appends using the selected sheet's used area."""
    run_multi_sheet_update_uses_selected_sheet_write_position(
        TableIOExcelOpenPyXL, capsys)


def test_excel_write_formatted_listdata_applies_formatting_and_filter(
        capsys: CaptureFixture[str]) -> None:
    """Per-cell formatting and one filtered table are written."""
    run_write_formatted_listdata_applies_formatting_and_filter(
        TableIOExcelOpenPyXL, '.xlsx', inspect_formatted_workbook, capsys)


def test_excel_table_width_uses_table_content_not_heading(
        capsys: CaptureFixture[str]) -> None:
    """Table column widths ignore headings written outside table cells."""
    inspector = partial(inspect_table_width_heading_workbook,
                        expected_width_a=13.0, expected_width_b=21.0)
    run_table_width_content(TableIOExcelOpenPyXL, '.xlsx', inspector, capsys)


def test_excel_write_multiple_filtered_ranges_keeps_all_tables(
        capsys: CaptureFixture[str]) -> None:
    """Sequential filtered writes are kept as separate worksheet tables."""
    inspector = inspect_multiple_filters_workbook
    run_multi_filtered_ranges(TableIOExcelOpenPyXL, '.xlsx', inspector, capsys)


def test_excel_table_width_is_widen_only_with_cap(
        capsys: CaptureFixture[str]) -> None:
    """Box rewrites keep an already widened column width."""
    inspector = partial(inspect_table_width_cap_workbook, expected_width=50.0)
    run_table_width_widen_cap(TableIOExcelOpenPyXL, '.xlsx', inspector, capsys)


def test_excel_box_write_removes_overlapping_filtered_table(
        capsys: CaptureFixture[str]) -> None:
    """Rewriting a boxed area removes any stale overlapping table metadata."""
    run_box_removes_filter(TableIOExcelOpenPyXL, '.xlsx',
                           inspect_rewrite_box_workbook, capsys)


def test_excel_find_and_write_cells(capsys: CaptureFixture[str]) -> None:
    """Found cell ranges can be read and updated without moving cursors."""
    run_find_value_and_write_cells(TableIOExcelOpenPyXL, '.xlsx',
                                   _inspect_find_and_write_cells_workbook,
                                   capsys)


def test_excel_boxed_table_partial_overwrite_raises(
        capsys: CaptureFixture[str]) -> None:
    """Boxed table writes reject overlaps that leave part of a table behind."""
    run_box_partial_overwrite(TableIOExcelOpenPyXL, capsys)


def test_excel_write_row_formatted_dictdata_applies_formatting(
        capsys: CaptureFixture[str]) -> None:
    """Row formatting for dict rows is copied to each written cell."""
    run_write_row_formatted_dictdata_applies_formatting(
        TableIOExcelOpenPyXL, '.xlsx', inspect_row_formatted_workbook, capsys)


def test_excel_write_dictdata_applies_first_row_format(
        capsys: CaptureFixture[str]) -> None:
    """Dict header cells can be formatted with first_row_format."""
    inspector = inspect_dict_header_fmt_workbook
    run_dictdata_header_format(TableIOExcelOpenPyXL, '.xlsx', inspector,
                               capsys)


def test_excel_write_fmtdictdata_applies_first_row_format(
        capsys: CaptureFixture[str]) -> None:
    """Formatted dict writes keep header and data-row formatting separate."""
    inspector = inspect_fmtdict_header_fmt_workbook
    run_write_fmtdictdata_applies_first_row_format(TableIOExcelOpenPyXL,
                                                   '.xlsx', inspector, capsys)


def test_excel_write_table_listdata_applies_borders(
        capsys: CaptureFixture[str]) -> None:
    """Writes the requested table borders to saved OpenPyXL cells."""
    inspector = inspect_bordered_workbook
    run_listdata_applies_borders(TableIOExcelOpenPyXL, '.xlsx', inspector,
                                 capsys)


def test_excel_box_rewrite_clears_old_borders(
        capsys: CaptureFixture[str]) -> None:
    """Rewriting the same boxed area clears any stale cell borders."""
    run_box_rewrite_clears_borders(TableIOExcelOpenPyXL, '.xlsx',
                                   inspect_box_rewrite_clears_borders_workbook,
                                   capsys)


def test_excel_read_formula_uses_cached_value(
        capsys: CaptureFixture[str]) -> None:
    """A formula cell is read as its cached value."""
    run_read_formula_cached(TableIOExcelOpenPyXL, '.xlsx',
                            create_formula_workbook, 3, capsys)


def test_excel_read_formula_without_cached_value_returns_none(
        capsys: CaptureFixture[str]) -> None:
    """A formula without a cached result is read as None."""
    run_read_formula_no_cache(TableIOExcelOpenPyXL, '.xlsx',
                              create_formula_workbook, capsys)


def test_excel_rejects_second_open(capsys: CaptureFixture[str]) -> None:
    """Opening the same Excel object twice raises RuntimeError."""
    run_open_rejects_second_open(TableIOExcelOpenPyXL, capsys)


def test_excel_select_missing_sheet_without_create_raises_key_error(
        capsys: CaptureFixture[str]) -> None:
    """Selecting a missing sheet without create=True raises KeyError."""
    run_select_missing_sheet_without_create_raises_key_error(
        TableIOExcelOpenPyXL, capsys)


def test_excel_written_heading_workbook_is_validator_clean() -> None:
    """Heading styles are written to validator-clean `.xlsx` files."""
    with TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / 'validator_clean.xlsx'
        with TableIOExcelOpenPyXL(file_path, FileAccess.CREATE) as table_io:
            table_io.write_heading('Example heading')
            table_io.write_table_listdata([['left', 'right']])
        result = OpenXmlValidator().validate(file_path)
        assert result.is_valid


def test_excel_written_strings_use_shared_string_table() -> None:
    """String cells are saved through a populated shared-string table."""
    read_root = cast(Callable[[Path], ET.Element],
                     getattr(tableio_excel_openpyxl,
                             '_read_shared_strings_root'))
    with TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / 'shared_strings.xlsx'
        with TableIOExcelOpenPyXL(file_path, FileAccess.CREATE) as table_io:
            table_io.write_table_listdata([['left', 'right']])
        shared_strings_root = read_root(file_path)
        with ZipFile(file_path, 'r') as archive:
            worksheet_xml = archive.read('xl/worksheets/sheet1.xml')
            shared_strings_xml = archive.read('xl/sharedStrings.xml')
        assert _shared_string_count(shared_strings_root) == 2
        assert b'inlineStr' not in worksheet_xml
        assert b'sharedStrings.xml' not in worksheet_xml
        assert b'left' in shared_strings_xml
        assert b'right' in shared_strings_xml


def test_excel_rewrite_shared_parts(tmp_path: Path) -> None:
    """Rewriting an archive with shared strings replaces only that entry."""
    rewrite_workbook = cast(Callable[[Path], None],
                            getattr(tableio_excel_openpyxl,
                                    '_rewrite_saved_workbook'))
    file_path = tmp_path / 'existing_shared.xlsx'
    content_types_xml = _existing_content_types_xml()
    workbook_rels_xml = _existing_workbook_rels_xml()
    with ZipFile(file_path, 'w') as archive:
        archive.writestr('[Content_Types].xml', content_types_xml)
        archive.writestr('xl/_rels/workbook.xml.rels', workbook_rels_xml)
        archive.writestr('xl/sharedStrings.xml', _shared_strings_xml())
    rewrite_workbook(file_path)
    with ZipFile(file_path, 'r') as archive:
        assert archive.namelist().count('xl/sharedStrings.xml') == 1
        assert archive.read('[Content_Types].xml') == content_types_xml
        assert archive.read('xl/_rels/workbook.xml.rels') == \
            workbook_rels_xml
        shared_strings_root = ET.fromstring(
            archive.read('xl/sharedStrings.xml'))
    assert _shared_string_count(shared_strings_root) == 1


def test_excel_rels_next_id() -> None:
    """Shared-string relationship IDs ignore nonstandard ID strings."""
    add_shared_rel = cast(Callable[[bytes], bytes],
                          getattr(tableio_excel_openpyxl,
                                  '_workbook_rels_with_shared_strings'))
    rels_xml = (
        b'<Relationships xmlns="http://schemas.openxmlformats.org/'
        b'package/2006/relationships"><Relationship Id="external" '
        b'Type="custom" Target="external.xml"/>'
        b'<Relationship Id="rIdx" Type="custom" Target="bad.xml"/>'
        b'<Relationship Id="rId7" Type="custom" Target="sheet.xml"/>'
        b'</Relationships>'
    )
    root = ET.fromstring(add_shared_rel(rels_xml))
    rels = root.findall(
        '{http://schemas.openxmlformats.org/package/2006/'
        'relationships}Relationship')
    assert rels[-1].get('Id') == 'rId8'
    assert rels[-1].get('Target') == 'sharedStrings.xml'


def test_excel_bordered_workbook_is_validator_clean() -> None:
    """Bordered tables are written to validator-clean `.xlsx` files."""
    run_bordered_workbook_is_validator_clean(
        TableIOExcelOpenPyXL, '.xlsx',
        lambda file_path: OpenXmlValidator().validate(file_path).is_valid)


def test_excel_update_creates_new_read_sheet_and_normalizes_table_headers(
        capsys: CaptureFixture[str]) -> None:
    """UPDATE mode mirrors created sheets and normalizes filter headers."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'update_headers'
        with TableIOExcelOpenPyXL(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_listdata([['keep', 'row']])
        with TableIOExcelOpenPyXL(file_name, FileAccess.UPDATE) as table_io:
            table_io.select_sheet('Numbers', create=True)
            table_io.write_table_listdata([[1, None], [2, 3]],
                                          filtered_data_range=True)
        inspect_normalized_headers(Path(temp_dir) / 'update_headers.xlsx',
                                   'Numbers')
    check_capsys(capsys)


def test_excel_styles_xml_with_sorted_fonts_keeps_unknown_tags_last(
        capsys: CaptureFixture[str]) -> None:
    """Unknown font child tags sort after the known Excel schema order."""
    sort_fonts = cast(Callable[[bytes], bytes],
                      getattr(tableio_excel_openpyxl,
                              '_styles_xml_with_sorted_fonts'))
    styles_xml = (
        b'<?xml version="1.0" encoding="utf-8"?>'
        b'<styleSheet '
        b'xmlns="http://schemas.openxmlformats.org/'
        b'spreadsheetml/2006/main">'
        b'<fonts count="1"><font><color rgb="FF000000"/>'
        b'<mystery val="1"/><b/><name val="Calibri"/>'
        b'</font></fonts></styleSheet>'
    )
    sorted_xml = sort_fonts(styles_xml)
    namespace = (
        '{http://schemas.openxmlformats.org/'
        'spreadsheetml/2006/main}'
    )
    root = ET.fromstring(sorted_xml)
    font = root.find(f'{namespace}fonts/{namespace}font')
    assert font is not None
    assert [element.tag.split('}', 1)[-1] for element in font] == [
        'b',
        'color',
        'name',
        'mystery'
    ]
    check_capsys(capsys)


def test_excel_close_removes_temp_file_on_rewrite_failure(
        monkeypatch: pytest.MonkeyPatch, capsys: CaptureFixture[str]) -> None:
    """Workbook close cleans up the temporary `.xlsx` on rewrite failure."""
    run_close_removes_temp_file_on_rewrite_failure(TableIOExcelOpenPyXL,
                                                   tableio_excel_openpyxl,
                                                   '_rewrite_saved_workbook',
                                                   monkeypatch, capsys)
