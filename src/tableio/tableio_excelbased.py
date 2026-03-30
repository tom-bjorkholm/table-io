#! /usr/bin/env python3
"""Intermediate base class for Excel-based file formats."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Callable, Optional, Sequence
from mformat.mformat import PathLike
from tableio.tableio import FileAccess
from tableio.tableio_spreadsheetbased import TableIOSpreadsheetBased, \
    excel_column_name


class TableIOExcelBased(TableIOSpreadsheetBased):
    """Intermediate TableIO base class for Excel-based file formats.

    This class is used to provide a base class for Excel-based
    file formats. It is not intended to be used directly, but rather
    to be subclassed by a specific Excel-based file format
    such as Excel or Open Document Spreadsheet.

    The main purpose of this class is to provide a place where common
    functionality for Excel-based file formats can be implemented.
    This class starts out empty, but whenever common functionality
    is detected it should be refactored into this class.
    """

    _DATETIME_NUMBER_FORMAT = 'yyyy-mm-dd hh:mm:ss'
    """Excel number format used for datetime values."""

    def __init__(self, file_name: PathLike,
                 file_access: FileAccess,
                 file_exists_callback: Optional[Callable[[str], None]]
                 = None):
        """Initialize the TableIO_SpreadsheetBased class.

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
        super().__init__(file_name=file_name,
                         file_access=file_access,
                         file_exists_callback=file_exists_callback)

    @classmethod
    def file_name_extension(cls) -> str:
        """Return the standard file name extension for Excel files."""
        return '.xlsx'

    @classmethod
    def _datetime_number_format(cls) -> str:
        """Return the Excel number format used for datetime values."""
        return cls._DATETIME_NUMBER_FORMAT

    @staticmethod
    def _excel_column_name(column: int) -> str:
        """Return the Excel A1 column name for one zero-based column."""
        return excel_column_name(column)

    @classmethod
    def _excel_cell_ref(cls, row: int, column: int) -> str:
        """Return one Excel A1 cell reference for zero-based coordinates."""
        return f'{cls._excel_column_name(column)}{row + 1}'

    @classmethod
    def _excel_range_ref(cls, top: int, left: int,
                         bottom: int, right: int) -> str:
        """Return one Excel A1 range string for zero-based bounds."""
        start = cls._excel_cell_ref(top, left)
        end = cls._excel_cell_ref(bottom - 1, right - 1)
        return f'{start}:{end}'

    @staticmethod
    def _filtered_table_header(value: object, index: int) -> str:
        """Return the normalized Excel table header for one cell value."""
        if isinstance(value, str) and value != '':
            return value
        if value is None:
            return f'Column{index + 1}'
        return str(value)

    @classmethod
    def _filtered_table_headers(cls, values: Sequence[object]) -> list[str]:
        """Return normalized Excel table headers for one header row."""
        return [cls._filtered_table_header(value, index)
                for index, value in enumerate(values)]
