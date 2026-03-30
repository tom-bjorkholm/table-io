#! /usr/bin/env python3
"""Intermediate base class for spreadsheet-based file formats."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import date, datetime, time
from decimal import Decimal
from typing import Callable, NamedTuple, Optional
from mformat.mformat import PathLike
from tableio.tableio import Box, FileAccess, Position, TableIO
from tableio.valueconversion import UnreasonableTypeConversion, \
    UnreasonableValueConversion, value2type_of
from tableio.value_type import CellT, DictData, DictDataMap, Fmt, \
    FmtDictData, FmtListData, ListData, ListDataSeq, ReadResult, Value, \
    ValueFmt, row_format_each_cell_dict, row_format_each_cell_list, \
    value_to_str


_FILTER_RANGE_PREFIX = 'TableIOFilter_'
_COLUMN_WIDTH_PADDING = 2
_MAX_COLUMN_WIDTH = 50
_HEADING_FONT_SIZES: dict[int, int] = {
    1: 14,
    2: 12,
    3: 11
}


def excel_column_name(column: int) -> str:
    """Return the Excel-style A1 column name for one zero-based column."""
    ret = ''
    current = column + 1
    while current > 0:
        current, remainder = divmod(current - 1, 26)
        ret = chr(ord('A') + remainder) + ret
    return ret


class _ScanResult(NamedTuple):
    """Details gathered while scanning one worksheet section."""

    headings: list[str]
    table_top: int
    table_bottom: int
    table_left: int
    table_right: int
    last_read_row: int
    next_read_row: int


class _SheetState(NamedTuple):
    """Sequential state tracked for one sheet during an open session."""

    read_row: int
    write_row: int
    heading_written: bool


class TableIOSpreadsheetBased(TableIO):
    """Intermediate TableIO base class for spreadsheet-based file formats.

    This class holds the public spreadsheet semantics shared between Excel
    and ODS backends: sequential reads, boxed reads and writes, headings,
    filtered ranges, and the conversion between list or dict tables and the
    rectangular grid stored in the document.
    """

    def __init__(self, file_name: PathLike,
                 file_access: FileAccess,
                 file_exists_callback: Optional[Callable[[str], None]]
                 = None):
        """Initialize the spreadsheet-based TableIO class."""
        super().__init__(file_name=file_name,
                         file_access=file_access,
                         file_exists_callback=file_exists_callback)
        self.read_row: int = 0
        self.write_row: int = 0
        self._sheet_states: dict[str, _SheetState] = {}

    @staticmethod
    def _heading_font_size(level: int) -> int:
        """Return the font size used for one heading level."""
        return _HEADING_FONT_SIZES[level]

    @staticmethod
    def _python_value_from_spreadsheet(value: object) -> Value:  # pylint: disable=too-many-return-statements # noqa: E501
        """Convert one backend value to the public Value type."""
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, date):
            return datetime.combine(value, time())
        if isinstance(value, Decimal):
            if value == value.to_integral_value():
                return int(value)
            return float(value)
        if isinstance(value, (str, bool, int, float)):
            return value
        return str(value)

    @staticmethod
    def _spreadsheet_value_from_python(value: object) -> Value:
        """Convert one Python value to a spreadsheet-compatible value."""
        return TableIOSpreadsheetBased._python_value_from_spreadsheet(value)

    @staticmethod
    def _sheet_key(sheet_name: str) -> str:
        """Return the normalized dictionary key for one sheet name."""
        return sheet_name.casefold()

    @classmethod
    def _find_matching_sheet_name(
            cls, existing_sheet_names: list[str],
            sheet_name: str) -> Optional[str]:
        """Return the existing sheet name matching the requested name."""
        wanted_key = cls._sheet_key(sheet_name)
        for existing_name in existing_sheet_names:
            if cls._sheet_key(existing_name) == wanted_key:
                return existing_name
        return None

    def _current_sheet_key(self) -> str:
        """Return the normalized key of the current sheet."""
        return self._sheet_key(self._current_sheet_name())

    def _make_current_sheet_state(self) -> _SheetState:
        """Build the initial sequential state for the current sheet."""
        write_row = 0
        if self.file_access == FileAccess.UPDATE:
            write_row = self._last_used_row(self._write_sheet()) + 1
        return _SheetState(read_row=0, write_row=write_row,
                           heading_written=False)

    def _load_current_sheet_state(self) -> None:
        """Load the current sheet state into the public cursor fields."""
        key = self._current_sheet_key()
        state = self._sheet_states.get(key)
        if state is None:
            state = self._make_current_sheet_state()
            self._sheet_states[key] = state
        self.read_row = state.read_row
        self.write_row = state.write_row
        self.heading_written = state.heading_written

    def _save_current_sheet_state(self) -> None:
        """Persist the public cursor fields for the current sheet."""
        self._sheet_states[self._current_sheet_key()] = _SheetState(
            read_row=self.read_row,
            write_row=self.write_row,
            heading_written=self.heading_written)

    def _initialize_positions(self) -> None:
        """Initialize the default read and write cursors."""
        self._sheet_states = {}
        self._load_current_sheet_state()

    def _read_sheet(self) -> object:
        """Return the readable sheet-like object."""
        err = 'Subclass must implement _read_sheet method'
        raise NotImplementedError(err)
        # pylint: disable=unreachable
        return object()

    def _write_sheet(self) -> object:
        """Return the writable sheet-like object."""
        err = 'Subclass must implement _write_sheet method'
        raise NotImplementedError(err)
        # pylint: disable=unreachable
        return object()

    def _write_value_to_sheet(self, sheet: object, row: int,
                              column: int, value: object) -> None:
        """Write one plain value to one backend cell."""
        _ = sheet
        _ = row
        _ = column
        _ = value
        err = 'Subclass must implement _write_value_to_sheet method'
        raise NotImplementedError(err)

    def _set_cell_format(self, sheet: object, row: int, column: int,
                         fmt: Optional[Fmt]) -> None:
        """Apply optional formatting to one backend cell."""
        _ = sheet
        _ = row
        _ = column
        _ = fmt
        err = 'Subclass must implement _set_cell_format method'
        raise NotImplementedError(err)

    def _apply_heading_style(self, row: int, column: int, level: int) -> None:
        """Apply the backend heading style to one cell."""
        _ = row
        _ = column
        _ = level
        err = 'Subclass must implement _apply_heading_style method'
        raise NotImplementedError(err)

    def _last_used_row(self, sheet: object) -> int:
        """Return the last used row index on a backend sheet."""
        _ = sheet
        err = 'Subclass must implement _last_used_row method'
        raise NotImplementedError(err)
        # pylint: disable=unreachable
        return -1

    def _last_used_column(self, sheet: object) -> int:
        """Return the last used column index on a backend sheet."""
        _ = sheet
        err = 'Subclass must implement _last_used_column method'
        raise NotImplementedError(err)
        # pylint: disable=unreachable
        return -1

    def _cell_value(self, sheet: object, row: int, column: int) -> Value:
        """Return one backend cell converted to the public Value type."""
        _ = sheet
        _ = row
        _ = column
        err = 'Subclass must implement _cell_value method'
        raise NotImplementedError(err)
        # pylint: disable=unreachable
        return ''

    def _filtered_range_infos(self) -> list[tuple[str, tuple[int, int,
                                                             int, int]]]:
        """Return the backend filtered ranges with zero-based bounds."""
        err = 'Subclass must implement _filtered_range_infos method'
        raise NotImplementedError(err)
        # pylint: disable=unreachable
        return []

    def _delete_filtered_range(self, name: str) -> None:
        """Delete one backend filtered range by name."""
        _ = name
        err = 'Subclass must implement _delete_filtered_range method'
        raise NotImplementedError(err)

    def _add_filtered_range(self, bounds: tuple[int, int, int, int],
                            name: str) -> None:
        """Create one backend filtered range."""
        _ = bounds
        _ = name
        err = 'Subclass must implement _add_filtered_range method'
        raise NotImplementedError(err)

    def _set_column_width_if_wider(self, column: int, width: float) -> None:
        """Widen one backend column if the target width is larger."""
        _ = column
        _ = width
        err = 'Subclass must implement _set_column_width_if_wider method'
        raise NotImplementedError(err)

    def _used_bounds_by_cell_scan(self, sheet: object, row_limit: int,
                                  column_limit: int) -> tuple[int, int]:
        """Return the last used row and column by scanning cell values."""
        last_row = -1
        last_column = -1
        for row in range(row_limit):
            for column in range(column_limit):
                if self._cell_value(sheet, row, column) is None:
                    continue
                last_row = max(last_row, row)
                last_column = max(last_column, column)
        return last_row, last_column

    def _write_value(self, row: int, column: int, value: object,
                     fmt: Optional[Fmt] = None) -> None:
        """Write one value to the writable sheet and readable snapshot."""
        write_sheet = self._write_sheet()
        read_sheet = self._read_sheet()
        self._write_value_to_sheet(write_sheet, row, column, value)
        self._set_cell_format(write_sheet, row, column, fmt)
        if read_sheet is write_sheet:
            return
        self._write_value_to_sheet(read_sheet, row, column, value)

    def _clear_range(self, top: int, left: int,
                     bottom: int, right: int) -> None:
        """Clear values and simple formatting in a rectangle."""
        write_sheet = self._write_sheet()
        read_sheet = self._read_sheet()
        for row in range(top, bottom):
            for column in range(left, right):
                self._write_value_to_sheet(write_sheet, row, column, None)
                if read_sheet is not write_sheet:
                    self._write_value_to_sheet(read_sheet, row, column, None)

    def _read_limits(
            self, box: Optional[Box]) -> tuple[int, int, int, Optional[int]]:
        """Return the row and column limits for a read operation."""
        read_sheet = self._read_sheet()
        left = 0 if box is None else box.left
        top = self.read_row if box is None else box.top
        bottom = box.bottom if box is not None and \
            box.bottom is not None else self._scan_limit_bottom(read_sheet,
                                                                top)
        right = box.right if box is not None else None
        return left, top, bottom, right

    def _scan_limit_bottom(self, sheet: object, top: int) -> int:
        """Return the exclusive bottom limit used when scanning rows."""
        last_used = self._last_used_row(sheet)
        if last_used < top:
            return top
        return last_used + 1

    def _scan_limit_right(self, sheet: object, left: int,
                          right: Optional[int]) -> int:
        """Return the exclusive right limit used when scanning rows."""
        if right is not None:
            return right
        last_used = self._last_used_column(sheet)
        if last_used < left:
            return left
        return last_used + 1

    def _row_nonempty_columns(self, sheet: object, row: int, left: int,
                              right: Optional[int]) -> list[int]:
        """Return the non-empty columns in one row within the scan limits."""
        scan_right = self._scan_limit_right(sheet, left, right)
        ret: list[int] = []
        for column in range(left, scan_right):
            if self._cell_value(sheet, row, column) is not None:
                ret.append(column)
        return ret

    def _row_is_empty(self, sheet: object, row: int,
                      left: int, right: Optional[int]) -> bool:
        """Return whether the selected row region contains no values."""
        return not self._row_nonempty_columns(sheet, row, left, right)

    def _row_is_heading(self,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                        sheet: object, row: int, left: int,
                        right: Optional[int], bottom: int) -> bool:
        """Return whether the row matches the heading layout."""
        nonempty_columns = self._row_nonempty_columns(sheet, row, left, right)
        if nonempty_columns != [left]:
            return False
        if row + 1 >= bottom:
            return False
        return self._row_is_empty(sheet, row + 1, left, right)

    def _scan_section(self, box: Optional[Box]) -> _ScanResult:
        """Scan the next readable section on the active sheet."""
        sheet = self._read_sheet()
        left, top, bottom, right = self._read_limits(box)
        row = top
        last_read_row = top - 1
        while row < bottom and self._row_is_empty(sheet, row, left, right):
            last_read_row = row
            row += 1
        headings: list[str] = []
        while row < bottom and self._row_is_heading(sheet, row, left,
                                                    right, bottom):
            heading = self._cell_value(sheet, row, left)
            headings.append(value_to_str(heading, none_is_empty=True))
            last_read_row = row
            row += 1
            while row < bottom and self._row_is_empty(sheet, row, left,
                                                      right):
                last_read_row = row
                row += 1
        table_top = row
        table_bottom = row
        table_right = left
        while row < bottom:
            nonempty_columns = self._row_nonempty_columns(sheet, row, left,
                                                          right)
            if not nonempty_columns:
                last_read_row = row
                row += 1
                break
            last_read_row = row
            table_bottom = row + 1
            if right is None:
                table_right = max(table_right, max(nonempty_columns) + 1)
            else:
                table_right = right
            row += 1
        return _ScanResult(headings=headings, table_top=table_top,
                           table_bottom=table_bottom, table_left=left,
                           table_right=table_right,
                           last_read_row=last_read_row,
                           next_read_row=row)

    def _read_grid(self, scan: _ScanResult) -> ListData[Value]:
        """Read a rectangular grid from the scanned section."""
        read_sheet = self._read_sheet()
        if scan.table_bottom <= scan.table_top or \
                scan.table_right <= scan.table_left:
            return []
        ret: ListData[Value] = []
        for row in range(scan.table_top, scan.table_bottom):
            ret.append([
                self._cell_value(read_sheet, row, column)
                for column in range(scan.table_left, scan.table_right)
            ])
        return ret

    def _update_read_positions(self, scan: _ScanResult,
                               box: Optional[Box]) -> None:
        """Update default read and write positions after a read."""
        self.write_row = scan.last_read_row + 1
        if box is None:
            self.read_row = scan.next_read_row
        self._save_current_sheet_state()

    @staticmethod
    def _range_contains(first: tuple[int, int, int, int],
                        second: tuple[int, int, int, int]) -> bool:
        """Return whether one exclusive rectangle contains another."""
        return first[0] <= second[0] and first[1] <= second[1] and \
            first[2] >= second[2] and first[3] >= second[3]

    @staticmethod
    def _ranges_overlap(first: tuple[int, int, int, int],
                        second: tuple[int, int, int, int]) -> bool:
        """Return whether two zero-based exclusive rectangles overlap."""
        return first[0] < second[2] and second[0] < first[2] and \
            first[1] < second[3] and second[1] < first[3]

    def _sheet_table_regions(self) -> list[tuple[int, int, int, int]]:
        """Return detected table-like regions on the active readable sheet."""
        read_sheet = self._read_sheet()
        bottom = self._scan_limit_bottom(read_sheet, 0)
        if bottom <= 0:
            return []
        ret: list[tuple[int, int, int, int]] = []
        row = 0
        while row < bottom:
            if self._row_is_empty(read_sheet, row, 0, None):
                row += 1
                continue
            if self._row_is_heading(read_sheet, row, 0, None, bottom):
                row += 2
                continue
            top = row
            left: Optional[int] = None
            right = 0
            while row < bottom:
                nonempty_columns = self._row_nonempty_columns(
                    read_sheet, row, 0, None)
                if not nonempty_columns:
                    break
                row_left = min(nonempty_columns)
                row_right = max(nonempty_columns) + 1
                if left is None:
                    left = row_left
                else:
                    left = min(left, row_left)
                right = max(right, row_right)
                row += 1
            assert left is not None
            ret.append((top, left, row, right))
        return ret

    def _existing_table_regions(self) -> list[tuple[int, int, int, int]]:
        """Return persisted and inferred table regions on the active sheet."""
        ret: list[tuple[int, int, int, int]] = []
        for _, bounds in self._filtered_range_infos():
            if bounds not in ret:
                ret.append(bounds)
        for bounds in self._sheet_table_regions():
            if bounds not in ret:
                ret.append(bounds)
        return ret

    def _check_boxed_table_overwrite(
            self, bounds: tuple[int, int, int, int]) -> None:
        """Reject writes that would leave part of an existing table behind."""
        for existing_bounds in self._existing_table_regions():
            if not self._ranges_overlap(bounds, existing_bounds):
                continue
            if self._range_contains(bounds, existing_bounds):
                continue
            msg = 'Boxed table write would partly overwrite an existing table.'
            raise ValueError(msg)

    def _filter_range_name_in_use(self, name: str) -> bool:
        """Return whether the backend already contains the filter name."""
        for existing_name, _ in self._filtered_range_infos():
            if existing_name == name:
                return True
        return False

    def _next_filter_range_name(self) -> str:
        """Return a backend-unique name for one filtered data range."""
        filter_index = 1
        while True:
            name = f'{_FILTER_RANGE_PREFIX}{filter_index}'
            if not self._filter_range_name_in_use(name):
                return name
            filter_index += 1

    def _remove_overlapping_filtered_ranges(
            self, bounds: tuple[int, int, int, int]) -> None:
        """Remove backend filtered ranges that overlap the write bounds."""
        for name, existing_bounds in self._filtered_range_infos():
            if self._ranges_overlap(bounds, existing_bounds):
                self._delete_filtered_range(name)

    def _write_filtered_data_range(
            self, bounds: tuple[int, int, int, int]) -> None:
        """Create one backend filtered data range for the given bounds."""
        self._add_filtered_range(bounds, self._next_filter_range_name())

    @staticmethod
    def _values_match(cell_value: Value, find_value: Value,
                      type_conversion: bool) -> bool:
        """Return whether one cell matches one requested value."""
        if type(cell_value) is type(find_value) and cell_value == find_value:
            return True
        if not type_conversion:
            return False
        try:
            converted = value2type_of(cell_value, find_value,
                                      accept_none=find_value is None)
        except (UnreasonableTypeConversion, UnreasonableValueConversion):
            return False
        return converted == find_value

    @classmethod
    def _split_cell_grid(cls, data: ListDataSeq[CellT]) -> tuple[
            ListData[Value], list[list[Optional[Fmt]]]]:
        """Return a grid of plain values and matching cell formats."""
        values: ListData[Value] = []
        formats: list[list[Optional[Fmt]]] = []
        for row in data:
            value_row: list[Value] = []
            format_row: list[Optional[Fmt]] = []
            for cell in row:
                value, fmt = cls._split_cell_value(cell)
                value_row.append(value)
                format_row.append(fmt)
            values.append(value_row)
            formats.append(format_row)
        return values, formats

    def _find_bounds(self, box: Optional[Box]) -> tuple[int, int, int, int]:
        """Return the search limits for one find operation."""
        read_sheet = self._read_sheet()
        top = 0 if box is None else box.top
        left = 0 if box is None else box.left
        if box is not None and box.bottom is not None:
            bottom = box.bottom
        else:
            bottom = max(top, self._last_used_row(read_sheet) + 1)
        if box is not None and box.right is not None:
            right = box.right
        else:
            right = max(left, self._last_used_column(read_sheet) + 1)
        return top, left, bottom, right

    def _grid_matches(self,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                      sheet: object, top: int, left: int,
                      find_value: ListData[Value],
                      type_conversion: bool) -> bool:
        """Return whether one sheet region matches the requested grid."""
        for row_offset, find_row in enumerate(find_value):
            for column_offset, expected_value in enumerate(find_row):
                cell_value = self._cell_value(sheet, top + row_offset,
                                              left + column_offset)
                if not self._values_match(cell_value, expected_value,
                                          type_conversion):
                    return False
        return True

    @staticmethod
    def _column_width_text(value: object) -> str:
        """Return the text used to estimate a readable column width."""
        if value is None:
            return ''
        return str(value)

    def _table_column_width(self, top: int, bottom: int,
                            column: int) -> float:
        """Return a width target for one table column."""
        max_length = 0
        write_sheet = self._write_sheet()
        for row in range(top, bottom):
            value = self._cell_value(write_sheet, row, column)
            max_length = max(max_length,
                             len(self._column_width_text(value)))
        return float(min(_MAX_COLUMN_WIDTH,
                         max_length + _COLUMN_WIDTH_PADDING))

    def _update_table_column_widths(self, top: int, left: int,
                                    bottom: int, right: int) -> None:
        """Widen backend columns to fit the written table content."""
        for column in range(left, right):
            self._set_column_width_if_wider(
                column, self._table_column_width(top, bottom, column))

    def _write_start(self, box: Optional[Box]) -> tuple[int, int]:
        """Return the start position for a write operation."""
        if box is not None:
            return box.top, box.left
        row = self.write_row
        if row > 0:
            if not self._row_is_empty(self._write_sheet(), row - 1, 0, None):
                row += 1
        self.write_row = row
        return row, 0

    def _update_write_position(self, next_row: int) -> None:
        """Update the default write cursor after a write operation."""
        self.write_row = next_row
        self._save_current_sheet_state()

    def _write_grid(self,  # pylint: disable=too-many-locals
                    values: ListData[Value],
                    formats: list[list[Optional[Fmt]]],
                    filtered_data_range: bool = False,
                    box: Optional[Box] = None) -> Position:
        """Write a rectangular grid of values and optional formats."""
        start_row, start_column = self._write_start(box)
        row_count = len(values)
        column_count = len(values[0])
        write_bottom = start_row + row_count
        write_right = start_column + column_count
        clear_bottom = box.bottom if box is not None and \
            box.bottom is not None else write_bottom
        clear_right = box.right if box is not None and \
            box.right is not None else write_right
        affected_bounds = (
            start_row,
            start_column,
            clear_bottom if box is not None else write_bottom,
            clear_right if box is not None else write_right
        )
        if box is not None:
            self._check_boxed_table_overwrite(affected_bounds)
        self._remove_overlapping_filtered_ranges(affected_bounds)
        if box is not None:
            self._clear_range(start_row, start_column, clear_bottom,
                              clear_right)
        for row_offset, row in enumerate(values):
            for column_offset, value in enumerate(row):
                fmt = formats[row_offset][column_offset]
                self._write_value(start_row + row_offset,
                                  start_column + column_offset, value, fmt)
        if filtered_data_range:
            self._write_filtered_data_range((start_row, start_column,
                                             write_bottom, write_right))
        self._update_table_column_widths(start_row, start_column,
                                         write_bottom, write_right)
        next_row = max(self.write_row, clear_bottom + 1)
        self._update_write_position(next_row)
        return Position(row=start_row + row_count - 1,
                        column=start_column + column_count - 1)

    def _write_heading(self, heading: str, level: int) -> Position:
        """Write a heading to the active sheet."""
        start_row, start_column = self._write_start(None)
        self._write_value(start_row, start_column, heading)
        self._apply_heading_style(start_row, start_column, level)
        self._update_write_position(start_row + 2)
        return Position(row=start_row, column=start_column)

    @classmethod
    def _split_cell_value(cls, cell: CellT) -> tuple[Value, Optional[Fmt]]:
        """Return the plain value and optional cell format."""
        if isinstance(cell, ValueFmt):
            value = cls._spreadsheet_value_from_python(cell.value)
            return value, cell.fmt
        return cls._spreadsheet_value_from_python(cell), None

    def _write_table_listdata(self, data: ListDataSeq[CellT],
                              impl_meta: TableIO.ImplMetaForWrite) -> Position:
        """Write list data to the active sheet."""
        values, formats = self._split_cell_grid(data)
        return self._write_grid(values, formats,
                                impl_meta.filtered_data_range,
                                impl_meta.box)

    def _write_table_fmtlistdata(
            self, data: FmtListData,
            impl_meta: TableIO.ImplMetaForWrite) -> Position:
        """Write row-formatted list data to the active sheet."""
        return self._write_table_listdata(row_format_each_cell_list(data),
                                          impl_meta=impl_meta)

    def _write_table_dictdata(
            self, data: DictDataMap[CellT],
            impl_meta: TableIO.ImplMetaForDictWrite) -> Position:
        """Write dict data to the active sheet."""
        values: ListData[Value] = [list(impl_meta.column_order)]
        formats: list[list[Optional[Fmt]]] = [
            [impl_meta.first_row_format for _ in impl_meta.column_order]
        ]
        for row in data:
            value_row: list[Value] = []
            format_row: list[Optional[Fmt]] = []
            for column_name in impl_meta.column_order:
                value, fmt = self._split_cell_value(row[column_name])
                value_row.append(value)
                format_row.append(fmt)
            values.append(value_row)
            formats.append(format_row)
        return self._write_grid(values, formats,
                                impl_meta.common_impl.filtered_data_range,
                                impl_meta.common_impl.box)

    def _write_table_fmtdictdata(
            self, data: FmtDictData,
            impl_meta: TableIO.ImplMetaForDictWrite) -> Position:
        """Write row-formatted dict data to the active sheet."""
        return self._write_table_dictdata(row_format_each_cell_dict(data),
                                          impl_meta=impl_meta)

    def _read_table_listdata(self, box: Optional[Box] = None) -> \
            ReadResult[ListData[Value]]:
        """Read list data from the active sheet."""
        scan = self._scan_section(box)
        data = self._read_grid(scan)
        self._update_read_positions(scan, box)
        return ReadResult(data=data, headings=scan.headings,
                          last_read_row=scan.last_read_row)

    def _read_table_dictdata(self, box: Optional[Box] = None) -> \
            ReadResult[DictData[Value]]:
        """Read dict data from the active sheet."""
        scan = self._scan_section(box)
        rows = self._read_grid(scan)
        data: DictData[Value] = []
        if rows:
            header = [value_to_str(value, none_is_empty=False)
                      for value in rows[0]]
            for row in rows[1:]:
                data.append(dict(zip(header, row, strict=True)))
        self._update_read_positions(scan, box)
        return ReadResult(data=data, headings=scan.headings,
                          last_read_row=scan.last_read_row)

    def _find_value(self, find_value: ListData[Value],
                    type_conversion: bool = True,
                    box: Optional[Box] = None) -> Optional[Box]:
        """Find the first matching value grid on the active sheet."""
        read_sheet = self._read_sheet()
        top, left, bottom, right = self._find_bounds(box)
        row_count = len(find_value)
        column_count = len(find_value[0])
        last_row = bottom - row_count
        last_column = right - column_count
        if last_row < top or last_column < left:
            return None
        for row in range(top, last_row + 1):
            for column in range(left, last_column + 1):
                if self._grid_matches(read_sheet, row, column,
                                      find_value, type_conversion):
                    return Box(top=row, left=column,
                               bottom=row + row_count,
                               right=column + column_count)
        return None

    def _read_cells(self, box: Box) -> ListData[Value]:
        """Read the exact cell rectangle described by the box."""
        read_sheet = self._read_sheet()
        assert box.bottom is not None
        assert box.right is not None
        ret: ListData[Value] = []
        for row in range(box.top, box.bottom):
            ret.append([
                self._cell_value(read_sheet, row, column)
                for column in range(box.left, box.right)
            ])
        return ret

    def _write_cells(self, data: ListDataSeq[CellT], box: Box) -> None:
        """Write the exact cell rectangle described by the box."""
        values, formats = self._split_cell_grid(data)
        top = box.top
        left = box.left
        bottom = box.bottom if box.bottom is not None else top + len(values)
        right = box.right if box.right is not None else left + len(values[0])
        self._clear_range(top, left, bottom, right)
        for row_offset, row in enumerate(values):
            for column_offset, value in enumerate(row):
                self._write_value(top + row_offset, left + column_offset,
                                  value, formats[row_offset][column_offset])
