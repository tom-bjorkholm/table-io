#! /usr/bin/env python3
"""TableIO class for OpenDocument Spreadsheet files using ODFdo."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Any, Callable, Optional
from xml.etree import ElementTree as ET
from odfdo import Cell, Document, Element, Style, Table
from odfdo.body import Spreadsheet
from odfdo.utils import is_RFC3066
from mformat.mformat import PathLike
from tableio._archive_rewrite import rewrite_zip_archive, \
    temporary_output_path
from tableio.border_helper import BorderWeight, CellBorder, CellStyleState, \
    DEFAULT_CELL_STYLE, NO_BORDERS
from tableio.color import Color
from tableio.tableio import Descriptor, FileAccess
from tableio.tableio_spreadsheetbased import TableIOSpreadsheetBased, \
    excel_column_name
from tableio.value_type import Fmt, Value, get_checked_type
from tableio.capability import CAP_ALL_IMPLEMENTED, Capabilities


_DEFAULT_TABLE_NAME = 'Sheet1'
_HIGHLIGHT_RGB: dict[Color, str] = {
    Color.RED: '#ffc7ce',
    Color.GREEN: '#c6efce',
    Color.YELLOW: '#ffff00'
}
_COLUMN_WIDTH_CM_PER_UNIT = 0.25
_BORDER_TEXT: dict[BorderWeight, str] = {
    BorderWeight.THIN: '0.75pt solid #000000',
    BorderWeight.THICK: '1.75pt solid #000000'
}
_XML_NS = {
    'manifest': 'urn:oasis:names:tc:opendocument:xmlns:manifest:1.0',
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'calcext': 'urn:org:documentfoundation:names:experimental:calc:'
    'xmlns:calcext:1.0',
    'svg': 'urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0'
}

for _prefix, _namespace in _XML_NS.items():
    ET.register_namespace(_prefix, _namespace)


def _manifest_xml_without_configuration_entries(data: bytes) -> bytes:
    """Return manifest XML without unused Configurations2 file entries."""
    root = ET.fromstring(data)
    for entry in list(root.findall('manifest:file-entry', _XML_NS)):
        full_path = entry.get('{%s}full-path' % _XML_NS['manifest'])
        if full_path is None or not full_path.startswith('Configurations2/'):
            continue
        root.remove(entry)
    return bytes(ET.tostring(root, encoding='utf-8',
                             xml_declaration=True))


def _referenced_style_names(root: ET.Element) -> set[str]:
    """Return the set of style names referenced from one XML tree."""
    referenced: set[str] = set()
    for element in root.iter():
        for attr_name, attr_value in element.attrib.items():
            if attr_name.endswith('}style-name') and attr_value:
                referenced.add(attr_value)
    return referenced


def _content_xml_without_unused_styles(data: bytes) -> bytes:
    """Return content XML with unused automatic styles removed."""
    root = ET.fromstring(data)
    automatic_styles = root.find('office:automatic-styles', _XML_NS)
    if automatic_styles is None:
        return bytes(ET.tostring(root, encoding='utf-8',
                                 xml_declaration=True))
    referenced_names = _referenced_style_names(root)
    for style in list(automatic_styles.findall('style:style', _XML_NS)):
        style_name = style.get('{%s}name' % _XML_NS['style'])
        if style_name is None or style_name in referenced_names:
            continue
        automatic_styles.remove(style)
    return bytes(ET.tostring(root, encoding='utf-8',
                             xml_declaration=True))


def _styles_xml_with_required_defaults(data: bytes) -> bytes:
    """Return styles XML with default table and table-row styles added."""
    root = ET.fromstring(data)
    office_styles = root.find('office:styles', _XML_NS)
    if office_styles is None:
        return bytes(ET.tostring(root, encoding='utf-8',
                                 xml_declaration=True))
    existing_families = {
        style.get('{%s}family' % _XML_NS['style'])
        for style in office_styles.findall('style:default-style', _XML_NS)
    }
    for family in ['table', 'table-row']:
        if family in existing_families:
            continue
        ET.SubElement(office_styles, '{%s}default-style' % _XML_NS['style'],
                      {'{%s}family' % _XML_NS['style']: family})
    return bytes(ET.tostring(root, encoding='utf-8',
                             xml_declaration=True))


def _rewrite_saved_document(file_name: Path) -> None:
    """Rewrite one saved ODS archive to remove validator complaints."""
    def rewrite_entry(item: object, data: bytes) -> Optional[bytes]:
        """Rewrite or drop one ODS archive entry when needed."""
        file_name_text = getattr(item, 'filename')
        if file_name_text.startswith('Configurations2/'):
            return None
        if file_name_text == 'META-INF/manifest.xml':
            return _manifest_xml_without_configuration_entries(data)
        if file_name_text == 'content.xml':
            return _content_xml_without_unused_styles(data)
        if file_name_text == 'styles.xml':
            return _styles_xml_with_required_defaults(data)
        return data
    rewrite_zip_archive(file_name, rewrite_entry)


class TableIOOdsOdfdo(TableIOSpreadsheetBased):
    """TableIO class for OpenDocument Spreadsheet ODS files using odfdo.

    The implementation operates on one current sheet at a time.
    """

    def __init__(self, file_name: PathLike,
                 file_access: FileAccess,
                 file_exists_callback: Optional[Callable[[str], None]]
                 = None,
                 lang: str = 'en-UK'):
        """Initialize the TableIOOdsOdfdo class.

        Args:
            file_name: The name of the file to open.
            file_access: What access is requested to the file.
            file_exists_callback: Callback used when CREATE would overwrite.
            lang: The RFC3066 language code for newly created ODS files.
        """
        super().__init__(file_name=file_name,
                         file_access=file_access,
                         file_exists_callback=file_exists_callback)
        self.lang: str = self._checked_lang(lang)
        self.document: Optional[Document] = None
        self.table: Optional[Table] = None
        self._style_index: int = 1
        self._cell_style_names: dict[
            tuple[bool, bool, Color, Optional[int], CellBorder],
            str] = {}
        self._cell_style_states: dict[
            tuple[str, int, int], CellStyleState] = {}
        self._column_style_names: dict[str, str] = {}

    @classmethod
    def get_capabilities(cls) -> Capabilities:
        """Return the standard spreadsheet backend capabilities."""
        return CAP_ALL_IMPLEMENTED

    @classmethod
    def get_description(cls) -> Descriptor:
        """Get the description of the TableIOOdsOdfdo class."""
        return Descriptor(format_name='ODS', implementation='odfdo',
                          capabilities=cls.get_capabilities(),
                          mandatory_args=[], optional_args=['lang'])

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
            self._set_document_language(document)
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
        self._cell_style_states = {}
        self._column_style_names = {}
        self._initialize_positions()

    @staticmethod
    def _checked_lang(lang: str) -> str:
        """Validate one document language string."""
        if not is_RFC3066(lang):
            msg = ('Language must be "xx" lang or "xx-YY" lang-COUNTRY '
                   'code (RFC3066)')
            raise TypeError(msg)
        return lang

    @staticmethod
    def _split_rfc3066_language(lang: str) -> tuple[str, str]:
        """Split one validated RFC3066 language string."""
        language_parts = lang.split('-')
        if len(language_parts) == 2:
            return language_parts[0], language_parts[1]
        return language_parts[0], ''

    def _set_document_language(self, document: Document) -> None:
        """Set the ODS metadata and default cell language."""
        language, country = self._split_rfc3066_language(self.lang)
        document.set_language(self.lang)
        default_styles = [
            style for style in document.styles.default_styles
            if style.family == 'table-cell'
        ]
        for style in default_styles:
            style.set_properties(area='text', language=language,
                                 country=country)

    def _end_state(self) -> None:
        """Finalize in-memory state before closing."""

    def _write_file_suffix(self) -> None:
        """Write the ODS document to disk when the file is writable."""
        if self.file_access == FileAccess.READ:
            return
        assert self.document is not None
        file_path = Path(self.file_name)
        temp_path = temporary_output_path(file_path, '.ods')
        try:
            self.document.save(temp_path)
            _rewrite_saved_document(temp_path)
            temp_path.replace(file_path)
        finally:
            if temp_path.exists():
                temp_path.unlink()

    def _close(self) -> None:
        """Release document references."""
        self.table = None
        self.document = None
        self._cell_style_states = {}

    def _table_name_map(self) -> dict[str, Table]:
        """Return the document tables indexed case-insensitively."""
        ret: dict[str, Table] = {}
        for table in self._spreadsheet_body().get_tables():
            ret[str(table.name).casefold()] = table
        return ret

    def _list_sheets(self) -> list[str]:
        """List the sheets in the document."""
        return [str(table.name)
                for table in self._spreadsheet_body().get_tables()]

    def _select_sheet(self, sheet_name: str, create: bool = False) -> None:
        """Select one document sheet, optionally creating it."""
        assert self.table is not None
        table = self._table_name_map().get(self._sheet_key(sheet_name))
        if table is None:
            if not create:
                raise KeyError(sheet_name)
            self._check_file_is_writable()
            table = Table(sheet_name)
            self._spreadsheet_body().append(table)
        self._save_current_sheet_state()
        self.table = table
        self._load_current_sheet_state()

    def _current_sheet_name(self) -> str:
        """Return the name of the selected sheet."""
        assert self.table is not None
        return str(self.table.name)

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

    def _database_range_container(self) -> Element:
        """Return the container for ODS database ranges."""
        spreadsheet = self._spreadsheet_body()
        container = spreadsheet.get_element('table:database-ranges')
        if container is not None:
            return container
        container = Element.from_tag('table:database-ranges')
        spreadsheet.append(container)
        return container

    def _database_ranges(self) -> list[Element]:
        """Return the ODS database range elements."""
        return self._spreadsheet_body().get_elements(
            'descendant::table:database-ranges/table:database-range')

    @staticmethod
    def _quoted_table_name(table_name: str) -> str:
        """Return a table name formatted for an ODF range address."""
        if all(character.isalnum() or character == '_'
               for character in table_name):
            return table_name
        return f"'{table_name}'"

    @classmethod
    def _database_range_address(cls, table_name: str,
                                bounds: tuple[int, int, int, int]) -> str:
        """Return one ODS database range address."""
        top, left, bottom, right = bounds
        q_table = cls._quoted_table_name(table_name)
        start = f'{excel_column_name(left)}{top + 1}'
        end = f'{excel_column_name(right - 1)}{bottom}'
        return f'{q_table}.{start}:{q_table}.{end}'

    @staticmethod
    def _split_range_endpoint(endpoint: str) -> tuple[str, str]:
        """Split one table-qualified ODF cell endpoint."""
        normalized = endpoint.replace('$', '')
        if normalized.startswith("'"):
            split_pos = normalized.find("'.")
            if split_pos < 0:
                raise ValueError(f'Invalid endpoint {endpoint!r}')
            table_name = normalized[1:split_pos]
            cell_ref = normalized[split_pos + 2:]
            return table_name, cell_ref
        table_name, cell_ref = normalized.split('.', 1)
        return table_name, cell_ref

    @staticmethod
    def _cell_ref_to_position(cell_ref: str) -> tuple[int, int]:
        """Convert one A1 cell reference to zero-based coordinates."""
        column_text = ''
        row_text = ''
        for character in cell_ref.upper():
            if character.isalpha():
                if row_text:
                    raise ValueError(f'Invalid cell reference {cell_ref!r}')
                column_text += character
                continue
            if character.isdigit():
                row_text += character
                continue
            raise ValueError(f'Invalid cell reference {cell_ref!r}')
        if not column_text or not row_text:
            raise ValueError(f'Invalid cell reference {cell_ref!r}')
        column = 0
        for character in column_text:
            column = column * 26 + ord(character) - ord('A') + 1
        return int(row_text) - 1, column - 1

    @classmethod
    def _endpoint_position(cls, endpoint: str) -> tuple[str, int, int]:
        """Return table name and coordinates for one range endpoint."""
        table_name, cell_ref = cls._split_range_endpoint(endpoint)
        row, column = cls._cell_ref_to_position(cell_ref)
        return table_name, row, column

    @classmethod
    def _database_range_bounds(
            cls, database_range: Element) -> tuple[str, tuple[int, int,
                                                              int, int]]:
        """Return table name and bounds for one ODS database range."""
        address = database_range.get_attribute_string(
            'table:target-range-address')
        if not address:
            raise ValueError('Missing target range address.')
        endpoints = str(address).split(':', 1)
        start_table, start_row, start_column = cls._endpoint_position(
            endpoints[0])
        if len(endpoints) == 1:
            end_row = start_row
            end_column = start_column
        else:
            end_table, end_row, end_column = cls._endpoint_position(
                endpoints[1])
            if end_table != start_table:
                raise ValueError('Database range spans several tables.')
        top = min(start_row, end_row)
        left = min(start_column, end_column)
        bottom = max(start_row, end_row) + 1
        right = max(start_column, end_column) + 1
        return start_table, (top, left, bottom, right)

    def _write_value_to_sheet(self, sheet: object, row: int,
                              column: int, value: object) -> None:
        """Write one value to one ODS cell."""
        table = get_checked_type(sheet, Table)
        table.set_cell((column, row),
                       Cell(self._spreadsheet_value_from_python(value)),
                       clone=False)
        self._cell_style_states.pop(self._cell_style_state_key(
            table, row, column), None)

    def _set_cell_format(self, sheet: object, row: int, column: int,
                         fmt: Optional[Fmt]) -> None:
        """Apply cell formatting to one ODS cell."""
        if fmt is None:
            return
        table = get_checked_type(sheet, Table)
        current = self._cell_style_state(table, row, column)
        self._apply_cell_style(
            table, row, column,
            CellStyleState(fmt=fmt,
                           font_size=current.font_size,
                           borders=current.borders))

    def _set_cell_borders(self, sheet: object, row: int, column: int,
                          borders: CellBorder) -> None:
        """Apply normalized borders to one ODS cell."""
        table = get_checked_type(sheet, Table)
        current = self._cell_style_state(table, row, column)
        self._apply_cell_style(
            table, row, column,
            CellStyleState(fmt=current.fmt,
                           font_size=current.font_size,
                           borders=borders))

    def _apply_heading_style(self, row: int, column: int, level: int) -> None:
        """Apply the heading style to one ODS cell."""
        assert self.table is not None
        current = self._cell_style_state(self.table, row, column)
        self._apply_cell_style(
            self.table, row, column,
            CellStyleState(fmt=Fmt(bold=True),
                           font_size=self._heading_font_size(level),
                           borders=current.borders))

    def _last_used_row(self, sheet: object) -> int:
        """Return the last used row index on one ODS table."""
        table = get_checked_type(sheet, Table)
        return self._used_bounds_by_cell_scan(table, table.height,
                                              table.width)[0]

    def _last_used_column(self, sheet: object) -> int:
        """Return the last used column index on one ODS table."""
        table = get_checked_type(sheet, Table)
        return self._used_bounds_by_cell_scan(table, table.height,
                                              table.width)[1]

    def _cell_value(self, sheet: object, row: int, column: int) -> Value:
        """Return one ODS cell as a public Value."""
        table = get_checked_type(sheet, Table)
        return self._python_value_from_spreadsheet(
            table.get_value((column, row)))

    def _filtered_range_infos(self) -> list[tuple[str, tuple[int, int,
                                                             int, int]]]:
        """Return filtered ranges for the active table."""
        assert self.table is not None
        ret: dict[str, tuple[int, int, int, int]] = {}
        for database_range in self._database_ranges():
            name = database_range.get_attribute_string('table:name')
            if name is None:
                continue
            display_buttons = database_range.get_attribute_string(
                'table:display-filter-buttons')
            if display_buttons != 'true':
                continue
            table_name, bounds = self._database_range_bounds(database_range)
            if table_name != self.table.name:
                continue
            ret[str(name)] = bounds
        for named_range in self._spreadsheet_body().get_named_ranges():
            if named_range.usage != 'filter':
                continue
            if named_range.table_name != self.table.name:
                continue
            left, top, right, bottom = named_range.crange
            ret.setdefault(str(named_range.name),
                           (top, left, bottom + 1, right + 1))
        return list(ret.items())

    def _delete_filtered_range(self, name: str) -> None:
        """Delete one filtered range by name."""
        for database_range in self._database_ranges():
            range_name = database_range.get_attribute_string('table:name')
            if range_name == name:
                database_range.delete()
        self._spreadsheet_body().delete_named_range(name)

    def _add_filtered_range(self, bounds: tuple[int, int, int, int],
                            name: str) -> None:
        """Create one filtered database range for the active table."""
        assert self.table is not None
        database_range = Element.from_tag('table:database-range')
        database_range.set_attribute('table:name', name)
        database_range.set_attribute('table:contains-header', 'true')
        database_range.set_attribute('table:display-filter-buttons', 'true')
        database_range.set_attribute(
            'table:target-range-address',
            self._database_range_address(str(self.table.name), bounds))
        self._database_range_container().append(database_range)

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

    @staticmethod
    def _cell_style_state_key(table: Table, row: int,
                              column: int) -> tuple[str, int, int]:
        """Return the cache key for one touched ODS cell."""
        return str(table.name), row, column

    def _cell_style_state(self, table: Table, row: int,
                          column: int) -> CellStyleState:
        """Return the current in-memory style state for one cell."""
        return self._cell_style_states.get(
            self._cell_style_state_key(table, row, column),
            DEFAULT_CELL_STYLE)

    def _apply_cell_style(self, table: Table, row: int, column: int,
                          style: CellStyleState) -> None:
        """Store and apply one composed ODS cell style."""
        key = self._cell_style_state_key(table, row, column)
        cell = table.get_cell((column, row), clone=False)
        if style == DEFAULT_CELL_STYLE:
            self._cell_style_states.pop(key, None)
            setattr(cell, 'style', None)
            return
        self._cell_style_states[key] = style
        cell.style = self._cell_style_name(style.fmt,
                                           font_size=style.font_size,
                                           borders=style.borders)

    @staticmethod
    def _border_property_text(weight: BorderWeight) -> Optional[str]:
        """Return one ODF border property value."""
        if weight == BorderWeight.NONE:
            return None
        return _BORDER_TEXT[weight]

    def _cell_style_name(self, fmt: Fmt,
                         font_size: Optional[int] = None,
                         borders: CellBorder = NO_BORDERS) -> str:
        """Return the cached style name for one cell format combination."""
        key = (fmt.bold, fmt.italic, fmt.highlight, font_size, borders)
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
        table_props: dict[str, Any] = {}
        if fmt.highlight != Color.NONE:
            table_props['fo:background-color'] = _HIGHLIGHT_RGB[
                fmt.highlight]
        for property_name, weight in [
                ('fo:border-top', borders.top),
                ('fo:border-right', borders.right),
                ('fo:border-bottom', borders.bottom),
                ('fo:border-left', borders.left)]:
            border_text = self._border_property_text(weight)
            if border_text is not None:
                table_props[property_name] = border_text
        if table_props:
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
