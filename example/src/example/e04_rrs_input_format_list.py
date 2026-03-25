#! /usr/bin/env python3
"""Example of how to use the tableio package."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# This example is totally equivalent to e03_rrs_input_format.py, but uses
# a list of lists instead of a list of dictionaries.

from typing import Optional
from tableio.factory import create_tableio
from tableio.optional_args import OptionalArgs
from tableio.tableio import FileAccess
from tableio.value_type import Value
from tableio.capability import Capabilities, CAP_NEEDED, CAP_NOT_USED
from .cmd_for_examples import cmd_parse_and_run_example

# Define the capabilities we want to use for this example:
# - can_write: True, we want to write the data to a file.
# - filtered_data_range: True, we want to use the filtered data range.
# TableIO readers/writers that do not support these capabilities will be
# filtered out and not used for this example.


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
def e04_rrs_input_format_list(format_name: str, output_file_name: str,
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
        # Define the data with the column order for the data to match what
        # https://www.racingrulesofsailing.org expects.
        # The values are the data to write to the file.
        # We include non-English characters in the data, to show that we
        # are not restricted to English characters.
        data: list[list[Value]] = [[
            'Class', 'Division', 'Nationality', 'MNA No.', 'Sail Number',
            'Boat Name', 'First Name', 'Last Name', 'Club Name',
            'Email', 'Phone', 'Whats App Number'],
            ['ILCA', None, 'SWE', 134567, '13456',
             'Sjöbjörn', 'Örjan', 'Äldalsåker', 'Älvsborgs Segelsällskap',
             'ingen.mottagare@exempel.se', '+46701234567', '+46701234567'],
            ['ILCA', None, 'USA', 123456, '12345',
             'Daddy\'s Money', 'John', 'Doe', 'New York Yacht Club',
             'no.receiver@example.com', '+12234567890', '+123456789'],
            ['Europe', None, 'GER', 145678, '145',
             'Viel Spaß', 'Thöß', 'Müller', 'Hamburger Segelclub',
             'keiner.empfaenger@beispiel.de', '+491234567', '+491234567']]
        # Write the data to the file.
        # We pass the data, the column order and the filtered data range.
        # The filtered data range is set to True so that human readers
        # of the resulting excel file can easily find the data they are
        # looking for.
        tableio.write_table_listdata(data, filtered_data_range=True)
    return 0


if __name__ == '__main__':
    # Parse the command line arguments and run the example.
    # We pass the capabilities we want to use for this example,
    # to the command line parser to filter out the possibility for the
    # user to specify a reader/writer that does not support
    # the capabilities.
    cmd_parse_and_run_example(example_name='e04_rrs_input_format_list',
                              func=e04_rrs_input_format_list, caps=CAPS)
