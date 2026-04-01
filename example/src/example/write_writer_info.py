#! /usr/bin/env python3
"""Write information about the writer to a file."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
from tableio import ListData, TableIO, Value
from tableio.capability import capability_to_str


def write_writer_info(tableio: TableIO,
                      requested_format_name: Optional[str] = None,
                      requested_implementation: Optional[str] = None) -> None:
    """Write a small table that describes the chosen writer backend."""
    data: ListData[Value] = [
        ['Attribute', 'Value', 'Requested value'],
        ['Type name', tableio.get_description().format_name,
         requested_format_name if requested_format_name else '(none)'],
        ['Implementation', tableio.get_description().implementation,
         requested_implementation if requested_implementation else '(none)'],
        ['Priority', tableio.get_description().priority, ''],
    ]
    if tableio.get_description().mandatory_args:
        for arg in tableio.get_description().mandatory_args:
            data.append(['Mandatory argument', arg, ''])
    else:
        data.append(['Mandatory arguments', '(none)', ''])
    if tableio.get_description().optional_args:
        for arg in tableio.get_description().optional_args:
            data.append(['Optional argument', arg, ''])
    else:
        data.append(['Optional arguments', '(none)', ''])
    caps = tableio.get_description().capabilities
    for key, value in zip(caps._fields, caps):
        data.append(['Capability ' + str(key), capability_to_str(value), ''])
    tableio.write_table_listdata(data)
