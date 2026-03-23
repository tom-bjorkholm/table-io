#! /usr/bin/env python3
"""Example of how to use the tableio package."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from os import getenv
from typing import Optional
from tableio.factory import create_tableio
from tableio.optional_args import OptionalArgs
from tableio.tableio import FileAccess
from tableio.value_type import Value, DictData, ListData
from tableio.capability import Capabilities, SingleCapability, Strictness
from .cmd_for_examples import cmd_parse_and_run_example

CAP_USED = SingleCapability(supported=True, strictness=Strictness.STRICT)
CAP_NOT_USED = SingleCapability(supported=False, strictness=Strictness.IGNORE)

CAPS = Capabilities(
    can_write=CAP_USED,
    can_read=CAP_NOT_USED,
    can_fmt_row=CAP_NOT_USED,
    can_fmt_value=CAP_NOT_USED,
    filtered_data_range=CAP_USED,
    can_write_box=CAP_NOT_USED,
    can_read_box=CAP_NOT_USED,
    can_write_highlight=CAP_NOT_USED
)


# pylint: disable=duplicate-code
def e03_rrs_input_format(format_name: str, output_file_name: str,
                         implementation_name: Optional[str],
                         optional_args: OptionalArgs) -> int:
    """Write a table to show how to use the more capabilities."""
    with create_tableio(format_name=format_name,
                        file_name=output_file_name,
                        file_access=FileAccess.CREATE,
                        implementation=implementation_name,
                        capabilities=CAPS,
                        args=optional_args) as tableio:
        column_order: list[str] = [
            'Class', 'Division', 'Nationality','MNA No.', 'Sail Number',
            'Boat Name', 'First Name', 'Last Name', 'Club Name', 'Email',
            'Phone', 'Whats App Number']
        if getenv('RRS_DICT_INPUT'):
            data1: DictData[Value] = [
                {'Class': 'ILCA', 'Division': None, 'Nationality': 'USA',
                 'MNA No.': '123456', 'Sail Number': '12345',
                 'Boat Name': 'Daddy\'s Money', 'First Name': 'John',
                 'Last Name': 'Doe', 'Club Name': 'NY YC',
                 'Email': 'john.doe@example.com', 'Phone': '+123456789',
                 'Whats App Number': '+123456789'},
                {'Class': 'ILCA', 'Division': None, 'Nationality': 'SWE',
                 'MNA No.': '123456', 'Sail Number': '13456',
                 'Boat Name': 'Sjöbjörn', 'First Name': 'Örjan',
                 'Last Name': 'Äldalsåker', 'Club Name': 'Älvsborgs YC',
                 'Email': 'no.receiver@exempel.se', 'Phone': '+46701234567',
                 'Whats App Number': '+46701234567'},
            ]
            tableio.write_table_dictdata(data1, column_order=column_order,
                                         filtered_data_range=True)
        else:
            data2: ListData[Value] = [
                column_order,
                ['ILCA', None, 'USA', '123456', '12345', 'Daddy\'s Money',
                 'John', 'Doe', 'NY YC', 'john.doe@example.com',
                 '+123456789', '+123456789'],
                ['ILCA', None, 'SWE', '123456', '13456', 'Sjöbjörn',
                 'Örjan', 'Äldalsåker', 'Älvsborgs YC',
                 'no.receiver@exempel.se', '+46701234567', '+46701234567'],
            ]
            tableio.write_table_listdata(data2)
    return 0
# pylint: enable=duplicate-code


if __name__ == '__main__':
    cmd_parse_and_run_example(example_name='e03_rrs_input_format',
                              func=e03_rrs_input_format, caps=CAPS)
