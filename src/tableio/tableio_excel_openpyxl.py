#! /usr/bin/env python3
"""TableIO reader/writer class for Excel files using OpenPyXL."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Callable, Optional
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils.cell import get_column_letter, range_boundaries
from openpyxl.worksheet.table import Table
from openpyxl.worksheet.worksheet import Worksheet
from mformat.mformat import PathLike
from tableio.color import Color
from tableio.tableio import Descriptor, FileAccess
from tableio.tableio_excelbased import TableIOExcelBased
from tableio.value_type import Fmt, Value, get_checked_type
from tableio.capability import Capabilities, CAP_ALL_IMPLEMENTED

_HIGHLIGHT_RGB: dict[Color, str] = {
    Color.RED: 'FFFFC7CE',
    Color.GREEN: 'FFC6EFCE',
    Color.YELLOW: 'FFFFFF00'
}


class TableIOExcelOpenPyXL(TableIOExcelBased):
    """TableIO reader/writer class for Excel files using OpenPyXL.

    The implementation operates on one current worksheet at a time. In
    UPDATE mode the default write position is after the last used row in
    the selected worksheet.
    """

    def __init__(self, file_name: PathLike,
                 file_access: FileAccess,
                 file_exists_callback: Optional[Callable[[str], None]]
                 = None):
        """Initialize the TableIOExcelOpenPyXL class."""
        super().__init__(file_name=file_name,
                         file_access=file_access,
                         file_exists_callback=file_exists_callback)
        self.workbook: Optional[Workbook] = None
        self.read_workbook: Optional[Workbook] = None
        self.worksheet: Optional[Worksheet] = None
        self.read_worksheet: Optional[Worksheet] = None

    @classmethod
    def get_capabilities(cls) -> Capabilities:
        """Return the standard spreadsheet backend capabilities."""
        return CAP_ALL_IMPLEMENTED

    @classmethod
    def get_description(cls) -> Descriptor:
        """Get the description of the TableIOExcelOpenPyXL class."""
        return Descriptor(format_name='Excel', implementation='OpenPyXL',
                          capabilities=cls.get_capabilities(),
                          mandatory_args=[], optional_args=[])

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
        self._initialize_positions()

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
    def _worksheet_name_map(
            workbook: Workbook) -> dict[str, Worksheet]:
        """Return the workbook worksheets indexed case-insensitively."""
        ret: dict[str, Worksheet] = {}
        for worksheet in workbook.worksheets:
            ret[worksheet.title.casefold()] = worksheet
        return ret

    def _set_active_worksheets(self, worksheet: Worksheet,
                               read_worksheet: Worksheet) -> None:
        """Set the current writable and readable worksheets."""
        assert self.workbook is not None
        assert self.read_workbook is not None
        self.worksheet = worksheet
        self.read_worksheet = read_worksheet
        self.workbook.active = self.workbook.index(worksheet)
        if self.read_workbook is self.workbook:
            return
        self.read_workbook.active = self.read_workbook.index(read_worksheet)

    def _list_sheets(self) -> list[str]:
        """List the sheets in the workbook."""
        assert self.workbook is not None
        return list(self.workbook.sheetnames)

    def _select_sheet(self, sheet_name: str, create: bool = False) -> None:
        """Select one workbook sheet, optionally creating it."""
        assert self.workbook is not None
        assert self.read_workbook is not None
        assert self.worksheet is not None
        assert self.read_worksheet is not None
        sheet_key = self._sheet_key(sheet_name)
        workbook_map = self._worksheet_name_map(self.workbook)
        read_map = self._worksheet_name_map(self.read_workbook)
        worksheet = workbook_map.get(sheet_key)
        read_worksheet = read_map.get(sheet_key)
        if worksheet is None:
            if not create:
                raise KeyError(sheet_name)
            self._check_file_is_writable()
            worksheet = self.workbook.create_sheet(title=sheet_name)
            if self.read_workbook is self.workbook:
                read_worksheet = worksheet
            else:
                read_worksheet = self.read_workbook.create_sheet(
                    title=sheet_name)
        assert read_worksheet is not None
        self._save_current_sheet_state()
        self._set_active_worksheets(worksheet, read_worksheet)
        self._load_current_sheet_state()

    def _current_sheet_name(self) -> str:
        """Return the name of the selected worksheet."""
        assert self.worksheet is not None
        return self.worksheet.title

    def _read_sheet(self) -> object:
        """Return the readable worksheet."""
        assert self.read_worksheet is not None
        return self.read_worksheet

    def _write_sheet(self) -> object:
        """Return the writable worksheet."""
        assert self.worksheet is not None
        return self.worksheet

    @staticmethod
    def _highlight_fill(highlight: Color) -> PatternFill:
        """Return the fill object for the requested highlight color."""
        if highlight == Color.NONE:
            return PatternFill()
        return PatternFill(fill_type='solid',
                           fgColor=_HIGHLIGHT_RGB[highlight])

    def _write_value_to_sheet(self, sheet: object, row: int,
                              column: int, value: object) -> None:
        """Write one value to one worksheet cell."""
        worksheet = get_checked_type(sheet, Worksheet)
        cell = worksheet.cell(row=row + 1, column=column + 1)
        cell.style = 'Normal'
        cell.value = self._spreadsheet_value_from_python(value)

    def _set_cell_format(self, sheet: object, row: int, column: int,
                         fmt: Optional[Fmt]) -> None:
        """Apply cell formatting to one worksheet cell."""
        if fmt is None:
            return
        worksheet = get_checked_type(sheet, Worksheet)
        cell = worksheet.cell(row=row + 1, column=column + 1)
        cell.font = Font(bold=fmt.bold, italic=fmt.italic)
        cell.fill = self._highlight_fill(fmt.highlight)

    def _apply_heading_style(self, row: int, column: int, level: int) -> None:
        """Apply the heading font to one worksheet cell."""
        assert self.worksheet is not None
        cell = self.worksheet.cell(row=row + 1, column=column + 1)
        cell.font = Font(bold=True, size=self._heading_font_size(level))

    def _last_used_row(self, sheet: object) -> int:
        """Return the last used row index on a worksheet."""
        worksheet = get_checked_type(sheet, Worksheet)
        return self._used_bounds_by_cell_scan(worksheet, worksheet.max_row,
                                              worksheet.max_column)[0]

    def _last_used_column(self, sheet: object) -> int:
        """Return the last used column index on a worksheet."""
        worksheet = get_checked_type(sheet, Worksheet)
        return self._used_bounds_by_cell_scan(worksheet, worksheet.max_row,
                                              worksheet.max_column)[1]

    def _cell_value(self, sheet: object, row: int, column: int) -> Value:
        """Return one worksheet cell as a public Value."""
        worksheet = get_checked_type(sheet, Worksheet)
        raw = worksheet.cell(row=row + 1, column=column + 1).value
        return self._python_value_from_spreadsheet(raw)

    @staticmethod
    def _table_bounds(table_ref: str) -> tuple[int, int, int, int]:
        """Return zero-based exclusive bounds for one worksheet table."""
        min_column, min_row, max_column, max_row = range_boundaries(table_ref)
        assert min_column is not None
        assert min_row is not None
        assert max_column is not None
        assert max_row is not None
        return min_row - 1, min_column - 1, max_row, max_column

    def _filtered_range_infos(self) -> list[tuple[str, tuple[int, int,
                                                             int, int]]]:
        """Return the worksheet tables and their bounds."""
        assert self.worksheet is not None
        ret: list[tuple[str, tuple[int, int, int, int]]] = []
        for table_name in list(self.worksheet.tables):
            table = self.worksheet.tables[table_name]
            ret.append((table_name, self._table_bounds(table.ref)))
        return ret

    def _delete_filtered_range(self, name: str) -> None:
        """Delete one worksheet table by name."""
        assert self.worksheet is not None
        del self.worksheet.tables[name]

    def _normalize_filtered_table_header(self, top: int, left: int,
                                         right: int) -> None:
        """Convert the filtered table header row to strings when needed."""
        assert self.worksheet is not None
        assert self.read_worksheet is not None
        headers = self._filtered_table_headers([
            self.worksheet.cell(row=top + 1, column=column + 1).value
            for column in range(left, right)
        ])
        for column_offset, header_value in enumerate(headers):
            column = left + column_offset
            cell = self.worksheet.cell(row=top + 1, column=column + 1)
            cell.value = header_value
            if self.read_worksheet is not self.worksheet:
                read_cell = self.read_worksheet.cell(row=top + 1,
                                                     column=column + 1)
                read_cell.value = header_value

    def _add_filtered_range(self, bounds: tuple[int, int, int, int],
                            name: str) -> None:
        """Add one lightweight Excel table for a filtered data range."""
        assert self.worksheet is not None
        self._normalize_filtered_table_header(bounds[0], bounds[1], bounds[3])
        self.worksheet.add_table(
            Table(displayName=name,
                  ref=self._excel_range_ref(bounds[0], bounds[1],
                                            bounds[2], bounds[3])))

    def _set_column_width_if_wider(self, column: int, width: float) -> None:
        """Widen one worksheet column if the target width is larger."""
        assert self.worksheet is not None
        column_letter = get_column_letter(column + 1)
        column_dimension = self.worksheet.column_dimensions[column_letter]
        if column_dimension.width is None or width > column_dimension.width:
            column_dimension.width = width
