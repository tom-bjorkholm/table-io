#! /usr/bin/env python3
"""First really simple example of how to use the tableio package."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
from datetime import datetime
from tableio.factory import create_tableio
from tableio.optional_args import OptionalArgs
from tableio.tableio import FileAccess
from tableio.value_type import Value, ListDataSeq
from .cmd_for_examples import cmd_parse_and_run_example
from .write_writer_info import write_writer_info


# pylint: disable=duplicate-code
def e00_really_simple_write_table(format_name: str,
                                  output_file_name: str,
                                  implementation_name: Optional[str],
                                  optional_args: OptionalArgs) -> int:
    """Write a table to a file."""
    # As we want to keep this really simple,
    # we ignore some command line arguments.
    #
    _ = optional_args  # pylint: disable=unused-variable
    #
    # We are going to write a table from a list of lists.
    # The list of lists is a list of rows, where each row is a list of values.
    # The values are the data to write to the file.
    #
    data: ListDataSeq[Value] = [
        ['English', 'German', 'Swedish'],
        ['Hello', 'Hallo', 'Hej'],
        ['World', 'Welt', 'Värld'],
        # And we are not restricted to strings
        # We can use numbers, booleans, and dates.
        [3.14159, True, datetime.now()]
    ]
    #
    # Create the tableio object with the factory.
    # We pass the format name and the file name to the factory.
    # We also pass the file access, which is CREATE to create a new file.
    # We do not pass any implementation name, so the factory will use the
    # default implementation for the format name.
    # We do not pass any capabilities, so the factory will use the
    # best implementation for the format name.
    # We use the context manager to ensure that the file get proper
    # file suffixes written and is properly closed when we are done.
    # If we do more complicated things it is safest to specify the
    # capabilities explicitly, as you will see in the later examples.
    #
    with create_tableio(format_name=format_name,
                        file_name=output_file_name,
                        file_access=FileAccess.CREATE) as tableio:
        #
        # Write the table to the file.
        # The tableio object has a write_table_listdata method that
        # writes the table to the file.
        #
        tableio.write_table_listdata(data)
        #
        # That was all we need to do to write the table to the file.
        #
        # As somebody may get confused by the fact that we did not
        # use the command line arguments, we will write out what
        # we actually did.
        #
        write_writer_info(tableio,
                          requested_format_name=format_name,
                          requested_implementation=implementation_name)
    #
    # When we exit the context manager, the file is closed and the
    # tableio object is destroyed.
    #
    return 0
# pylint: enable=duplicate-code


if __name__ == '__main__':
    # Call the command line parser to parse the command line arguments,
    # and then call the function above with the parsed arguments.
    cmd_parse_and_run_example(example_name='e00_really_simple_write_table',
                              func=e00_really_simple_write_table)
