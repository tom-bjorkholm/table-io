#! /usr/bin/env python3
"""Write a table, read it back and verify the round-trip."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
from tableio import CAP_NEEDED, CAP_NOT_USED, Capabilities, FileAccess, \
    ListDataSeq, OptionalArgs, OptionalArgsDict, Value, create_tableio
from .cmd_for_examples import cmd_parse_and_run_example
from .write_writer_info import write_writer_info


# pylint: disable=duplicate-code
# This example needs both write and read support.
#
# The formatting and box related capabilities are marked as not used
# because this example is intentionally kept simple.
#
CAPS = Capabilities(can_write=CAP_NEEDED, can_read=CAP_NEEDED,
                    can_fmt_row=CAP_NOT_USED, can_fmt_value=CAP_NOT_USED,
                    filtered_data_range=CAP_NOT_USED,
                    can_write_box=CAP_NOT_USED, can_read_box=CAP_NOT_USED,
                    can_write_highlight=CAP_NOT_USED)


# pylint: disable=duplicate-code
def e01_simple_read_write(format_name: str, output_file_name: str,
                          implementation_name: Optional[str],
                          optional_args: OptionalArgs) -> int:
    """Write a small table and read it back again."""
    #
    # We use two headings so the example shows that headings are separate
    # from the table data itself.
    #
    head1 = 'Example of how to use the tableio package.'
    head2 = 'A subheading.'
    #
    # CSV is a special case for read-back examples.
    #
    # CSV does not store rich type information, so reading numbers back can
    # depend on how values were written. Using csv_quoting='nonnumeric'
    # keeps strings quoted and numeric values unquoted, which makes this
    # round-trip example easier for a beginner to understand.
    #
    if format_name.lower() == 'csv':
        if optional_args:
            optional_args['csv_quoting'] = 'nonnumeric'
        else:
            optional_args = OptionalArgsDict(csv_quoting='nonnumeric')
    #
    # The table data itself is a simple 2x2 list of rows.
    #
    # A beginner can read this example as:
    # each inner list is one row, and the values in that row become cells.
    #
    data: ListDataSeq[Value] = [['Hello', 'World'], [1, 3.14]]
    #
    # Open the output file in CREATE mode.
    #
    # Using the tableio object as a context manager means the file is
    # closed automatically when we leave the with block.
    #
    with create_tableio(format_name=format_name, file_name=output_file_name,
                        file_access=FileAccess.CREATE,
                        implementation=implementation_name, capabilities=CAPS,
                        args=optional_args) as tableio:
        #
        # Headings are written before the table.
        #
        # When we later read the table back with read_table_listdata(),
        # these headings are returned separately from the table data.
        #
        tableio.write_heading(head1)
        tableio.write_heading(head2)
        #
        # write_table_listdata() is the simplest way to write a table when
        # the data already exists as a list of rows.
        #
        tableio.write_table_listdata(data)
        #
        # This extra heading and helper output are only there to make the
        # produced example file more informative when a programmer opens it.
        #
        tableio.write_heading('Writer information:')
        write_writer_info(tableio, requested_format_name=format_name,
                          requested_implementation=implementation_name)
    #
    # Reopen the same file in READ mode to show the matching read API.
    #
    with create_tableio(format_name=format_name, file_name=output_file_name,
                        file_access=FileAccess.READ,
                        implementation=implementation_name, capabilities=CAPS,
                        args=optional_args) as tableio:
        #
        # read_table_listdata() returns an object that contains both the
        # headings found before the table and the table data itself.
        #
        read_data = tableio.read_table_listdata()
    #
    # These asserts are a simple self-check for the example program.
    #
    # If they pass, the example has shown a successful write-then-read
    # round-trip through the selected tableio backend.
    #
    assert read_data.headings == [head1, head2]
    assert read_data.data == data
    return 0
# pylint: enable=duplicate-code


if __name__ == '__main__':
    cmd_parse_and_run_example(example_name='e01_simple_read_write',
                              func=e01_simple_read_write, caps=CAPS)
