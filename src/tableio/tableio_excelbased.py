#! /usr/bin/env python3
"""Intermediate base class for Excel-based file formats."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Callable, Optional
from mformat.mformat import PathLike
from tableio.tableio import FileAccess
from tableio.tableio_spreadsheetbased import TableIOSpreadsheetBased


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
