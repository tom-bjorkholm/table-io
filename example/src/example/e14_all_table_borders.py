#! /usr/local/bin/python3
"""Example of using all table borders."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
from tableio import create_tableio, FileAccess, Capabilities, \
    TableBorderStyle, CAP_NEEDED, CAP_IGNORABLE, CAP_NOT_USED, \
    OptionalArgs, ValueFmt, ListData, Fmt, Color, Box, TableIO
from .cmd_for_examples import cmd_parse_and_run_example


# pylint: disable=duplicate-code
CAPS = Capabilities(can_write=CAP_NEEDED, can_read=CAP_NOT_USED,
                    can_fmt_row=CAP_IGNORABLE, can_fmt_value=CAP_IGNORABLE,
                    filtered_data_range=CAP_IGNORABLE,
                    can_write_box=CAP_NOT_USED, can_read_box=CAP_NOT_USED,
                    can_write_borders=CAP_NEEDED, multi_sheet=CAP_NOT_USED,
                    can_find_value_position=CAP_NOT_USED,
                    can_write_highlight=CAP_IGNORABLE)
# pylint: enable=duplicate-code


def write_border_style_example(tio: TableIO,
                               border_style: TableBorderStyle) -> None:
    """Write one sample table with the given border style.

    Args:
        tio: The tableio object to write to.
        border_style: The border style to use.
    """
    data: ListData[ValueFmt] = [
        [ValueFmt(value='A-Column', fmt=Fmt(bold=True)),
         ValueFmt(value='B-Column', fmt=Fmt(bold=True)),
         ValueFmt(value='C-Column', fmt=Fmt(bold=True))],
        [ValueFmt(value=3.1415, fmt=Fmt()),
         ValueFmt(value=2.7182, fmt=Fmt()),
         ValueFmt(value='Yellow bold', fmt=Fmt(bold=True,
                                               highlight=Color.YELLOW))],
        [ValueFmt(value=True, fmt=Fmt()),
         ValueFmt(value=False, fmt=Fmt()),
         ValueFmt(value='Red bold', fmt=Fmt(bold=True, highlight=Color.RED))],
        [ValueFmt(value='ListData[ValueFmt]', fmt=Fmt()),
         ValueFmt(value=border_style.name, fmt=Fmt()),
         ValueFmt(value='Green', fmt=Fmt(highlight=Color.GREEN))]]
    # Write a heading above each sample so the generated file becomes a
    # border-style catalog that is easy to browse visually.
    heading_pos = tio.write_heading(heading='write_table_listdata() with '
                                    f'{border_style.name}')
    # The Box places the table under that heading and shifts it one column
    # to the right. That extra left margin makes the table's left border
    # easier to see when viewing the result in Excel.
    table_box = Box(top=heading_pos.row + 2, left=1, bottom=None, right=None)
    # e14 always writes the same table shape.
    # Only border_style=... changes, so the output files let a new user
    # compare the TableBorderStyle values visually under each other.
    tio.write_table_listdata(data=data, box=table_box,
                             border_style=border_style)


def e14_all_table_borders(format_name: str, output_file_name: str,
                          implementation_name: Optional[str],
                          optional_args: OptionalArgs) -> int:
    """Show all table border styles.

    The result of this example is a file with all table border styles.
    In the resulting file(s) the user can see what the different border
    styles look like.
    """
    # The setup is the same as in the earlier examples.
    # The teaching point here is that we keep the table data fixed and only
    # vary border_style=... so the visual differences are easy to compare.
    # pylint: disable=duplicate-code
    with create_tableio(format_name=format_name, file_name=output_file_name,
                        file_access=FileAccess.CREATE,
                        implementation=implementation_name, capabilities=CAPS,
                        args=optional_args) as tio:
        # pylint: enable=duplicate-code
        tio.write_heading('Showing all table border styles')
        # Write one sample table for each enum value so the output file
        # becomes a quick visual reference for choosing a border style.
        for border_style in TableBorderStyle:
            write_border_style_example(tio=tio, border_style=border_style)
    return 0


if __name__ == '__main__':
    cmd_parse_and_run_example(example_name='e14_all_table_borders',
                              func=e14_all_table_borders, caps=CAPS)
