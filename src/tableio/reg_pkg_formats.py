#! /usr/local/bin/python3
"""Formats defined in the package for registration with the factory.

The function in this module returns a list of TableIO subclasses
defined in this package. The returned classes are registered with
the factory during the factory's initialization.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from tableio.tableio_mformat import TableIOMformatHtml, TableIOMformatMd, \
    TableIOMformatRst, TableIOMformatTxt, TableIOMformatLatex, \
    TableIOMformatDocx, TableIOMformatOdt, TableIOMformatPdf, \
    TableIOMformatRtf
from tableio.tableio_csv import TableIOCsv
from tableio.tableio_excel_openpyxl import TableIOExcelOpenPyXL
from tableio.tableio_ods_odfdo import TableIOOdsOdfdo
from tableio.tableio import TableIO


def register_formats_in_pkg() -> list[type[TableIO]]:
    """Get formats defined in the package to register with the factory."""
    ret: list[type[TableIO]] = [TableIOMformatHtml, TableIOMformatMd,
                                TableIOMformatRst, TableIOMformatTxt,
                                TableIOMformatLatex, TableIOMformatDocx,
                                TableIOMformatOdt, TableIOMformatPdf,
                                TableIOMformatRtf, TableIOCsv,
                                TableIOExcelOpenPyXL, TableIOOdsOdfdo]
    return ret
