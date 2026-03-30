#! /usr/local/bin/python3
"""Tests for the tableio_excel_pylightxl module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from pytest import CaptureFixture

from tableio.capability import CAP_IGNORED, CAP_IMPLEMENTED
from tableio.color import Color
from tableio.factory import create_tableio
from tableio.tableio import Box, FileAccess
from tableio.tableio_excel_openpyxl import TableIOExcelOpenPyXL
from tableio.tableio_excel_pylightxl import TableIOExcelPylightxl
from tableio.value_type import Fmt, FmtDictRow, ValueFmt

from .check_capsys import check_capsys
from .excel_test_file_helper import create_formula_workbook, \
    create_update_workbook, inspect_find_and_write_cells_workbook, \
    inspect_updated_workbook
from .spreadsheet_test_helper import \
    run_boxed_table_partial_overwrite_raises, \
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
    run_update_default_write_starts_after_last_used_row


def test_excel_pylightxl_get_capabilities(
        capsys: CaptureFixture[str]) -> None:
    """The backend reports the honest pylightxl feature set."""
    capabilities = TableIOExcelPylightxl.get_capabilities()
    assert capabilities.can_read == CAP_IMPLEMENTED
    assert capabilities.can_write == CAP_IMPLEMENTED
    assert capabilities.can_fmt_row == CAP_IGNORED
    assert capabilities.can_fmt_value == CAP_IGNORED
    assert capabilities.filtered_data_range == CAP_IGNORED
    assert capabilities.can_write_box == CAP_IMPLEMENTED
    assert capabilities.can_read_box == CAP_IMPLEMENTED
    assert capabilities.can_write_highlight == CAP_IGNORED
    assert capabilities.multi_sheet == CAP_IMPLEMENTED
    assert capabilities.can_find_value_position == CAP_IMPLEMENTED
    check_capsys(capsys)


def test_excel_pylightxl_get_description_uses_lower_priority(
        capsys: CaptureFixture[str]) -> None:
    """The backend stays below OpenPyXL in default factory preference."""
    description = TableIOExcelPylightxl.get_description()
    assert description.format_name == 'Excel'
    assert description.implementation == 'pylightxl'
    assert description.priority == 8
    assert description.priority < TableIOExcelOpenPyXL.get_description(
    ).priority
    check_capsys(capsys)


def test_excel_factory_can_create_pylightxl_explicitly(
        capsys: CaptureFixture[str]) -> None:
    """The factory can create the backend when requested explicitly."""
    with TemporaryDirectory() as temp_dir:
        table_io = create_tableio('Excel', Path(temp_dir) / 'explicit',
                                  FileAccess.CREATE,
                                  implementation='pylightxl')
        assert isinstance(table_io, TableIOExcelPylightxl)
    check_capsys(capsys)


def test_excel_pylightxl_round_trip_sequential_list_reads(
        capsys: CaptureFixture[str]) -> None:
    """Two list sections can be written and then read back sequentially."""
    run_round_trip_sequential_list_reads(TableIOExcelPylightxl, capsys)


def test_excel_pylightxl_round_trip_dictdata_in_box(
        capsys: CaptureFixture[str]) -> None:
    """Dict data can be written into and read back from a box."""
    run_round_trip_dictdata_in_box(TableIOExcelPylightxl, capsys)


def test_excel_pylightxl_multi_sheet_write_positions_are_per_sheet(
        capsys: CaptureFixture[str]) -> None:
    """Sequential writes keep an independent default position per sheet."""
    run_multi_sheet_write_positions_are_per_sheet(
        TableIOExcelPylightxl, capsys)


def test_excel_pylightxl_multi_sheet_read_positions_are_per_sheet(
        capsys: CaptureFixture[str]) -> None:
    """Sequential reads resume independently when switching sheets."""
    run_multi_sheet_read_positions_are_per_sheet(
        TableIOExcelPylightxl, capsys)


def test_excel_pylightxl_multi_sheet_heading_state_is_per_sheet(
        capsys: CaptureFixture[str]) -> None:
    """Each sheet tracks whether a default heading level was used before."""
    run_multi_sheet_heading_state_is_per_sheet(
        TableIOExcelPylightxl, capsys)


def test_excel_pylightxl_multi_sheet_read_only_create_raises(
        capsys: CaptureFixture[str]) -> None:
    """READ mode can select an existing sheet but cannot create one."""
    run_multi_sheet_read_only_create_raises(
        TableIOExcelPylightxl, capsys)


def test_excel_pylightxl_update_default_write_starts_after_last_used_row(
        capsys: CaptureFixture[str]) -> None:
    """UPDATE mode appends after the used area with a blank row separator."""
    run_update_default_write_starts_after_last_used_row(
        TableIOExcelPylightxl, '.xlsx', create_update_workbook,
        inspect_updated_workbook, capsys)


def test_excel_pylightxl_multi_sheet_update_uses_selected_sheet_write_position(
        capsys: CaptureFixture[str]) -> None:
    """UPDATE mode appends using the selected sheet's used area."""
    run_multi_sheet_update_uses_selected_sheet_write_position(
        TableIOExcelPylightxl, capsys)


def test_excel_pylightxl_find_value_and_write_cells(
        capsys: CaptureFixture[str]) -> None:
    """Found cell ranges can be read and updated without moving cursors."""
    run_find_value_and_write_cells(
        TableIOExcelPylightxl, '.xlsx',
        inspect_find_and_write_cells_workbook, capsys)


def test_excel_pylightxl_boxed_table_partial_overwrite_raises(
        capsys: CaptureFixture[str]) -> None:
    """Boxed table writes reject overlaps that leave part of a table behind."""
    run_boxed_table_partial_overwrite_raises(
        TableIOExcelPylightxl, capsys)


def test_excel_pylightxl_read_formula_uses_cached_value(
        capsys: CaptureFixture[str]) -> None:
    """A formula cell is read as its cached value."""
    run_read_formula_uses_cached_value(
        TableIOExcelPylightxl, '.xlsx', create_formula_workbook, 3,
        capsys)


def test_excel_pylightxl_read_formula_without_cached_value_returns_none(
        capsys: CaptureFixture[str]) -> None:
    """A formula without a cached result is read as None."""
    run_read_formula_without_cached_value(
        TableIOExcelPylightxl, '.xlsx', create_formula_workbook,
        capsys)


def test_excel_pylightxl_open_rejects_second_open(
        capsys: CaptureFixture[str]) -> None:
    """Opening the same Excel object twice raises RuntimeError."""
    run_open_rejects_second_open(TableIOExcelPylightxl, capsys)


def test_excel_pylightxl_select_missing_sheet_without_create_raises(
        capsys: CaptureFixture[str]) -> None:
    """Selecting a missing sheet without create=True raises KeyError."""
    run_select_missing_sheet_without_create_raises_key_error(
        TableIOExcelPylightxl, capsys)


def test_excel_pylightxl_ignored_format_and_filter_requests_keep_data(
        capsys: CaptureFixture[str]) -> None:
    """Formatting and filtered-range requests are ignored but data is kept."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'ignored_features'
        with TableIOExcelPylightxl(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_listdata([
                [ValueFmt(value='name', fmt=Fmt(bold=True)),
                 ValueFmt(value='active',
                          fmt=Fmt(highlight=Color.YELLOW))],
                [ValueFmt(value='Alice',
                          fmt=Fmt(italic=True, highlight=Color.GREEN)),
                 ValueFmt(value=True,
                          fmt=Fmt(italic=True, highlight=Color.GREEN))]
            ], filtered_data_range=True)
            table_io.write_table_fmtdictdata(
                data=[FmtDictRow(values={'name': 'Bob', 'active': False},
                                 fmt=Fmt(bold=True))],
                column_order=['name', 'active'],
                first_row_format=Fmt(bold=True),
                filtered_data_range=True,
                box=Box(top=4, left=0, bottom=6, right=2))
        workbook = load_workbook(Path(temp_dir) / 'ignored_features.xlsx')
        worksheet = workbook.active
        assert isinstance(worksheet, Worksheet)
        assert worksheet['A1'].value == 'name'
        assert worksheet['B2'].value is True
        assert worksheet['A5'].value == 'name'
        assert worksheet['B6'].value is False
        assert not worksheet.tables
        assert worksheet['A1'].font.bold is False
        assert worksheet['A2'].font.italic is False
        workbook.close()
    check_capsys(capsys)


def test_excel_pylightxl_reads_openpyxl_datetime_cells(
        capsys: CaptureFixture[str]) -> None:
    """The read workaround handles ordinary OpenPyXL datetime cells."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'openpyxl_datetime.xlsx'
        workbook = Workbook()
        worksheet = workbook.active
        assert isinstance(worksheet, Worksheet)
        when = datetime(2026, 3, 24, 14, 30, 0)
        worksheet['A1'] = when
        worksheet['B1'] = 'x'
        workbook.save(file_name)
        workbook.close()
        with TableIOExcelPylightxl(
                Path(temp_dir) / 'openpyxl_datetime',
                FileAccess.READ) as table_io:
            result = table_io.read_table_listdata()
        assert result.data == [[when, 'x']]
    check_capsys(capsys)


def test_excel_pylightxl_writes_datetime_readably_and_reads_it_back(
        capsys: CaptureFixture[str]) -> None:
    """Written datetime cells stay readable in Excel and round-trip here."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'datetime_roundtrip'
        when = datetime(2026, 3, 24, 14, 30, 0)
        with TableIOExcelPylightxl(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_listdata([['when'], [when]])
        workbook = load_workbook(Path(temp_dir) / 'datetime_roundtrip.xlsx')
        worksheet = workbook.active
        assert isinstance(worksheet, Worksheet)
        assert worksheet['A2'].value == '2026/03/24 14:30:00'
        workbook.close()
        with TableIOExcelPylightxl(
                Path(temp_dir) / 'datetime_roundtrip',
                FileAccess.READ) as table_io:
            result = table_io.read_table_listdata()
        assert result.data == [['when'], [when]]
    check_capsys(capsys)


def test_excel_pylightxl_update_keeps_datetime_cells_readable(
        capsys: CaptureFixture[str]) -> None:
    """UPDATE mode preserves readable datetime data while appending rows."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'update_datetime.xlsx'
        workbook = Workbook()
        worksheet = workbook.active
        assert isinstance(worksheet, Worksheet)
        when = datetime(2026, 3, 24, 14, 30, 0)
        worksheet['A1'] = when
        worksheet['B1'] = 'start'
        workbook.save(file_name)
        workbook.close()
        with TableIOExcelPylightxl(
                Path(temp_dir) / 'update_datetime',
                FileAccess.UPDATE) as table_io:
            table_io.write_table_listdata([['new', 'row']])
        workbook = load_workbook(file_name)
        worksheet = workbook.active
        assert isinstance(worksheet, Worksheet)
        assert worksheet['A1'].value == '2026/03/24 14:30:00'
        assert worksheet['B1'].value == 'start'
        assert worksheet['A3'].value == 'new'
        workbook.close()
        with TableIOExcelPylightxl(
                Path(temp_dir) / 'update_datetime',
                FileAccess.READ) as table_io:
            first_result = table_io.read_table_listdata()
            second_result = table_io.read_table_listdata()
        assert first_result.data == [[when, 'start']]
        assert second_result.data == [['new', 'row']]
    check_capsys(capsys)
