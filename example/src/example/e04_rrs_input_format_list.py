#! /usr/bin/env python3
"""Write list-shaped data in the row order expected by RRS."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# This example is totally equivalent to e03_rrs_input_format.py, but uses
# a list of lists instead of a list of dictionaries.

from typing import Optional
from tableio import CAP_NEEDED, CAP_NOT_USED, Capabilities, FileAccess, \
    OptionalArgs, Value, create_tableio
from .cmd_for_examples import cmd_parse_and_run_example

# Define the capabilities we want to use for this example:
# - can_write: True, we want to write the data to a file.
# - filtered_data_range: True, we want to use the filtered data range.
# TableIO readers/writers that do not support these capabilities will be
# filtered out and not used for this example.


CAPS = Capabilities(can_write=CAP_NEEDED, can_read=CAP_NOT_USED,
                    can_fmt_row=CAP_NOT_USED, can_fmt_value=CAP_NOT_USED,
                    filtered_data_range=CAP_NEEDED, can_write_box=CAP_NOT_USED,
                    can_read_box=CAP_NOT_USED,
                    can_write_highlight=CAP_NOT_USED)


# pylint: disable=duplicate-code
def e04_rrs_input_format_list(format_name: str, output_file_name: str,
                              implementation_name: Optional[str],
                              optional_args: OptionalArgs) -> int:
    """Write list-shaped data in the row order expected by RRS."""
    # Create the tableio object with the factory.
    # We pass the capabilities needed for this example so the factory can
    # filter out readers and writers that do not support them.
    # Use the TableIO object as a context manager for writing data.
    with create_tableio(format_name=format_name, file_name=output_file_name,
                        file_access=FileAccess.CREATE,
                        implementation=implementation_name, capabilities=CAPS,
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
        # filtered_data_range=True helps human readers of the resulting
        # Excel file to easily find the data they are
        # looking for.
        tableio.write_table_listdata(data, filtered_data_range=True)
    return 0


if __name__ == '__main__':
    # Parse the command line and run the example.
    # The shared parser uses CAPS so it can hide backends that do not
    # support the features demonstrated here.
    cmd_parse_and_run_example(example_name='e04_rrs_input_format_list',
                              func=e04_rrs_input_format_list, caps=CAPS)
