#! /usr/bin/env python3
"""Reader/writer for CSV files."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import csv
import io
from itertools import chain
from typing import Literal, Optional, Callable, NamedTuple, Iterator
from mformat.mformat import PathLike
from tableio.tableio import FileAccess, Descriptor, Position, Box, TableIO
from tableio.value_type import Value, ListData, ListDataSeq, CellT, \
    FmtListData, FmtDictData, DictData, DictDataMap, \
    row_strip_format_list, row_strip_format_dict, \
    strip_format_list, strip_format_dict, ReadResult
from tableio.capability import Capabilities, SingleCapability, Strictness, \
    CapabilityNotSupported
from tableio.tableio_textbased import TableIOTextBased
from tableio.optional_args import CsvDialect, TimeDeltaFallback
from tableio.timedelta_helpers import fallback_value


type _QuoteStyle = Literal[0, 1, 2, 3, 4, 5]

_QUOTING_MAP: dict[str, _QuoteStyle] = {
    'all': csv.QUOTE_ALL,
    'minimal': csv.QUOTE_MINIMAL,
    'nonnumeric': csv.QUOTE_NONNUMERIC,
    'none': csv.QUOTE_NONE,
    'strings': csv.QUOTE_STRINGS,
    'notnull': csv.QUOTE_NOTNULL,
}


def _validate_quoting(quoting: str) -> _QuoteStyle:
    """Validate and convert a quoting string to a csv constant.

    Args:
        quoting: The quoting style string. Case-insensitive.
    Returns:
        The corresponding csv.QUOTE_* constant.
    Raises:
        ValueError: If the quoting string is not recognized.
    """
    lower = quoting.lower()
    if lower not in _QUOTING_MAP:
        allowed = ', '.join(sorted(_QUOTING_MAP))
        raise ValueError(
            f'Unknown quoting style: {quoting!r}. '
            f'Allowed values: {allowed}')
    return _QUOTING_MAP[lower]


class CsvDefinitions(NamedTuple):
    """Definitions of the CSV file format."""

    type: CsvDialect
    """The type of CSV file to write."""
    delimiter: Optional[str]
    """The delimiter to use for CSV files."""
    quoting: Optional[str]
    """The quoting style to use for CSV files.

    Allowed values (case-insensitive): 'all', 'minimal',
    'nonnumeric', 'none', 'strings', 'notnull'."""
    quotechar: Optional[str]
    """The quote character to use for CSV files."""
    lineterminator: Optional[str]
    """The line terminator to use for CSV files."""
    escapechar: Optional[str]
    """The escape character to use for CSV files."""


def _get_csv_dialect_type(csv_dialect: CsvDialect) -> type[csv.Dialect]:
    """Get the CSV dialect class from the CSV dialect enum."""
    if csv_dialect == CsvDialect.UNIX:
        return csv.unix_dialect
    if csv_dialect == CsvDialect.EXCEL:
        return csv.excel
    # pylint: disable=unreachable
    raise KeyError(f'Unknown CSV dialect: {csv_dialect}')


def _get_csv_dialect(csv_definitions: CsvDefinitions) -> csv.Dialect:
    """Get a CSV dialect instance from the CSV definitions."""
    dialect_type = _get_csv_dialect_type(csv_definitions.type)
    dialect = dialect_type()
    if csv_definitions.delimiter is not None:
        dialect.delimiter = csv_definitions.delimiter
    if csv_definitions.quoting is not None:
        quoting = _validate_quoting(csv_definitions.quoting)
        dialect.quoting = quoting
    if csv_definitions.quotechar is not None:
        dialect.quotechar = csv_definitions.quotechar
    if csv_definitions.lineterminator is not None:
        dialect.lineterminator = csv_definitions.lineterminator
    if csv_definitions.escapechar is not None:
        dialect.escapechar = csv_definitions.escapechar
    return dialect


def _is_heading_line(line: str) -> bool:
    """Check if a line (without line terminator) is a heading.

    A heading line starts with one or more '#' characters
    followed by a space. This matches the format produced by
    _write_heading and avoids false positives for values like
    a hexadecimal color code with a leading hash that starts
    with '#' but has no space after it.
    """
    if not line.startswith('#'):
        return False
    rest = line.lstrip('#')
    return len(rest) > 0 and rest[0] == ' '


class TableIOCsv(TableIOTextBased):
    """Reader/writer for CSV files.

    This is a TableIO reader/writer class for Comma Separated Value (CSV)
    files.
    A strict CSV file format includes only one table of data in a file.
    This means that on each row there is a list of values, that are usually
    read into a list of lists, or into a list of dicts using the values on
    the first line as the keys.
    This class adds extensions to the CSV format to support several tables in
    a file (separated by empty lines), and optional headings (lines starting
    with #) before each table.
    Tables and headings are always written at the end of the file (also in
    UPDATE mode), as text in the middle of a file cannot be replaced.
    Reading starts at the beginning of the file and continues after the
    previous read, independent of any writes.
    Notice: For best compatibility with other software use the strict CSV
    format by only writing a single table in a file and not using headings.
    """

    newline_mode: Optional[str] = ''
    """Open without newline translation, as required by the csv module."""

    def __init__(self,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                 file_name: PathLike, file_access: FileAccess,
                 file_exists_callback: Optional[Callable[[str], None]] = None,
                 character_encoding: str = 'utf-8',
                 csv_dialect: CsvDialect = CsvDialect.UNIX,
                 csv_delimiter: Optional[str] = None,
                 csv_quoting: Optional[str] = None,
                 csv_quotechar: Optional[str] = None,
                 csv_lineterminator: Optional[str] = None,
                 csv_escapechar: Optional[str] = None,
                 timedelta_fallback: Optional[TimeDeltaFallback] = None):
        """Initialize the TableIOCsv reader/writer class.

        CSV has no native timedelta type, so timedelta values are written
        as specified by timedelta_fallback (None for default
        TimeDeltaFallback.HMS_STRING). When reading, such values are
        returned as strings, use ``tableio.parse_timedelta`` to convert them.
        """
        super().__init__(file_name=file_name, file_access=file_access,
                         file_exists_callback=file_exists_callback,
                         character_encoding=character_encoding)
        self.csv_definitions: CsvDefinitions = \
            CsvDefinitions(type=csv_dialect, delimiter=csv_delimiter,
                           quoting=csv_quoting, quotechar=csv_quotechar,
                           lineterminator=csv_lineterminator,
                           escapechar=csv_escapechar)
        self.csv_dialect: csv.Dialect = _get_csv_dialect(self.csv_definitions)
        self.timedelta_fallback: Optional[TimeDeltaFallback] = \
            timedelta_fallback
        self.position_row: int = -1
        self.position_column: int = 0
        self.read_row: int = -1
        self._read_offset: int = 0

    def open(self) -> None:
        """Open the file.

        In UPDATE mode the write position is after the existing lines.
        Avoid using this method directly.
        Use derived class as a context manager instead, using a with statement.
        """
        super().open()
        self.read_row = -1
        self._read_offset = 0
        if self.file_access == FileAccess.UPDATE:
            self.position_row = self._count_lines() - 1

    def _count_lines(self) -> int:
        """Return the number of lines in the file."""
        assert self.file is not None
        self.file.seek(0, io.SEEK_SET)
        return sum(1 for _ in iter(self.file.readline, ''))

    def _line_end(self) -> str:
        """Return the line terminator of the CSV dialect."""
        return self.csv_dialect.lineterminator

    def _seek_write_position(self) -> None:
        """Move the file pointer to the end of the file for writing."""
        assert self.file is not None
        self.file.seek(0, io.SEEK_END)

    @classmethod
    def file_name_extension(cls) -> str:
        """Return the file name extension for CSV files."""
        return 'csv'

    @classmethod
    def get_description(cls) -> Descriptor:
        """Get the description of the TableIOCsv reader/writer class."""
        opts = ['file_exists_callback', 'character_encoding', 'csv_dialect',
                'csv_delimiter', 'csv_quoting', 'csv_quotechar',
                'csv_lineterminator', 'csv_escapechar', 'timedelta_fallback']
        return Descriptor(format_name='CSV', implementation='csv',
                          mandatory_args=[],
                          capabilities=cls.get_capabilities(),
                          optional_args=opts)

    @classmethod
    def get_capabilities(cls) -> Capabilities:
        """Return the capabilities of the TableIOCsv reader/writer class."""
        not_sup_ignore = SingleCapability(supported=False,
                                          strictness=Strictness.IGNORE)
        not_sup_strict = SingleCapability(supported=False,
                                          strictness=Strictness.STRICT)
        return Capabilities(can_write=SingleCapability(supported=True),
                            can_read=SingleCapability(supported=True),
                            can_fmt_row=not_sup_ignore,
                            can_fmt_value=not_sup_ignore,
                            filtered_data_range=not_sup_ignore,
                            can_write_box=not_sup_strict,
                            can_read_box=not_sup_strict,
                            can_write_highlight=not_sup_ignore,
                            can_write_borders=not_sup_ignore)

    def _end_state(self) -> None:
        """End the state of the CSV file."""

    def _write_file_suffix(self) -> None:
        """Write the CSV file suffix."""

    def _csv_value(self, value: Value) -> Value:
        """Return one value as written to CSV (timedelta as fallback)."""
        return fallback_value(value, self.timedelta_fallback)

    def _write_heading(self, heading: str, level: int) -> Position:
        """Write a heading to the file.

        A heading is a line starting with one or more '#' characters.
        The heading is preceded by an empty line and is followed by an
        empty line.
        Args:
            heading: The heading text to write.
            level: The level of the heading. 1 = highest, 3 = lowest.
                   If level is None and it is first heading, level 1 is used.
                   If level is None and it is not first heading,
                   level 2 is used.
        Raises:
            ValueError: If level is outside the range 1 to 3.
        Returns:
            The position of the last cell written.
        """
        assert self.file is not None
        self._seek_write_position()
        self.position_row += self._ensure_empty_line_before()
        line_end = self._line_end()
        self.file.write(f'{"#" * level} {heading}{line_end}{line_end}')
        self.position_row += 2
        self.position_column = 0
        return Position(row=self.position_row, column=self.position_column)

    def _write_table_listdata(self, data: ListDataSeq[CellT],
                              impl_meta: TableIO.ImplMetaForWrite) -> Position:
        """Write a table of list data to the file.

        Write a table of list data to the file.
        CSV does not support the box, nor formatting, nor filtered data range.
        Args:
            data: The list data to write.
            impl_meta: The implementation meta data.
        Raises:
            CapabilityNotSupported: If box is provided.
        Returns:
            The position of the last cell written.
        """
        assert self.file is not None
        if impl_meta.box is not None:
            err = 'Box is not allowed in CSV.'
            raise CapabilityNotSupported(err)
        ndata = strip_format_list(data)
        self._seek_write_position()
        self.position_row += self._ensure_empty_line_before()
        writer = csv.writer(self.file, dialect=self.csv_dialect)
        for row in ndata:
            writer.writerow([self._csv_value(value) for value in row])
        self.position_row += len(ndata)
        self.position_column = len(ndata[-1])
        self.position_row += self._ensure_empty_line_before()
        return Position(row=self.position_row, column=self.position_column)

    def _write_table_fmtlistdata(
            self, data: FmtListData,
            impl_meta: TableIO.ImplMetaForWrite) -> Position:
        """Write a table of list data to the file.

        Write a table of list data to the file.
        CSV does not support the box, nor formatting, nor filtered data range.
        Args:
            data: The list data to write.
            impl_meta: The implementation meta data.
        Raises:
            CapabilityNotSupported: If impl_meta.box is provided.
        Returns:
            The position of the last cell written. Not reliable.
        """
        ndata: ListDataSeq[Value] = row_strip_format_list(data)
        return self._write_table_listdata(ndata, impl_meta)

    def _write_table_dictdata(
            self, data: DictDataMap[CellT],
            impl_meta: TableIO.ImplMetaForDictWrite) -> Position:
        """Write a table of dict data to the file.

        Write a table of dict data to the file.
        CSV does not support the box, nor formatting, nor filtered data range.
        Args:
            data: The dict data to write.
            impl_meta: The implementation meta data.
        Raises:
            CapabilityNotSupported: If impl_meta.common_impl.box is provided.
        Returns:
            The position of the last cell written.
        """
        assert self.file is not None
        if impl_meta.common_impl.box is not None:
            err = 'Box is not allowed in CSV.'
            raise CapabilityNotSupported(err)
        self._seek_write_position()
        self.position_row += self._ensure_empty_line_before()
        ndata: DictDataMap[Value] = strip_format_dict(data)
        writer = csv.DictWriter(self.file, fieldnames=impl_meta.column_order,
                                dialect=self.csv_dialect)
        writer.writeheader()
        self.position_row += 1
        for row in ndata:
            writer.writerow({key: self._csv_value(value)
                             for key, value in row.items()})
        self.position_row += len(ndata)
        self.position_column = len(ndata[-1])
        self.position_row += self._ensure_empty_line_before()
        return Position(row=self.position_row, column=self.position_column)

    def _write_table_fmtdictdata(
            self, data: FmtDictData,
            impl_meta: TableIO.ImplMetaForDictWrite) -> Position:
        """Write a table of dict data to the file.

        Write a table of dict data to the file.
        CSV does not support the box, nor formatting, nor filtered data range.
        Args:
            data: The dict data to write.
            impl_meta: The implementation meta data.
        Raises:
            CapabilityNotSupported: If impl_meta.common_impl.box is provided.
        Returns:
            The position of the last cell written.
        """
        ndata: DictDataMap[Value] = row_strip_format_dict(data)
        return self._write_table_dictdata(ndata, impl_meta=impl_meta)

    def _read_line(self) -> str:
        """Read one physical line (with line end) and count it."""
        assert self.file is not None
        line = self.file.readline()
        if line:
            self.read_row += 1
        return line

    def _read_record_lines(self, first_line: str) -> list[str]:
        """Return the physical lines of the CSV record starting first_line.

        The csv reader requests continuation lines only while a quoted
        value is open, so line breaks inside quoted values are kept.
        """
        lines = [first_line]

        def continuation_lines() -> Iterator[str]:
            """Yield and record the lines following first_line."""
            for line in iter(self._read_line, ''):
                lines.append(line)
                yield line

        next(csv.reader(chain([first_line], continuation_lines()),
                        dialect=self.csv_dialect), None)
        return lines

    def _read_raw_sections(self) -> tuple[list[str], list[str]]:
        """Read heading and data lines from the current read position.

        Skips leading empty lines. Lines matching the heading
        pattern (one or more '#' followed by a space) that appear
        before the first data line are collected as headings with
        the leading '#' characters and space stripped. Data lines
        (with line ends, a quoted value may span several lines) are
        collected until an empty line or end of file.
        Returns:
            A tuple of (headings, data_lines).
        """
        assert self.file is not None
        self.file.seek(self._read_offset, io.SEEK_SET)
        headings: list[str] = []
        data_lines: list[str] = []
        for line in iter(self._read_line, ''):
            stripped = line.rstrip('\r\n')
            if not stripped:
                if data_lines:
                    break
                continue
            if _is_heading_line(stripped) and not data_lines:
                headings.append(stripped.lstrip('#').strip())
                continue
            data_lines.extend(self._read_record_lines(line))
        self._read_offset = self.file.tell()
        return headings, data_lines

    def _read_table_listdata(self, box: Optional[Box] = None) \
            -> ReadResult[ListData[Value]]:
        """Read a table of list data from the file.

        Read a table from the file. The table is read into a list of
        lists. Empty lines before the table are ignored. Lines
        starting with '#' followed by a space are read as headings.
        The first non-empty line not matching the heading pattern is
        the first row of the table. Reading stops when an empty line
        is encountered or the end of the file is reached.
        CSV does not support reading from a box.
        Args:
            box: Not allowed in CSV.
        Raises:
            CapabilityNotSupported: If box is provided.
        Returns:
            The data as a list of lists, and any headings found
            before the table.
        """
        assert self.file is not None
        if box is not None:
            err = 'Box is not allowed in CSV.'
            raise CapabilityNotSupported(err)
        headings, data_lines = self._read_raw_sections()
        if not data_lines:
            return ReadResult(data=[], headings=headings,
                              last_read_row=self.read_row)
        reader = csv.reader(data_lines, dialect=self.csv_dialect)
        data: ListData[Value] = [list(row) for row in reader]
        self.position_column = len(data[-1])
        return ReadResult(data=data, headings=headings,
                          last_read_row=self.read_row)

    def _read_table_dictdata(self, box: Optional[Box] = None) \
            -> ReadResult[DictData[Value]]:
        """Read a table of dict data from the file.

        Read a table from the file. The table is read into a list of
        dicts. Empty lines before the table are ignored. Lines
        starting with '#' followed by a space are read as headings.
        The first non-empty line not matching the heading pattern is
        the header row with column names. Subsequent lines are data
        rows. Reading stops when an empty line is encountered or the
        end of the file is reached.
        CSV does not support reading from a box.
        Args:
            box: Not allowed in CSV.
        Raises:
            CapabilityNotSupported: If box is provided.
        Returns:
            The data as a list of dicts, and any headings found
            before the table.
        """
        assert self.file is not None
        if box is not None:
            err = 'Box is not allowed in CSV.'
            raise CapabilityNotSupported(err)
        headings, data_lines = self._read_raw_sections()
        if not data_lines:
            return ReadResult(data=[], headings=headings,
                              last_read_row=self.read_row)
        reader = csv.DictReader(data_lines, dialect=self.csv_dialect)
        data: DictData[Value] = [dict(row) for row in reader]
        if reader.fieldnames is not None:
            self.position_column = len(reader.fieldnames)
        return ReadResult(data=data, headings=headings,
                          last_read_row=self.read_row)
