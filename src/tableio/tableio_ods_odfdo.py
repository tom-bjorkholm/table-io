#! /usr/bin/env python3
"""TableIO class for OpenDocument Spreadsheet files using ODFdo."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Any, Callable, Optional
from odfdo import Cell, Document, Style, Table
from odfdo.body import Spreadsheet
from mformat.mformat import PathLike
from tableio.color import Color
from tableio.tableio import Descriptor, FileAccess
from tableio.tableio_spreadsheetbased import TableIOSpreadsheetBased
from tableio.value_type import Fmt, Value, get_checked_type


_DEFAULT_TABLE_NAME = 'Sheet1'
_HIGHLIGHT_RGB: dict[Color, str] = {
    Color.RED: '#ffc7ce',
    Color.GREEN: '#c6efce',
    Color.YELLOW: '#ffff00'
}

_COLUMN_WIDTH_CM_PER_UNIT = 0.25


class TableIOOdsOdfdo(TableIOSpreadsheetBased):
    """TableIO class for OpenDocument Spreadsheet ODS files using odfdo."""

    def __init__(self, file_name: PathLike,
                 file_access: FileAccess,
                 file_exists_callback: Optional[Callable[[str], None]]
                 = None):
        """Initialize the TableIOOdsOdfdo class."""
        super().__init__(file_name=file_name,
                         file_access=file_access,
                         file_exists_callback=file_exists_callback)
        self.document: Optional[Document] = None
        self.table: Optional[Table] = None
        self._style_index: int = 1
        self._cell_style_names: dict[tuple[bool, bool, Color,
                                           Optional[int]], str] = {}
        self._column_style_names: dict[str, str] = {}

    @classmethod
    def get_description(cls) -> Descriptor:
        """Get the description of the TableIOOdsOdfdo class."""
        return Descriptor(format_name='ODS', implementation='odfdo',
                          capabilities=cls.get_capabilities(),
                          mandatory_args=[], optional_args=[])

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the file name extension of the ODS implementation."""
        return '.ods'

    def open(self) -> None:
        """Open the ODS document."""
        if self.document is not None:
            raise RuntimeError(f'File {self.file_name} already open')
        table: Optional[Table]
        if self.file_access == FileAccess.CREATE:
            document = Document('spreadsheet')
            body = get_checked_type(document.body, Spreadsheet)
            body.clear()
            table = Table(_DEFAULT_TABLE_NAME)
            body.append(table)
        else:
            document = Document(self.file_name)
            body = get_checked_type(document.body, Spreadsheet)
            table = body.get_table(position=0)
            if table is None:
                table = Table(_DEFAULT_TABLE_NAME)
                body.append(table)
        self.document = document
        assert table is not None
        self.table = table
        self._style_index = 1
        self._cell_style_names = {}
        self._column_style_names = {}
        self._initialize_positions()

    def _end_state(self) -> None:
        """Finalize in-memory state before closing."""

    def _write_file_suffix(self) -> None:
        """Write the ODS document to disk when the file is writable."""
        if self.file_access == FileAccess.READ:
            return
        assert self.document is not None
        self.document.save(self.file_name)

    def _close(self) -> None:
        """Release document references."""
        self.table = None
        self.document = None

    def _read_sheet(self) -> object:
        """Return the readable ODS table."""
        assert self.table is not None
        return self.table

    def _write_sheet(self) -> object:
        """Return the writable ODS table."""
        assert self.table is not None
        return self.table

    def _spreadsheet_body(self) -> Spreadsheet:
        """Return the spreadsheet body of the open ODS document."""
        assert self.document is not None
        return get_checked_type(self.document.body, Spreadsheet)

    def _write_value_to_sheet(self, sheet: object, row: int,
                              column: int, value: object) -> None:
        """Write one value to one ODS cell."""
        table = get_checked_type(sheet, Table)
        table.set_cell((column, row),
                       Cell(self._spreadsheet_value_from_python(value)),
                       clone=False)

    def _set_cell_format(self, sheet: object, row: int, column: int,
                         fmt: Optional[Fmt]) -> None:
        """Apply cell formatting to one ODS cell."""
        if fmt is None:
            return
        table = get_checked_type(sheet, Table)
        table.get_cell((column, row), clone=False).style = \
            self._cell_style_name(fmt)

    def _apply_heading_style(self, row: int, column: int, level: int) -> None:
        """Apply the heading style to one ODS cell."""
        assert self.table is not None
        self.table.get_cell((column, row), clone=False).style = \
            self._cell_style_name(Fmt(bold=True),
                                  font_size=self._heading_font_size(level))

    def _used_bounds(self, sheet: object) -> tuple[int, int]:
        """Return the last used row and column on one ODS table."""
        table = get_checked_type(sheet, Table)
        last_row = -1
        last_column = -1
        for row in range(table.height):
            for column in range(table.width):
                if self._cell_value(table, row, column) is None:
                    continue
                last_row = max(last_row, row)
                last_column = max(last_column, column)
        return last_row, last_column

    def _last_used_row(self, sheet: object) -> int:
        """Return the last used row index on one ODS table."""
        return self._used_bounds(sheet)[0]

    def _last_used_column(self, sheet: object) -> int:
        """Return the last used column index on one ODS table."""
        return self._used_bounds(sheet)[1]

    def _cell_value(self, sheet: object, row: int, column: int) -> Value:
        """Return one ODS cell as a public Value."""
        table = get_checked_type(sheet, Table)
        return self._python_value_from_spreadsheet(
            table.get_value((column, row)))

    def _filtered_range_infos(self) -> list[tuple[str, tuple[int, int,
                                                             int, int]]]:
        """Return the filter named ranges for the active table."""
        assert self.table is not None
        ret: list[tuple[str, tuple[int, int, int, int]]] = []
        for named_range in self._spreadsheet_body().get_named_ranges():
            if named_range.usage != 'filter':
                continue
            if named_range.table_name != self.table.name:
                continue
            left, top, right, bottom = named_range.crange
            ret.append((str(named_range.name),
                        (top, left, bottom + 1, right + 1)))
        return ret

    def _delete_filtered_range(self, name: str) -> None:
        """Delete one named filter range by name."""
        self._spreadsheet_body().delete_named_range(name)

    def _add_filtered_range(self, bounds: tuple[int, int, int, int],
                            name: str) -> None:
        """Create one named filter range for the active table."""
        assert self.table is not None
        top, left, bottom, right = bounds
        self.table.set_named_range(name=name,
                                   crange=(left, top, right - 1, bottom - 1),
                                   usage='filter')

    @staticmethod
    def _column_width_string(width: float) -> str:
        """Return the ODS column width string for one target width."""
        return f'{width * _COLUMN_WIDTH_CM_PER_UNIT:.2f}cm'

    @classmethod
    def _column_width_from_text(cls, width: str) -> Optional[float]:
        """Parse one ODS column width string to the internal width unit."""
        if not width.endswith('cm'):
            return None
        try:
            width_cm = float(width[:-2])
        except ValueError:
            return None
        return width_cm / _COLUMN_WIDTH_CM_PER_UNIT

    def _current_column_width(self, column: int) -> Optional[float]:
        """Return the current width of one ODS column."""
        assert self.document is not None
        assert self.table is not None
        odf_column = self.table.get_column(column)
        if odf_column.style is None:
            return None
        style = self.document.get_style('table-column', odf_column.style)
        if style is None:
            return None
        properties = get_checked_type(style, Style).get_properties(
            'table-column')
        if properties is None:
            return None
        width_text = properties.get('style:column-width')
        if width_text is None:
            return None
        return self._column_width_from_text(str(width_text))

    def _set_column_width_if_wider(self, column: int, width: float) -> None:
        """Widen one ODS column if the target width is larger."""
        assert self.table is not None
        current_width = self._current_column_width(column)
        if current_width is not None and current_width >= width:
            return
        odf_column = self.table.get_column(column)
        odf_column.style = self._column_style_name(width)
        self.table.set_column(column, odf_column)

    def _next_style_name(self, prefix: str, family: str) -> str:
        """Return a document-unique style name."""
        assert self.document is not None
        while True:
            name = f'{prefix}{self._style_index}'
            self._style_index += 1
            if self.document.get_style(family, name) is None:
                return name

    def _cell_style_name(self, fmt: Fmt,
                         font_size: Optional[int] = None) -> str:
        """Return the cached style name for one cell format combination."""
        key = (fmt.bold, fmt.italic, fmt.highlight, font_size)
        cached = self._cell_style_names.get(key)
        if cached is not None:
            return cached
        assert self.document is not None
        style_name = self._next_style_name('ce_tableio_', 'table-cell')
        if fmt.bold or fmt.italic:
            style = Style('table-cell', name=style_name, area='text',
                          bold=fmt.bold, italic=fmt.italic)
        else:
            style = Style('table-cell', name=style_name)
        text_props: dict[str, Any] = {}
        if font_size is not None:
            size_text = f'{font_size}pt'
            text_props['fo:font-size'] = size_text
            text_props['style:font-size-asian'] = size_text
            text_props['style:font-size-complex'] = size_text
        if text_props:
            style.set_properties(text_props, area='text')
        if fmt.highlight != Color.NONE:
            table_props: dict[str, Any] = {
                'fo:background-color': _HIGHLIGHT_RGB[fmt.highlight]
            }
            style.set_properties(table_props, area='table-cell')
        self.document.insert_style(style, automatic=True)
        self._cell_style_names[key] = style_name
        return style_name

    def _column_style_name(self, width: float) -> str:
        """Return the cached style name for one column width."""
        width_text = self._column_width_string(width)
        cached = self._column_style_names.get(width_text)
        if cached is not None:
            return cached
        assert self.document is not None
        style_name = self._next_style_name('co_tableio_', 'table-column')
        style = Style('table-column', name=style_name, width=width_text)
        self.document.insert_style(style, automatic=True)
        self._column_style_names[width_text] = style_name
        return style_name
