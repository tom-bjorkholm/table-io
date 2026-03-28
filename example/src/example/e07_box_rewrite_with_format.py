#! /usr/bin/env python3
"""Show how a returned Position can be used to build a box."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
from tableio.factory import create_tableio
from tableio.optional_args import OptionalArgs
from tableio.tableio import FileAccess, Box, Position
from tableio.value_type import Value, ListData, ValueFmt
from tableio.capability import Capabilities, CAP_NEEDED, CAP_NOT_USED
from tableio.color import Color
from tableio.value_type import Fmt
from .cmd_for_examples import cmd_parse_and_run_example


CAPS = Capabilities(
    can_write=CAP_NEEDED,
    can_read=CAP_NEEDED,
    can_fmt_row=CAP_NOT_USED,
    can_fmt_value=CAP_NEEDED,
    filtered_data_range=CAP_NOT_USED,
    can_write_box=CAP_NEEDED,
    can_read_box=CAP_NEEDED,
    can_write_highlight=CAP_NEEDED,
    multi_sheet=CAP_NOT_USED
)


def build_labelled_table() -> ListData[Value]:
    """Build a 10x10 table where each cell shows its coordinates."""
    return [
        [f'r{row}c{column}' for column in range(10)]
        for row in range(10)]


def build_bold_red_copy(data: ListData[Value]) -> ListData[ValueFmt]:
    """Return the same values wrapped in a bold red format."""
    result: ListData[ValueFmt] = []
    for row in data:
        result_row: list[ValueFmt] = []
        for value in row:
            result_row.append(ValueFmt(
                value=value,
                fmt=Fmt(bold=True, highlight=Color.RED)))
        result.append(result_row)
    return result


# pylint: disable=duplicate-code
def e07_box_rewrite_with_format(format_name: str, output_file_name: str,
                                implementation_name: Optional[str],
                                optional_args: OptionalArgs) -> int:
    """Rewrite a small box in place using formatting.

    This example shows another very useful pattern:
    1. Write a table and keep the returned Position.
    2. Use that Position to calculate where the table ended.
    3. Build a box from those coordinates.
    4. Read the boxed data.
    5. Write the same values back into the same box, now with formatting.
    """
    table_data = build_labelled_table()
    with create_tableio(format_name=format_name,
                        file_name=output_file_name,
                        file_access=FileAccess.CREATE,
                        implementation=implementation_name,
                        capabilities=CAPS,
                        args=optional_args) as tableio:
        #
        # CREATE mode allows writing and then reading back from the same
        # open file. That lets us keep the whole demonstration inside one
        # context manager.
        #
        table_end: Position = tableio.write_table_listdata(table_data)
        #
        # table_end is the last cell of the 10x10 table.
        #
        # For a table that started at row 0, column 0, the lower-left 2x2
        # box is:
        # - the last two rows
        # - the first two columns
        #
        # bottom and right are exclusive, so bottom is last_row + 1 and
        # right is 2.
        #
        lower_left_box = Box(top=table_end.row - 1,
                             left=0,
                             bottom=table_end.row + 1,
                             right=2)
        #
        # Read the existing values from that box.
        #
        boxed_result = tableio.read_table_listdata(box=lower_left_box)
        #
        # Wrap the values in ValueFmt so we can apply formatting while
        # keeping the original cell values unchanged.
        #
        formatted_box = build_bold_red_copy(boxed_result.data)
        #
        # Write the formatted values back into exactly the same rectangle.
        #
        # Because the write uses the same box, the values stay in place but
        # now appear bold with a red highlight.
        #
        tableio.write_table_listdata(formatted_box, box=lower_left_box)
    return 0
# pylint: enable=duplicate-code


if __name__ == '__main__':
    cmd_parse_and_run_example(example_name='e07_box_rewrite_with_format',
                              func=e07_box_rewrite_with_format, caps=CAPS)
