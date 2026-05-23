#! /usr/bin/env python3
"""TableIO reader/writer class for a file format based on mformat."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional, Callable
from mformat.mformat import PathLike, MultiFormat
from tableio.tableio import TableIO, Position, Box, FileAccess
from tableio.capability import Capabilities, SingleCapability, \
    Strictness, CapabilityNotSupported
from tableio.value_type import ListDataSeq, CellT, FmtListData, \
    row_fmt_from_cell_fmt_list, DictDataMap, FmtDictData, \
    row_fmt_from_cell_fmt_dict, ListData, Value, ReadResult, DictData, \
    list_row_to_str_list, Fmt, FmtListRow


def _allow_overwrite(_: str) -> None:
    """No-op callback signalling that overwrite is permitted.

    Passed to the mformat constructor so that it does not raise
    when the file already exists. The actual overwrite decision
    has already been made by the TableIO base class.
    """


class TableIOMformatBased(TableIO):
    """TableIO reader/writer class for a file format based on mformat.

    This is intermediate base for reader/writer classes based on mformat.
    It provides the common functionality for reader/writer classes based on
    different concrete mformat classes for output in different formats.
    The functionality common to all TableIO_mformatbased subclasses is
    collected here.

    The mformat class does not support reading, so reading is not supported
    for this class. Writing is supported, but not all features are supported.
    For example, box and filtered data range are not supported.
    Row formatting is supported, but value formatting is not.

    Returned position is not reliable, as different MultiFormat derived
    classes have different behavior. Returned position is not useful, as
    neither reading nor boxed writing is supported, it is returned only
    to satisfy the type hints of the TableIO class.
    """

    def __init__(self, file_name: PathLike, file_access: FileAccess,
                 file_exists_callback: Optional[Callable[[str], None]]
                 = None):
        """Initialize the TableIOMformatBased reader/writer class.

        Args:
            file_name: The name of the file to open.
            file_access: What access is requested to the file.
            file_exists_callback: A callback function to call if
                                  the file already exists when file_access
                                  is CREATE.
                                  Return to allow the file to be overwritten.
                                  Raise an exception to prevent the file from
                                  being overwritten.
                                  (May for instance save existing file as
                                  backup.)
                                  (Default is to raise an exception.)
        """
        if file_access != FileAccess.CREATE:
            msg = 'File access must be CREATE for mformat based classes.'
            msg += ' Read and update are not supported for mformat '
            msg += 'based classes.'
            raise CapabilityNotSupported(msg)
        super().__init__(file_name, file_access, file_exists_callback)
        self.mformat: Optional[MultiFormat] = None
        self.is_open: bool = False
        self.position_row: int = -1
        self.position_column: int = 0

    @classmethod
    def get_capabilities(cls) -> Capabilities:
        """Return the capabilities of the reader/writer class."""
        strict_no = SingleCapability(supported=False,
                                     strictness=Strictness.STRICT)
        return Capabilities(
            can_write=SingleCapability(supported=True), can_read=strict_no,
            can_fmt_row=cls.get_row_format_capability(),
            can_fmt_value=SingleCapability(supported=False),
            filtered_data_range=SingleCapability(supported=False),
            can_write_box=strict_no, can_read_box=strict_no,
            can_write_highlight=SingleCapability(supported=False),
            can_write_borders=SingleCapability(supported=False))

    @classmethod
    def get_row_format_capability(cls) -> SingleCapability:
        """Return the capability for row formatting."""
        msg = 'Subclass must implement get_row_format_capability method'
        raise NotImplementedError(msg)
        # pylint: disable=unreachable
        return SingleCapability(supported=False)

    def open(self) -> None:
        """Open the file.

        Open the file. Avoid calling this method directly,
        use the context manager instead.
        """
        # derived class __init__ must set self.mformat
        assert self.mformat is not None
        if self.is_open:
            msg = f'TableIOMformatBased: File {self.file_name} already open.'
            raise RuntimeError(msg)
        self.mformat.open()
        self.is_open = True

    def _close(self) -> None:
        """Close the file.

        Close the file. Avoid calling this method directly,
        use the context manager instead.
        """
        assert self.mformat is not None
        if self.is_open:
            self.mformat.close()
        self.is_open = False

    def _end_state(self) -> None:
        """End the state of the reader/writer class. NOP for this class."""

    def _write_file_suffix(self) -> None:
        """Write the file suffix. NOP for this class."""

    def _write_heading(self, heading: str, level: int) -> Position:
        """Write a heading to the file.

        Write a heading to the file. Headings are a line between tables.
        Args:
            heading: The heading text to write.
            level: The level of the heading. 1 = highest, 3 = lowest.
                   If level is None and it is first heading, level 1 is used.
                   If level is None and it is not first heading,
                   level 2 is used.
        Returns:
            The position of the last cell written. Not reliable.
        """
        assert self.mformat is not None
        self.mformat.new_heading(text=heading, level=level)
        self.position_row += 1
        self.position_column = 0
        return Position(row=self.position_row, column=self.position_column)

    def _write_table_listdata(self, data: ListDataSeq[CellT],
                              impl_meta: TableIO.ImplMetaForWrite) -> Position:
        """Write a table of list data to the file.

        Write a table of list data to the file.
        impl_meta.box is not supported for this class.
        impl_meta.filtered_data_range is ignored for this class.
        Args:
            data: The list data to write.
            impl_meta: The implementation meta data.
        Returns:
            The position of the last cell written. Not reliable.
        """
        row_fmt = row_fmt_from_cell_fmt_list(data)
        return self._write_table_fmtlistdata(data=row_fmt, impl_meta=impl_meta)

    def _write_table_fmtlistdata(self, data: FmtListData,
                                 impl_meta: TableIO.ImplMetaForWrite) \
            -> Position:
        """Write a table of formatted list data to the file.

        Write a table of formatted list data to the file.
        impl_meta.box is not supported for this class.
        impl_meta.filtered_data_range is ignored for this class.
        Args:
            data: The formatted list data to write.
            impl_meta: The implementation meta data.
        Returns:
            The position of the last cell written. Not reliable.
        """
        if impl_meta.box is not None:
            msg = 'Box is not supported for this class.'
            raise CapabilityNotSupported(msg)
        assert self.mformat is not None
        self.mformat.new_table(first_row=list_row_to_str_list(data[0].values,
                                                              True),
                               bold=data[0].fmt.bold,
                               italic=data[0].fmt.italic)
        for row in data[1:]:
            self.mformat.add_table_row(row=list_row_to_str_list(row.values,
                                                                True),
                                       bold=row.fmt.bold,
                                       italic=row.fmt.italic)
        self.position_row += len(data) + 2
        self.position_column = len(data[0].values)
        return Position(row=self.position_row, column=self.position_column)

    def _write_table_dictdata(self, data: DictDataMap[CellT],
                              impl_meta: TableIO.ImplMetaForDictWrite) \
            -> Position:
        """Write a table of dict data to the file.

        Write a table of dict data to the file.
        impl_meta.common_impl.box is not supported for this class.
        impl_meta.common_impl.filtered_data_range is ignored for this class.
        Args:
            data: The dict data to write.
            impl_meta: The implementation meta data.
        Returns:
            The position of the last cell written. Not reliable.
        """
        row_fmt = row_fmt_from_cell_fmt_dict(data)
        return self._write_table_fmtdictdata(data=row_fmt, impl_meta=impl_meta)

    def _write_table_fmtdictdata(self, data: FmtDictData,
                                 impl_meta: TableIO.ImplMetaForDictWrite) \
            -> Position:
        """Write a table of formatted dict data to the file.

        Write a table of formatted dict data to the file.
        impl_meta.box is not supported for this class.
        impl_meta.filtered_data_range is ignored for this class.
        The dict data is converted to list data with column_order
        as the header row, then written via _write_table_fmtlistdata.
        Args:
            data: The formatted dict data to write.
            impl_meta: The implementation meta data.
        Returns:
            The position of the last cell written. Not reliable.
        """
        if impl_meta.common_impl.box is not None:
            msg = 'Box is not supported for this class.'
            raise CapabilityNotSupported(msg)
        header_fmt = impl_meta.first_row_format
        if header_fmt is None:
            header_fmt = Fmt()
        header = FmtListRow(values=list(impl_meta.column_order),
                            fmt=header_fmt)
        list_data: list[FmtListRow] = [header]
        for row in data:
            values: list[Value] = [row.values[key]
                                   for key in
                                   impl_meta.column_order]
            list_data.append(FmtListRow(values=values, fmt=row.fmt))
        return self._write_table_fmtlistdata(data=list_data,
                                             impl_meta=impl_meta.common_impl)

    def _read_table_listdata(self, box: Optional[Box] = None) \
            -> ReadResult[ListData[Value]]:
        """Read a table of list data from the file.

        Reading is not supported for mformat based classes.
        """
        _ = box  # avoid unused variable warning
        msg = 'Reading is not supported for mformat based classes.'
        raise CapabilityNotSupported(msg)
        # pylint: disable=unreachable
        return ReadResult(data=ListData(), headings=[], last_read_row=0)

    def _read_table_dictdata(self, box: Optional[Box] = None) \
            -> ReadResult[DictData[Value]]:
        """Read a table of dict data from the file.

        Reading is not supported for mformat based classes.
        """
        _ = box  # avoid unused variable warning
        msg = 'Reading is not supported for mformat based classes.'
        raise CapabilityNotSupported(msg)
        # pylint: disable=unreachable
        return ReadResult(data=DictData(), headings=[], last_read_row=0)
