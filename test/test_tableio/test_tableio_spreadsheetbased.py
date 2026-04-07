#! /usr/local/bin/python3
"""Tests for the tableio_spreadsheetbased module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional

import pytest
from pytest import CaptureFixture

from tableio.border_helper import BorderWeight, CellBorder
from tableio.capability import Capabilities
from tableio.tableio import Box, Descriptor, FileAccess, Position
from tableio.tableio_types import TableBorderStyle
from tableio.tableio_spreadsheetbased import _ScanResult, \
    TableIOSpreadsheetBased
from tableio.value_type import CellT, Fmt, FmtListRow, ListDataSeq, Value, \
    ValueFmt
from tableio.capability import CAP_ALL_IMPLEMENTED

from .check_capsys import check_capsys
from .spreadsheet_test_helper import run_boxed_table_partial_overwrite_raises


class _MemorySheet:
    """In-memory sheet used by the spreadsheet-base tests."""

    def __init__(self) -> None:
        """Initialize the in-memory sheet."""
        self.values: dict[tuple[int, int], Value] = {}
        self.formats: dict[tuple[int, int], Fmt] = {}
        self.borders: dict[tuple[int, int], CellBorder] = {}
        self.filtered_ranges: dict[str, tuple[int, int, int, int]] = {}
        self.column_widths: dict[int, float] = {}
        self.heading_levels: dict[tuple[int, int], int] = {}

    def set_value(self, row: int, column: int, value: Value) -> None:
        """Store one cell value."""
        self.values[(row, column)] = value

    def clear_value(self, row: int, column: int) -> None:
        """Remove one cell value if present."""
        self.values.pop((row, column), None)


class _MinimalSpreadsheetTableIO(TableIOSpreadsheetBased):
    """Minimal subclass exposing inherited abstract spreadsheet hooks."""

    def __init__(self, file_name: str | Path,
                 file_access: FileAccess = FileAccess.CREATE):
        """Initialize the minimal spreadsheet test double."""
        super().__init__(file_name=file_name, file_access=file_access)

    @classmethod
    def get_description(cls) -> Descriptor:
        """Return a descriptor that allows test instantiation."""
        return Descriptor(format_name='minimal-spreadsheet',
                          implementation='test',
                          capabilities=Capabilities(),
                          mandatory_args=[],
                          optional_args=[])

    @classmethod
    def get_capabilities(cls) -> Capabilities:
        """Return empty capabilities for the minimal implementation."""
        return Capabilities()

    @classmethod
    def file_name_extension(cls) -> str:
        """Return the file name extension used in tests."""
        return 'sheet'

    def open(self) -> None:
        """Initialize the inherited per-sheet positions."""
        self._initialize_positions()

    def _close(self) -> None:
        """No-op close hook for tests."""

    def _end_state(self) -> None:
        """No-op end-state hook for tests."""

    def _write_file_suffix(self) -> None:
        """No-op suffix hook for tests."""

    def _list_sheets(self) -> list[str]:
        """Return the single test sheet name."""
        return ['Sheet1']

    def _select_sheet(self, sheet_name: str, create: bool = False) -> None:
        """Validate the requested test sheet name."""
        _ = create
        if sheet_name != 'Sheet1':
            raise KeyError(sheet_name)

    def _current_sheet_name(self) -> str:
        """Return the single test sheet name."""
        return 'Sheet1'

    def run_read_sheet(self) -> object:
        """Expose the inherited _read_sheet method for tests."""
        return self._read_sheet()

    def run_write_sheet(self) -> object:
        """Expose the inherited _write_sheet method for tests."""
        return self._write_sheet()

    def run_write_value_to_sheet(self, sheet: object, row: int,
                                 column: int, value: object) -> None:
        """Expose the inherited _write_value_to_sheet method for tests."""
        self._write_value_to_sheet(sheet, row, column, value)

    def run_set_cell_format(self, sheet: object, row: int,
                            column: int, fmt: Optional[Fmt]) -> None:
        """Expose the inherited _set_cell_format method for tests."""
        self._set_cell_format(sheet, row, column, fmt)

    def run_set_cell_borders(self, sheet: object, row: int, column: int,
                             borders: CellBorder) -> None:
        """Expose the inherited _set_cell_borders method for tests."""
        self._set_cell_borders(sheet, row, column, borders)

    def run_apply_heading_style(self, row: int, column: int,
                                level: int) -> None:
        """Expose the inherited _apply_heading_style method for tests."""
        self._apply_heading_style(row, column, level)

    def run_last_used_row(self, sheet: object) -> int:
        """Expose the inherited _last_used_row method for tests."""
        return self._last_used_row(sheet)

    def run_last_used_column(self, sheet: object) -> int:
        """Expose the inherited _last_used_column method for tests."""
        return self._last_used_column(sheet)

    def run_cell_value(self, sheet: object, row: int, column: int) -> Value:
        """Expose the inherited _cell_value method for tests."""
        return self._cell_value(sheet, row, column)

    def run_filtered_range_infos(self) -> list[tuple[str, tuple[int, int,
                                                                int, int]]]:
        """Expose the inherited _filtered_range_infos method for tests."""
        return self._filtered_range_infos()

    def run_delete_filtered_range(self, name: str) -> None:
        """Expose the inherited _delete_filtered_range method for tests."""
        self._delete_filtered_range(name)

    def run_add_filtered_range(self, bounds: tuple[int, int, int, int],
                               name: str) -> None:
        """Expose the inherited _add_filtered_range method for tests."""
        self._add_filtered_range(bounds, name)

    def run_set_column_width_if_wider(self, column: int, width: float) -> \
            None:
        """Expose the inherited width helper for tests."""
        self._set_column_width_if_wider(column, width)


# pylint: disable-next=too-many-instance-attributes,too-many-public-methods
class _RecordingSpreadsheetTableIO(TableIOSpreadsheetBased):
    """Concrete in-memory spreadsheet backend used by the tests."""

    def __init__(self, file_name: str | Path,
                 file_access: FileAccess = FileAccess.CREATE,
                 separate_read_sheet: bool = False):
        """Initialize the in-memory spreadsheet backend."""
        super().__init__(file_name=file_name, file_access=file_access)
        self._separate_read_sheet = separate_read_sheet
        self._sheet_order: list[str] = ['Sheet1']
        self._selected_sheet_name = 'Sheet1'
        self._write_sheets: dict[str, _MemorySheet] = {
            'Sheet1': _MemorySheet()
        }
        self._read_sheets: dict[str, _MemorySheet] = {
            'Sheet1': _MemorySheet() if separate_read_sheet else
            self._write_sheets['Sheet1']
        }
        self.is_open = False

    @classmethod
    def get_description(cls) -> Descriptor:
        """Return the descriptor for the recording backend."""
        return Descriptor(format_name='recording-spreadsheet',
                          implementation='test',
                          capabilities=cls.get_capabilities(),
                          mandatory_args=[],
                          optional_args=[])

    @classmethod
    def get_capabilities(cls) -> Capabilities:
        """Return the capabilities for the recording backend."""
        return CAP_ALL_IMPLEMENTED

    @classmethod
    def file_name_extension(cls) -> str:
        """Return the file name extension used in tests."""
        return 'sheet'

    def open(self) -> None:
        """Open the in-memory backend."""
        if self.is_open:
            raise RuntimeError(f'File {self.file_name} already open')
        self.is_open = True
        self._initialize_positions()

    def _close(self) -> None:
        """Close the in-memory backend."""
        self.is_open = False

    def _end_state(self) -> None:
        """No-op end-state hook for tests."""

    def _write_file_suffix(self) -> None:
        """No-op suffix hook for tests."""

    def _list_sheets(self) -> list[str]:
        """Return the configured sheet names."""
        return list(self._sheet_order)

    def _select_sheet(self, sheet_name: str, create: bool = False) -> None:
        """Select or create the requested in-memory sheet."""
        matched_name = self._find_matching_sheet_name(self._sheet_order,
                                                      sheet_name)
        if matched_name is None:
            if not create:
                raise KeyError(sheet_name)
            self._check_file_is_writable()
            matched_name = sheet_name
            self._sheet_order.append(sheet_name)
            self._write_sheets[sheet_name] = _MemorySheet()
            if self._separate_read_sheet:
                self._read_sheets[sheet_name] = _MemorySheet()
            else:
                self._read_sheets[sheet_name] = self._write_sheets[sheet_name]
        self._save_current_sheet_state()
        self._selected_sheet_name = matched_name
        self._load_current_sheet_state()

    def _current_sheet_name(self) -> str:
        """Return the selected in-memory sheet name."""
        return self._selected_sheet_name

    def _read_sheet(self) -> object:
        """Return the readable in-memory sheet."""
        return self._read_sheets[self._selected_sheet_name]

    def _write_sheet(self) -> object:
        """Return the writable in-memory sheet."""
        return self._write_sheets[self._selected_sheet_name]

    def _write_value_to_sheet(self, sheet: object, row: int,
                              column: int, value: object) -> None:
        """Write one value to the in-memory sheet."""
        memory_sheet = sheet
        assert isinstance(memory_sheet, _MemorySheet)
        key = (row, column)
        memory_sheet.formats.pop(key, None)
        memory_sheet.borders.pop(key, None)
        memory_sheet.heading_levels.pop(key, None)
        if value is None:
            memory_sheet.values.pop(key, None)
            return
        memory_sheet.values[key] = self._spreadsheet_value_from_python(value)

    def _set_cell_format(self, sheet: object, row: int, column: int,
                         fmt: Optional[Fmt]) -> None:
        """Apply one optional format to one in-memory cell."""
        memory_sheet = sheet
        assert isinstance(memory_sheet, _MemorySheet)
        key = (row, column)
        if fmt is None:
            memory_sheet.formats.pop(key, None)
            return
        memory_sheet.formats[key] = fmt

    def _set_cell_borders(self, sheet: object, row: int, column: int,
                          borders: CellBorder) -> None:
        """Apply one normalized border value to one in-memory cell."""
        memory_sheet = sheet
        assert isinstance(memory_sheet, _MemorySheet)
        key = (row, column)
        if all(weight == BorderWeight.NONE for weight in borders):
            memory_sheet.borders.pop(key, None)
            return
        memory_sheet.borders[key] = borders

    def _apply_heading_style(self, row: int, column: int, level: int) -> None:
        """Record one heading style application."""
        memory_sheet = self._write_sheets[self._selected_sheet_name]
        memory_sheet.heading_levels[(row, column)] = level

    def _last_used_row(self, sheet: object) -> int:
        """Return the last row index with any value."""
        memory_sheet = sheet
        assert isinstance(memory_sheet, _MemorySheet)
        if not memory_sheet.values:
            return -1
        return max(row for row, _ in memory_sheet.values)

    def _last_used_column(self, sheet: object) -> int:
        """Return the last column index with any value."""
        memory_sheet = sheet
        assert isinstance(memory_sheet, _MemorySheet)
        if not memory_sheet.values:
            return -1
        return max(column for _, column in memory_sheet.values)

    def _cell_value(self, sheet: object, row: int, column: int) -> Value:
        """Return one in-memory cell value."""
        memory_sheet = sheet
        assert isinstance(memory_sheet, _MemorySheet)
        return memory_sheet.values.get((row, column))

    def _filtered_range_infos(self) -> list[tuple[str, tuple[int, int,
                                                             int, int]]]:
        """Return the configured filtered ranges for the selected sheet."""
        memory_sheet = self._write_sheets[self._selected_sheet_name]
        return list(memory_sheet.filtered_ranges.items())

    def _delete_filtered_range(self, name: str) -> None:
        """Delete one filtered range from the selected sheet."""
        memory_sheet = self._write_sheets[self._selected_sheet_name]
        del memory_sheet.filtered_ranges[name]

    def _add_filtered_range(self, bounds: tuple[int, int, int, int],
                            name: str) -> None:
        """Add one filtered range to the selected sheet."""
        memory_sheet = self._write_sheets[self._selected_sheet_name]
        memory_sheet.filtered_ranges[name] = bounds

    def _set_column_width_if_wider(self, column: int, width: float) -> None:
        """Store the widest requested width for one column."""
        memory_sheet = self._write_sheets[self._selected_sheet_name]
        current = memory_sheet.column_widths.get(column)
        if current is None or width > current:
            memory_sheet.column_widths[column] = width

    def seed_value(self, row: int, column: int, value: object) -> None:
        """Populate both read and write sheets with one starting value."""
        self._write_value_to_sheet(self._write_sheet(), row, column, value)
        read_sheet = self._read_sheet()
        write_sheet = self._write_sheet()
        if read_sheet is not write_sheet:
            self._write_value_to_sheet(read_sheet, row, column, value)

    def write_sheet_data(self) -> _MemorySheet:
        """Return the writable sheet object for direct assertions."""
        sheet = self._write_sheet()
        assert isinstance(sheet, _MemorySheet)
        return sheet

    def read_sheet_data(self) -> _MemorySheet:
        """Return the readable sheet object for direct assertions."""
        sheet = self._read_sheet()
        assert isinstance(sheet, _MemorySheet)
        return sheet

    @staticmethod
    def convert_from_spreadsheet(value: object) -> Value:
        """Expose the backend-to-public conversion helper for tests."""
        return TableIOSpreadsheetBased._python_value_from_spreadsheet(value)

    @staticmethod
    def convert_to_spreadsheet(value: object) -> Value:
        """Expose the public-to-backend conversion helper for tests."""
        return TableIOSpreadsheetBased._spreadsheet_value_from_python(value)

    def run_write_value(self, row: int, column: int, value: object,
                        fmt: Optional[Fmt] = None) -> None:
        """Expose the value-writing helper for tests."""
        self._write_value(row, column, value, fmt)

    def run_clear_range(self, top: int, left: int,
                        bottom: int, right: int) -> None:
        """Expose the range-clearing helper for tests."""
        self._clear_range(top, left, bottom, right)

    def run_scan_limit_right(self, sheet: object, left: int,
                             right: Optional[int]) -> int:
        """Expose the scan-right helper for tests."""
        return self._scan_limit_right(sheet, left, right)

    def run_row_is_heading(  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
            self, sheet: object, row: int, left: int,
            right: Optional[int], bottom: int) -> bool:
        """Expose the row-heading helper for tests."""
        return self._row_is_heading(sheet, row, left, right, bottom)

    def run_scan_section(self, box: Optional[Box]) -> _ScanResult:
        """Expose the section scanner for tests."""
        return self._scan_section(box)

    def run_read_grid(self, scan: _ScanResult) -> list[list[Value]]:
        """Expose the grid reader for tests."""
        return self._read_grid(scan)

    def run_filter_range_name_in_use(self, name: str) -> bool:
        """Expose filtered-range name lookup for tests."""
        return self._filter_range_name_in_use(name)

    def run_next_filter_range_name(self) -> str:
        """Expose filtered-range name generation for tests."""
        return self._next_filter_range_name()

    def run_remove_overlapping_filtered_ranges(
            self, bounds: tuple[int, int, int, int]) -> None:
        """Expose filtered-range overlap removal for tests."""
        self._remove_overlapping_filtered_ranges(bounds)

    def run_write_filtered_data_range(
            self, bounds: tuple[int, int, int, int]) -> None:
        """Expose filtered-range creation for tests."""
        self._write_filtered_data_range(bounds)

    @staticmethod
    def column_width_text(value: object) -> str:
        """Expose the column-width text conversion helper for tests."""
        return TableIOSpreadsheetBased._column_width_text(value)

    def run_table_column_width(self, top: int, bottom: int,
                               column: int) -> float:
        """Expose the table-column-width helper for tests."""
        return self._table_column_width(top, bottom, column)

    def run_update_table_column_widths(self, top: int, left: int,
                                       bottom: int, right: int) -> None:
        """Expose the width-update helper for tests."""
        self._update_table_column_widths(top, left, bottom, right)

    def run_sheet_table_regions(self) -> list[tuple[int, int, int, int]]:
        """Expose inferred table-region detection for tests."""
        return self._sheet_table_regions()

    @classmethod
    def split_plain_cell_value(
            cls, cell: Value) -> tuple[Value, Optional[Fmt]]:
        """Expose plain cell splitting for tests."""
        return cls._split_cell_value(cell)

    @classmethod
    def split_formatted_cell_value(
            cls, cell: ValueFmt) -> tuple[Value, Optional[Fmt]]:
        """Expose formatted cell splitting for tests."""
        return cls._split_cell_value(cell)

    def run_find_value(self, find_value: list[list[Value]],
                       type_conversion: bool = True,
                       box: Optional[Box] = None) -> Optional[Box]:
        """Expose the grid-find helper for tests."""
        return self._find_value(find_value, type_conversion, box)

    def run_read_cells(self, box: Box) -> list[list[Value]]:
        """Expose exact cell reads for tests."""
        return self._read_cells(box)

    def run_write_cells(self, data: ListDataSeq[CellT],
                        box: Box) -> None:
        """Expose exact cell writes for tests."""
        self._write_cells(data, box)


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        pytest.param(None, None, id='none'),
        pytest.param(datetime(2026, 3, 27, 8, 9, 10),
                     datetime(2026, 3, 27, 8, 9, 10),
                     id='datetime'),
        pytest.param(date(2026, 3, 27),
                     datetime(2026, 3, 27, 0, 0, 0),
                     id='date'),
        pytest.param(Decimal('4'), 4, id='decimal-int'),
        pytest.param(Decimal('4.5'), 4.5, id='decimal-float'),
        pytest.param('text', 'text', id='str'),
        pytest.param(True, True, id='bool'),
        pytest.param(7, 7, id='int'),
        pytest.param(2.5, 2.5, id='float'),
        pytest.param(complex(1, 2), '(1+2j)', id='other-object')
    ]
)
def test_python_value_from_spreadsheet_converts_supported_types(
        value: object, expected: Value,
        capsys: CaptureFixture[str]) -> None:
    """Spreadsheet helper converts backend values to the public value type."""
    assert _RecordingSpreadsheetTableIO.convert_from_spreadsheet(value) == \
        expected
    assert _RecordingSpreadsheetTableIO.convert_to_spreadsheet(value) == \
        expected
    check_capsys(capsys)


def test_spreadsheet_base_abstract_hooks_raise_not_implemented(
        capsys: CaptureFixture[str]) -> None:
    """Protected spreadsheet hooks stay abstract by default."""
    table_io = _MinimalSpreadsheetTableIO('sample')
    with pytest.raises(NotImplementedError, match='_read_sheet method'):
        table_io.run_read_sheet()
    with pytest.raises(NotImplementedError, match='_write_sheet method'):
        table_io.run_write_sheet()
    with pytest.raises(NotImplementedError,
                       match='_write_value_to_sheet method'):
        table_io.run_write_value_to_sheet(object(), 0, 0, 'value')
    with pytest.raises(NotImplementedError, match='_set_cell_format method'):
        table_io.run_set_cell_format(object(), 0, 0, Fmt())
    with pytest.raises(NotImplementedError, match='_set_cell_borders method'):
        table_io.run_set_cell_borders(
            object(), 0, 0,
            CellBorder(BorderWeight.NONE, BorderWeight.NONE,
                       BorderWeight.NONE, BorderWeight.NONE))
    with pytest.raises(NotImplementedError,
                       match='_apply_heading_style method'):
        table_io.run_apply_heading_style(0, 0, 1)
    with pytest.raises(NotImplementedError, match='_last_used_row method'):
        table_io.run_last_used_row(object())
    with pytest.raises(NotImplementedError, match='_last_used_column method'):
        table_io.run_last_used_column(object())
    with pytest.raises(NotImplementedError, match='_cell_value method'):
        table_io.run_cell_value(object(), 0, 0)
    with pytest.raises(NotImplementedError,
                       match='_filtered_range_infos method'):
        table_io.run_filtered_range_infos()
    with pytest.raises(NotImplementedError,
                       match='_delete_filtered_range method'):
        table_io.run_delete_filtered_range('TableIOFilter_1')
    with pytest.raises(
            NotImplementedError, match='_add_filtered_range method'):
        table_io.run_add_filtered_range((0, 0, 1, 1), 'TableIOFilter_1')
    with pytest.raises(NotImplementedError,
                       match='_set_column_width_if_wider method'):
        table_io.run_set_column_width_if_wider(0, 10.0)
    check_capsys(capsys)


def test_spreadsheet_write_value_updates_separate_read_snapshot(
        capsys: CaptureFixture[str]) -> None:
    """Writing one value mirrors data to the read snapshot, not the format."""
    with TemporaryDirectory() as temp_dir:
        table_io = _RecordingSpreadsheetTableIO(
            Path(temp_dir) / 'sample',
            FileAccess.CREATE,
            separate_read_sheet=True)
        with table_io:
            table_io.run_write_value(1, 2, 'alpha', Fmt(bold=True))
            assert table_io.write_sheet_data().values[(1, 2)] == 'alpha'
            assert table_io.read_sheet_data().values[(1, 2)] == 'alpha'
            assert table_io.write_sheet_data().formats[(1, 2)] == \
                Fmt(bold=True)
            assert (1, 2) not in table_io.read_sheet_data().formats
    check_capsys(capsys)


def test_spreadsheet_clear_range_clears_write_and_read_snapshots(
        capsys: CaptureFixture[str]) -> None:
    """Clearing a rectangle removes the values from both sheet snapshots."""
    with TemporaryDirectory() as temp_dir:
        table_io = _RecordingSpreadsheetTableIO(
            Path(temp_dir) / 'sample',
            FileAccess.CREATE,
            separate_read_sheet=True)
        with table_io:
            table_io.seed_value(0, 0, 'left')
            table_io.seed_value(0, 1, 'right')
            table_io.run_clear_range(0, 0, 1, 2)
            assert table_io.write_sheet_data().values == {}
            assert table_io.read_sheet_data().values == {}
    check_capsys(capsys)


def test_spreadsheet_scan_helpers_cover_edge_cases(
        capsys: CaptureFixture[str]) -> None:
    """Sheet scanning handles empty prefixes, headings, and empty tables."""
    with TemporaryDirectory() as temp_dir:
        table_io = _RecordingSpreadsheetTableIO(Path(temp_dir) / 'sample')
        with table_io:
            sheet = table_io.write_sheet_data()
            assert table_io.run_scan_limit_right(sheet, 2, None) == 2
            table_io.seed_value(0, 0, 'Tail heading')
            assert table_io.run_row_is_heading(sheet, 0, 0, None, 1) is \
                False
            table_io.run_clear_range(0, 0, 1, 1)
            table_io.seed_value(1, 0, 'Report')
            table_io.seed_value(3, 0, 'name')
            table_io.seed_value(3, 1, 'active')
            table_io.seed_value(4, 0, 'Alice')
            table_io.seed_value(4, 1, True)
            scan = table_io.run_scan_section(None)
            assert scan.headings == ['Report']
            assert scan.table_top == 3
            assert scan.table_bottom == 5
            assert scan.table_left == 0
            assert scan.table_right == 2
            assert scan.last_read_row == 4
            assert scan.next_read_row == 5
            empty_grid = table_io.run_read_grid(_ScanResult(
                headings=[],
                table_top=2,
                table_bottom=2,
                table_left=1,
                table_right=3,
                last_read_row=1,
                next_read_row=2))
            assert not empty_grid
    check_capsys(capsys)


def test_spreadsheet_filter_range_helpers_remove_overlaps_and_pick_next_name(
        capsys: CaptureFixture[str]) -> None:
    """Filtered-range helpers reuse the first free name and remove overlaps."""
    with TemporaryDirectory() as temp_dir:
        table_io = _RecordingSpreadsheetTableIO(Path(temp_dir) / 'sample')
        with table_io:
            sheet = table_io.write_sheet_data()
            sheet.filtered_ranges['TableIOFilter_1'] = (0, 0, 2, 2)
            sheet.filtered_ranges['TableIOFilter_3'] = (4, 4, 6, 6)
            assert table_io.run_filter_range_name_in_use('TableIOFilter_1') \
                is \
                True
            assert table_io.run_filter_range_name_in_use('TableIOFilter_2') \
                is \
                False
            assert table_io.run_next_filter_range_name() == 'TableIOFilter_2'
            table_io.run_remove_overlapping_filtered_ranges((1, 1, 3, 3))
            assert sheet.filtered_ranges == {
                'TableIOFilter_3': (4, 4, 6, 6)
            }
            table_io.run_write_filtered_data_range((0, 0, 2, 2))
            assert sheet.filtered_ranges['TableIOFilter_1'] == (0, 0, 2, 2)
    check_capsys(capsys)


def test_spreadsheet_column_width_helpers_measure_and_cap_widths(
        capsys: CaptureFixture[str]) -> None:
    """Column width helpers use text lengths and the configured max width."""
    with TemporaryDirectory() as temp_dir:
        table_io = _RecordingSpreadsheetTableIO(Path(temp_dir) / 'sample')
        with table_io:
            table_io.seed_value(0, 0, None)
            table_io.seed_value(1, 0, 'x' * 80)
            table_io.seed_value(0, 1, 'id')
            assert table_io.column_width_text(None) == ''
            assert table_io.column_width_text(12) == '12'
            assert table_io.run_table_column_width(0, 2, 0) == 50.0
            assert table_io.run_table_column_width(0, 1, 1) == 4.0
            table_io.run_update_table_column_widths(0, 0, 2, 2)
            assert table_io.write_sheet_data().column_widths == {
                0: 50.0,
                1: 4.0
            }
    check_capsys(capsys)


def test_spreadsheet_write_start_and_heading_keep_blank_separator(
        capsys: CaptureFixture[str]) -> None:
    """Sequential writes and headings keep one empty row between sections."""
    with TemporaryDirectory() as temp_dir:
        table_io = _RecordingSpreadsheetTableIO(Path(temp_dir) / 'sample')
        with table_io:
            first = table_io.write_table_listdata([['left', 'right']])
            heading = table_io.write_heading('Second block')
            second = table_io.write_table_listdata([['resume', 'here']])
            assert first == Position(0, 1)
            assert heading == Position(2, 0)
            assert second == Position(4, 1)
            assert table_io.write_row == 6
            assert table_io.write_sheet_data().heading_levels[(2, 0)] == 1
            assert table_io.write_sheet_data().values == {
                (0, 0): 'left',
                (0, 1): 'right',
                (2, 0): 'Second block',
                (4, 0): 'resume',
                (4, 1): 'here'
            }
    check_capsys(capsys)


def test_spreadsheet_write_table_fmtlistdata_applies_row_formats(
        capsys: CaptureFixture[str]) -> None:
    """Row-formatted list data is expanded to per-cell formats."""
    with TemporaryDirectory() as temp_dir:
        table_io = _RecordingSpreadsheetTableIO(Path(temp_dir) / 'sample')
        with table_io:
            result = table_io.write_table_fmtlistdata([
                FmtListRow(values=['name', 'active'], fmt=Fmt(bold=True)),
                FmtListRow(values=['Alice', True], fmt=Fmt(italic=True))
            ])
            assert result == Position(1, 1)
            assert table_io.write_sheet_data().formats == {
                (0, 0): Fmt(bold=True),
                (0, 1): Fmt(bold=True),
                (1, 0): Fmt(italic=True),
                (1, 1): Fmt(italic=True)
            }
    check_capsys(capsys)


def test_spreadsheet_write_table_listdata_applies_borders(
        capsys: CaptureFixture[str]) -> None:
    """Table writes apply normalized borders to every affected cell."""
    with TemporaryDirectory() as temp_dir:
        table_io = _RecordingSpreadsheetTableIO(Path(temp_dir) / 'sample')
        with table_io:
            table_io.write_table_listdata(
                [['name', 'value'], ['Alice', 1], ['Bob', 2]],
                border_style=TableBorderStyle.OUTER_FIRST_ROW_THICK_INNER_THIN)
            assert table_io.write_sheet_data().borders == {
                (0, 0): CellBorder(
                    top=BorderWeight.THICK,
                    right=BorderWeight.THIN,
                    bottom=BorderWeight.THICK,
                    left=BorderWeight.THICK),
                (0, 1): CellBorder(
                    top=BorderWeight.THICK,
                    right=BorderWeight.THICK,
                    bottom=BorderWeight.THICK,
                    left=BorderWeight.THIN),
                (1, 0): CellBorder(
                    top=BorderWeight.THICK,
                    right=BorderWeight.THIN,
                    bottom=BorderWeight.THIN,
                    left=BorderWeight.THICK),
                (1, 1): CellBorder(
                    top=BorderWeight.THICK,
                    right=BorderWeight.THICK,
                    bottom=BorderWeight.THIN,
                    left=BorderWeight.THIN),
                (2, 0): CellBorder(
                    top=BorderWeight.THIN,
                    right=BorderWeight.THIN,
                    bottom=BorderWeight.THICK,
                    left=BorderWeight.THICK),
                (2, 1): CellBorder(
                    top=BorderWeight.THIN,
                    right=BorderWeight.THICK,
                    bottom=BorderWeight.THICK,
                    left=BorderWeight.THIN)
            }
    check_capsys(capsys)


def test_spreadsheet_box_rewrite_clears_old_borders(
        capsys: CaptureFixture[str]) -> None:
    """Rewriting the same box with no borders clears old border styles."""
    with TemporaryDirectory() as temp_dir:
        table_io = _RecordingSpreadsheetTableIO(Path(temp_dir) / 'sample')
        with table_io:
            box = Box(top=1, left=2, bottom=3, right=4)
            table_io.write_table_listdata(
                [['left', 'right'], ['down', 'here']],
                box=box,
                border_style=TableBorderStyle.ALL_THICK)
            assert table_io.write_sheet_data().borders
            table_io.write_table_listdata(
                [['new', 'values'], ['stay', 'plain']],
                box=box,
                border_style=TableBorderStyle.NONE)
            assert table_io.write_sheet_data().borders == {}
    check_capsys(capsys)


def test_spreadsheet_find_value_matches_per_cell_with_type_conversion(
        capsys: CaptureFixture[str]) -> None:
    """Grid search can match converted values cell by cell."""
    with TemporaryDirectory() as temp_dir:
        table_io = _RecordingSpreadsheetTableIO(Path(temp_dir) / 'sample')
        with table_io:
            table_io.seed_value(1, 2, '1')
            table_io.seed_value(1, 3, 'true')
            exact = table_io.run_find_value([[1, True]],
                                            type_conversion=False)
            converted = table_io.run_find_value([[1, True]])
            restricted = table_io.run_find_value(
                [[1, True]], box=Box(top=0, left=0, bottom=1, right=4))
            assert exact is None
            assert converted == Box(top=1, left=2, bottom=2, right=4)
            assert restricted is None
    check_capsys(capsys)


def test_spreadsheet_find_value_returns_none_for_too_small_box(
        capsys: CaptureFixture[str]) -> None:
    """Grid search returns None when the search box cannot fit the grid."""
    with TemporaryDirectory() as temp_dir:
        table_io = _RecordingSpreadsheetTableIO(Path(temp_dir) / 'sample')
        with table_io:
            table_io.seed_value(0, 0, 'alpha')
            assert table_io.run_find_value(
                [['alpha', 'beta']],
                box=Box(top=0, left=0, bottom=1, right=1)) is None
    check_capsys(capsys)


def test_spreadsheet_read_and_write_cells_keep_cursor_positions(
        capsys: CaptureFixture[str]) -> None:
    """Exact cell reads and writes do not move the sequential cursors."""
    with TemporaryDirectory() as temp_dir:
        table_io = _RecordingSpreadsheetTableIO(Path(temp_dir) / 'sample')
        with table_io:
            table_io.write_table_listdata([
                ['name', 'active'],
                ['Alice', True]
            ], box=Box(top=1, left=1, bottom=3, right=3))
            table_io.read_row = 7
            table_io.write_row = 9
            table_io.run_write_cells([
                [ValueFmt(value='Alice', fmt=Fmt(bold=True)),
                 ValueFmt(value=False, fmt=Fmt(bold=True))]
            ], Box(top=2, left=1, bottom=3, right=3))
            assert table_io.run_read_cells(
                Box(top=2, left=1, bottom=3, right=3)) == [
                    ['Alice', False]
                ]
            assert table_io.read_row == 7
            assert table_io.write_row == 9
            assert table_io.write_sheet_data().formats[(2, 1)] == \
                Fmt(bold=True)
            assert table_io.write_sheet_data().formats[(2, 2)] == \
                Fmt(bold=True)
    check_capsys(capsys)


def test_spreadsheet_boxed_table_write_rejects_partial_overwrite(
        capsys: CaptureFixture[str]) -> None:
    """Boxed table writes reject overlaps that leave part behind."""
    run_boxed_table_partial_overwrite_raises(
        _RecordingSpreadsheetTableIO, capsys)


def test_spreadsheet_sheet_table_regions_skip_headings_and_blank_breaks(
        capsys: CaptureFixture[str]) -> None:
    """Inferred table regions skip headings and stop at blank rows."""
    with TemporaryDirectory() as temp_dir:
        table_io = _RecordingSpreadsheetTableIO(Path(temp_dir) / 'sample')
        with table_io:
            table_io.seed_value(0, 0, 'Report')
            table_io.seed_value(2, 1, 'name')
            table_io.seed_value(3, 2, 'Alice')
            table_io.seed_value(5, 0, 'tail')
            assert table_io.run_sheet_table_regions() == [
                (2, 1, 4, 3),
                (5, 0, 6, 1)
            ]
    check_capsys(capsys)


def test_spreadsheet_boxed_table_write_allows_full_replacement(
        capsys: CaptureFixture[str]) -> None:
    """Boxed table writes may fully replace a table with a larger one."""
    with TemporaryDirectory() as temp_dir:
        table_io = _RecordingSpreadsheetTableIO(Path(temp_dir) / 'sample')
        with table_io:
            table_io.write_table_listdata([
                ['name', 'active'],
                ['Alice', True]
            ], box=Box(top=1, left=1, bottom=3, right=3))
            table_io.write_table_listdata([
                ['name', 'active', 'note'],
                ['Alice', False, 'updated']
            ], box=Box(top=1, left=1, bottom=3, right=4))
            assert table_io.run_sheet_table_regions() == [(1, 1, 3, 4)]
            assert table_io.write_sheet_data().values[(2, 3)] == 'updated'
    check_capsys(capsys)


def test_spreadsheet_update_mode_initializes_write_row_from_last_used_row(
        capsys: CaptureFixture[str]) -> None:
    """UPDATE mode starts writing after the last used row in the sheet."""
    with TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / 'sample.sheet'
        file_path.touch()
        table_io = _RecordingSpreadsheetTableIO(
            Path(temp_dir) / 'sample', FileAccess.UPDATE)
        table_io.seed_value(2, 0, 'existing')
        with table_io:
            assert table_io.write_row == 3
            table_io.select_sheet('Second', create=True)
            assert table_io.write_row == 0
            table_io.write_table_listdata([['fresh', 'sheet']])
            table_io.select_sheet('Sheet1')
            assert table_io.write_row == 3
        assert file_path.exists()
    check_capsys(capsys)


def test_spreadsheet_split_cell_value_handles_plain_and_formatted_cells(
        capsys: CaptureFixture[str]) -> None:
    """split_cell_value preserves plain values and unwraps ValueFmt cells."""
    plain = _RecordingSpreadsheetTableIO.split_plain_cell_value(3.5)
    formatted = _RecordingSpreadsheetTableIO.split_formatted_cell_value(
        ValueFmt(value=datetime(2026, 3, 28, 0, 0, 0), fmt=Fmt(bold=True)))
    assert plain == (3.5, None)
    assert formatted == (
        datetime(2026, 3, 28, 0, 0, 0),
        Fmt(bold=True)
    )
    check_capsys(capsys)
