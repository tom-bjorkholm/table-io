#! /usr/bin/env python3
"""TableIO reader/writer class for Excel files using pylightxl."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Optional, Protocol, cast
from xml.etree import ElementTree as ET
from zipfile import ZipFile
from mformat.mformat import PathLike
from openpyxl.writer.theme import theme_xml
from pylightxl import Database, writexl  # type: ignore[import-untyped]
from pylightxl import pylightxl as pylightxl_impl
from tableio._archive_rewrite import rewrite_zip_archive, \
    temporary_output_path
from tableio.capability import CAP_IMPLEMENTED, CAP_IGNORED, Capabilities
from tableio.tableio import Descriptor, FileAccess
from tableio.tableio_excelbased import TableIOExcelBased
from tableio.value_type import Fmt, Value


_DEFAULT_SHEET_NAME = 'Sheet1'
_DATE_STYLE_CODES = {'14', '15', '16', '17'}
_TIME_STYLE_CODES = {'18', '19', '20', '21'}
_DATETIME_STYLE_CODE = '22'
_DATETIME_NUMFMT_ID = '164'
_DATETIME_DISPLAY_FORMAT = 'yyyy-mm-dd hh:mm:ss'
_STYLE_CODE_TO_INDEX = {
    '14': '1',
    '18': '2',
    '22': '3'
}
_XML_NS = {
    'content': 'http://schemas.openxmlformats.org/package/2006/content-types',
    'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
    'rels': 'http://schemas.openxmlformats.org/package/2006/relationships'
}
_WORKSHEET_XML_NS = {
    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/'
    'relationships',
    'x14ac': 'http://schemas.microsoft.com/office/spreadsheetml/2009/9/ac',
    'xr': 'http://schemas.microsoft.com/office/spreadsheetml/2014/revision'
}
_IGNORABLE_PREFIXES = 'x14ac xr'

ET.register_namespace('', _XML_NS['main'])
for _prefix, _namespace in _WORKSHEET_XML_NS.items():
    ET.register_namespace(_prefix, _namespace)


class _WorksheetLike(Protocol):  # pylint: disable=too-few-public-methods
    """Typed subset of the pylightxl worksheet API used here."""

    _data: dict[str, dict[str, object]]

    def _calc_size(self) -> None:
        """Recalculate cached worksheet size information."""

    def update_address(self, address: str, val: object) -> None:
        """Update one worksheet cell by Excel address."""


def _worksheet_names(database: Database) -> list[str]:
    """Return the workbook sheet names with a concrete static type."""
    return cast(list[str], database.ws_names)


def _database_worksheet(database: Database, sheet_name: str) -> _WorksheetLike:
    """Return one worksheet from the database with a concrete static type."""
    return cast(_WorksheetLike, database.ws(sheet_name))


def _worksheet_cells(worksheet: _WorksheetLike) -> dict[str, dict[str,
                                                                  object]]:
    """Return the internal worksheet cell dictionary."""
    return worksheet._data  # pylint: disable=protected-access


def _recalculate_worksheet_size(worksheet: _WorksheetLike) -> None:
    """Recalculate the cached worksheet size after cell deletion."""
    worksheet._calc_size()  # pylint: disable=protected-access


def _worksheet_id_attr(tag_sheet: ET.Element) -> Optional[str]:
    """Return the relationship id stored on one workbook sheet element."""
    rel_id = tag_sheet.get('{%s}id' % _XML_NS['rels'])
    if rel_id is not None:
        return rel_id
    for key, value in tag_sheet.attrib.items():
        if key.endswith('}id'):
            return value
    return tag_sheet.get('id')


def _sheet_xml_targets(file_name: str) -> dict[str, tuple[int, str]]:
    """Return sheet order and XML target path for each workbook sheet."""
    with ZipFile(file_name, 'r') as zip_file:
        workbook_root = ET.fromstring(zip_file.read('xl/workbook.xml'))
        rel_root = ET.fromstring(zip_file.read('xl/_rels/workbook.xml.rels'))
    rel_map: dict[str, str] = {}
    for relationship in rel_root.findall('rels:Relationship', _XML_NS):
        target = relationship.get('Target')
        rel_id = relationship.get('Id')
        if rel_id is None or target is None:
            continue
        if target.startswith('/xl/'):
            target = target[4:]
        rel_map[rel_id] = target
    ret: dict[str, tuple[int, str]] = {}
    for tag_sheet in workbook_root.findall('main:sheets/main:sheet', _XML_NS):
        name = tag_sheet.get('name')
        rel_id = _worksheet_id_attr(tag_sheet)
        sheet_id = tag_sheet.get('sheetId')
        if name is None or rel_id is None or sheet_id is None:
            continue
        target = rel_map.get(rel_id)
        if target is None:
            continue
        ret[name] = (int(sheet_id), target)
    return ret


def _xml_text(element: Optional[ET.Element]) -> str:
    """Return the text of one XML element, defaulting to the empty string."""
    if element is None or element.text is None:
        return ''
    return element.text


def _inline_string_text(cell: ET.Element) -> str:
    """Return the concatenated text of one inline string cell."""
    texts = [
        _xml_text(tag_text)
        for tag_text in cell.findall('./main:is//main:t', _XML_NS)
    ]
    return ''.join(texts)


def _number_from_cell_text(raw_value: str) -> object:
    """Return one numeric cell text as int, float or the original string."""
    test_value = raw_value[1:] if raw_value.startswith('-') else raw_value
    if test_value.isdigit():
        return int(raw_value)
    try:
        return float(raw_value)
    except ValueError:
        return raw_value


def _xml_bytes(root: ET.Element) -> bytes:
    """Return one XML element serialized as UTF-8 bytes."""
    ET.register_namespace('', _XML_NS['main'])
    for prefix, namespace in _WORKSHEET_XML_NS.items():
        ET.register_namespace(prefix, namespace)
    return cast(bytes, ET.tostring(root, encoding='utf-8',
                                   xml_declaration=True))


def _datetime_from_excel_number(number: int | float) -> datetime:
    """Return one Excel serial number converted to a Python datetime."""
    excel_start = cast(datetime, pylightxl_impl.EXCEL_STARTDATE)
    total_seconds = round(float(number) * 86400)
    return excel_start + timedelta(seconds=total_seconds)


def _datetime_to_excel_number(value: datetime) -> float:
    """Return one Python datetime converted to an Excel serial number."""
    excel_start = cast(datetime, pylightxl_impl.EXCEL_STARTDATE)
    delta = value - excel_start
    return delta.days + delta.seconds / 86400 + \
        delta.microseconds / 86400000000


def _sheet_data_from_xml(
        xml_data: bytes, shared_strings: dict[int, str],
        styles: dict[int, str]) -> dict[str, dict[str, object]]:
    """Return one worksheet cell dictionary parsed from worksheet XML."""
    root = ET.fromstring(xml_data)
    ret: dict[str, dict[str, object]] = {}
    for cell in root.findall('./main:sheetData/main:row/main:c', _XML_NS):
        address = cell.get('r')
        if address is None:
            continue
        tag_value = cell.find('./main:v', _XML_NS)
        tag_formula = cell.find('./main:f', _XML_NS)
        tag_inline = cell.find('./main:is', _XML_NS)
        if tag_value is None and tag_formula is None and tag_inline is None:
            continue
        cell_type = cell.get('t')
        style_code = styles.get(int(cell.get('s', '0')), '0')
        raw_value = _xml_text(tag_value)
        value: object
        if cell_type == 'inlineStr':
            value = _inline_string_text(cell)
        elif cell_type == 's':
            try:
                value = shared_strings[int(raw_value)]
            except (KeyError, ValueError):
                value = raw_value
        elif cell_type == 'b':
            value = raw_value == '1'
        elif cell_type in ('str', 'e') or raw_value == '':
            value = raw_value
        else:
            value = _number_from_cell_text(raw_value)
        ret[address] = {'v': value,
                        'f': _xml_text(tag_formula),
                        's': style_code,
                        'c': ''}
    return ret


def _load_named_ranges(workbook_root: ET.Element, database: Database) -> None:
    """Load workbook defined names into the pylightxl database."""
    for defined_name in workbook_root.findall(
            'main:definedNames/main:definedName', _XML_NS):
        name = defined_name.get('name')
        address = defined_name.text
        if name is None or address is None or '!' not in address:
            continue
        worksheet_name, cell_range = address.replace('$', '').split('!', 1)
        database.add_nr(name=name, ws=worksheet_name.replace("'", ''),
                        address=cell_range)


def _read_database(file_name: str) -> Database:
    """Read one workbook with pylightxl plus workbook-namespace fixes."""
    checked_file_name = pylightxl_impl.readxl_check_excelfile(file_name)
    sheet_targets = _sheet_xml_targets(checked_file_name)
    shared_strings = pylightxl_impl.readxl_get_sharedStrings(checked_file_name)
    styles = pylightxl_impl.readxl_get_styles(checked_file_name)
    database = Database()
    with ZipFile(checked_file_name, 'r') as zip_file:
        workbook_root = ET.fromstring(zip_file.read('xl/workbook.xml'))
        _load_named_ranges(workbook_root, database)
        for sheet_name, (_, target) in sorted(sheet_targets.items(),
                                              key=lambda item: item[1][0]):
            data = _sheet_data_from_xml(zip_file.read(f'xl/{target}'),
                                        shared_strings, styles)
            database.add_ws(ws=sheet_name, data=data)
    database.set_emptycell(None)
    return database


def _style_index_for_code(style_code: str) -> Optional[str]:
    """Return the compact styles.xml xf index for one stored style code."""
    if style_code in _DATE_STYLE_CODES:
        return _STYLE_CODE_TO_INDEX['14']
    if style_code in _TIME_STYLE_CODES:
        return _STYLE_CODE_TO_INDEX['18']
    if style_code == _DATETIME_STYLE_CODE:
        return _STYLE_CODE_TO_INDEX['22']
    return None


def _styles_xml() -> bytes:
    """Return a minimal styles.xml supporting date, time and datetime tags."""
    text = '\n'.join([
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<styleSheet xmlns="http://schemas.openxmlformats.org/'
        'spreadsheetml/2006/main">',
        f'<numFmts count="1"><numFmt numFmtId="{_DATETIME_NUMFMT_ID}" '
        f'formatCode="{_DATETIME_DISPLAY_FORMAT}"/></numFmts>',
        '<fonts count="1"><font><sz val="11"/><name val="Calibri"/>'
        '<family val="2"/></font></fonts>',
        '<fills count="2"><fill><patternFill patternType="none"/>'
        '</fill><fill><patternFill patternType="gray125"/></fill></fills>',
        '<borders count="1"><border><left/><right/><top/><bottom/>'
        '<diagonal/></border></borders>',
        '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" '
        'borderId="0"/></cellStyleXfs>',
        '<cellXfs count="4"><xf numFmtId="0" fontId="0" fillId="0" '
        'borderId="0" xfId="0"/><xf numFmtId="14" fontId="0" '
        'fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>'
        '<xf numFmtId="18" fontId="0" fillId="0" borderId="0" '
        'xfId="0" applyNumberFormat="1"/><xf numFmtId="'
        f'{_DATETIME_NUMFMT_ID}" '
        'fontId="0" fillId="0" borderId="0" xfId="0" '
        'applyNumberFormat="1"/></cellXfs>',
        '<cellStyles count="1"><cellStyle name="Normal" xfId="0" '
        'builtinId="0"/></cellStyles>',
        '<dxfs count="0"/>',
        '<tableStyles count="0" defaultTableStyle="TableStyleMedium2" '
        'defaultPivotStyle="PivotStyleLight16"/>',
        '</styleSheet>'
    ])
    return text.encode('utf-8')


def _theme_xml() -> bytes:
    """Return the standard Excel theme XML."""
    return theme_xml.encode('utf-8')


class TableIOExcelPylightxl(TableIOExcelBased):
    """TableIO reader/writer class for Excel files using pylightxl.

    The backend uses pylightxl for workbook IO and keeps the public
    spreadsheet semantics from TableIOSpreadsheetBased. Cell formatting and
    filtered ranges are ignored because pylightxl does not write those Excel
    features, but core data reads and writes, multi-sheet handling, boxed
    operations and value search are supported.
    """

    def __init__(self, file_name: PathLike, file_access: FileAccess,
                 file_exists_callback: Optional[Callable[[str], None]]
                 = None) -> None:
        """Initialize the pylightxl-backed Excel reader/writer."""
        super().__init__(file_name=file_name, file_access=file_access,
                         file_exists_callback=file_exists_callback)
        self.database: Optional[Database] = None
        self.worksheet: Optional[object] = None
        self._sheet_style_codes: dict[str, dict[str, str]] = {}

    @classmethod
    def get_description(cls) -> Descriptor:
        """Return the descriptor for the pylightxl Excel backend."""
        return Descriptor(format_name='Excel', implementation='pylightxl',
                          capabilities=cls.get_capabilities(),
                          mandatory_args=[], optional_args=[], priority=8)

    @classmethod
    def get_capabilities(cls) -> Capabilities:
        """Return the honest capabilities of the pylightxl backend."""
        return Capabilities(can_read=CAP_IMPLEMENTED,
                            can_write=CAP_IMPLEMENTED, can_fmt_row=CAP_IGNORED,
                            can_fmt_value=CAP_IGNORED,
                            filtered_data_range=CAP_IGNORED,
                            can_write_box=CAP_IMPLEMENTED,
                            can_read_box=CAP_IMPLEMENTED,
                            can_write_highlight=CAP_IGNORED,
                            multi_sheet=CAP_IMPLEMENTED,
                            can_find_value_position=CAP_IMPLEMENTED,
                            can_write_borders=CAP_IGNORED)

    def open(self) -> None:
        """Open the workbook."""
        if self.database is not None:
            raise RuntimeError(f'File {self.file_name} already open')
        if self.file_access == FileAccess.CREATE:
            database = Database()
            database.add_ws(_DEFAULT_SHEET_NAME, data={})
            database.set_emptycell(None)
        else:
            database = _read_database(self.file_name)
            if not _worksheet_names(database):
                database.add_ws(_DEFAULT_SHEET_NAME, data={})
                database.set_emptycell(None)
        self.database = database
        self.worksheet = _database_worksheet(database,
                                             _worksheet_names(database)[0])
        self._sheet_style_codes = {}
        self._initialize_sheet_style_codes()
        self._initialize_positions()

    def _initialize_sheet_style_codes(self) -> None:
        """Load compact style metadata from the open database."""
        assert self.database is not None
        style_codes = _DATE_STYLE_CODES | _TIME_STYLE_CODES | {
            _DATETIME_STYLE_CODE
        }
        for sheet_name in _worksheet_names(self.database):
            worksheet = _database_worksheet(self.database, sheet_name)
            self._sheet_style_codes[self._sheet_key(sheet_name)] = {
                address: str(cell_data.get('s', ''))
                for address, cell_data in _worksheet_cells(worksheet).items()
                if str(cell_data.get('s', '')) in style_codes
            }

    def _end_state(self) -> None:
        """Finalize in-memory state before closing."""

    def _write_file_suffix(self) -> None:
        """Write the workbook to disk when the file is writable."""
        if self.file_access == FileAccess.READ:
            return
        assert self.database is not None
        source_path = Path(self.file_name)
        temp_path = self._temporary_workbook_path(source_path)
        try:
            writexl(self.database, temp_path)
            self._rewrite_workbook_xml(temp_path)
            temp_path.replace(source_path)
        finally:
            if temp_path.exists():
                temp_path.unlink()

    def _close(self) -> None:
        """Release workbook references."""
        self.worksheet = None
        self.database = None
        self._sheet_style_codes = {}

    @staticmethod
    def _temporary_workbook_path(source_path: Path) -> Path:
        """Return a temporary workbook path that does not yet exist."""
        return temporary_output_path(source_path, '.xlsx')

    @staticmethod
    def _invalid_placeholder_cell(cell: ET.Element) -> bool:
        """Return whether one written cell is a pylightxl blank placeholder."""
        if cell.get('t') is not None:
            return False
        if cell.find('./main:f', _XML_NS) is not None:
            return False
        return _xml_text(cell.find('./main:v', _XML_NS)) == 'None'

    @staticmethod
    def _normalize_written_bool_cell(cell: ET.Element) -> bool:
        """Convert one written True/False text cell into a real bool cell."""
        if cell.get('t') is not None:
            return False
        if cell.find('./main:f', _XML_NS) is not None:
            return False
        tag_value = cell.find('./main:v', _XML_NS)
        raw_value = _xml_text(tag_value)
        if raw_value not in {'True', 'False'}:
            return False
        assert tag_value is not None
        cell.set('t', 'b')
        tag_value.text = '1' if raw_value == 'True' else '0'
        return True

    def _rewrite_workbook_xml(self, file_name: Path) -> None:
        """Clean written worksheet XML and add required workbook metadata."""
        sheet_targets = _sheet_xml_targets(str(file_name))

        def rewrite_entry(item: object, data: bytes) -> Optional[bytes]:
            """Rewrite or drop one workbook archive entry when needed."""
            file_name_text = getattr(item, 'filename')
            if file_name_text in ['xl/styles.xml', 'xl/theme/theme1.xml']:
                return None
            if file_name_text == '[Content_Types].xml':
                return self._content_types_with_required_parts(data)
            if file_name_text == 'xl/_rels/workbook.xml.rels':
                return self._workbook_rels_with_required_parts(data)
            if file_name_text.startswith('xl/worksheets/'):
                return self._worksheet_xml_for_output(file_name_text, data,
                                                      sheet_targets)
            return data
        rewrite_zip_archive(
            file_name, rewrite_entry,
            {'xl/styles.xml': _styles_xml(),
             'xl/theme/theme1.xml': _theme_xml()})

    def _content_types_with_required_parts(self, data: bytes) -> bytes:
        """Return content types XML updated with styles and theme parts."""
        root = ET.fromstring(data)
        required_parts = {
            '/xl/styles.xml': (
                'application/vnd.openxmlformats-officedocument.'
                'spreadsheetml.styles+xml'
            ),
            '/xl/theme/theme1.xml': (
                'application/vnd.openxmlformats-officedocument.theme+xml'
            )
        }
        existing_parts = {
            override.get('PartName'): override
            for override in root.findall('content:Override', _XML_NS)
            if override.get('PartName') is not None
        }
        for part_name, content_type in required_parts.items():
            override = existing_parts.get(part_name)
            if override is not None:
                override.set('ContentType', content_type)
                continue
            ET.SubElement(root, '{%s}Override' % _XML_NS['content'],
                          {'PartName': part_name,
                           'ContentType': content_type})
        return _xml_bytes(root)

    def _workbook_rels_with_required_parts(self, data: bytes) -> bytes:
        """Return workbook relations XML updated with styles and theme."""
        root = ET.fromstring(data)
        required_relationships = {
            ('http://schemas.openxmlformats.org/officeDocument/2006/'
             'relationships/styles'): 'styles.xml',
            ('http://schemas.openxmlformats.org/officeDocument/2006/'
             'relationships/theme'): 'theme/theme1.xml'
        }
        existing_relationships = {
            relationship.get('Type'): relationship
            for relationship in root.findall('rels:Relationship', _XML_NS)
            if relationship.get('Type') is not None
        }
        used_ids = {
            relationship.get('Id')
            for relationship in root.findall('rels:Relationship', _XML_NS)
            if relationship.get('Id') is not None
        }
        next_index = 1
        for relationship_type, target in required_relationships.items():
            relationship = existing_relationships.get(relationship_type)
            if relationship is not None:
                relationship.set('Target', target)
                continue
            next_id = f'rId{next_index}'
            while next_id in used_ids:
                next_index += 1
                next_id = f'rId{next_index}'
            ET.SubElement(root, '{%s}Relationship' % _XML_NS['rels'],
                          {'Id': next_id,
                           'Type': relationship_type,
                           'Target': target})
            used_ids.add(next_id)
        return _xml_bytes(root)

    def _entry_style_codes(
            self, entry_name: str,
            sheet_targets: dict[str, tuple[int, str]]) -> dict[str, str]:
        """Return the compact style codes for one worksheet archive entry."""
        for sheet_name, (_, target) in sheet_targets.items():
            if entry_name == f'xl/{target}':
                return self._sheet_style_codes.get(self._sheet_key(sheet_name),
                                                   {})
        return {}

    def _rewrite_row_xml(self, row: ET.Element,
                         style_codes: dict[str, str]) -> bool:
        """Clean one row element and apply compact cell styles."""
        changed = False
        for cell in list(row.findall('main:c', _XML_NS)):
            if self._invalid_placeholder_cell(cell):
                row.remove(cell)
                changed = True
                continue
            if self._normalize_written_bool_cell(cell):
                changed = True
            address = cell.get('r')
            if address is None:
                continue
            style_code = style_codes.get(address)
            if style_code is None:
                continue
            style_index = _style_index_for_code(style_code)
            if style_index is None:
                continue
            cell.set('s', style_index)
            changed = True
        return changed

    def _worksheet_xml_for_output(
            self, entry_name: str, data: bytes,
            sheet_targets: dict[str, tuple[int, str]]) -> bytes:
        """Return cleaned worksheet XML updated with compact style markers."""
        style_codes = self._entry_style_codes(entry_name, sheet_targets)
        root = ET.fromstring(data)
        root.set('{%s}Ignorable' % _WORKSHEET_XML_NS['mc'],
                 _IGNORABLE_PREFIXES)
        sheet_data = root.find('./main:sheetData', _XML_NS)
        if sheet_data is None:
            return _xml_bytes(root)
        changed = False
        for row in list(sheet_data.findall('main:row', _XML_NS)):
            changed = self._rewrite_row_xml(row, style_codes) or changed
            if not row.findall('main:c', _XML_NS):
                sheet_data.remove(row)
                changed = True
        return _xml_bytes(root)

    def _current_style_codes(self) -> dict[str, str]:
        """Return the compact style map for the current sheet."""
        key = self._current_sheet_key()
        if key not in self._sheet_style_codes:
            self._sheet_style_codes[key] = {}
        return self._sheet_style_codes[key]

    def _list_sheets(self) -> list[str]:
        """List the sheets in the workbook."""
        assert self.database is not None
        return _worksheet_names(self.database)

    def _select_sheet(self, sheet_name: str, create: bool = False) -> None:
        """Select one workbook sheet, optionally creating it."""
        assert self.database is not None
        matched_name = self._find_matching_sheet_name(
            _worksheet_names(self.database), sheet_name)
        if matched_name is None:
            if not create:
                raise KeyError(sheet_name)
            self._check_file_is_writable()
            self.database.add_ws(sheet_name, data={})
            matched_name = sheet_name
        self._save_current_sheet_state()
        self.worksheet = _database_worksheet(self.database, matched_name)
        self._current_style_codes()
        self._load_current_sheet_state()

    def _current_sheet_name(self) -> str:
        """Return the name of the selected worksheet."""
        assert self.database is not None
        assert self.worksheet is not None
        for sheet_name in _worksheet_names(self.database):
            if _database_worksheet(self.database,
                                   sheet_name) is self.worksheet:
                return sheet_name
        return _worksheet_names(self.database)[0]

    def _read_sheet(self) -> object:
        """Return the readable worksheet."""
        assert self.worksheet is not None
        return self.worksheet

    def _write_sheet(self) -> object:
        """Return the writable worksheet."""
        assert self.worksheet is not None
        return self.worksheet

    def _write_value_to_sheet(self, sheet: object, row: int, column: int,
                              value: object) -> None:
        """Write one value to one worksheet cell."""
        worksheet = cast(_WorksheetLike, sheet)
        address = self._excel_cell_ref(row, column)
        style_codes = self._current_style_codes()
        style_codes.pop(address, None)
        if value is None:
            _worksheet_cells(worksheet).pop(address, None)
            _recalculate_worksheet_size(worksheet)
            return
        write_value = value
        if isinstance(value, datetime):
            write_value = _datetime_to_excel_number(value)
            style_codes[address] = _DATETIME_STYLE_CODE
        worksheet.update_address(address, write_value)
        if address in _worksheet_cells(worksheet):
            _worksheet_cells(worksheet)[address]['s'] = \
                style_codes.get(address, '')

    def _set_cell_format(self, sheet: object, row: int, column: int,
                         fmt: Optional[Fmt]) -> None:
        """Ignore cell formatting because pylightxl cannot write it."""
        _ = sheet
        _ = row
        _ = column
        _ = fmt

    def _apply_heading_style(self, row: int, column: int, level: int) -> None:
        """Ignore heading styling because pylightxl cannot write it."""
        _ = row
        _ = column
        _ = level

    def _last_used_row(self, sheet: object) -> int:
        """Return the last used row index on a worksheet."""
        worksheet = cast(_WorksheetLike, sheet)
        worksheet_cells = _worksheet_cells(worksheet)
        if not worksheet_cells:
            return -1
        return max(cast(tuple[int, int],
                        pylightxl_impl.utility_address2index(address))[0] - 1
                   for address in worksheet_cells)

    def _last_used_column(self, sheet: object) -> int:
        """Return the last used column index on a worksheet."""
        worksheet = cast(_WorksheetLike, sheet)
        worksheet_cells = _worksheet_cells(worksheet)
        if not worksheet_cells:
            return -1
        return max(cast(tuple[int, int],
                        pylightxl_impl.utility_address2index(address))[1] - 1
                   for address in worksheet_cells)

    def _cell_value(self, sheet: object, row: int, column: int) -> Value:
        """Return one worksheet cell as a public Value."""
        worksheet = cast(_WorksheetLike, sheet)
        address = self._excel_cell_ref(row, column)
        cell_data = _worksheet_cells(worksheet).get(address)
        if cell_data is None:
            return None
        value = cell_data.get('v')
        formula = cell_data.get('f', '')
        style_code = str(cell_data.get('s', ''))
        if formula != '' and value == '':
            return None
        return self._parse_typed_cell_value(value, style_code)

    @classmethod
    def _parse_typed_cell_value(cls, value: object, style_code: str) -> Value:
        """Convert one stored pylightxl cell value to the public Value type."""
        if style_code in _DATE_STYLE_CODES and isinstance(value, str):
            return datetime.strptime(value, '%Y/%m/%d')
        if style_code in _DATE_STYLE_CODES and isinstance(value, (int, float)):
            date_value = _datetime_from_excel_number(value)
            return datetime(date_value.year, date_value.month, date_value.day)
        if style_code in _TIME_STYLE_CODES and isinstance(value, (int, float)):
            time_value = _datetime_from_excel_number(value)
            return time_value.strftime('%H:%M:%S')
        if style_code == _DATETIME_STYLE_CODE and isinstance(value, str):
            return datetime.strptime(value, '%Y/%m/%d %H:%M:%S')
        if style_code == _DATETIME_STYLE_CODE and \
                isinstance(value, (int, float)):
            return _datetime_from_excel_number(value)
        return cls._python_value_from_spreadsheet(value)

    def _filtered_range_infos(self) -> list[tuple[str, tuple[int, int,
                                                             int, int]]]:
        """Return no filtered ranges because pylightxl ignores them."""
        return []

    def _delete_filtered_range(self, name: str) -> None:
        """Ignore filtered-range deletion because none are written."""
        _ = name

    def _add_filtered_range(self, bounds: tuple[int, int, int, int],
                            name: str) -> None:
        """Ignore filtered-range requests.

        pylightxl cannot write Excel filtered ranges.
        """
        _ = bounds
        _ = name

    def _set_column_width_if_wider(self, column: int, width: float) -> None:
        """Ignore width updates because pylightxl cannot write them."""
        _ = column
        _ = width
