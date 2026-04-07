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


def e13_table_borders(format_name: str, output_file_name: str,
                      implementation_name: Optional[str],
                      optional_args: OptionalArgs) -> int:
    """Show example of using table borders.

    This example shows how to use table borders on 4 different tables,
    demonstrating the use of different border styles and the 4 different
    methods for writing tables.
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
        tio.write_heading('Table borders usage examples')
        # Specify the data for the first table.
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
        # We right a heading to tell reader how table is written.
        tio.write_heading('ListDate[ValueFmt] with '
                          'OUTER_FIRST_ROW_THICK_INNER_THIN')
        # We just write the ListData[ValueFmt] as usual and
        # specify the border style.
        tio.write_table_listdata(
            data=data1,
            border_style=TableBorderStyle.OUTER_FIRST_ROW_THICK_INNER_THIN)
        # Specify the data for the second table.
        data2: DictData[ValueFmt] = [
            {'A-Col': ValueFmt(value='Upper left', fmt=Fmt(italic=True)),
             'B-Col': ValueFmt(value=1.4142, fmt=Fmt()),
             'C-Col': ValueFmt(value='Upper rigth',
                               fmt=Fmt(highlight=Color.GREEN))},
            {'A-Col': ValueFmt(value=3.1415, fmt=Fmt(italic=True)),
             'B-Col': ValueFmt(value=2.7182, fmt=Fmt()),
             'C-Col': ValueFmt(value='Right middle',
                               fmt=Fmt(highlight=Color.YELLOW))},
            {'A-Col': ValueFmt(value=True, fmt=Fmt(bold=True)),
             'B-Col': ValueFmt(value=False, fmt=Fmt()),
             'C-Col': ValueFmt(value='Lower right',
                               fmt=Fmt(highlight=Color.RED))}]
        # We right a heading to tell reader how table is written.
        tio.write_heading('DictData[ValueFmt] with OUTER_THICK_INNER_THIN')
        # We just write the DictData[ValueFmt] as usual and
        # specify the border style.
        tio.write_table_dictdata(
            data=data2, column_order=['A-Col', 'B-Col', 'C-Col'],
            first_row_format=Fmt(bold=True),
            border_style=TableBorderStyle.OUTER_THICK_INNER_THIN)
        # Specify the data for the third table.
        data3: FmtListData = [
            FmtListRow(values=['A-Column', 'B-Column', 'C-Column'],
                       fmt=Fmt(bold=True)),
            FmtListRow(values=[3.1415, 2.7182, 1.4142],
                       fmt=Fmt(italic=True)),
            FmtListRow(values=[True, False, 'Lower right'],
                       fmt=Fmt(highlight=Color.RED))]
        # We right a heading to tell reader how table is written.
        tio.write_heading('FmtListData[Value] with ALL_THIN')
        # We just write the FmtListData[Value] as usual and
        # specify the border style.
        tio.write_table_fmtlistdata(
            data=data3,
            border_style=TableBorderStyle.ALL_THIN)
        # Specify the data for the fourth table.
        data4: FmtDictData = [
            FmtDictRow(values={'A-Col': 'Upper left', 'B-Col': 1.4142,
                               'C-Col': 'Upper rigth'},
                       fmt=Fmt(italic=True)),
            FmtDictRow(values={'A-Col': 3.1415, 'B-Col': 2.7182,
                               'C-Col': 'Right middle'},
                       fmt=Fmt()),
            FmtDictRow(values={'A-Col': True, 'B-Col': False,
                               'C-Col': 'Lower right'},
                       fmt=Fmt(highlight=Color.RED))]
        # We right a heading to tell reader how table is written.
        tio.write_heading('FmtDictData[Value] with OUTER_THICK')
        # We just write the FmtDictData[Value] as usual and
        # specify the border style.
        tio.write_table_fmtdictdata(
            data=data4,
            column_order=['A-Col', 'B-Col', 'C-Col'],
            first_row_format=Fmt(bold=True),
            border_style=TableBorderStyle.OUTER_THICK)
    return 0


if __name__ == '__main__':
    cmd_parse_and_run_example(example_name='e13_table_borders',
                              func=e13_table_borders, caps=CAPS)
