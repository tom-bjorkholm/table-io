#! /usr/bin/env python3
"""Example of how to use the tableio package."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# This example is showing 2 things not demonstated in the earlier examples:
# - That the excel output produced by tableio can be used for software
#   other than excel, that expects an excel file as input. The excel file
#   produced by this example has been imprted at the RRS website:
#   https://www.racingrulesofsailing.org
# - That non-English characters can be used in the data.

from typing import Optional
from tableio.factory import create_tableio
from tableio.optional_args import OptionalArgs
from tableio.tableio import FileAccess
from tableio.value_type import Value, DictData
from tableio.capability import Capabilities, CAP_NEEDED, CAP_NOT_USED
from .cmd_for_examples import cmd_parse_and_run_example

# Define the capabilities we want to use for this example:
# - can_write: True, we want to write the data to a file.
# - filtered_data_range: True, we want to use the filtered data range.
# TableIO readers/writers that do not support these capabilities will be
# filtered out and not used for this example.


# pylint: disable=duplicate-code

CAPS = Capabilities(
    can_write=CAP_NEEDED,
    can_read=CAP_NOT_USED,
    can_fmt_row=CAP_NOT_USED,
    can_fmt_value=CAP_NOT_USED,
    filtered_data_range=CAP_NEEDED,
    can_write_box=CAP_NOT_USED,
    can_read_box=CAP_NOT_USED,
    can_write_highlight=CAP_NOT_USED
)


# pylint: disable=duplicate-code
def e03_rrs_input_format(format_name: str, output_file_name: str,
                         implementation_name: Optional[str],
                         optional_args: OptionalArgs) -> int:
    """Write a table to show how to use the more capabilities."""
    # Create the tableio object with the factory.
    # We pass the capabilities we want to use for this example,
    # to the factory to filter out readers/writers that do not support
    # the capabilities.
    # Use the TableIO object as context manageer for writing data.
    with create_tableio(format_name=format_name,
                        file_name=output_file_name,
                        file_access=FileAccess.CREATE,
                        implementation=implementation_name,
                        capabilities=CAPS,
                        args=optional_args) as tableio:
        # Define the column order for the data to match what
        # https://www.racingrulesofsailing.org expects.
        column_order: list[str] = [
            'Class', 'Division', 'Nationality', 'MNA No.', 'Sail Number',
            'Boat Name', 'First Name', 'Last Name', 'Club Name', 'Email',
            'Phone', 'Whats App Number']
        # Define the data to write to the file.
        # In this example we use a list of dictionaries.
        # The keys of the dictionaries are the column names.
        # The values are the data to write to the file.
        # We include non-English characters in the data, to show that we
        # are not restricted to English characters.
        data1: DictData[Value] = [
            {'Class': 'ILCA', 'Division': None, 'Nationality': 'SWE',
             'MNA No.': 134567, 'Sail Number': '13456',
             'Boat Name': 'Sjöbjörn', 'First Name': 'Örjan',
             'Last Name': 'Äldalsåker', 'Club Name': 'Älvsborgs Segelsällskap',
             'Email': 'ingen.mottagare@exempel.se', 'Phone': '+46701234567',
             'Whats App Number': '+46701234567'},
            {'Class': 'ILCA', 'Division': None, 'Nationality': 'USA',
             'MNA No.': 123456, 'Sail Number': '12345',
             'Boat Name': 'Daddy\'s Money', 'First Name': 'John',
             'Last Name': 'Doe', 'Club Name': 'New York Yacht Club',
             'Email': 'no.receiver@example.com', 'Phone': '+12234567890',
             'Whats App Number': '+123456789'},
            {'Class': 'Europe', 'Division': None, 'Nationality': 'GER',
             'MNA No.': 145678, 'Sail Number': '145',
             'Boat Name': 'Viel Spaß', 'First Name': 'Thöß',
             'Last Name': 'Müller', 'Club Name': 'Hamburger Segelclub',
             'Email': 'keiner.empfaenger@beispiel.de', 'Phone': '+491234567',
             'Whats App Number': '+491234567'},
        ]
        # Write the data to the file.
        # We pass the data, the column order and the filtered data range.
        # The filtered data range is set to True so that human readers
        # of the resulting excel file can easily find the data they are
        # looking for.
        tableio.write_table_dictdata(data1, column_order=column_order,
                                     filtered_data_range=True)
    return 0


if __name__ == '__main__':
    # Parse the command line arguments and run the example.
    # We pass the capabilities we want to use for this example,
    # to the command line parser to filter out the possibility for the
    # user to specify a reader/writer that does not support
    # the capabilities.
    cmd_parse_and_run_example(example_name='e03_rrs_input_format',
                              func=e03_rrs_input_format, caps=CAPS)
