#! /usr/local/bin/python3
"""Shared test helpers for spreadsheet-backed TableIO implementations."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import io
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Callable, Optional

import pytest
from pytest import CaptureFixture

from tableio.color import Color
from tableio.tableio import Box, FileAccess, Position, TableIO
from tableio.tableio_spreadsheetbased import TableIOSpreadsheetBased
from tableio.tableio_types import TableBorderStyle
from tableio.value_type import Fmt, FmtDictRow, Value, ValueFmt

from .check_capsys import check_capsys


def run_round_trip_sequential_list_reads(
        tableio_class: type[TableIO],
        capsys: CaptureFixture[str]) -> None:
    """Run the shared sequential list read/write round-trip case."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'sample'
        first_data: list[list[Value]] = [
            ['Flag', 'When'],
            [True, datetime(2026, 3, 23, 10, 0, 0)]
        ]
        second_data: list[list[Value]] = [['One', 'Two'], ['Three', 'Four']]
        with tableio_class(file_name, FileAccess.CREATE) as table_io:
            table_io.write_heading('Report')
            table_io.write_heading('Flags')
            table_io.write_table_listdata(first_data)
            table_io.write_table_listdata(second_data)
        with tableio_class(file_name, FileAccess.READ) as table_io:
            first_result = table_io.read_table_listdata()
            second_result = table_io.read_table_listdata()
        assert first_result.headings == ['Report', 'Flags']
        assert first_result.data == first_data
        assert second_result.headings == []
        assert second_result.data == second_data
    check_capsys(capsys)


def run_round_trip_dictdata_in_box(
        tableio_class: type[TableIO],
        capsys: CaptureFixture[str]) -> None:
    """Run the shared boxed dict-data round-trip case."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'boxed'
        data: list[dict[str, Value]] = [
            {'name': 'Alice', 'active': True},
            {'name': 'Bob', 'active': None}
        ]
        box = Box(top=1, left=1, bottom=4, right=3)
        with tableio_class(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_dictdata(data=data, column_order=[
                'name', 'active'
            ], box=box)
        with tableio_class(file_name, FileAccess.READ) as table_io:
            result = table_io.read_table_dictdata(box=box)
        assert result.headings == []
        assert result.data == data
    check_capsys(capsys)


def run_update_default_write_starts_after_last_used_row(
        tableio_class: type[TableIO],
        extension: str,
        create_file: Callable[[Path], None],
        inspect_file: Callable[[Path], None],
        capsys: CaptureFixture[str]) -> None:
    """Run the shared UPDATE append-position case."""
    with TemporaryDirectory() as temp_dir:
        saved_path = Path(temp_dir) / f'update{extension}'
        create_file(saved_path)
        with tableio_class(
                Path(temp_dir) / 'update', FileAccess.UPDATE) as table_io:
            table_io.write_table_listdata([['new', 'row']])
        inspect_file(saved_path)
    check_capsys(capsys)


def run_write_formatted_listdata_applies_formatting_and_filter(
        tableio_class: type[TableIO],
        extension: str,
        inspect_file: Callable[[Path], None],
        capsys: CaptureFixture[str]) -> None:
    """Run the shared formatted-list write case."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'formatted'
        data = [
            [ValueFmt(value='Name', fmt=Fmt(bold=True)),
             ValueFmt(value='Active', fmt=Fmt(bold=True))],
            [ValueFmt(value='Alice', fmt=Fmt(italic=True,
                                             highlight=Color.YELLOW)),
             ValueFmt(value=True, fmt=Fmt(italic=True,
                                          highlight=Color.YELLOW))]
        ]
        with tableio_class(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_listdata(data, filtered_data_range=True)
        inspect_file(Path(temp_dir) / f'formatted{extension}')
    check_capsys(capsys)


def run_write_multiple_filtered_ranges_keeps_all_ranges(
        tableio_class: type[TableIO],
        extension: str,
        inspect_file: Callable[[Path], None],
        capsys: CaptureFixture[str]) -> None:
    """Run the shared multiple filtered-ranges write case."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'multiple_filters'
        first_data: list[list[Value]] = [['Name', 'Active'], ['Alice', True]]
        second_data: list[list[Value]] = [
            ['Issue', 'State'],
            ['TIO-123', 'Done']
        ]
        with tableio_class(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_listdata(first_data, filtered_data_range=True)
            table_io.write_table_listdata(second_data,
                                          filtered_data_range=True)
        inspect_file(Path(temp_dir) / f'multiple_filters{extension}')
    check_capsys(capsys)


def run_table_width_is_widen_only_with_cap(
        tableio_class: type[TableIO],
        extension: str,
        inspect_file: Callable[[Path], None],
        capsys: CaptureFixture[str]) -> None:
    """Run the shared table-width widening cap case."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'table_width_cap'
        box = Box(top=0, left=0, bottom=2, right=1)
        with tableio_class(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_listdata([
                ['text'],
                ['x' * 80]
            ], box=box)
            table_io.write_table_listdata([
                ['text'],
                ['y']
            ], box=box)
        inspect_file(Path(temp_dir) / f'table_width_cap{extension}')
    check_capsys(capsys)


def run_table_width_uses_table_content_not_heading(
        tableio_class: type[TableIO],
        extension: str,
        inspect_file: Callable[[Path], None],
        capsys: CaptureFixture[str]) -> None:
    """Run the shared table-width case with one heading and one table."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'table_width_heading'
        with tableio_class(file_name, FileAccess.CREATE) as table_io:
            table_io.write_heading('Heading text that is much wider than '
                                   'column A needs')
            table_io.write_table_listdata([
                ['id', 'report date'],
                ['A', datetime(2026, 3, 24, 14, 30, 0)]
            ])
        inspect_file(Path(temp_dir) / f'table_width_heading{extension}')
    check_capsys(capsys)


def run_box_write_removes_overlapping_filtered_range(
        tableio_class: type[TableIO],
        extension: str,
        inspect_file: Callable[[Path], None],
        capsys: CaptureFixture[str]) -> None:
    """Run the shared overlapping filtered-range rewrite case."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'rewrite_box'
        box = Box(top=0, left=0, bottom=2, right=2)
        with tableio_class(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_listdata(
                [['Name', 'Active'], ['Alice', True]],
                filtered_data_range=True,
                box=box)
            table_io.write_table_listdata(
                [['updated', 'value'], ['new', 'row']], box=box)
        inspect_file(Path(temp_dir) / f'rewrite_box{extension}')
    check_capsys(capsys)


def run_write_table_listdata_applies_borders(
        tableio_class: type[TableIO],
        extension: str,
        inspect_file: Callable[[Path], None],
        capsys: CaptureFixture[str]) -> None:
    """Run the shared bordered table write case."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'borders'
        with tableio_class(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_listdata(
                [['name', 'value'], ['Alice', 1]],
                border_style=TableBorderStyle.OUTER_THICK_INNER_THIN)
        inspect_file(Path(temp_dir) / f'borders{extension}')
    check_capsys(capsys)


def run_box_rewrite_clears_old_borders(
        tableio_class: type[TableIO],
        extension: str,
        inspect_file: Callable[[Path], None],
        capsys: CaptureFixture[str]) -> None:
    """Run the shared border-clearing boxed rewrite case."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'rewrite_borders'
        box = Box(top=0, left=0, bottom=2, right=2)
        with tableio_class(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_listdata(
                [['left', 'right'], ['down', 'here']],
                box=box,
                border_style=TableBorderStyle.ALL_THICK)
            table_io.write_table_listdata(
                [['new', 'values'], ['stay', 'plain']],
                box=box,
                border_style=TableBorderStyle.NONE)
        inspect_file(Path(temp_dir) / f'rewrite_borders{extension}')
    check_capsys(capsys)


def run_bordered_workbook_is_validator_clean(
        tableio_class: type[TableIO],
        extension: str,
        validate_file: Callable[[Path], bool]) -> None:
    """Run the shared bordered-workbook validator case."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'validator_borders'
        with tableio_class(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_listdata(
                [['left', 'right'], ['down', 'here']],
                border_style=TableBorderStyle.OUTER_FIRST_ROW_THICK_INNER_THIN)
        assert validate_file(Path(temp_dir) / f'validator_borders{extension}')


def run_find_value_and_write_cells(
        tableio_class: type[TableIOSpreadsheetBased],
        extension: str,
        inspect_file: Callable[[Path], None],
        capsys: CaptureFixture[str]) -> None:
    """Run the shared find-value and exact-cell-write case."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'find_and_write_cells'
        table_box = Box(top=1, left=1, bottom=4, right=3)
        found_box = Box(top=3, left=1, bottom=4, right=3)
        table_io = tableio_class(file_name, FileAccess.CREATE)
        with table_io:
            table_data: list[list[Value]] = [
                ['name', 'active'],
                ['Alice', True],
                ['Bob', False]
            ]
            table_io.write_table_listdata(table_data, box=table_box)
            read_row = table_io.read_row
            write_row = table_io.write_row
            assert table_io.find_value([['Bob', False]]) == found_box
            assert table_io.read_row == read_row
            assert table_io.write_row == write_row
            assert table_io.read_cells(found_box) == [['Bob', False]]
            assert table_io.read_row == read_row
            assert table_io.write_row == write_row
            table_io.write_cells([
                [ValueFmt(value='Bob',
                          fmt=Fmt(highlight=Color.YELLOW)),
                 ValueFmt(value=True,
                          fmt=Fmt(highlight=Color.YELLOW))]
            ], found_box)
            assert table_io.read_cells(found_box) == [['Bob', True]]
            assert table_io.read_row == read_row
            assert table_io.write_row == write_row
        inspect_file(Path(temp_dir) / f'find_and_write_cells{extension}')
    check_capsys(capsys)


def run_boxed_table_partial_overwrite_raises(
        tableio_class: type[TableIO],
        capsys: CaptureFixture[str]) -> None:
    """Run the shared partial boxed-table overwrite rejection case."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'partial_overwrite'
        with tableio_class(file_name, FileAccess.CREATE) as table_io:
            table_data: list[list[Value]] = [
                ['name', 'active'],
                ['Alice', True]
            ]
            replacement_data: list[list[Value]] = [['Alice', False]]
            table_io.write_table_listdata(
                table_data, box=Box(top=1, left=1, bottom=3, right=3))
            with pytest.raises(ValueError, match='partly overwrite'):
                table_io.write_table_listdata(
                    replacement_data,
                    box=Box(top=2, left=1, bottom=3, right=3))
    check_capsys(capsys)


def run_write_row_formatted_dictdata_applies_formatting(
        tableio_class: type[TableIO],
        extension: str,
        inspect_file: Callable[[Path], None],
        capsys: CaptureFixture[str]) -> None:
    """Run the shared row-formatted dict-data write case."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'row_formatted'
        data = [
            FmtDictRow(values={'name': 'Alice', 'active': True},
                       fmt=Fmt(bold=True, highlight=Color.GREEN)),
            FmtDictRow(values={'name': 'Bob', 'active': False},
                       fmt=Fmt(italic=True, highlight=Color.RED))
        ]
        with tableio_class(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_fmtdictdata(
                data=data,
                column_order=['name', 'active'],
                filtered_data_range=True)
        inspect_file(Path(temp_dir) / f'row_formatted{extension}')
    check_capsys(capsys)


def run_write_dictdata_applies_first_row_format(
        tableio_class: type[TableIO],
        extension: str,
        inspect_file: Callable[[Path], None],
        capsys: CaptureFixture[str]) -> None:
    """Run the shared dict-data header formatting case."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'dict_header_fmt'
        data: list[dict[str, Value]] = [
            {'name': 'Alice', 'active': True}
        ]
        with tableio_class(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_dictdata(
                data=data,
                column_order=['name', 'active'],
                first_row_format=Fmt(bold=True,
                                     highlight=Color.YELLOW))
        inspect_file(Path(temp_dir) / f'dict_header_fmt{extension}')
    check_capsys(capsys)


def run_write_fmtdictdata_applies_first_row_format(
        tableio_class: type[TableIO],
        extension: str,
        inspect_file: Callable[[Path], None],
        capsys: CaptureFixture[str]) -> None:
    """Run the shared formatted dict-data header formatting case."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'fmtdict_header_fmt'
        data = [
            FmtDictRow(values={'name': 'Alice', 'active': True},
                       fmt=Fmt(italic=True, highlight=Color.GREEN))
        ]
        with tableio_class(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_fmtdictdata(
                data=data,
                column_order=['name', 'active'],
                first_row_format=Fmt(bold=True))
        inspect_file(Path(temp_dir) / f'fmtdict_header_fmt{extension}')
    check_capsys(capsys)


def run_read_formula_uses_cached_value(
        tableio_class: type[TableIO],
        extension: str,
        create_formula_file: Callable[[Path, Optional[int]], None],
        cached_value: int,
        capsys: CaptureFixture[str]) -> None:
    """Run the shared formula-read case with a cached value."""
    with TemporaryDirectory() as temp_dir:
        saved_path = Path(temp_dir) / f'formula{extension}'
        create_formula_file(saved_path, cached_value)
        with tableio_class(
                Path(temp_dir) / 'formula', FileAccess.READ) as table_io:
            result = table_io.read_table_listdata()
        assert result.data == [[cached_value, 'x']]
    check_capsys(capsys)


def run_read_formula_without_cached_value(
        tableio_class: type[TableIO],
        extension: str,
        create_formula_file: Callable[[Path, Optional[int]], None],
        capsys: CaptureFixture[str]) -> None:
    """Run the shared formula-read case without a cached value."""
    with TemporaryDirectory() as temp_dir:
        saved_path = Path(temp_dir) / f'formula{extension}'
        create_formula_file(saved_path, None)
        with tableio_class(
                Path(temp_dir) / 'formula', FileAccess.READ) as table_io:
            result = table_io.read_table_listdata()
        assert result.data == [[None, 'x']]
    check_capsys(capsys)


def run_multi_sheet_write_positions_are_per_sheet(
        tableio_class: type[TableIO],
        capsys: CaptureFixture[str]) -> None:
    """Run the shared per-sheet write-position case."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'multi_write'
        with tableio_class(file_name, FileAccess.CREATE) as table_io:
            first_sheet = table_io.current_sheet_name()
            assert table_io.list_sheets() == [first_sheet]
            first_position = table_io.write_table_listdata([
                ['left', 'right']
            ])
            table_io.select_sheet('Second', create=True)
            second_position = table_io.write_table_listdata([
                ['other', 'sheet']
            ])
            table_io.select_sheet(first_sheet.lower())
            resumed_position = table_io.write_table_listdata([
                ['resume', 'here']
            ])
        assert first_position == Position(0, 1)
        assert second_position == Position(0, 1)
        assert resumed_position == Position(2, 1)
    check_capsys(capsys)


def run_multi_sheet_read_positions_are_per_sheet(
        tableio_class: type[TableIO],
        capsys: CaptureFixture[str]) -> None:
    """Run the shared per-sheet read-position case."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'multi_read'
        with tableio_class(file_name, FileAccess.CREATE) as table_io:
            first_sheet = table_io.current_sheet_name()
            table_io.write_table_listdata([['first', 'table']])
            table_io.write_table_listdata([['second', 'table']])
            table_io.select_sheet('Second', create=True)
            table_io.write_table_listdata([['other', 'sheet']])
            table_io.select_sheet(first_sheet)
        with tableio_class(file_name, FileAccess.READ) as table_io:
            first_sheet = table_io.current_sheet_name()
            first_result = table_io.read_table_listdata()
            table_io.select_sheet('second')
            second_result = table_io.read_table_listdata()
            table_io.select_sheet(first_sheet)
            resumed_result = table_io.read_table_listdata()
        assert first_result.data == [['first', 'table']]
        assert second_result.data == [['other', 'sheet']]
        assert resumed_result.data == [['second', 'table']]
    check_capsys(capsys)


def run_multi_sheet_heading_state_is_per_sheet(
        tableio_class: type[TableIO],
        capsys: CaptureFixture[str]) -> None:
    """Run the shared per-sheet heading state case."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'multi_heading'
        first_position = Position(0, 0)
        second_position = Position(0, 0)
        with tableio_class(file_name, FileAccess.CREATE) as table_io:
            first_sheet = table_io.current_sheet_name()
            assert table_io.heading_written is False
            first_position = table_io.write_heading('First heading')
            assert table_io.heading_written is True
            table_io.select_sheet('Second', create=True)
            assert table_io.heading_written is False
            second_position = table_io.write_heading('Second heading')
            table_io.select_sheet(first_sheet)
            assert table_io.heading_written is True
        assert first_position == Position(0, 0)
        assert second_position == Position(0, 0)
    check_capsys(capsys)


def run_multi_sheet_read_only_create_raises(
        tableio_class: type[TableIO],
        capsys: CaptureFixture[str]) -> None:
    """Run the shared READ-mode sheet-creation error case."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'multi_read_only'
        with tableio_class(file_name, FileAccess.CREATE) as table_io:
            first_sheet = table_io.current_sheet_name()
            table_io.select_sheet('Existing', create=True)
            table_io.write_table_listdata([['left', 'right']])
            table_io.select_sheet(first_sheet)
        with tableio_class(file_name, FileAccess.READ) as table_io:
            table_io.select_sheet('existing', create=True)
            assert table_io.current_sheet_name() == 'Existing'
            with pytest.raises(io.UnsupportedOperation,
                               match='opened for reading'):
                table_io.select_sheet('Missing', create=True)
    check_capsys(capsys)


def run_multi_sheet_update_uses_selected_sheet_write_position(
        tableio_class: type[TableIO],
        capsys: CaptureFixture[str]) -> None:
    """Run the shared UPDATE selected-sheet append case."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'multi_update'
        with tableio_class(file_name, FileAccess.CREATE) as table_io:
            first_sheet = table_io.current_sheet_name()
            table_io.write_table_listdata([['keep', 'first']])
            table_io.select_sheet('Second', create=True)
            table_io.write_table_listdata([['old', 'row']])
            table_io.select_sheet(first_sheet)
        with tableio_class(file_name, FileAccess.UPDATE) as table_io:
            table_io.select_sheet('Second')
            appended_position = table_io.write_table_listdata([
                ['new', 'row']
            ])
        with tableio_class(file_name, FileAccess.READ) as table_io:
            table_io.select_sheet('Second')
            first_result = table_io.read_table_listdata()
            second_result = table_io.read_table_listdata()
        assert appended_position == Position(2, 1)
        assert first_result.data == [['old', 'row']]
        assert second_result.data == [['new', 'row']]
    check_capsys(capsys)


def run_open_rejects_second_open(tableio_class: type[TableIO],
                                 capsys: CaptureFixture[str]) -> None:
    """Run the shared double-open error case."""
    with TemporaryDirectory() as temp_dir:
        table_io = tableio_class(
            Path(temp_dir) / 'open_twice', FileAccess.CREATE)
        table_io.open()
        with pytest.raises(RuntimeError, match='already open'):
            table_io.open()
        table_io.close()
    check_capsys(capsys)


def run_select_missing_sheet_without_create_raises_key_error(
        tableio_class: type[TableIO],
        capsys: CaptureFixture[str]) -> None:
    """Run the shared missing-sheet selection error case."""
    with TemporaryDirectory() as temp_dir:
        with tableio_class(
                Path(temp_dir) / 'missing_sheet',
                FileAccess.CREATE) as table_io:
            with pytest.raises(KeyError, match='Missing'):
                table_io.select_sheet('Missing')
    check_capsys(capsys)
