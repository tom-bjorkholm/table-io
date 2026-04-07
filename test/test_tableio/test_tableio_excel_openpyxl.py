#! /usr/local/bin/python3
"""Tests for the tableio_excel_openpyxl module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from tempfile import TemporaryDirectory
from openxml_audit import OpenXmlValidator  # type: ignore[import-untyped]
from pytest import CaptureFixture
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
    inspect_normalized_header_workbook, inspect_rewrite_box_workbook, \
    inspect_row_formatted_workbook, inspect_table_width_cap_workbook, \
    inspect_table_width_heading_workbook
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
    run_table_width_uses_table_content_not_heading, \
    run_table_width_is_widen_only_with_cap, \
    run_update_default_write_starts_after_last_used_row, \
    run_write_dictdata_applies_first_row_format, \
    run_write_fmtdictdata_applies_first_row_format, \
    run_write_formatted_listdata_applies_formatting_and_filter, \
    run_write_table_listdata_applies_borders, \
    run_write_multiple_filtered_ranges_keeps_all_ranges, \
    run_write_row_formatted_dictdata_applies_formatting


def _inspect_find_and_write_cells_workbook(file_path: Path) -> None:
    """Check exact cell writes after finding one row in the worksheet."""
    inspect_find_and_write_cells_workbook_common(
        file_path, expect_highlight=True)


def test_excel_round_trip_sequential_list_reads(
        capsys: CaptureFixture[str]) -> None:
    """Two list sections can be written and then read back sequentially."""
    run_round_trip_sequential_list_reads(TableIOExcelOpenPyXL, capsys)


def test_excel_round_trip_dictdata_in_box(
        capsys: CaptureFixture[str]) -> None:
    """Dict data can be written into and read back from a box."""
    run_round_trip_dictdata_in_box(TableIOExcelOpenPyXL, capsys)


def test_excel_multi_sheet_write_positions_are_per_sheet(
        capsys: CaptureFixture[str]) -> None:
    """Sequential writes keep an independent default position per sheet."""
    run_multi_sheet_write_positions_are_per_sheet(
        TableIOExcelOpenPyXL, capsys)


def test_excel_multi_sheet_read_positions_are_per_sheet(
        capsys: CaptureFixture[str]) -> None:
    """Sequential reads resume independently when switching sheets."""
    run_multi_sheet_read_positions_are_per_sheet(
        TableIOExcelOpenPyXL, capsys)


def test_excel_multi_sheet_heading_state_is_per_sheet(
        capsys: CaptureFixture[str]) -> None:
    """Each sheet tracks whether a default heading level was used before."""
    run_multi_sheet_heading_state_is_per_sheet(
        TableIOExcelOpenPyXL, capsys)


def test_excel_multi_sheet_read_only_create_raises(
        capsys: CaptureFixture[str]) -> None:
    """READ mode can select an existing sheet but cannot create one."""
    run_multi_sheet_read_only_create_raises(
        TableIOExcelOpenPyXL, capsys)


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
        TableIOExcelOpenPyXL, '.xlsx', inspect_formatted_workbook,
        capsys)


def test_excel_table_width_uses_table_content_not_heading(
        capsys: CaptureFixture[str]) -> None:
    """Table column widths ignore headings written outside table cells."""
    run_table_width_uses_table_content_not_heading(
        TableIOExcelOpenPyXL, '.xlsx',
        lambda file_path: inspect_table_width_heading_workbook(
            file_path, 13.0, 21.0), capsys)


def test_excel_write_multiple_filtered_ranges_keeps_all_tables(
        capsys: CaptureFixture[str]) -> None:
    """Sequential filtered writes are kept as separate worksheet tables."""
    run_write_multiple_filtered_ranges_keeps_all_ranges(
        TableIOExcelOpenPyXL, '.xlsx',
        inspect_multiple_filters_workbook, capsys)


def test_excel_table_width_is_widen_only_with_cap(
        capsys: CaptureFixture[str]) -> None:
    """Box rewrites keep an already widened column width."""
    run_table_width_is_widen_only_with_cap(
        TableIOExcelOpenPyXL, '.xlsx',
        lambda file_path: inspect_table_width_cap_workbook(
            file_path, 50.0), capsys)


def test_excel_box_write_removes_overlapping_filtered_table(
        capsys: CaptureFixture[str]) -> None:
    """Rewriting a boxed area removes any stale overlapping table metadata."""
    run_box_write_removes_overlapping_filtered_range(
        TableIOExcelOpenPyXL, '.xlsx',
        inspect_rewrite_box_workbook, capsys)


def test_excel_find_value_and_write_cells(
        capsys: CaptureFixture[str]) -> None:
    """Found cell ranges can be read and updated without moving cursors."""
    run_find_value_and_write_cells(
        TableIOExcelOpenPyXL, '.xlsx',
        _inspect_find_and_write_cells_workbook, capsys)


def test_excel_boxed_table_partial_overwrite_raises(
        capsys: CaptureFixture[str]) -> None:
    """Boxed table writes reject overlaps that leave part of a table behind."""
    run_boxed_table_partial_overwrite_raises(
        TableIOExcelOpenPyXL, capsys)


def test_excel_write_row_formatted_dictdata_applies_formatting(
        capsys: CaptureFixture[str]) -> None:
    """Row formatting for dict rows is copied to each written cell."""
    run_write_row_formatted_dictdata_applies_formatting(
        TableIOExcelOpenPyXL, '.xlsx',
        inspect_row_formatted_workbook, capsys)


def test_excel_write_dictdata_applies_first_row_format(
        capsys: CaptureFixture[str]) -> None:
    """Dict header cells can be formatted with first_row_format."""
    run_write_dictdata_applies_first_row_format(
        TableIOExcelOpenPyXL, '.xlsx',
        inspect_dict_header_fmt_workbook, capsys)


def test_excel_write_fmtdictdata_applies_first_row_format(
        capsys: CaptureFixture[str]) -> None:
    """Formatted dict writes keep header and data-row formatting separate."""
    run_write_fmtdictdata_applies_first_row_format(
        TableIOExcelOpenPyXL, '.xlsx',
        inspect_fmtdict_header_fmt_workbook, capsys)


def test_excel_write_table_listdata_applies_borders(
        capsys: CaptureFixture[str]) -> None:
    """Writes the requested table borders to saved OpenPyXL cells."""
    run_write_table_listdata_applies_borders(
        TableIOExcelOpenPyXL, '.xlsx', inspect_bordered_workbook, capsys)


def test_excel_box_rewrite_clears_old_borders(
        capsys: CaptureFixture[str]) -> None:
    """Rewriting the same boxed area clears any stale cell borders."""
    run_box_rewrite_clears_old_borders(
        TableIOExcelOpenPyXL, '.xlsx',
        inspect_box_rewrite_clears_borders_workbook, capsys)


def test_excel_read_formula_uses_cached_value(
        capsys: CaptureFixture[str]) -> None:
    """A formula cell is read as its cached value."""
    run_read_formula_uses_cached_value(
        TableIOExcelOpenPyXL, '.xlsx', create_formula_workbook, 3,
        capsys)


def test_excel_read_formula_without_cached_value_returns_none(
        capsys: CaptureFixture[str]) -> None:
    """A formula without a cached result is read as None."""
    run_read_formula_without_cached_value(
        TableIOExcelOpenPyXL, '.xlsx', create_formula_workbook,
        capsys)


def test_excel_open_rejects_second_open(
        capsys: CaptureFixture[str]) -> None:
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
            table_io.write_table_listdata(
                [[1, None], [2, 3]],
                filtered_data_range=True)
        inspect_normalized_header_workbook(
            Path(temp_dir) / 'update_headers.xlsx', 'Numbers')
    check_capsys(capsys)
