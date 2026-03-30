#! /usr/bin/env python3
"""TableIO writer class for Excel files using XlsxWriter."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import io
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, NamedTuple, Optional, Protocol

from mformat.mformat import PathLike
import xlsxwriter  # type: ignore[import-untyped]

from tableio.capability import CAP_ALL_IMPLEMENTED, CAP_UNSUPPORTED, \
    Capabilities, CapabilityNotSupported
from tableio.color import Color
from tableio.tableio import Descriptor, FileAccess
from tableio.tableio_excelbased import TableIOExcelBased
from tableio.value_type import Fmt, ReadResult, Value


_HIGHLIGHT_RGB: dict[Color, str] = {
    Color.RED: '#FFC7CE',
    Color.GREEN: '#C6EFCE',
    Color.YELLOW: '#FFFF00'
}
_DEFAULT_COLUMN_WIDTH = 13.0


class _CellStyle(NamedTuple):
    """Formatting stored for one in-memory cell."""

    fmt: Fmt
    font_size: Optional[int] = None


class _FormatKey(NamedTuple):
    """Cache key for one XlsxWriter format object."""

    bold: bool
    italic: bool
    highlight: Color
    font_size: Optional[int]
    datetime_value: bool


class _WorksheetLike(Protocol):
    """Protocol for the subset of Worksheet methods used here."""

    tables: list[dict[str, object]]
    table_cells: dict[tuple[int, int], str]
    filter_cells: dict[tuple[int, int], tuple[str, str]]

    def add_table(self, *args: object, **kwargs: object) -> int:
        """Add one table to the worksheet."""

    def set_column(self, *args: object, **kwargs: object) -> object:
        """Set one worksheet column width."""

    def write(self, row: int, col: int, *args: object) -> object:
        """Write one cell value."""

    def write_blank(self, row: int, col: int, blank: object,
                    cell_format: Optional[object] = None) -> object:
        """Write one blank cell."""


class _WorkbookLike(Protocol):
    """Protocol for the subset of Workbook methods used here."""

    def add_worksheet(self,
                      name: Optional[str] = None) -> _WorksheetLike:
        """Add one worksheet to the workbook."""

    def add_format(self,
                   properties: Optional[dict[str, object]] = None) -> object:
        """Create one format in the workbook."""

    def close(self) -> None:
        """Close the workbook and write it to disk."""


@dataclass
class _SheetState:
    """In-memory state for one XlsxWriter worksheet."""

    worksheet: _WorksheetLike
    name: str
    values: dict[tuple[int, int], Value] = field(default_factory=dict)
    styles: dict[tuple[int, int], _CellStyle] = field(default_factory=dict)
    filtered_ranges: dict[str, tuple[int, int, int, int]] = \
        field(default_factory=dict)
    column_widths: dict[int, float] = field(default_factory=dict)


class TableIOExcelXlsxWriter(TableIOExcelBased):
    """TableIO writer class for Excel files using XlsxWriter.

    XlsxWriter is a creation-only backend. It can create `.xlsx` files with
    multiple sheets, formatting, filtered table ranges and boxed writes, but
    it cannot read or modify an existing workbook. This implementation keeps
    an in-memory sheet model so the shared spreadsheet writing logic can still
    manage cursor positions, boxed overwrites and filtered-range metadata
    during one open CREATE session.
    """

    def __init__(self, file_name: PathLike,
                 file_access: FileAccess,
                 file_exists_callback: Optional[Callable[[str], None]]
                 = None) -> None:
        """Initialize the XlsxWriter-backed Excel writer."""
        super().__init__(file_name=file_name,
                         file_access=file_access,
                         file_exists_callback=file_exists_callback)
        self.workbook: Optional[_WorkbookLike] = None
        self._sheet_order: list[str] = []
        self._sheet_name_map: dict[str, _SheetState] = {}
        self.sheet_state: Optional[_SheetState] = None
        self._format_cache: dict[_FormatKey, object] = {}
        self._filter_names: set[str] = set()

    @classmethod
    def get_capabilities(cls) -> Capabilities:
        """Return the capabilities for the XlsxWriter Excel backend."""
        return CAP_ALL_IMPLEMENTED._replace(
            can_read=CAP_UNSUPPORTED,
            can_read_box=CAP_UNSUPPORTED,
            can_find_value_position=CAP_UNSUPPORTED)

    @classmethod
    def get_description(cls) -> Descriptor:
        """Return the descriptor for the XlsxWriter Excel backend."""
        return Descriptor(format_name='Excel',
                          implementation='XlsxWriter',
                          capabilities=cls.get_capabilities(),
                          mandatory_args=[],
                          optional_args=[],
                          priority=20)

    def open(self) -> None:
        """Open one workbook for CREATE access."""
        if self.workbook is not None:
            raise RuntimeError(f'File {self.file_name} already open')
        if self.file_access != FileAccess.CREATE:
            msg = ('XlsxWriter can only create new Excel files. '
                   'READ and UPDATE are not supported.')
            raise io.UnsupportedOperation(msg)
        workbook = xlsxwriter.Workbook(self.file_name)
        self.workbook = workbook
        self._sheet_order = []
        self._sheet_name_map = {}
        self.sheet_state = self._create_sheet_state('Sheet1')
        self._format_cache = {}
        self._filter_names = set()
        self._initialize_positions()

    def _end_state(self) -> None:
        """Finalize in-memory state before closing."""

    def _write_file_suffix(self) -> None:
        """Write the workbook to disk."""
        if self.workbook is None:
            return
        workbook = self.workbook
        self.workbook = None
        workbook.close()

    def _close(self) -> None:
        """Release workbook and worksheet references."""
        self.sheet_state = None
        self._sheet_order = []
        self._sheet_name_map = {}
        self._format_cache = {}
        self._filter_names = set()
        self.workbook = None

    def _create_sheet_state(self, sheet_name: str) -> _SheetState:
        """Create and register one worksheet state."""
        assert self.workbook is not None
        worksheet = self.workbook.add_worksheet(sheet_name)
        sheet_state = _SheetState(worksheet=worksheet, name=sheet_name)
        self._sheet_order.append(sheet_name)
        self._sheet_name_map[self._sheet_key(sheet_name)] = sheet_state
        return sheet_state

    def _current_sheet_state(self) -> _SheetState:
        """Return the selected worksheet state."""
        assert self.sheet_state is not None
        return self.sheet_state

    def _list_sheets(self) -> list[str]:
        """List the sheets in the workbook."""
        return list(self._sheet_order)

    def _select_sheet(self, sheet_name: str, create: bool = False) -> None:
        """Select one workbook sheet, optionally creating it."""
        matched = self._sheet_name_map.get(self._sheet_key(sheet_name))
        if matched is None:
            if not create:
                raise KeyError(sheet_name)
            matched = self._create_sheet_state(sheet_name)
        self._save_current_sheet_state()
        self.sheet_state = matched
        self._load_current_sheet_state()

    def _current_sheet_name(self) -> str:
        """Return the name of the selected worksheet."""
        return self._current_sheet_state().name

    def _read_sheet(self) -> object:
        """Return the in-memory readable worksheet state."""
        return self._current_sheet_state()

    def _write_sheet(self) -> object:
        """Return the in-memory writable worksheet state."""
        return self._current_sheet_state()

    def _write_value_to_sheet(self, sheet: object, row: int,
                              column: int, value: object) -> None:
        """Write one value to one worksheet cell."""
        assert isinstance(sheet, _SheetState)
        key = (row, column)
        sheet.styles.pop(key, None)
        typed_value = self._spreadsheet_value_from_python(value)
        if typed_value is None:
            sheet.values.pop(key, None)
        else:
            sheet.values[key] = typed_value
        self._write_actual_cell(sheet, row, column)

    def _set_cell_format(self, sheet: object, row: int, column: int,
                         fmt: Optional[Fmt]) -> None:
        """Apply cell formatting to one worksheet cell."""
        if fmt is None:
            return
        assert isinstance(sheet, _SheetState)
        sheet.styles[(row, column)] = _CellStyle(fmt=fmt)
        self._write_actual_cell(sheet, row, column)

    def _apply_heading_style(self, row: int, column: int, level: int) -> None:
        """Apply the heading style to one worksheet cell."""
        sheet = self._current_sheet_state()
        sheet.styles[(row, column)] = _CellStyle(
            fmt=Fmt(bold=True),
            font_size=self._heading_font_size(level))
        self._write_actual_cell(sheet, row, column)

    def _last_used_row(self, sheet: object) -> int:
        """Return the last used row index on a worksheet."""
        assert isinstance(sheet, _SheetState)
        if not sheet.values:
            return -1
        return max(row for row, _ in sheet.values)

    def _last_used_column(self, sheet: object) -> int:
        """Return the last used column index on a worksheet."""
        assert isinstance(sheet, _SheetState)
        if not sheet.values:
            return -1
        return max(column for _, column in sheet.values)

    def _cell_value(self, sheet: object, row: int, column: int) -> Value:
        """Return one worksheet cell as a public Value."""
        assert isinstance(sheet, _SheetState)
        return sheet.values.get((row, column))

    def _filtered_range_infos(self) -> list[tuple[str, tuple[int, int,
                                                             int, int]]]:
        """Return the worksheet filtered ranges."""
        return list(self._current_sheet_state().filtered_ranges.items())

    def _delete_filtered_range(self, name: str) -> None:
        """Delete one worksheet filtered range."""
        sheet = self._current_sheet_state()
        bounds = sheet.filtered_ranges.pop(name, None)
        if bounds is not None:
            self._remove_table_metadata(sheet, bounds, name)
        self._filter_names.discard(name)

    def _add_filtered_range(self, bounds: tuple[int, int, int, int],
                            name: str) -> None:
        """Add one Excel table for a filtered data range."""
        sheet = self._current_sheet_state()
        top, left, bottom, right = bounds
        headers = self._filtered_table_headers([
            sheet.values.get((top, column))
            for column in range(left, right)
        ])
        columns = [{'header': header} for header in headers]
        worksheet = sheet.worksheet
        result = worksheet.add_table(top, left, bottom - 1, right - 1,
                                     {'name': name,
                                      'style': None,
                                      'banded_rows': False,
                                      'autofilter': True,
                                      'columns': columns})
        if result != 0:
            raise ValueError('Unable to create filtered Excel table range.')
        for column_offset, header in enumerate(headers):
            self._write_value(top, left + column_offset, header,
                              self._cell_fmt(top, left + column_offset))
        sheet.filtered_ranges[name] = bounds
        self._filter_names.add(name)

    def _set_column_width_if_wider(self, column: int, width: float) -> None:
        """Widen one worksheet column if the target width is larger."""
        sheet = self._current_sheet_state()
        current = sheet.column_widths.get(column)
        if current is not None and current >= width:
            return
        if current is None and width <= _DEFAULT_COLUMN_WIDTH:
            return
        sheet.column_widths[column] = width
        sheet.worksheet.set_column(column, column, width)

    def _filter_range_name_in_use(self, name: str) -> bool:
        """Return whether one filter range name is already used."""
        return name in self._filter_names

    def _read_table_listdata(self, box: Optional[object] = None) -> \
            ReadResult[list[list[Value]]]:
        """Reject list-data reads for the write-only backend."""
        _ = box
        raise CapabilityNotSupported('read table data')

    def _read_table_dictdata(self, box: Optional[object] = None) -> \
            ReadResult[list[dict[str, Value]]]:
        """Reject dict-data reads for the write-only backend."""
        _ = box
        raise CapabilityNotSupported('read table data')

    def _cell_fmt(self, row: int, column: int) -> Optional[Fmt]:
        """Return the public format stored for one cell."""
        style = self._current_sheet_state().styles.get((row, column))
        if style is None:
            return None
        return style.fmt

    @classmethod
    def _remove_table_metadata(cls, sheet: _SheetState,
                               bounds: tuple[int, int, int, int],
                               name: str) -> None:
        """Remove one pending XlsxWriter table from worksheet internals."""
        worksheet = sheet.worksheet
        cell_range = cls._excel_range_ref(bounds[0], bounds[1],
                                          bounds[2], bounds[3])
        worksheet.tables = [
            table for table in worksheet.tables
            if table.get('name') != name
        ]
        for row in range(bounds[0], bounds[2]):
            for column in range(bounds[1], bounds[3]):
                if worksheet.table_cells.get((row, column)) == cell_range:
                    del worksheet.table_cells[(row, column)]
        for column in range(bounds[1], bounds[3]):
            filter_info = worksheet.filter_cells.get((bounds[0], column))
            if filter_info == ('table', cell_range):
                del worksheet.filter_cells[(bounds[0], column)]

    def _write_actual_cell(self, sheet: _SheetState, row: int,
                           column: int) -> None:
        """Write the current in-memory cell state to XlsxWriter."""
        value = sheet.values.get((row, column))
        style = sheet.styles.get((row, column))
        cell_format = self._xlsx_format(style, isinstance(value, datetime))
        worksheet = sheet.worksheet
        if value is None:
            worksheet.write_blank(row, column, None, cell_format)
            return
        worksheet.write(row, column, value, cell_format)

    def _xlsx_format(self, style: Optional[_CellStyle],
                     datetime_value: bool) -> Optional[object]:
        """Return the cached XlsxWriter format for one cell style."""
        if style is None and not datetime_value:
            return None
        if style is None:
            key = _FormatKey(bold=False, italic=False,
                             highlight=Color.NONE,
                             font_size=None,
                             datetime_value=True)
        else:
            key = _FormatKey(bold=style.fmt.bold,
                             italic=style.fmt.italic,
                             highlight=style.fmt.highlight,
                             font_size=style.font_size,
                             datetime_value=datetime_value)
        cached = self._format_cache.get(key)
        if cached is not None:
            return cached
        assert self.workbook is not None
        format_dict: dict[str, object] = {}
        if key.bold:
            format_dict['bold'] = True
        if key.italic:
            format_dict['italic'] = True
        if key.highlight != Color.NONE:
            format_dict['bg_color'] = _HIGHLIGHT_RGB[key.highlight]
            format_dict['pattern'] = 1
        if key.font_size is not None:
            format_dict['font_size'] = key.font_size
        if key.datetime_value:
            format_dict['num_format'] = self._datetime_number_format()
        xlsx_format = self.workbook.add_format(format_dict)
        self._format_cache[key] = xlsx_format
        return xlsx_format
