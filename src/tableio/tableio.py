#! /usr/bin/env python3
"""Reader/writer base class for a file format."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import io
from datetime import datetime
from pathlib import Path
from types import TracebackType
from typing import NamedTuple, Callable, Optional
from mformat.mformat import PathLike
from tableio.capability import Capabilities, SingleCapability, Strictness, \
    CapabilityNotSupported
from tableio.tableio_types import Box, Descriptor, FileAccess, Position
from tableio.value_type import CellT, ListDataSeq, DictDataMap, \
    normalize_dict_data, ReadResult, ListData, Value, Fmt, DictData, \
    FmtListData, FmtDictData, FmtDictRow, row_strip_format_list, \
    row_strip_format_dict

__all__ = ['Box', 'Descriptor', 'FileAccess', 'Position', 'TableIO']


class TableIO:
    """File format reader/writer base class for table data."""

    def __init__(self, file_name: PathLike,
                 file_access: FileAccess,
                 file_exists_callback: Optional[Callable[[str], None]]
                 = None):
        """Initialize the TableIO reader/writer class.

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
        """
        self.file_access: FileAccess = file_access
        self.file_exists_callback: Optional[Callable[[str], None]] = \
            file_exists_callback
        self.file_name: str = \
            self.file_name_with_extension(file_name,
                                          self.file_name_extension())
        self._file_exists_check()
        self.heading_written: bool = False

    @classmethod
    def get_description(cls) -> Descriptor:
        """Get the description of the reader/writer class.

        Must be overridden by subclasses.
        An implementation that produce the same file format but with
        stricter adherance to the file format specification or
        better compatibitity with other software should have
        a higher priority (even it has fewer capabilities).
        """
        err = 'Subclass must implement get_description method'
        raise NotImplementedError(err)
        # pylint: disable=unreachable
        return Descriptor(name='', mandatory_args=[],
                          capabilities=Capabilities(),
                          optional_args=['file_exists_callback'])

    @classmethod
    def get_capabilities(cls) -> Capabilities:
        """Return the capabilities of the reader/writer class.

        Must be overridden by subclasses.
        """
        err = 'Subclass must implement get_capabilities method'
        raise NotImplementedError(err)
        # pylint: disable=unreachable
        return Capabilities()

    @staticmethod
    def file_name_with_extension(file_name: PathLike,
                                 extension: str) -> str:
        """Return the file name with the extension."""
        if not extension.startswith('.'):
            extension = f'.{extension}'
        if str(file_name).lower().endswith(extension.lower()):
            return str(file_name)
        return f'{str(file_name)}{extension}'

    @classmethod
    def file_name_extension(cls) -> str:
        """Return the extension of the file name."""
        msg = 'Subclass must implement file_name_extension method'
        raise NotImplementedError(msg)
        # pylint: disable=unreachable
        return ''

    def __enter__(self) -> 'TableIO':
        """Enter the context manager."""
        self.open()
        return self

    def __exit__(self, exc_type: type[BaseException] | None,
                 exc_value: BaseException | None,
                 traceback: TracebackType | None) -> bool:
        """Exit the context manager.

        Closes the file. If the with block raised an exception,
        close errors are noted on it to preserve it as primary.

        Args:
            exc_type: The type of the exception.
            exc_value: The value of the exception.
            traceback: The traceback of the exception.
        Returns:
            False if an exception should propagate, True otherwise.
        """
        if exc_type is None:
            self.close()
            return True
        try:
            self.close()
        # pylint: disable-next=broad-exception-caught
        except Exception as close_exc:
            assert exc_value is not None
            exc_value.add_note(
                f'Additionally, close() raised: {close_exc}')
        return False

    def write_heading(self, heading: str,
                      level: Optional[int] = None) -> Position:
        """Write a heading to the file.

        Write a heading to the file. Headings are a line between tables.
        For example in CSV format the heading has an empty line before and
        after and it starts with one or more '#' characters.
        Do not confuse the heading with the first row of a table,
        with the names of the columns.
        Args:
            heading: The heading text to write.
            level: The level of the heading. 1 = highest, 3 = lowest.
                   If level is None and it is first heading in the sheet,
                   level 1 is used.
                   If level is None and it is not first heading in the sheet,
                   level 2 is used.
        Raises:
            ValueError: If level is outside the range 1 to 3.
            io.UnsupportedOperation: If the file is opened for reading.
        Returns:
            The position of the last cell written. Position is in the
            current sheet.
        """
        self._check_file_is_writable()
        if level is None:
            if self.heading_written:
                level = 2
            else:
                level = 1
        if not 1 <= level <= 3:
            err = 'Heading level must be in range 1 to 3.'
            raise ValueError(err)
        if '\n' in heading:
            err = 'Heading cannot contain a newline.'
            raise ValueError(err)
        self.heading_written = True
        return self._write_heading(heading, level)

    class ImplMetaForWrite(NamedTuple):
        """Meta data for writing table to pass to implementation."""

        filtered_data_range: bool
        """If True, data will be written as a range that can be filtered."""
        box: Optional[Box]
        """The box to write the data into."""

    class ImplMetaForDictWrite(NamedTuple):
        """Meta data for writing dict table to pass to implementation."""

        common_impl: 'TableIO.ImplMetaForWrite'
        """Common meta data for writing dict/list to pass to implementation."""
        column_order: list[str]
        """The order of the columns."""
        first_row_format: Optional[Fmt]
        """The format specification for the first row."""

    def write_table_listdata(self, data: ListDataSeq[CellT],
                             filtered_data_range: bool = False,
                             box: Optional[Box] = None) -> Position:
        """Write a table of list data to the file.

        Write a table of list data to the file.
        If a box is provided the data will be written into the box.
        The data must fit into the box.
        Notice when spefifying a box: It is not allowed to write a
        table that partly overwrites an existing table.
        Args:
            data: The list data to write.
            filtered_data_range: If True, the data written will be
                                 marked as a data range that can be filtered.
            box: The box to write the data into. If box.bottom or box.right is
                not None, the data must fill the box.
        Raises:
            ValueError: If the data shape is invalid or does not fit in box.
            CapabilityNotSupported: If a requested capability is unsupported
                                    and strict.
            io.UnsupportedOperation: If the file is opened for reading.
        Returns:
            The position of the last cell written. Position is in the
            current sheet.
        """
        self._check_file_is_writable()
        c_box = self._check_box_write(box)
        self._check_listdimensions(data, c_box)
        c_filt_range = self._check_filtered_data_range(filtered_data_range)
        impl_meta: TableIO.ImplMetaForWrite = \
            TableIO.ImplMetaForWrite(filtered_data_range=c_filt_range,
                                     box=c_box)
        return self._write_table_listdata(data=data, impl_meta=impl_meta)

    def write_table_fmtlistdata(self, data: FmtListData,
                                filtered_data_range: bool = False,
                                box: Optional[Box] = None) -> Position:
        """Write a table of list data to the file.

        Write a table of list data to the file.
        If a box is provided the data will be written into the box.
        The data must fit into the box.
        Notice when spefifying a box: It is not allowed to write a
        table that partly overwrites an existing table.
        Args:
            data: The list data to write.
            filtered_data_range: If True, the data written will be
                                 marked as a data range that can be filtered.
            box: The box to write the data into. If box.bottom or box.right is
                not None, the data must fill the box.
        Raises:
            ValueError: If the data shape is invalid or does not fit in box.
            CapabilityNotSupported: If a requested capability is unsupported
                                    and strict.
            io.UnsupportedOperation: If the file is opened for reading.
        Returns:
            The position of the last cell written. Position is in the
            current sheet.
        """
        self._check_file_is_writable()
        c_box = self._check_box_write(box)
        self._check_listdimensions(row_strip_format_list(data), c_box)
        c_filt_range = self._check_filtered_data_range(filtered_data_range)
        impl_meta: TableIO.ImplMetaForWrite = \
            TableIO.ImplMetaForWrite(filtered_data_range=c_filt_range,
                                     box=c_box)
        return self._write_table_fmtlistdata(data=data, impl_meta=impl_meta)

    def write_table_dictdata(self,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                             data: DictDataMap[CellT],
                             column_order: list[str],
                             first_row_format: Optional[Fmt] = None,
                             missing_ok: bool = False,
                             extra_ok: bool = False,
                             filtered_data_range: bool = False,
                             box: Optional[Box] = None) -> Position:
        """Write a table of dict data to the file.

        Write a table of dict data to the file.
        If a box is provided the data will be written into the box.
        The data must fit into the box.
        Notice when spefifying a box: It is not allowed to write a
        table that partly overwrites an existing table.
        Args:
            data: The dict data to write.
            column_order: The order of the columns.
            first_row_format: The format specification for the first row.
                              The table will get a first row with the names
                              of the columns. This format specification will
                              be applied to the first row. If None, no format
                              will be applied to the first row.
            missing_ok: If True, None is inserted for missing column data.
                        If False, an exception is raised.
            extra_ok: If True, data for extra columns are ignored.
                      If False, an exception is raised if data for extra
                      columns are present.
            filtered_data_range: If True, the data written will be
                                 marked as a data range that can be filtered.
            box: The box to write the data into. If box.bottom or box.right is
                not None, the data must fill the box.
        Raises:
            ValueError: If missing_ok is False and data is missing for a
                        column in the column_order.
            ValueError: If extra_ok is False and data is present for a
                        key not in the column_order.
            ValueError: If the data shape is invalid or does not fit in box.
            CapabilityNotSupported: If a requested capability is unsupported
                                    and strict.
            io.UnsupportedOperation: If the file is opened for reading.
        Returns:
            The position of the last cell written. Position is in the
            current sheet.
        """
        self._check_file_is_writable()
        c_box = self._check_box_write(box)
        ndata = normalize_dict_data(data, column_order, missing_ok, extra_ok)
        self._check_dictdimensions(ndata, c_box)
        c_filt_range = self._check_filtered_data_range(filtered_data_range)
        common_impl: TableIO.ImplMetaForWrite = \
            TableIO.ImplMetaForWrite(filtered_data_range=c_filt_range,
                                     box=c_box)
        impl_meta: TableIO.ImplMetaForDictWrite = \
            TableIO.ImplMetaForDictWrite(common_impl=common_impl,
                                         column_order=column_order,
                                         first_row_format=first_row_format)
        return self._write_table_dictdata(data=ndata, impl_meta=impl_meta)

    def write_table_fmtdictdata(self,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                                data: FmtDictData,
                                column_order: list[str],
                                first_row_format: Optional[Fmt] = None,
                                missing_ok: bool = False,
                                extra_ok: bool = False,
                                filtered_data_range: bool = False,
                                box: Optional[Box] = None) -> Position:
        """Write a table of dict data to the file.

        Write a table of dict data to the file.
        If a box is provided the data will be written into the box.
        The data must fit into the box.
        Notice when spefifying a box: It is not allowed to write a
        table that partly overwrites an existing table.
        Args:
            data: The dict data to write.
            column_order: The order of the columns.
            first_row_format: The format specification for the first row.
                              The table will get a first row with the names
                              of the columns. This format specification will
                              be applied to the first row. If None, no format
                              will be applied to the first row.
            missing_ok: If True, None is inserted for missing column data.
                        If False, an exception is raised.
            extra_ok: If True, data for extra columns are ignored.
                      If False, an exception is raised if data for extra
                      columns are present.
            filtered_data_range: If True, the data written will be
                                 marked as a data range that can be filtered.
            box: The box to write the data into. If box.bottom or box.right is
                not None, the data must fill the box.
        Raises:
            ValueError: If missing_ok is False and data is missing for a
                        column in the column_order.
            ValueError: If extra_ok is False and data is present for a
                        key not in the column_order.
            ValueError: If the data shape is invalid or does not fit in box.
            CapabilityNotSupported: If a requested capability is unsupported
                                    and strict.
            io.UnsupportedOperation: If the file is opened for reading.
        Returns:
            The position of the last cell written. Position is in the
            current sheet.
        """
        self._check_file_is_writable()
        c_box = self._check_box_write(box)
        stripped_data = row_strip_format_dict(data)
        normalized_values = normalize_dict_data(stripped_data, column_order,
                                                missing_ok, extra_ok)
        self._check_dictdimensions(normalized_values, c_box)
        if normalized_values is stripped_data:
            normalized_data = data
        else:
            normalized_data = [
                FmtDictRow(values=row_values, fmt=row.fmt)
                for row, row_values in zip(data, normalized_values,
                                           strict=True)]
        c_filt_range = self._check_filtered_data_range(filtered_data_range)
        common_impl: TableIO.ImplMetaForWrite = \
            TableIO.ImplMetaForWrite(filtered_data_range=c_filt_range,
                                     box=c_box)
        impl_meta: TableIO.ImplMetaForDictWrite = \
            TableIO.ImplMetaForDictWrite(common_impl=common_impl,
                                         column_order=column_order,
                                         first_row_format=first_row_format)
        return self._write_table_fmtdictdata(data=normalized_data,
                                             impl_meta=impl_meta)

    def read_table_listdata(self, box: Optional[Box] = None) \
            -> ReadResult[ListData[Value]]:
        """Read a table of list data from the file.

        If a box is provided the data will be read from the box, and the
        reading is restricted to the box.
        Anything found in the leftmost column that does form a table of at
        least 2 cells in size is considered to be a heading and is returned
        as a list of headings.
        Args:
            box: The box to read the data from.
        Raises:
            CapabilityNotSupported: If reading from a box is unsupported and
                                    strict.
        Returns:
            The data read from the table and the headings before the table.
        """
        c_box = self._check_box_read(box)
        return self._read_table_listdata(c_box)

    def read_table_dictdata(self, box: Optional[Box] = None) \
            -> ReadResult[DictData[Value]]:
        """Read a table of dict data from the file.

        If a box is provided the data will be read from the box, and the
        reading is restricted to the box.
        Anything found in the leftmost column that does form a table of
        at least 2 cells in size is considered to be a heading and is
        returned as a list of headings.
        Args:
            box: The box to read the data from.
        Raises:
            CapabilityNotSupported: If reading from a box is unsupported and
                                    strict.
        Returns:
            The data read from the table and the headings before the table.
        """
        c_box = self._check_box_read(box)
        return self._read_table_dictdata(c_box)

    def list_sheets(self) -> list[str]:
        """List the sheets in the file.

        Returns:
            A list of the sheet names. Sheet names are case preserving,
            but compared case insensitively.
        Raises:
            CapabilityNotSupported: If multiple sheets are not supported.
        """
        if not self.get_capabilities().multi_sheet.supported:
            raise CapabilityNotSupported('multi sheet')
        return self._list_sheets()

    def select_sheet(self, sheet_name: str, create: bool = False) -> None:
        """Select a sheet in the file.

        Select a sheet in the file that will be used for subsequent writes
        and reads. Cursor positions (read and write positions) are per sheet.

        Args:
            sheet_name: The name of the sheet to select. Sheet names are
                        case preserving, but compared case insensitively.
            create: If True, create the sheet if it does not exist.
        Raises:
            CapabilityNotSupported: If multiple sheets are not supported.
            KeyError: If the sheet name is not found and create is False.
            io.UnsupportedOperation: If create is True, the sheet does not
                                     exist, and the file is opened for
                                     reading.
        """
        if not self.get_capabilities().multi_sheet.supported:
            raise CapabilityNotSupported('multi sheet')
        return self._select_sheet(sheet_name, create)

    def current_sheet_name(self) -> str:
        """Return the name of the current sheet.

        Returns:
            The name of the current sheet. Sheet names are case preserving,
            but compared case insensitively.
        Raises:
            CapabilityNotSupported: If multiple sheets are not supported.
        """
        if not self.get_capabilities().multi_sheet.supported:
            raise CapabilityNotSupported('multi sheet')
        return self._current_sheet_name()

    def find_value(self, find_value: Value | ListDataSeq[Value],
                   type_conversion: bool = True,
                   box: Optional[Box] = None) -> Optional[Box]:
        """Find the position of a value or values in the file.

        Search for a position of a value or values in the current sheet of
        the file. The first position found is returned.
        If several matching values are present, the first found is returned.
        Here "first" means on a lower row index, and if row indices are equal,
        on a lower column index.
        For comparison the value in a cell is first compared without type
        conversion, mismatching if types differ.
        Then type conversion to each corresponding find_value cell is
        attempted using value2type_of(...), if allowed by type_conversion.
        Args:
            find_value: The value or values to find. A rectangular area of
                        values to find. A single value is used as a 1x1 area.
            type_conversion: If True, each cell value in the searched area is
                             also converted to the type of the corresponding
                             find_value cell for comparison. If False, no type
                             conversion is attempted.
            box: Search within this box. If None, the entire current sheet is
                 searched.
        Raises:
            CapabilityNotSupported: If find_value_position capability is not
                                    supported.
        Returns:
            A box tightly fitting around the first found value or values.
            None if no matching value is found.
        """
        if not self.get_capabilities().can_find_value_position.supported:
            err = 'Finding value position is not supported'
            raise CapabilityNotSupported(err)
        c_box = self._check_box_read(box)
        value_area = self._value_area(find_value)
        return self._find_value(value_area, type_conversion, c_box)

    def read_cells(self, box: Box) -> ListData[Value]:
        """Read the cells in the current sheet of the file.

        Read cells from the box position in the current sheet of the file.
        The cell reading is independent of the table positions in the file.
        This call does not affect the cursor position.
        Args:
            box: The box to read the cells from. Neither of box.bottom or
            box.right may be None.
        Raises:
            ValueError: If box.bottom or box.right is None.
            CapabilityNotSupported: If reading from a box is unsupported.
        Returns:
            The values of the cells read from the file.
        """
        if box.bottom is None or box.right is None:
            err = 'box.bottom and box.right must be not None'
            raise ValueError(err)
        if not self.get_capabilities().can_read_box.supported:
            err = 'Reading from a box is not supported'
            raise CapabilityNotSupported(err)
        return self._read_cells(box)

    def write_cells(self, data: ListDataSeq[CellT], box: Box) -> None:
        """Write the cells to the current sheet of the file.

        Write cells to the box position in the current sheet of the file.
        The cell writing is independent of the table positions in the file.
        This call does not affect the cursor position.
        Notice: This method allows writing of cells to arbitrary positions
        in the file, which might destroy table and heading structures, and
        may make it impossible to read the file back into a table. It is
        the responsibility of the caller to ensure that the file keeps
        a valid structure for whatever purpose the file is intended for.
        Args:
            data: The data to write.
            box: The box to write the cells to. If box.bottom or box.right is
                 not None, the data must fill the box.
        Raises:
            ValueError: If box.bottom or box.right is not None and the data
                        does not fit and fill the box.
            CapabilityNotSupported: If writing to a box is unsupported.
            io.UnsupportedOperation: If the file is opened for reading.
        """
        self._check_file_is_writable()
        self._check_listdimensions(data, box, is_table=False)
        if not self.get_capabilities().can_write_box.supported:
            err = 'Writing to a box is not supported'
            raise CapabilityNotSupported(err)
        self._write_cells(data, box)

    def open(self) -> None:
        """Open the file.

        Avoid using this method directly.
        Use derived class as a context manager instead, using a with statement.
        """
        err = 'Subclass must implement open method'
        raise NotImplementedError(err)

    def close(self) -> None:
        """Close the file.

        Avoid using this method directly.
        Use derived class as a context manager instead, using a with statement.
        """
        try:
            self._end_state()
            self._write_file_suffix()
        # pylint: disable-next=broad-exception-caught
        except Exception as err:
            try:
                self._close()
            # pylint: disable-next=broad-exception-caught
            except Exception as close_err:
                err.add_note(
                    f'Additionally, _close() raised: {close_err}')
            raise
        self._close()

    def _end_state(self) -> None:
        """End the state of the file."""
        err = 'Subclass must implement _end_state method'
        raise NotImplementedError(err)

    def _write_file_suffix(self) -> None:
        """Write the file suffix."""
        err = 'Subclass must implement _write_file_suffix method'
        raise NotImplementedError(err)

    def _close(self) -> None:
        """Close the file."""
        err = 'Subclass must implement _close method'
        raise NotImplementedError(err)

    def _check_listdimensions(self, data: ListDataSeq[CellT],
                              box: Optional[Box] = None,
                              is_table: bool = True) -> None:
        """Check the dimensions of the list data.

        Args:
            data: The list data to check.
            box: The box to check the data into.
        Raises:
            ValueError: If the data does not have the same number of columns in
                        each row.
            ValueError: If the data does not fit into the box.
            ValueError: If the data is not at least 2 cells in size.
        """
        if not data:
            err = 'Data is empty'
            raise ValueError(err)
        if not data[0]:
            err = 'First row is empty'
            raise ValueError(err)
        if is_table:
            if len(data[0]) < 2 and len(data) < 2:
                err = 'Data is not at least 2 cells in size'
                raise ValueError(err)
        for row in data:
            if len(row) != len(data[0]):
                err = 'All rows must have the same number of columns'
                raise ValueError(err)
        if box is not None:
            if box.bottom is not None and len(data) != box.bottom - box.top:
                err = 'Data does not fit into box. Wrong number of rows.'
                raise ValueError(err)
            if box.right is not None and len(data[0]) != box.right - box.left:
                err = 'Data does not fit into box. Wrong number of columns.'
                raise ValueError(err)

    def _value_area(
            self, value: Value | ListDataSeq[Value]) -> ListData[Value]:
        """Return one scalar or rectangular value pattern as a list grid."""
        if value is None or isinstance(value, (str, bool, int, float,
                                               datetime)):
            return [[value]]
        self._check_listdimensions(value, is_table=False)
        return [list(row) for row in value]

    def _check_dictdimensions(self, data: DictDataMap[CellT],
                              box: Optional[Box] = None) -> None:
        """Check the dimensions of the dict data.

        Args:
            data: The dict data to check.
            box: The box to check the data into.
        Raises:
            ValueError: If the data does not fit into the box.
            ValueError: If the data is not at least 2 cells in size.
        """
        if not data:
            err = 'Data is empty'
            raise ValueError(err)
        if not data[0]:
            err = 'First row is empty'
            raise ValueError(err)
        if len(data[0]) < 2 and len(data) < 2:
            err = 'Data is not at least 2 cells in size'
            raise ValueError(err)
        if box is None:
            return
        if box.bottom is not None and (len(data)+1) != box.bottom - box.top:
            err = 'Data does not fit into box. Wrong number of rows.'
            raise ValueError(err)
        if box.right is not None and len(data[0]) != box.right - box.left:
            err = 'Data does not fit into box. Wrong number of columns.'
            raise ValueError(err)

    def _check_box_write(self, box: Optional[Box]) -> Optional[Box]:
        """Check if the box is OK to use for writing.

        Args:
            box: The box to check.
        Raises:
            CapabilityNotSupported: If writing to a box is unsupported and
                                    strict.
        Returns:
            The box if it is supported.
            None if it is not supported and ignored.
        """
        cap_box = self.get_capabilities().can_write_box
        return self._check_box_impl(box, cap_box, 'write to a box')

    def _check_box_read(self, box: Optional[Box]) -> Optional[Box]:
        """Check if the box is OK to use for reading.

        Args:
            box: The box to check.
        Raises:
            CapabilityNotSupported: If reading from a box is unsupported and
                                    strict.
        Returns:
            The box if it is supported.
            None if it is not supported and ignored.
        """
        cap_box = self.get_capabilities().can_read_box
        return self._check_box_impl(box, cap_box, 'read from a box')

    @staticmethod
    def _check_box_impl(box: Optional[Box],
                        cap: SingleCapability,
                        action: str) -> Optional[Box]:
        """Check if the box is OK to use for the given capability.

        Args:
            box: The box to check.
            cap: The capability to check.
            action: The action the box is requested for.
        Raises:
            CapabilityNotSupported: If the box is not supported and strict.
        Returns:
            The box if it is supported.
            None if it is not supported and ignored.
        """
        if box is None or cap.supported:
            return box
        if cap.strictness == Strictness.IGNORE:
            return None
        raise CapabilityNotSupported(action)

    def _check_filtered_data_range(self, filtered_data_range: bool) -> bool:
        """Check if the filtered data range is supported.

        Args:
            filtered_data_range: If True, the data written will be
                                 marked as a data range that can be filtered.
        Returns:
            True if the filtered data range is requested and supported.
            False if the filtered data range is not requested.
            False if the filtered data range is not supported and ignored.
        Raises:
            CapabilityNotSupported: If writing a filtered data range is not
                                    supported and strict.
        """
        if not filtered_data_range:
            return False
        cap_filtered_data_range = self.get_capabilities().filtered_data_range
        if cap_filtered_data_range.supported:
            return filtered_data_range
        if cap_filtered_data_range.strictness == Strictness.IGNORE:
            return False
        raise CapabilityNotSupported('write a filtered data range')

    def _write_heading(self, heading: str, level: int) -> Position:
        """Write a heading to the file.

        Write a heading to the file. Headings are a line between tables.
        For example in CSV format the heading has an empty line before and
        after, and it starts with one or more '#' characters.
        Do not confuse the heading with the first row of a table,
        with the names of the columns.

        Args:
            heading: The heading text to write.
            level: The level of the heading. 1 = highest, 3 = lowest.
        Returns:
            The position of the last cell written. Position is in the
            current sheet.
        """
        err = 'Subclass must implement _write_heading method'
        _ = heading  # avoid unused variable warning
        _ = level  # avoid unused variable warning
        raise NotImplementedError(err)

    def _write_table_listdata(self, data: ListDataSeq[CellT],
                              impl_meta: ImplMetaForWrite) -> Position:
        """Write a table of list data to the file.

        Args:
            data: The list data to write.
            impl_meta: The meta data for the table write operation,
                       passed to the implementation class.
        Returns:
            The position of the last cell written. Position is in the
            current sheet.
        """
        _ = data  # avoid unused variable warning
        _ = impl_meta  # avoid unused variable warning
        err = 'Subclass must implement _write_table_listdata method'
        raise NotImplementedError(err)

    def _write_table_fmtlistdata(self, data: FmtListData,
                                 impl_meta: ImplMetaForWrite) -> Position:
        """Write a table of list data to the file.

        Args:
            data: The list data to write.
            impl_meta: The meta data for the table write operation,
                       passed to the implementation class.
        Returns:
            The position of the last cell written. Position is in the
            current sheet.
        """
        _ = data  # avoid unused variable warning
        _ = impl_meta  # avoid unused variable warning
        err = 'Subclass must implement _write_table_fmtlistdata method'
        raise NotImplementedError(err)

    def _write_table_dictdata(self, data: DictDataMap[CellT],
                              impl_meta: ImplMetaForDictWrite) -> Position:
        """Write a table of dict data to the file.

        Args:
            data: The dict data to write.
            impl_meta: The meta data for the dict table write operation,
                       passed to the implementation class.
        Returns:
            The position of the last cell written. Position is in the
            current sheet.
        """
        _ = data  # avoid unused variable warning
        _ = impl_meta  # avoid unused variable warning
        err = 'Subclass must implement _write_table_dictdata method'
        raise NotImplementedError(err)

    def _write_table_fmtdictdata(self, data: FmtDictData,
                                 impl_meta: ImplMetaForDictWrite) -> Position:
        """Write a table of dict data to the file.

        Args:
            data: The dict data to write.
            impl_meta: The meta data for the dict table write operation,
                       passed to the implementation class.
        Returns:
            The position of the last cell written. Position is in the
            current sheet.
        """
        _ = data  # avoid unused variable warning
        _ = impl_meta  # avoid unused variable warning
        err = 'Subclass must implement _write_table_fmtdictdata method'
        raise NotImplementedError(err)

    def _read_table_listdata(self, box: Optional[Box] = None) \
            -> ReadResult[ListData[Value]]:
        """Read a table of list data from the file.

        Must be implemented by derived classes.
        If a box is provided the data will be read from the box, and the
        reading is restricted to the box.
        Anything found in the leftmost column that does form a table of at
        least 2 cells in size is considered to be a heading and is returned
        as a list of headings.
        Args:
            box: The box to read the data from.
        Returns:
            The data read from the table and the headings before the table.
        """
        err = 'Subclass must implement _read_table_listdata method'
        _ = box  # avoid unused variable warning
        raise NotImplementedError(err)

    def _read_table_dictdata(self, box: Optional[Box] = None) \
            -> ReadResult[DictData[Value]]:
        """Read a table of dict data from the file.

        Must be implemented by derived classes.
        If a box is provided the data will be read from the box, and the
        reading is restricted to the box.
        Anything found in the leftmost column that does form a table of at
        least 2 cells in size is considered to be a heading and is returned
        as a list of headings.
        Args:
            box: The box to read the data from.
        Returns:
            The data read from the table and the headings before the table.
        """
        err = 'Subclass must implement _read_table_dictdata method'
        _ = box  # avoid unused variable warning
        raise NotImplementedError(err)

    def _file_exists_check(self) -> None:
        """Check if the file exists.

        If the file exists and the file access is CREATE, the
        file_exists_callback is called to decide if the file can be
        overwritten.
        If file access is READ or UPDATE, the file must exist.
        """
        file_exists = Path(self.file_name).exists()
        if self.file_access == FileAccess.CREATE:
            if not file_exists:
                return
            if self.file_exists_callback is not None:
                self.file_exists_callback(self.file_name)
                return
            msg = 'Cowardly refusing to overwrite existing file '
            msg += f'{self.file_name}.\n\n'
            msg += '(Use a different file name or provide a '
            msg += 'file_exists_callback \n'
            msg += ' function to allow the file to be overwritten.)\n'
            raise FileExistsError(msg)
        if not file_exists:
            msg = f'File does not exist: {self.file_name}.'
            raise FileNotFoundError(msg)

    def _check_file_is_writable(self) -> None:
        """Raise if the file access mode does not allow writing."""
        if self.file_access == FileAccess.READ:
            msg = f'File {self.file_name} is opened for reading.'
            raise io.UnsupportedOperation(msg)

    def _list_sheets(self) -> list[str]:
        """List the sheets in the file.

        Returns:
            A list of the sheet names. Sheet names are case preserving,
            but compared case insensitively.
        """
        err = 'Subclass must implement _list_sheets method'
        raise NotImplementedError(err)

    def _select_sheet(self, sheet_name: str, create: bool = False) -> None:
        """Select a sheet in the file.

        Args:
            sheet_name: The name of the sheet to select.
            create: If True, create the sheet if it does not exist.
        Raises:
            KeyError: If the sheet name is not found and create is False.
            io.UnsupportedOperation: If the file is opened for reading,
                                     and create is True, and the sheet does
                                     not exist.
        """
        err = 'Subclass must implement _select_sheet method'
        _ = sheet_name  # avoid unused variable warning
        _ = create  # avoid unused variable warning
        raise NotImplementedError(err)

    def _current_sheet_name(self) -> str:
        """Return the name of the current sheet.

        Returns:
            The name of the current sheet. Sheet names are case preserving,
            but compared case insensitively.
        """
        err = 'Subclass must implement _current_sheet_name method'
        raise NotImplementedError(err)

    def _find_value(self, find_value: ListData[Value],
                    type_conversion: bool = True,
                    box: Optional[Box] = None) -> Optional[Box]:
        """Backend hook for find_value()."""
        err = 'Subclass must implement _find_value method'
        _ = find_value  # avoid unused variable warning
        _ = type_conversion  # avoid unused variable warning
        _ = box  # avoid unused variable warning
        raise NotImplementedError(err)

    def _read_cells(self, box: Box) -> ListData[Value]:
        """Backend hook for read_cells()."""
        err = 'Subclass must implement _read_cells method'
        _ = box  # avoid unused variable warning
        raise NotImplementedError(err)

    def _write_cells(self, data: ListDataSeq[CellT], box: Box) -> None:
        """Backend hook for write_cells()."""
        err = 'Subclass must implement _write_cells method'
        _ = data  # avoid unused variable warning
        _ = box  # avoid unused variable warning
        raise NotImplementedError(err)
