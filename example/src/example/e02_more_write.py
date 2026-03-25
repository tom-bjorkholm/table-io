#! /usr/bin/env python3
"""Example of how to use the tableio package."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
from datetime import datetime, timedelta
from tableio.factory import create_tableio
from tableio.optional_args import OptionalArgs
from tableio.tableio import FileAccess
from tableio.value_type import Fmt, ValueFmt, \
    DictData, ListData, FmtListData, FmtDictData, \
    FmtListRow, FmtDictRow
from tableio.color import Color
from tableio.capability import Capabilities, CAP_NEEDED, CAP_NOT_USED, \
    CAP_IGNORABLE
from .cmd_for_examples import cmd_parse_and_run_example


CAPS = Capabilities(
    can_write=CAP_NEEDED,
    can_read=CAP_NOT_USED,
    can_fmt_row=CAP_IGNORABLE,
    can_fmt_value=CAP_IGNORABLE,
    filtered_data_range=CAP_IGNORABLE,
    can_write_box=CAP_NOT_USED,
    can_read_box=CAP_NOT_USED,
    can_write_highlight=CAP_IGNORABLE
)


# pylint: disable=duplicate-code
def e02_more_write(format_name: str, output_file_name: str,
                   implementation_name: Optional[str],
                   optional_args: OptionalArgs) -> int:
    """Write a table to show how to use the more capabilities."""
    with create_tableio(format_name=format_name,
                        file_name=output_file_name,
                        file_access=FileAccess.CREATE,
                        implementation=implementation_name,
                        capabilities=CAPS,
                        args=optional_args) as tableio:
        tableio.write_heading('Example of how to write formatted data.')
        tableio.write_heading('Formatted List data.')
        data1: ListData[ValueFmt] = [
            [ValueFmt(value='Jira key', fmt=Fmt(bold=True)),
             ValueFmt(value='Type', fmt=Fmt(bold=True)),
             ValueFmt(value='Satus', fmt=Fmt(bold=True, italic=True))],
            [ValueFmt(value='TIO-123', fmt=Fmt(italic=True)),
             ValueFmt(value='Task', fmt=Fmt(italic=True)),
             ValueFmt(value='In Progress', fmt=Fmt(italic=True))],
            [ValueFmt(value='TIO-456', fmt=Fmt(italic=True,
                                               highlight=Color.YELLOW)),
             ValueFmt(value='Bug', fmt=Fmt(italic=True,
                                           highlight=Color.YELLOW)),
             ValueFmt(value='To Do', fmt=Fmt(italic=True,
                                             highlight=Color.YELLOW))],
            [ValueFmt(value='TIO-789', fmt=Fmt()),
             ValueFmt(value='Story', fmt=Fmt()),
             ValueFmt(value='Delayed', fmt=Fmt(bold=True,
                                               highlight=Color.RED))],
            [ValueFmt(value='TIO-101', fmt=Fmt()),
             ValueFmt(value='Epic', fmt=Fmt()),
             ValueFmt(value='Done', fmt=Fmt(italic=True,
                                            bold=True,
                                            highlight=Color.GREEN))]]
        tableio.write_table_listdata(data1, filtered_data_range=True)
        tableio.write_heading('Formatted Dict data.')
        data2: DictData[ValueFmt] = [
            {'Jira key': ValueFmt(value='TIO-123', fmt=Fmt(italic=True)),
             'Reporter': ValueFmt(value='John Doe', fmt=Fmt(bold=True)),
             'Assgnee': ValueFmt(value='Jane Doe', fmt=Fmt(italic=True,
                                                           bold=True))},
            {'Jira key': ValueFmt(value='TIO-456', fmt=Fmt()),
             'Reporter': ValueFmt(value='Jane Doe', fmt=Fmt()),
             'Assgnee': ValueFmt(value='John Doe',
                                 fmt=Fmt(italic=True,
                                         bold=True,
                                         highlight=Color.GREEN))},
            {'Jira key': ValueFmt(value='TIO-789', fmt=Fmt()),
             'Reporter': ValueFmt(value='John Doe', fmt=Fmt()),
             'Assgnee': ValueFmt(value='Unassigned',
                                 fmt=Fmt(italic=True,
                                         bold=True,
                                         highlight=Color.RED))}]
        column_order2: list[str] = ['Jira key', 'Assgnee', 'Reporter']
        tableio.write_table_dictdata(data=data2,
                                     column_order=column_order2,
                                     filtered_data_range=True,
                                     first_row_format=Fmt(bold=True))
        tableio.write_heading('Formatted List data with FmtListRow.')
        data3: FmtListData = [
            FmtListRow(values=['Jira key', 'Story Points', 'report date'],
                       fmt=Fmt(bold=True)),
            FmtListRow(values=['TIO-123', 13, datetime.now()],
                       fmt=Fmt(italic=True, highlight=Color.GREEN)),
            FmtListRow(values=['TIO-456', 5,
                               datetime.now() - timedelta(days=30)],
                       fmt=Fmt()),
            FmtListRow(values=['TIO-789', 3,
                               datetime.fromisoformat('2010-12-25')],
                       fmt=Fmt(italic=True, highlight=Color.RED))
        ]
        tableio.write_table_fmtlistdata(data3, filtered_data_range=True)
        tableio.write_heading('Formatted Dict data with FmtDictRow.')
        data4: FmtDictData = [
            FmtDictRow(values={'Jira key': 'TIO-123', 'Story Points': 13,
                               'report date': datetime.now()},
                       fmt=Fmt(bold=True, highlight=Color.GREEN)),
            FmtDictRow(values={'Jira key': 'TIO-456', 'Story Points': 5,
                               'report date':
                               datetime.now() - timedelta(days=30)},
                       fmt=Fmt(italic=True, highlight=Color.YELLOW)),
            FmtDictRow(values={'Jira key': 'TIO-789', 'Story Points': 3,
                               'report date':
                               datetime.fromisoformat('2010-12-25')},
                       fmt=Fmt(bold=True, italic=True, highlight=Color.RED))
        ]
        column_order4: list[str] = ['Jira key', 'report date', 'Story Points']
        tableio.write_table_fmtdictdata(data=data4,
                                        column_order=column_order4,
                                        first_row_format=Fmt(bold=True),
                                        filtered_data_range=True)
    return 0
# pylint: enable=duplicate-code


if __name__ == '__main__':
    cmd_parse_and_run_example(example_name='e02_more_write',
                              func=e02_more_write, caps=CAPS)
