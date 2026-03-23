#! /usr/bin/env python3
"""TableIO reader/writer class for Excel files using OpenPyXL."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import date, datetime, time
from typing import Callable, NamedTuple, Optional

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils.cell import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

from mformat.mformat import PathLike

from tableio.capability import Capabilities, SingleCapability, Strictness
from tableio.color import Color
from tableio.tableio import Box, Descriptor, FileAccess, Position
from tableio.tableio_excelbased import TableIOExcelBased
from tableio.value_type import CellT, DictData, DictDataMap, Fmt, \
    FmtDictData, FmtListData, ListData, ListDataSeq, ReadResult, Value, \
    ValueFmt, row_format_each_cell_dict, row_format_each_cell_list, \
    value_to_str


_SUPPORTED: SingleCapability = SingleCapability(supported=True,
                                                strictness=Strictness.STRICT)

_HEADING_FONT_SIZES: dict[int, int] = {
    1: 14,
    2: 12,
    3: 11
}

_HIGHLIGHT_RGB: dict[Color, str] = {
    Color.RED: 'FFFF0000',
    Color.GREEN: 'FF00FF00',
    Color.YELLOW: 'FFFFFF00'
}


class _ScanResult(NamedTuple):
    """Details gathered while scanning one worksheet section."""

    headings: list[str]
    table_top: int
    table_bottom: int
    table_left: int
    table_right: int
    last_read_row: int
    next_read_row: int


class TableIOExcelOpenPyXL(TableIOExcelBased):
    """TableIO reader/writer class for Excel files using OpenPyXL.

    The first implementation uses a single active worksheet only.
    In UPDATE mode the default write position is after the last used row in
    that worksheet. This keeps appends simple, but using box explicitly is
    strongly recommended when writing in UPDATE mode.
    """

    def __init__(self, file_name: PathLike,
                 file_access: FileAccess,
                 file_exists_callback: Optional[Callable[[str], None]]
                 = None):
        """Initialize the TableIOExcelOpenPyXL class.

        Args:
            file_name: The name of the file to open.
            file_access: What access is requested to the file.
            file_exists_callback: A callback function to call if the file
                                  already exists when file_access is CREATE.
                                  Return to allow the file to be overwritten.
                                  Raise an exception to prevent the file from
                                  being overwritten.
                                  (May for instance save existing file as
                                  backup.)
                                  (Default is to raise an exception.)
        Notes:
            In UPDATE mode the default write position is after the last used
            row on the active worksheet. That makes simple appends convenient,
            but box should be preferred when writing updates so the target
            range is explicit.
        """
        super().__init__(file_name=file_name,
                         file_access=file_access,
                         file_exists_callback=file_exists_callback)
        self.workbook: Workbook | None = None
        self.read_workbook: Workbook | None = None
        self.worksheet: Worksheet | None = None
        self.read_worksheet: Worksheet | None = None
        self.read_row: int = 0
        self.write_row: int = 0

    @classmethod
    def get_description(cls) -> Descriptor:
        """Get the description of the TableIOExcelOpenPyXL class.

        Returns:
            Descriptor: The description of the TableIOExcelOpenPyXL class.
        """
        return Descriptor(format_name='Excel', implementation='OpenPyXL',
                          capabilities=cls.get_capabilities(),
                          mandatory_args=[], optional_args=[])

    @classmethod
    def get_capabilities(cls) -> Capabilities:
        """Get the capabilities of the TableIOExcelOpenPyXL class.

        Returns:
            Capabilities: The capabilities of the TableIOExcelOpenPyXL class.
        """
        return Capabilities(can_read=_SUPPORTED, can_write=_SUPPORTED,
                            can_fmt_row=_SUPPORTED, can_fmt_value=_SUPPORTED,
                            filtered_data_range=_SUPPORTED,
                            can_write_box=_SUPPORTED, can_read_box=_SUPPORTED,
                            can_write_highlight=_SUPPORTED)

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the file name extension of the TableIOExcelOpenPyXL class.

        Returns:
            str: The file name extension of the TableIOExcelOpenPyXL class.
        """
        return '.xlsx'

    def open(self) -> None:
        """Open the Excel workbook."""
        if self.workbook is not None:
            raise RuntimeError(f'File {self.file_name} already open')
        if self.file_access == FileAccess.CREATE:
            workbook = Workbook()
            self.workbook = workbook
            self.read_workbook = workbook
        elif self.file_access == FileAccess.READ:
            workbook = load_workbook(self.file_name, data_only=True)
            self.workbook = workbook
            self.read_workbook = workbook
        else:
            self.workbook = load_workbook(self.file_name)
            self.read_workbook = load_workbook(self.file_name,
                                               data_only=True)
        assert self.workbook is not None
        assert self.read_workbook is not None
        worksheet = self.workbook.active
        read_worksheet = self.read_workbook.active
        assert isinstance(worksheet, Worksheet)
        assert isinstance(read_worksheet, Worksheet)
        self.worksheet = worksheet
        self.read_worksheet = read_worksheet
        self.read_row = 0
        if self.file_access == FileAccess.UPDATE:
            self.write_row = self._last_used_row(self.worksheet) + 1
        else:
            self.write_row = 0

    def _end_state(self) -> None:
        """Finalize in-memory state before closing."""

    def _write_file_suffix(self) -> None:
        """Write the workbook to disk when the file is writable."""
        if self.file_access == FileAccess.READ:
            return
        assert self.workbook is not None
        self.workbook.save(self.file_name)

    def _close(self) -> None:
        """Close any open workbook handles."""
        if self.read_workbook is not None and \
                self.read_workbook is not self.workbook:
            self.read_workbook.close()
            self.read_workbook = None
            self.read_worksheet = None
        if self.workbook is not None:
            self.workbook.close()
            self.workbook = None
            self.worksheet = None
        self.read_workbook = None
        self.read_worksheet = None

    @staticmethod
    def _python_value_from_excel(value: object) -> Value:
        """Convert an Excel cell value to the closest supported Value."""
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, date):
            return datetime.combine(value, time())
        if isinstance(value, (str, bool, int, float)):
            return value
        return str(value)

    @staticmethod
    def _excel_value_from_python(value: object) -> Value:
        """Convert a Python value to the closest Excel-supported value."""
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, date):
            return datetime.combine(value, time())
        if isinstance(value, (str, bool, int, float)):
            return value
        return str(value)

    @staticmethod
    def _range_ref(top: int, left: int, bottom: int, right: int) -> str:
        """Return an Excel A1 range string for a zero-based rectangle."""
        start = f'{get_column_letter(left + 1)}{top + 1}'
        end = f'{get_column_letter(right)}{bottom}'
        return f'{start}:{end}'

    @staticmethod
    def _highlight_fill(highlight: Color) -> PatternFill:
        """Return the fill object for the requested highlight color."""
        if highlight == Color.NONE:
            return PatternFill()
        return PatternFill(fill_type='solid',
                           fgColor=_HIGHLIGHT_RGB[highlight])

    def _set_cell_format(self, worksheet: Worksheet, row: int, column: int,
                         fmt: Fmt | None) -> None:
        """Apply cell formatting to the worksheet cell."""
        if fmt is None:
            return
        cell = worksheet.cell(row=row + 1, column=column + 1)
        cell.font = Font(bold=fmt.bold, italic=fmt.italic)
        cell.fill = self._highlight_fill(fmt.highlight)

    def _write_value_to_cell(self, worksheet: Worksheet, row: int,
                             column: int, value: object) -> None:
        """Write one value to one worksheet cell."""
        cell = worksheet.cell(row=row + 1, column=column + 1)
        cell.style = 'Normal'
        cell.value = self._excel_value_from_python(value)

    def _write_value(self, row: int, column: int, value: object,
                     fmt: Fmt | None = None) -> None:
        """Write one value to the writable workbook and read snapshot."""
        assert self.worksheet is not None
        assert self.read_worksheet is not None
        self._write_value_to_cell(self.worksheet, row, column, value)
        self._set_cell_format(self.worksheet, row, column, fmt)
        if self.read_worksheet is self.worksheet:
            return
        self._write_value_to_cell(self.read_worksheet, row, column, value)

    def _clear_range(self, top: int, left: int,
                     bottom: int, right: int) -> None:
        """Clear values and simple formatting in a worksheet rectangle."""
        assert self.worksheet is not None
        assert self.read_worksheet is not None
        for row in range(top, bottom):
            for column in range(left, right):
                self._write_value_to_cell(self.worksheet, row, column, None)
                if self.read_worksheet is not self.worksheet:
                    self._write_value_to_cell(self.read_worksheet, row,
                                              column, None)

    def _used_bounds(self, worksheet: Worksheet) -> tuple[int, int]:
        """Return the last used row and column on a worksheet."""
        last_row = -1
        last_column = -1
        for row in worksheet.iter_rows():
            for cell in row:
                if cell.value is None:
                    continue
                last_row = max(last_row, cell.row - 1)
                last_column = max(last_column, cell.column - 1)
        return last_row, last_column

    def _last_used_row(self, worksheet: Worksheet) -> int:
        """Return the last used row index on a worksheet."""
        return self._used_bounds(worksheet)[0]

    def _last_used_column(self, worksheet: Worksheet) -> int:
        """Return the last used column index on a worksheet."""
        return self._used_bounds(worksheet)[1]

    def _cell_value(self, worksheet: Worksheet, row: int,
                    column: int) -> Value:
        """Return one worksheet cell converted to the public Value type."""
        raw = worksheet.cell(row=row + 1, column=column + 1).value
        return self._python_value_from_excel(raw)

    def _read_limits(
            self, box: Box | None) -> tuple[int, int, int, int | None]:
        """Return the row and column limits for a read operation."""
        assert self.read_worksheet is not None
        left = 0 if box is None else box.left
        top = self.read_row if box is None else box.top
        last_used_row = self._last_used_row(self.read_worksheet)
        bottom = box.bottom if box is not None and \
            box.bottom is not None else last_used_row + 1
        right = box.right if box is not None else None
        return left, top, bottom, right

    def _scan_limit_right(self, worksheet: Worksheet, left: int,
                          right: int | None) -> int:
        """Return the exclusive right limit used when scanning rows."""
        if right is not None:
            return right
        last_used = self._last_used_column(worksheet)
        if last_used < left:
            return left
        return last_used + 1

    def _row_nonempty_columns(self, worksheet: Worksheet, row: int, left: int,
                              right: int | None) -> list[int]:
        """Return the non-empty columns in a row within the scan limits."""
        scan_right = self._scan_limit_right(worksheet, left, right)
        ret: list[int] = []
        for column in range(left, scan_right):
            if self._cell_value(worksheet, row, column) is not None:
                ret.append(column)
        return ret

    def _row_is_empty(self, worksheet: Worksheet, row: int,
                      left: int, right: int | None) -> bool:
        """Return whether the selected row region contains no values."""
        return not self._row_nonempty_columns(worksheet, row, left, right)

    # pylint: disable-next=too-many-arguments,too-many-positional-arguments
    def _row_is_heading(self,
                        worksheet: Worksheet, row: int, left: int,
                        right: int | None, bottom: int) -> bool:
        """Return whether the row matches the heading layout."""
        nonempty_columns = self._row_nonempty_columns(worksheet, row, left,
                                                      right)
        if nonempty_columns != [left]:
            return False
        if row + 1 >= bottom:
            return False
        return self._row_is_empty(worksheet, row + 1, left, right)

    def _scan_section(self, box: Box | None) -> _ScanResult:
        """Scan the next readable section on the active worksheet."""
        assert self.read_worksheet is not None
        worksheet = self.read_worksheet
        left, top, bottom, right = self._read_limits(box)
        row = top
        last_read_row = top - 1
        while row < bottom and self._row_is_empty(worksheet, row, left, right):
            last_read_row = row
            row += 1
        headings: list[str] = []
        while row < bottom and self._row_is_heading(worksheet, row, left,
                                                    right, bottom):
            heading = self._cell_value(worksheet, row, left)
            headings.append(value_to_str(heading, none_is_empty=True))
            last_read_row = row
            row += 1
            while row < bottom and self._row_is_empty(worksheet, row, left,
                                                      right):
                last_read_row = row
                row += 1
        table_top = row
        table_bottom = row
        table_right = left
        while row < bottom:
            nonempty_columns = self._row_nonempty_columns(worksheet, row, left,
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
        assert self.read_worksheet is not None
        if scan.table_bottom <= scan.table_top or \
                scan.table_right <= scan.table_left:
            return []
        ret: ListData[Value] = []
        for row in range(scan.table_top, scan.table_bottom):
            ret.append([
                self._cell_value(self.read_worksheet, row, column)
                for column in range(scan.table_left, scan.table_right)
            ])
        return ret

    def _update_read_positions(self, scan: _ScanResult,
                               box: Box | None) -> None:
        """Update default read and write positions after a read."""
        self.write_row = scan.last_read_row + 1
        if box is not None:
            return
        self.read_row = scan.next_read_row

    def _write_start(self, box: Box | None) -> tuple[int, int]:
        """Return the start position for a write operation."""
        if box is not None:
            return box.top, box.left
        row = self.write_row
        if row > 0:
            assert self.worksheet is not None
            if not self._row_is_empty(self.worksheet, row - 1, 0, None):
                row += 1
        self.write_row = row
        return row, 0

    def _update_write_position(self, next_row: int) -> None:
        """Update the default write cursor after a write operation."""
        self.write_row = next_row

    def _write_grid(self,  # pylint: disable=too-many-locals
                    values: ListData[Value],
                    formats: list[list[Fmt | None]],
                    filtered_data_range: bool = False,
                    box: Box | None = None) -> Position:
        """Write a rectangular grid of values and optional formats."""
        start_row, start_column = self._write_start(box)
        row_count = len(values)
        column_count = len(values[0])
        clear_bottom = box.bottom if box is not None and \
            box.bottom is not None else start_row + row_count
        clear_right = box.right if box is not None and \
            box.right is not None else start_column + column_count
        if box is not None:
            self._clear_range(start_row, start_column, clear_bottom,
                              clear_right)
        for row_offset, row in enumerate(values):
            for column_offset, value in enumerate(row):
                fmt = formats[row_offset][column_offset]
                self._write_value(start_row + row_offset,
                                  start_column + column_offset, value, fmt)
        if filtered_data_range:
            assert self.worksheet is not None
            self.worksheet.auto_filter.ref = self._range_ref(
                start_row, start_column, start_row + row_count,
                start_column + column_count)
        next_row = max(self.write_row, clear_bottom + 1)
        self._update_write_position(next_row)
        return Position(row=start_row + row_count - 1,
                        column=start_column + column_count - 1)

    def _write_heading(self, heading: str, level: int) -> Position:
        """Write a heading to the active worksheet."""
        start_row, start_column = self._write_start(None)
        self._write_value(start_row, start_column, heading)
        assert self.worksheet is not None
        cell = self.worksheet.cell(row=start_row + 1, column=start_column + 1)
        cell.font = Font(bold=True, size=_HEADING_FONT_SIZES[level])
        self._update_write_position(start_row + 2)
        return Position(row=start_row, column=start_column)

    def _write_table_listdata(self,  # pylint: disable=arguments-renamed
                              data: ListDataSeq[CellT],
                              filtered_data_range: bool = False,
                              box: Box | None = None) -> Position:
        """Write list data to the active worksheet."""
        values: ListData[Value] = []
        formats: list[list[Fmt | None]] = []
        for row in data:
            value_row: list[Value] = []
            format_row: list[Fmt | None] = []
            for cell in row:
                if isinstance(cell, ValueFmt):
                    value_row.append(self._excel_value_from_python(
                        cell.value))
                    format_row.append(cell.fmt)
                else:
                    value_row.append(self._excel_value_from_python(cell))
                    format_row.append(None)
            values.append(value_row)
            formats.append(format_row)
        return self._write_grid(values, formats, filtered_data_range, box)

    def _write_table_fmtlistdata(self, data: FmtListData,
                                 filtered_data_range: bool = False,
                                 box: Box | None = None) -> Position:
        """Write row-formatted list data to the active worksheet."""
        return self._write_table_listdata(row_format_each_cell_list(data),
                                          filtered_data_range, box)

    # pylint: disable-next=too-many-locals,arguments-renamed
    def _write_table_dictdata(self, data: DictDataMap[CellT],
                              column_order: list[str],
                              filtered_data_range: bool = False,
                              box: Box | None = None) -> Position:
        """Write dict data to the active worksheet."""
        values: ListData[Value] = [list(column_order)]
        formats: list[list[Fmt | None]] = [[None for _ in column_order]]
        for row in data:
            value_row: list[Value] = []
            format_row: list[Fmt | None] = []
            for column_name in column_order:
                cell = row[column_name]
                if isinstance(cell, ValueFmt):
                    value_row.append(self._excel_value_from_python(
                        cell.value))
                    format_row.append(cell.fmt)
                else:
                    value_row.append(self._excel_value_from_python(cell))
                    format_row.append(None)
            values.append(value_row)
            formats.append(format_row)
        return self._write_grid(values, formats, filtered_data_range, box)

    def _write_table_fmtdictdata(self, data: FmtDictData,
                                 column_order: list[str],
                                 filtered_data_range: bool = False,
                                 box: Box | None = None) -> Position:
        """Write row-formatted dict data to the active worksheet."""
        return self._write_table_dictdata(row_format_each_cell_dict(data),
                                          column_order,
                                          filtered_data_range, box)

    def _read_table_listdata(self, box: Box | None = None) -> \
            ReadResult[ListData[Value]]:
        """Read list data from the active worksheet."""
        scan = self._scan_section(box)
        data = self._read_grid(scan)
        self._update_read_positions(scan, box)
        return ReadResult(data=data, headings=scan.headings,
                          last_read_row=scan.last_read_row)

    def _read_table_dictdata(self, box: Box | None = None) -> \
            ReadResult[DictData[Value]]:
        """Read dict data from the active worksheet."""
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
