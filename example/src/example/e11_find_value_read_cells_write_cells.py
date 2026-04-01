#! /usr/bin/env python3
"""Show value search, cell reads and cell writes with formatting."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
from tableio import CAP_NEEDED, CAP_NOT_USED, Box, Capabilities, Color, \
    FileAccess, Fmt, ListData, OptionalArgs, Value, ValueFmt, \
    create_tableio
from .cmd_for_examples import cmd_parse_and_run_example


# pylint: disable=duplicate-code
CAPS = Capabilities(
    can_write=CAP_NEEDED,
    can_read=CAP_NEEDED,
    can_fmt_row=CAP_NOT_USED,
    can_fmt_value=CAP_NEEDED,
    filtered_data_range=CAP_NOT_USED,
    can_write_box=CAP_NEEDED,
    can_read_box=CAP_NEEDED,
    can_write_highlight=CAP_NEEDED,
    multi_sheet=CAP_NOT_USED,
    can_find_value_position=CAP_NEEDED
)
# pylint: enable=duplicate-code


def build_economic_table() -> ListData[Value]:
    """Build a small table with fictive economic figures."""
    return [
        ['Economic entity', 2024, 2025],
        ['Revenue', 1250000, 1390000],
        ['Operating costs', 830000, 900000],
        ['Operating profit', 420000, 490000]]


def build_bold_green_cells(data: ListData[Value]) -> ListData[ValueFmt]:
    """Wrap existing values so they are written bold with green highlight."""
    result: ListData[ValueFmt] = []
    for row in data:
        result_row: list[ValueFmt] = []
        for value in row:
            result_row.append(
                ValueFmt(
                    value=value,
                    fmt=Fmt(bold=True, highlight=Color.GREEN)))
        result.append(result_row)
    return result


def e11_find_value_read_cells_write_cells(
        format_name: str,
        output_file_name: str,
        implementation_name: Optional[str],
        optional_args: OptionalArgs) -> int:
    """Find a label cell, read nearby values and rewrite them formatted."""
    #
    # The table starts in the top-left corner of the sheet.
    #
    # That keeps the example easy to inspect because the coordinates match
    # the data as written: row 0 is the header row and column 0 is the
    # label column.
    #
    economic_table = build_economic_table()
    with create_tableio(format_name=format_name,
                        file_name=output_file_name,
                        file_access=FileAccess.CREATE,
                        implementation=implementation_name,
                        capabilities=CAPS,
                        args=optional_args) as tableio:
        #
        # First write a normal table with no special formatting.
        #
        # This gives us a realistic starting point: the workbook already
        # contains data, and now we want to locate one row and update just
        # a few cells in it.
        #
        tableio.write_table_listdata(economic_table)
        #
        # find_value() searches the current sheet and returns a Box.
        #
        # Because we search for a single cell value, the returned box is a
        # 1x1 rectangle around the matching cell.
        #
        revenue_label_box = tableio.find_value('Revenue')
        #
        # This example table definitely contains 'Revenue', so a missing
        # match would mean the example data was changed unexpectedly.
        #
        assert revenue_label_box is not None
        assert revenue_label_box.bottom is not None
        assert revenue_label_box.right is not None
        #
        # The label is in column 0, and the year values are immediately to
        # the right of it.
        #
        # read_cells() needs an explicit box. We therefore build a new box
        # on the same row as the found label, starting at the column just to
        # the right of the found cell and spanning two value cells.
        #
        revenue_values_box = Box(top=revenue_label_box.top,
                                 left=revenue_label_box.right,
                                 bottom=revenue_label_box.bottom,
                                 right=revenue_label_box.right + 2)
        #
        # read_cells() returns the values exactly as a rectangular list of
        # rows. Here the result is one row with two cells: the figures for
        # 2024 and 2025.
        #
        revenue_values = tableio.read_cells(revenue_values_box)
        #
        # To keep the numeric values unchanged while changing presentation,
        # we wrap each value in ValueFmt and give it a format.
        #
        # In this example we make the revenue figures bold and give them a
        # green highlight so the updated cells stand out clearly.
        #
        formatted_revenue_values = build_bold_green_cells(revenue_values)
        #
        # write_cells() writes into the exact box we provide.
        #
        # Because we use the same box we just read from, the values stay in
        # place and only their formatting changes.
        #
        tableio.write_cells(formatted_revenue_values, box=revenue_values_box)
    return 0


if __name__ == '__main__':
    cmd_parse_and_run_example(
        example_name='e11_find_value_read_cells_write_cells',
        func=e11_find_value_read_cells_write_cells, caps=CAPS)
