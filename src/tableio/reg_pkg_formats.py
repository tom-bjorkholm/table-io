#! /usr/local/bin/python3
"""Register the formats defined in the package with the factory."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from tableio.tableio_mformat import TableIOMformatHtml, TableIOMformatMd, \
    TableIOMformatRst, TableIOMformatTxt, TableIOMformatLatex, \
    TableIOMformatDocx, TableIOMformatOdt, TableIOMformatPdf, \
    TableIOMformatRtf
from tableio.tableio_csv import TableIOCsv
from tableio.tableio import TableIO


def register_formats_in_pkg() -> list[type[TableIO]]:
    """Get formats defined in the package to register with the factory."""
    ret: list[type[TableIO]] = [TableIOMformatHtml, TableIOMformatMd,
                                TableIOMformatRst, TableIOMformatTxt,
                                TableIOMformatLatex, TableIOMformatDocx,
                                TableIOMformatOdt, TableIOMformatPdf,
                                TableIOMformatRtf, TableIOCsv]
    return ret
