#! /usr/bin/env python3
"""Show boxed read and boxed write in a second context manager."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
from tableio import CAP_NEEDED, CAP_NOT_USED, Box, Capabilities, \
    FileAccess, ListData, OptionalArgs, Position, Value, create_tableio
from .cmd_for_examples import cmd_parse_and_run_example


# pylint: disable=duplicate-code
CAPS = Capabilities(can_write=CAP_NEEDED, can_read=CAP_NEEDED,
                    can_fmt_row=CAP_NOT_USED, can_fmt_value=CAP_NOT_USED,
                    filtered_data_range=CAP_NOT_USED, can_write_box=CAP_NEEDED,
                    can_read_box=CAP_NEEDED, can_write_highlight=CAP_NOT_USED,
                    multi_sheet=CAP_NOT_USED)
# pylint: enable=duplicate-code


def build_large_table() -> ListData[Value]:
    """Build a 10x10 table of integers.

    We use simple integer values because they make it easy to see which
    cells were copied. For example, the value 23 means row 2, column 3.
    """
    data: ListData[Value] = []
    for row in range(10):
        data_row: list[Value] = []
        for column in range(10):
            data_row.append(row * 10 + column)
        data.append(data_row)
    return data


# pylint: disable=duplicate-code
def e06_box_read_write_update(format_name: str, output_file_name: str,
                              implementation_name: Optional[str],
                              optional_args: OptionalArgs) -> int:
    """Write a large table, then copy one box in UPDATE mode.

    The point of this example is to show a workflow that is common in real
    programs:
    1. Create a file and write a larger table.
    2. Reopen the same file in a new context manager with UPDATE access.
    3. Read a small rectangular box from the larger table.
    4. Write that same boxed data somewhere else in the same sheet.
    """
    #
    # We keep the first write very simple on purpose:
    # no headings and no extra tables.
    #
    # That means the table starts in cell (row=0, column=0), which makes
    # the later box coordinates easy to understand for a beginner.
    #
    large_table = build_large_table()
    with create_tableio(format_name=format_name, file_name=output_file_name,
                        file_access=FileAccess.CREATE,
                        implementation=implementation_name, capabilities=CAPS,
                        args=optional_args) as tableio:
        #
        # write_table_listdata() returns the position of the last cell
        # written. We keep that position because it tells us where the
        # large table ended.
        #
        large_table_end: Position = tableio.write_table_listdata(large_table)
    #
    # Open the file again in UPDATE mode.
    #
    # UPDATE is the right access mode when we want to both read existing
    # content and write new content into the same file.
    #
    with create_tableio(format_name=format_name, file_name=output_file_name,
                        file_access=FileAccess.UPDATE,
                        implementation=implementation_name, capabilities=CAPS,
                        args=optional_args) as tableio:
        #
        # Boxes use 0-based coordinates, and bottom/right are exclusive.
        #
        # So this source box reads:
        # - rows 2 and 3
        # - columns 3 and 4
        #
        # That gives us a 2x2 box.
        #
        source_box = Box(top=2, left=3, bottom=4, right=5)
        boxed_result = tableio.read_table_listdata(box=source_box)
        #
        # The large table ends at column 9.
        #
        # We want the copied 2x2 table to begin 3 columns to the right of
        # that larger table. The first free column is 10, so starting at
        # 13 leaves columns 10, 11 and 12 empty.
        #
        target_left = large_table_end.column + 4
        #
        # The copy is placed on the same rows as the source to make the
        # visual result easy to inspect in the spreadsheet.
        #
        # We deliberately set bottom=None and right=None here.
        #
        # That is a useful trick to know:
        # when bottom or right is None, the box does not force a fixed
        # size in that direction. Instead, the write uses the size of the
        # data we pass in. Because boxed_result.data is 2x2, the written
        # box will also become 2x2.
        #
        target_box = Box(top=source_box.top, left=target_left, bottom=None,
                         right=None)
        #
        # Because we pass box=target_box, the write starts exactly at that
        # rectangle instead of at the normal sequential write position.
        #
        tableio.write_table_listdata(boxed_result.data, box=target_box)
    return 0
# pylint: enable=duplicate-code


if __name__ == '__main__':
    cmd_parse_and_run_example(example_name='e06_box_read_write_update',
                              func=e06_box_read_write_update, caps=CAPS)
