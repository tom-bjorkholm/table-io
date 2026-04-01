#! /usr/bin/env python3
"""Write dict-shaped data in the column order expected by RRS."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# This example shows two things not demonstrated in the earlier examples:
# - The Excel output produced by tableio can be used as input for software
#   other than Excel. The Excel file produced by this example has been
#   imported at the RRS website:
#   https://www.racingrulesofsailing.org
# - Non-English characters can be used in the data.

from typing import Optional
from tableio import CAP_NEEDED, CAP_NOT_USED, Capabilities, DictData, \
    FileAccess, OptionalArgs, Value, create_tableio
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
    """Write dict-shaped data in the column order expected by RRS."""
    # Create the tableio object with the factory.
    # We pass the capabilities needed for this example so the factory can
    # filter out readers and writers that do not support them.
    # Use the TableIO object as a context manager for writing data.
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
        # filtered_data_range=True helps human readers of the resulting
        # Excel file to easily find the data they are
        # looking for.
        tableio.write_table_dictdata(data1, column_order=column_order,
                                     filtered_data_range=True)
    return 0


if __name__ == '__main__':
    # Parse the command line and run the example.
    # The shared parser uses CAPS so it can hide backends that do not
    # support the features demonstrated here.
    cmd_parse_and_run_example(example_name='e03_rrs_input_format',
                              func=e03_rrs_input_format, caps=CAPS)
