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
CAPS = Capabilities(can_write=CAP_NEEDED,
                    can_read=CAP_NOT_USED,
                    can_fmt_row=CAP_IGNORABLE,
                    can_fmt_value=CAP_IGNORABLE,
                    filtered_data_range=CAP_IGNORABLE,
                    can_write_box=CAP_NOT_USED,
                    can_read_box=CAP_NOT_USED,
                    can_write_borders=CAP_NEEDED,
                    multi_sheet=CAP_NOT_USED,
                    can_find_value_position=CAP_NOT_USED,
                    can_write_highlight=CAP_IGNORABLE)
# pylint: enable=duplicate-code


def write_list(tio: TableIO, border_style: TableBorderStyle) -> None:
    """Write ListData[ValueFmt] with the given border style.

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
         ValueFmt(value='Red bold', fmt=Fmt(bold=True,
                                            highlight=Color.RED))],
        [ValueFmt(value='ListData[ValueFmt]', fmt=Fmt()),
         ValueFmt(value=border_style.name, fmt=Fmt()),
         ValueFmt(value='Green', fmt=Fmt(highlight=Color.GREEN))]]
    pos = tio.write_heading(heading='write_table_listdata() with '
                            f'{border_style.name}')
    box = Box(top=pos.row+2, left=1, bottom=None, right=None)
    tio.write_table_listdata(data=data, box=box, border_style=border_style)


def e14_all_table_borders(format_name: str, output_file_name: str,
                          implementation_name: Optional[str],
                          optional_args: OptionalArgs) -> int:
    """Show all table border styles.

    The result of this example is a file with all table border styles.
    In the resuling file(s) the user can see what the different border styles
    look like.
    """
    # As usual we create a tableio object and use it as a context manager.
    # pylint: disable=duplicate-code
    with create_tableio(format_name=format_name,
                        file_name=output_file_name,
                        file_access=FileAccess.CREATE,
                        implementation=implementation_name,
                        capabilities=CAPS,
                        args=optional_args) as tio:
        # pylint: enable=duplicate-code
        tio.write_heading('Showing all table border styles')
        # Loop over all table border styles and write a table for each.
        for border_style in TableBorderStyle:
            write_list(tio=tio, border_style=border_style)
    return 0


if __name__ == '__main__':
    cmd_parse_and_run_example(example_name='e14_all_table_borders',
                              func=e14_all_table_borders, caps=CAPS)
