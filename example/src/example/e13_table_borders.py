#! /usr/local/bin/python3
"""Example of using table borders."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
from tableio import create_tableio, FileAccess, Capabilities, \
    TableBorderStyle, CAP_NEEDED, CAP_IGNORABLE, CAP_NOT_USED, \
    OptionalArgs, ValueFmt, ListData, DictData, Fmt, Color, \
    FmtListData, FmtDictData, FmtListRow, FmtDictRow
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


def e13_table_borders(format_name: str, output_file_name: str,
                      implementation_name: Optional[str],
                      optional_args: OptionalArgs) -> int:
    """Show example of using table borders.

    This example shows the four write_table_*() calls that accept
    border_style=... and demonstrates how different TableBorderStyle values
    look on the written tables.
    """
    # The setup is the same as in the earlier examples.
    # As usual, we call the factory to create a TableIO object,
    # and use it as a context manager to ensure that the file is closed.
    # The new thing to look for in this file is border_style=... in the
    # table-writing calls below.
    # pylint: disable=duplicate-code
    with create_tableio(format_name=format_name, file_name=output_file_name,
                        file_access=FileAccess.CREATE,
                        implementation=implementation_name, capabilities=CAPS,
                        args=optional_args) as tio:
        # pylint: enable=duplicate-code
        tio.write_heading('Table border API examples')
        # 1. write_table_listdata()
        # Pass a TableBorderStyle enum member to border_style=... in the
        # same call where you write the table data.
        data1: ListData[ValueFmt] = [
            [ValueFmt(value='A-Column', fmt=Fmt(bold=True)),
             ValueFmt(value='B-Column', fmt=Fmt(bold=True)),
             ValueFmt(value='C-Column', fmt=Fmt(bold=True))],
            [ValueFmt(value=3.1415, fmt=Fmt(italic=True)),
             ValueFmt(value=2.7182, fmt=Fmt()),
             ValueFmt(value=1.4142, fmt=Fmt(highlight=Color.YELLOW))],
            [ValueFmt(value=True, fmt=Fmt(bold=True)),
             ValueFmt(value=False, fmt=Fmt()),
             ValueFmt(value='Lower right', fmt=Fmt(highlight=Color.RED))]]
        # The heading in the output tells the reader which API call and
        # border style produced the next table.
        tio.write_heading('write_table_listdata() with '
                          'OUTER_FIRST_ROW_THICK_INNER_THIN')
        # The table data is written exactly as usual.
        # The only border-specific part is border_style=...
        tio.write_table_listdata(
            data=data1,
            border_style=TableBorderStyle.OUTER_FIRST_ROW_THICK_INNER_THIN)
        # 2. write_table_dictdata()
        # Dict-shaped tables use the same border_style=... keyword.
        data2: DictData[ValueFmt] = [
            {'A-Col': ValueFmt(value='Upper left', fmt=Fmt(italic=True)),
             'B-Col': ValueFmt(value=1.4142, fmt=Fmt()),
             'C-Col': ValueFmt(value='Upper right',
                               fmt=Fmt(highlight=Color.GREEN))},
            {'A-Col': ValueFmt(value=3.1415, fmt=Fmt(italic=True)),
             'B-Col': ValueFmt(value=2.7182, fmt=Fmt()),
             'C-Col': ValueFmt(value='Right middle',
                               fmt=Fmt(highlight=Color.YELLOW))},
            {'A-Col': ValueFmt(value=True, fmt=Fmt(bold=True)),
             'B-Col': ValueFmt(value=False, fmt=Fmt()),
             'C-Col': ValueFmt(value='Lower right',
                               fmt=Fmt(highlight=Color.RED))}]
        tio.write_heading('write_table_dictdata() with '
                          'OUTER_THICK_INNER_THIN')
        # first_row_format=... and border_style=... can be used together in
        # the same write_table_dictdata() call.
        tio.write_table_dictdata(
            data=data2, column_order=['A-Col', 'B-Col', 'C-Col'],
            first_row_format=Fmt(bold=True),
            border_style=TableBorderStyle.OUTER_THICK_INNER_THIN)
        # 3. write_table_fmtlistdata()
        # Row-formatted list data still uses the same border_style=...
        # argument when you want table borders.
        data3: FmtListData = [
            FmtListRow(values=['A-Column', 'B-Column', 'C-Column'],
                       fmt=Fmt(bold=True)),
            FmtListRow(values=[3.1415, 2.7182, 1.4142], fmt=Fmt(italic=True)),
            FmtListRow(values=[True, False, 'Lower right'],
                       fmt=Fmt(highlight=Color.RED))]
        tio.write_heading('write_table_fmtlistdata() with ALL_THIN')
        tio.write_table_fmtlistdata(data=data3,
                                    border_style=TableBorderStyle.ALL_THIN)
        # 4. write_table_fmtdictdata()
        # The border style is chosen the same way here too.
        data4: FmtDictData = [
            FmtDictRow(values={'A-Col': 'Upper left', 'B-Col': 1.4142,
                               'C-Col': 'Upper right'},
                       fmt=Fmt(italic=True)),
            FmtDictRow(values={'A-Col': 3.1415, 'B-Col': 2.7182,
                               'C-Col': 'Right middle'},
                       fmt=Fmt()),
            FmtDictRow(values={'A-Col': True, 'B-Col': False,
                               'C-Col': 'Lower right'},
                       fmt=Fmt(highlight=Color.RED))]
        tio.write_heading('write_table_fmtdictdata() with OUTER_THICK')
        tio.write_table_fmtdictdata(data=data4,
                                    column_order=['A-Col', 'B-Col', 'C-Col'],
                                    first_row_format=Fmt(bold=True),
                                    border_style=TableBorderStyle.OUTER_THICK)
    return 0


if __name__ == '__main__':
    cmd_parse_and_run_example(example_name='e13_table_borders',
                              func=e13_table_borders, caps=CAPS)
