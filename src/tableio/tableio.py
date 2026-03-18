#! /usr/bin/env python3
"""Reader/writer base class for a file format."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from types import TracebackType
from typing import NamedTuple, Callable, Optional
from mformat.mformat import PathLike
from tableio.capability import Capabilities, SingleCapability, Strictness
from tableio.value_type import CellT, ListDataSeq, DictDataMap, \
    normalize_dict_data, ReadResult, ListData, Value, DictData


class Descriptor(NamedTuple):
    """Descriptors of the reader/writer class for a file format.

    A descriptor is holds the metadata about a reader/writer
    class for a file format and is used by the factory.
    There may be several reader/writer classes for the same file
    as long as they have different values for the implementation.

    The capabilities describe what the reader/writer class can do.
    The mandatory and optional arguments describe the arguments that
    the reader/writer class expects.
    """

    format_name: str
    """The name of the file format."""
    implementation: str
    """The implementation of the reader/writer class."""
    capabilities: Capabilities
    """The capabilities of the reader/writer class."""
    mandatory_args: list[str]
    """The mandatory arguments of the reader/writer class."""
    optional_args: list[str]
    """The optional arguments of the reader/writer class."""
    priority: int = 10
    """The priority of this implementation. 0 = lowest, 100 = highest."""


class Box(NamedTuple):
    """A rectangular area in a file.

    The box is defined by the edges.
     - top: top row, that is first row inside the box.
     - left: left column, that is leftmost column in the box.
     - bottom: bottom edge, first row below the box.
     - right: right edge, first column to the right of the box.
    Row and column indices are 0-based.
    If bottom or right is None, the box will expand according to the data.
    """

    top: int
    left: int
    bottom: Optional[int]
    right: Optional[int]


class Position(NamedTuple):
    """A position in a file.

    The position is defined by the row and column.
    Row and column indices are 0-based.
    This is used to report the position of the last cell written.
    """

    row: int
    column: int


class TableIO:
    """File format reader/writer base class for table data."""

    def __init__(self, file_name: PathLike,
                 file_exists_callback: Optional[Callable[[str], None]]
                 = None):
        """Initialize the TableIO reader/writer class.

        Args:
            file_name: The name of the file to write to.
            file_exists_callback: A callback function to call if the file
                                  already exists. Return to allow the file to
                                  be overwritten. Raise an exception to
                                  prevent the file from being overwritten.
                                  (May for instance save existing file as
                                  backup.)
                                  (Default is to raise an exception.)
        """
        self.file_exists_callback: Optional[Callable[[str], None]] = \
            file_exists_callback
        self.file_name: str = \
            self.file_name_with_extension(file_name,
                                          self.file_name_extension())
        self.heading_written: bool = False

    @classmethod
    def get_desciption(cls) -> Descriptor:
        """Get the description of the reader/writer class.

        Must be overridden by subclasses.
        An implementation that produce the same file format but with
        stricter adherance to the file format specification or
        better compatibitity with other software should have
        a higher priority (even it has fewer capabilities).
        """
        err = 'Subclass must implement get_desciption method'
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
        return f"{str(file_name)}.{extension}"

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
                   If level is None and it is first heading, level 1 is used.
                   If level is None and it is not first heading,
                   level 2 is used.
        Returns:
            The position of the last cell written.
        """
        if not level:
            if self.heading_written:
                level = 2
            else:
                level = 1
        self.heading_written = True
        return self._write_heading(heading, level)

    def write_table_listdata(self, data: ListDataSeq[CellT],
                             box: Optional[Box] = None) -> Position:
        """Write a table of list data to the file.

        Write a table of list data to the file.
        If a box is provided the data will be written into the box.
        The data must fit into the box.
        Args:
            data: The list data to write.
            box: The box to write the data into.
        Returns:
            The position of the last cell written.
        """
        self._check_listdimensions(data, box)
        c_box = self._check_box_write(box)
        return self._write_table_listdata(data, c_box)

    def write_table_dictdata(self,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                             data: DictDataMap[CellT],
                             column_order: list[str],
                             missing_ok: bool = False,
                             extra_ok: bool = False,
                             box: Optional[Box] = None) -> Position:
        """Write a table of dict data to the file.

        Write a table of dict data to the file.
        If a box is provided the data will be written into the box.
        The data must fit into the box.
        Args:
            data: The dict data to write.
            box: The box to write the data into.
            column_order: The order of the columns.
            missing_ok: If True, None is inserted for missing column data.
                        If False, an exception is raised.
            extra_ok: If True, data for extra columns are ignored.
                      If False, an exception is raised if data for extra
                      columns are present.
        Raises:
            ValueError: If missing_ok is False and data is missing for a
                        column in the column_order.
            ValueError: If extra_ok is False and data is present for a
                        key not in the column_order.
        Returns:
            The position of the last cell written.
        """
        ndata = normalize_dict_data(data, column_order, missing_ok, extra_ok)
        self._check_dictdimensions(ndata, box)
        c_box = self._check_box_write(box)
        return self._write_table_dictdata(ndata, column_order, c_box)

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
        Returns:
            The data read from the table and the headings before the table.
        """
        c_box = self._check_box_read(box)
        return self._read_table_dictdata(c_box)

    def open(self) -> None:
        """Open the file.

        Avoid using this method directly.
        Use MultiFormat as a context manager instead, using a with statement.
        """
        err = 'Subclass must implement open method'
        raise NotImplementedError(err)

    def close(self) -> None:
        """Close the file.

        Avoid using this method directly.
        Use MultiFormat as a context manager instead, using a with statement.
        """
        try:  # we need to close the file even if an exception is raised
            self._end_state()
            self._write_file_suffix()
            self._close()
        finally:
            self._close()
        # The _close method should internally guard against multiple closes.

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

    def _write_table_listdata(self, data: ListDataSeq[CellT],
                              box: Optional[Box] = None) -> Position:
        """Write a table of list data to the file.

        Args:
            data: The list data to write.
            box: The box to write the data into.
        Returns:
            The position of the last cell written.
        """
        _ = data  # avoid unused variable warning
        _ = box  # avoid unused variable warning
        err = 'Subclass must implement _write_table_listdata method'
        raise NotImplementedError(err)

    def _check_listdimensions(self, data: ListDataSeq[CellT],
                              box: Optional[Box] = None) -> None:
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
        if len(data[0]) < 2 and len(data) < 2:
            err = 'Data is not at least 2 cells in size'
            raise ValueError(err)
        for row in data:
            if len(row) != len(data[0]):
                err = 'All rows must have the same number of columns'
                raise ValueError(err)
        if box is not None:
            if box.bottom is not None and len(data) > box.bottom - box.top:
                err = 'Data does not fit into box. Too many rows.'
                raise ValueError(err)
            if box.right is not None and len(data[0]) > box.right - box.left:
                err = 'Data does not fit into box. Too many columns.'
                raise ValueError(err)

    def _check_dictdimensions(self, data: DictDataMap[CellT],
                              box: Optional[Box] = None) -> None:
        """Check the dimensions of the dict data.

        Args:
            data: The dict data to check.
            column_order: The order of the columns.
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
        if box.bottom is not None and (len(data)+1) > box.bottom - box.top:
            err = 'Data does not fit into box. Too many rows.'
            raise ValueError(err)
        if box.right is not None and len(data[0]) > box.right - box.left:
            err = 'Data does not fit into box. Too many columns.'
            raise ValueError(err)

    def _check_box_write(self, box: Optional[Box]) -> Optional[Box]:
        """Check if the box is OK to use for writing.

        Args:
            box: The box to check.
        """
        cap_box = self.get_capabilities().can_write_box
        return self._check_box_impl(box, cap_box)

    def _check_box_read(self, box: Optional[Box]) -> Optional[Box]:
        """Check if the box is OK to use for reading.

        Args:
            box: The box to check.
        """
        cap_box = self.get_capabilities().can_read_box
        return self._check_box_impl(box, cap_box)

    @staticmethod
    def _check_box_impl(box: Optional[Box],
                        cap: SingleCapability) -> Optional[Box]:
        """Check if the box is OK to use for the given capability.

        Args:
            box: The box to check.
            cap: The capability to check.
        """
        if box is None or cap.supported:
            return box
        if cap.strictness == Strictness.IGNORE:
            return None
        err = 'Box is not supported for reading.'
        raise ValueError(err)

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
            The position of the last cell written.
        """
        err = 'Subclass must implement _write_heading method'
        _ = heading  # avoid unused variable warning
        _ = level  # avoid unused variable warning
        raise NotImplementedError(err)

    def _write_table_dictdata(self, data: DictDataMap[CellT],
                              column_order: list[str],
                              box: Optional[Box] = None) -> Position:
        """Write a table of dict data to the file.

        Args:
            data: The dict data to write.
            column_order: The order of the columns.
            box: The box to write the data into.
        Returns:
            The position of the last cell written.
        """
        _ = data  # avoid unused variable warning
        _ = column_order  # avoid unused variable warning
        _ = box  # avoid unused variable warning
        err = 'Subclass must implement _write_table_dictdata method'
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
