#! /usr/bin/env python3
"""Example of how to use the tableio package."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
from tableio.factory import create_tableio
from tableio.optional_args import OptionalArgs
from tableio.tableio import FileAccess
from tableio.value_type import Value, ListDataSeq
from tableio.capability import Capabilities, SingleCapability, Strictness
from .cmd_for_examples import cmd_parse_and_run_example

CAP_USED = SingleCapability(supported=True, strictness=Strictness.STRICT)
CAP_NOT_USED = SingleCapability(supported=False, strictness=Strictness.IGNORE)

CAPS = Capabilities(
    can_write=CAP_USED,
    can_read=CAP_USED,
    can_fmt_row=CAP_NOT_USED,
    can_fmt_value=CAP_NOT_USED,
    filtered_data_range=CAP_NOT_USED,
    can_write_box=CAP_NOT_USED,
    can_read_box=CAP_NOT_USED,
    can_write_highlight=CAP_NOT_USED
)


def e01_simple_read_write(format_name: str, output_file_name: str,
                          implementation_name: Optional[str],
                          optional_args: OptionalArgs) -> int:
    """Write a table and read it back to verify round-trip."""
    head1 = 'Example of how to use the tableio package.'
    head2 = 'A subheading.'
    data: ListDataSeq[Value] = [['Hello', 'World'], ['foo', 'bar']]
    with create_tableio(format_name=format_name,
                        file_name=output_file_name,
                        file_access=FileAccess.CREATE,
                        implementation=implementation_name,
                        capabilities=CAPS,
                        args=optional_args) as tableio:
        tableio.write_heading(head1)
        tableio.write_heading(head2)
        tableio.write_table_listdata(data)
    with create_tableio(format_name=format_name,
                        file_name=output_file_name,
                        file_access=FileAccess.READ,
                        implementation=implementation_name,
                        capabilities=CAPS,
                        args=optional_args) as tableio:
        read_data = tableio.read_table_listdata()
    assert read_data.headings == [head1, head2]
    assert read_data.data == data
    return 0


if __name__ == '__main__':
    cmd_parse_and_run_example(example_name='e01_simple_read_write',
                              func=e01_simple_read_write, caps=CAPS)
