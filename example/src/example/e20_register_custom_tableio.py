#! /usr/bin/env python3
"""Show how user code can register a custom TableIO class."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import csv
import io
from typing import Callable, Literal, Optional, Sequence
from mformat.mformat import PathLike
from tableio import CAP_NEEDED, CAP_NOT_USED, Box, Capabilities, CellT, \
    CsvDialect, DictData, DictDataMap, FileAccess, FmtDictData, \
    FmtListData, ListData, ListDataSeq, OptionalArgs, Position, \
    ReadResult, Value, create_tableio
from tableio.capability import CAP_IMPLEMENTED, CAP_IGNORED, \
    CAP_UNSUPPORTED, CapabilityNotSupported
from tableio.factory import register_tableio
from tableio.tableio import Descriptor
from tableio.tableio_textbased import TableIOTextBased
from tableio.value_type import row_strip_format_dict, \
    row_strip_format_list, strip_format_dict, strip_format_list
from .cmd_for_examples import cmd_parse_and_run_example
from .write_writer_info import write_writer_info


CUSTOM_FORMAT_NAME = 'LineNumberedCSV'
CUSTOM_IMPLEMENTATION_NAME = 'user_line_numbered_csv'

CAPS = Capabilities(can_write=CAP_NEEDED, can_read=CAP_NEEDED,
                    can_fmt_row=CAP_NOT_USED, can_fmt_value=CAP_NOT_USED,
                    filtered_data_range=CAP_NOT_USED,
                    can_write_box=CAP_NOT_USED, can_read_box=CAP_NOT_USED,
                    can_write_highlight=CAP_NOT_USED, multi_sheet=CAP_NOT_USED,
                    can_find_value_position=CAP_NOT_USED)


def _is_heading_payload(payload: str) -> bool:
    """Return whether one payload line should be interpreted as a heading."""
    if not payload.startswith('#'):
        return False
    rest = payload.lstrip('#')
    return bool(rest) and rest[0] == ' '


def _csv_quoting_value(csv_quoting: str) -> Literal[0, 1, 2, 3, 4, 5]:
    """Convert a string like 'minimal' to the matching csv constant."""
    quoting_name = csv_quoting.lower()
    if quoting_name == 'all':
        return csv.QUOTE_ALL
    if quoting_name == 'minimal':
        return csv.QUOTE_MINIMAL
    if quoting_name == 'nonnumeric':
        return csv.QUOTE_NONNUMERIC
    if quoting_name == 'none':
        return csv.QUOTE_NONE
    if quoting_name == 'strings':
        return csv.QUOTE_STRINGS
    if quoting_name == 'notnull':
        return csv.QUOTE_NOTNULL
    allowed = 'all, minimal, nonnumeric, none, strings, notnull'
    msg = f'Unknown csv_quoting value {csv_quoting!r}. '
    msg += f'Allowed values: {allowed}'
    raise ValueError(msg)


class LineNumberedCsvTableIO(TableIOTextBased):
    """Example backend implemented in user code.

    The important teaching point is that this class is not part of the
    tableio package itself. It lives in an ordinary example script, just like
    user application code would.

    Most example programs in this directory import common public names
    directly from tableio. This example is different on purpose: a custom
    backend needs some lower-level implementation helpers that stay in
    submodules because they are not part of the beginner-facing public API.

    The class derives from TableIOTextBased instead of directly from TableIO.
    That is still a valid TableIO subclass, but it lets the example reuse the
    standard text-file open and close logic so the focus can stay on the
    hooks a custom backend needs to implement.
    """

    def __init__(self,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                 file_name: PathLike, file_access: FileAccess,
                 file_exists_callback: Optional[Callable[[str], None]]
                 = None,
                 character_encoding: str = 'utf-8',
                 csv_dialect: CsvDialect = CsvDialect.UNIX,
                 csv_delimiter: Optional[str] = None,
                 csv_quoting: Optional[str] = None,
                 csv_quotechar: Optional[str] = None,
                 csv_lineterminator: Optional[str] = None,
                 csv_escapechar: Optional[str] = None):
        """Initialize the user-defined backend.

        A user-defined TableIO class can choose whichever constructor
        arguments make sense for its own format. The factory will pass the
        normal file_name and file_access arguments, plus whichever optional
        arguments were declared in get_description().
        """
        super().__init__(file_name=file_name, file_access=file_access,
                         file_exists_callback=file_exists_callback,
                         character_encoding=character_encoding)
        if csv_dialect == CsvDialect.UNIX:
            dialect: csv.Dialect = csv.unix_dialect()
        else:
            dialect = csv.excel()
        if csv_delimiter is not None:
            dialect.delimiter = csv_delimiter
        if csv_quoting is not None:
            dialect.quoting = _csv_quoting_value(csv_quoting)
        if csv_quotechar is not None:
            dialect.quotechar = csv_quotechar
        if csv_lineterminator is not None:
            dialect.lineterminator = csv_lineterminator
        if csv_escapechar is not None:
            dialect.escapechar = csv_escapechar
        self.csv_dialect = dialect
        self.position_row: int = -1
        self.position_column: int = 0
        self._next_write_line_number: int = 1
        self._next_read_line_number: int = 1
        self._last_payload_line_empty: bool = False

    @classmethod
    def file_name_extension(cls) -> str:
        """Return the file extension used by this custom format."""
        return 'lncsv'

    @classmethod
    def get_description(cls) -> Descriptor:
        """Describe the custom format for the factory.

        This metadata is what makes the class visible through the factory.
        The format name is what the caller passes to create_tableio().
        The implementation name distinguishes this backend from other
        possible implementations of the same format.
        """
        optional_args = [
            'file_exists_callback', 'character_encoding', 'csv_dialect',
            'csv_delimiter', 'csv_quoting', 'csv_quotechar',
            'csv_lineterminator', 'csv_escapechar'
        ]
        return Descriptor(format_name=CUSTOM_FORMAT_NAME,
                          implementation=CUSTOM_IMPLEMENTATION_NAME,
                          capabilities=cls.get_capabilities(),
                          mandatory_args=[], optional_args=optional_args)

    @classmethod
    def get_capabilities(cls) -> Capabilities:
        """Describe what this example backend can and cannot do.

        A custom TableIO class should be honest here. These capability values
        are how the factory knows whether the backend fits a caller's
        request.
        """
        return Capabilities(can_write=CAP_IMPLEMENTED,
                            can_read=CAP_IMPLEMENTED, can_fmt_row=CAP_IGNORED,
                            can_fmt_value=CAP_IGNORED,
                            filtered_data_range=CAP_IGNORED,
                            can_write_box=CAP_UNSUPPORTED,
                            can_read_box=CAP_UNSUPPORTED,
                            can_write_highlight=CAP_IGNORED,
                            multi_sheet=CAP_UNSUPPORTED,
                            can_find_value_position=CAP_UNSUPPORTED)

    def _end_state(self) -> None:
        """Finish any buffered state before closing the file."""

    def _write_file_suffix(self) -> None:
        """Write any trailing file content before closing the file."""

    def _write_numbered_payload_line(self, payload: str) -> None:
        """Write one physical line with the custom line-number prefix."""
        assert self.file is not None
        if self._next_write_line_number > 99999:
            msg = 'LineNumberedCSV supports at most 99999 physical lines.'
            raise ValueError(msg)
        self.file.write(f'{self._next_write_line_number:05d}:{payload}\n')
        self._next_write_line_number += 1
        self._last_payload_line_empty = payload == ''
        self.position_row += 1

    def _ensure_empty_payload_line_before(self) -> None:
        """Insert one empty payload line when CSV-style separation is needed.

        The built-in CSV backend uses empty lines to separate headings and
        tables. This custom backend keeps the same idea, but every physical
        line in the file must still carry the 5-digit number prefix.
        """
        if self.position_row < 0 or self._last_payload_line_empty:
            return
        self._write_numbered_payload_line('')

    def _csv_line_from_row(self, row: Sequence[Value]) -> str:
        """Encode one row as one CSV payload line.

        The example format numbers physical lines, so one logical CSV row
        must fit on one physical line. To keep the example small and easy to
        understand, values that would make the CSV module emit embedded
        newlines are rejected.
        """
        buffer = io.StringIO()
        writer = csv.writer(buffer, dialect=self.csv_dialect)
        writer.writerow(row)
        payload = buffer.getvalue().rstrip('\r\n')
        if '\n' in payload or '\r' in payload:
            msg = 'LineNumberedCSV does not support embedded newlines in '
            msg += 'cell values.'
            raise ValueError(msg)
        return payload

    def _read_payload_line(self, numbered_line: str) -> str:
        """Validate one numbered line and return the payload part."""
        stripped_line = numbered_line.rstrip('\r\n')
        if len(stripped_line) < 6:
            msg = f'Invalid LineNumberedCSV line: {numbered_line!r}'
            raise ValueError(msg)
        if stripped_line[5] != ':' or not stripped_line[:5].isdigit():
            msg = f'Invalid LineNumberedCSV prefix: {numbered_line!r}'
            raise ValueError(msg)
        line_number = int(stripped_line[:5])
        if line_number != self._next_read_line_number:
            msg = 'Unexpected line number '
            msg += f'{line_number:05d}, expected '
            msg += f'{self._next_read_line_number:05d}.'
            raise ValueError(msg)
        self._next_read_line_number += 1
        self.position_row += 1
        payload = stripped_line[6:]
        self._last_payload_line_empty = payload == ''
        return payload

    def _read_raw_section(self) -> tuple[list[str], list[str]]:
        """Read one heading-and-table section from current file position."""
        assert self.file is not None
        headings: list[str] = []
        data_lines: list[str] = []
        in_data = False
        for numbered_line in self.file:
            payload = self._read_payload_line(numbered_line)
            if not payload:
                if in_data:
                    break
                continue
            if _is_heading_payload(payload) and not in_data:
                headings.append(payload.lstrip('#').strip())
                continue
            in_data = True
            data_lines.append(payload)
        return headings, data_lines

    def _read_csv_rows(self, box: Optional[Box]) -> tuple[list[str],
                                                          ListData[Value]]:
        """Read headings plus plain CSV rows from current position."""
        if box is not None:
            raise CapabilityNotSupported('read from a box')
        headings, data_lines = self._read_raw_section()
        if not data_lines:
            return headings, []
        rows: ListData[Value] = [
            list(row) for row in
            csv.reader(data_lines, dialect=self.csv_dialect)
        ]
        self.position_column = len(rows[-1])
        return headings, rows

    def _write_heading(self, heading: str, level: int) -> Position:
        """Write a heading using the same convention as the CSV backend."""
        self._ensure_empty_payload_line_before()
        self._write_numbered_payload_line(f'{"#" * level} {heading}')
        self._write_numbered_payload_line('')
        self.position_column = 0
        return Position(row=self.position_row, column=self.position_column)

    def _write_table_listdata(self, data: ListDataSeq[CellT],
                              impl_meta: TableIOTextBased.ImplMetaForWrite
                              ) -> Position:
        """Write list-shaped table data using numbered CSV lines."""
        if impl_meta.box is not None:
            raise CapabilityNotSupported('write to a box')
        self._ensure_empty_payload_line_before()
        plain_data = strip_format_list(data)
        for row in plain_data:
            self._write_numbered_payload_line(self._csv_line_from_row(row))
        self.position_column = len(plain_data[-1])
        self._ensure_empty_payload_line_before()
        return Position(row=self.position_row, column=self.position_column)

    def _write_table_fmtlistdata(
            self, data: FmtListData,
            impl_meta: TableIOTextBased.ImplMetaForWrite) -> Position:
        """Write row-formatted list data while ignoring the formatting."""
        return self._write_table_listdata(row_strip_format_list(data),
                                          impl_meta)

    def _write_table_dictdata(
            self, data: DictDataMap[CellT],
            impl_meta: TableIOTextBased.ImplMetaForDictWrite) -> Position:
        """Write dict-shaped table data with a header row first."""
        if impl_meta.common_impl.box is not None:
            raise CapabilityNotSupported('write to a box')
        self._ensure_empty_payload_line_before()
        plain_data = strip_format_dict(data)
        self._write_numbered_payload_line(
            self._csv_line_from_row(impl_meta.column_order))
        for row in plain_data:
            ordered_row = [row[column_name]
                           for column_name in impl_meta.column_order]
            self._write_numbered_payload_line(
                self._csv_line_from_row(ordered_row))
        self.position_column = len(impl_meta.column_order)
        self._ensure_empty_payload_line_before()
        return Position(row=self.position_row, column=self.position_column)

    def _write_table_fmtdictdata(
            self, data: FmtDictData,
            impl_meta: TableIOTextBased.ImplMetaForDictWrite) -> Position:
        """Write row-formatted dict data while ignoring the formatting."""
        return self._write_table_dictdata(row_strip_format_dict(data),
                                          impl_meta)

    def _read_table_listdata(self, box: Optional[Box] = None) \
            -> ReadResult[ListData[Value]]:
        """Read one list-shaped table from the numbered CSV file."""
        headings, rows = self._read_csv_rows(box)
        if not rows:
            return ReadResult(data=[], headings=headings,
                              last_read_row=self.position_row)
        return ReadResult(data=rows, headings=headings,
                          last_read_row=self.position_row)

    def _read_table_dictdata(self, box: Optional[Box] = None) \
            -> ReadResult[DictData[Value]]:
        """Read one dict-shaped table from the numbered CSV file."""
        headings, rows = self._read_csv_rows(box)
        if not rows:
            return ReadResult(data=[], headings=headings,
                              last_read_row=self.position_row)
        column_names = [
            value if isinstance(value, str) else ''
            for value in rows[0]
        ]
        data: DictData[Value] = [
            dict(zip(column_names, row, strict=False))
            for row in rows[1:]
        ]
        self.position_column = len(column_names)
        return ReadResult(data=data, headings=headings,
                          last_read_row=self.position_row)


def e20_register_custom_tableio(format_name: str, output_file_name: str,
                                implementation_name: Optional[str],
                                optional_args: OptionalArgs) -> int:
    """Write and read a file using a custom TableIO class.

    The body of the example intentionally looks very similar to e01.
    That similarity is part of the lesson: once a custom backend has been
    registered, the rest of the program can use the ordinary factory API.
    """
    heading1 = 'A user-defined TableIO class was registered with the factory.'
    heading2 = 'Each physical line in this format starts with 00001: style.'
    data: ListData[Value] = [
        ['Step', 'What happens'],
        ['1', 'User code defines a TableIO-derived class'],
        ['2', 'User code registers that class with register_tableio()'],
        ['3', 'The factory can now create the custom backend']
    ]
    writer = create_tableio(format_name=format_name,
                            file_name=output_file_name,
                            file_access=FileAccess.CREATE,
                            implementation=implementation_name,
                            capabilities=CAPS, args=optional_args)
    with writer as tableio:
        #
        # The important point here is that this code uses the same factory
        # call as the earlier examples. The custom format is now just one more
        # format known by the factory, beside the formats that tableio
        # registered itself.
        #
        tableio.write_heading(heading1)
        tableio.write_heading(heading2)
        tableio.write_table_listdata(data)
        #
        # Write extra information after the demo table so that a programmer
        # opening the generated file can see exactly which backend the
        # factory selected for this run.
        #
        tableio.write_heading('Writer information:')
        write_writer_info(tableio, requested_format_name=format_name,
                          requested_implementation=implementation_name)
    reader = create_tableio(format_name=format_name,
                            file_name=output_file_name,
                            file_access=FileAccess.READ,
                            implementation=implementation_name,
                            capabilities=CAPS, args=optional_args)
    with reader as tableio:
        read_back = tableio.read_table_listdata()
    assert read_back.headings == [heading1, heading2]
    assert read_back.data == data
    return 0


if __name__ == '__main__':
    #
    # The custom backend is registered here on purpose.
    #
    # This example wants to show that registration does not have to happen as
    # module-load side effect code. Ordinary runtime code is enough.
    #
    # register_tableio() takes the class object, not an instance.
    # After this call, create_tableio() can select the custom format in the
    # same way as it selects the predefined formats from the package.
    #
    # We do the registration before the shared command-line parsing because
    # cmd_parse_and_run_example() asks the factory which format names are
    # available for the -f argument.
    #
    register_tableio(LineNumberedCsvTableIO)
    cmd_parse_and_run_example(example_name='e20_register_custom_tableio',
                              func=e20_register_custom_tableio, caps=CAPS)
