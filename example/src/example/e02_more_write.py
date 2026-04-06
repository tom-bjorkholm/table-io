#! /usr/bin/env python3
"""Show several ways to write formatted table data."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
from datetime import datetime, timedelta
from tableio import CAP_IGNORABLE, CAP_NEEDED, CAP_NOT_USED, \
    Capabilities, Color, DictData, FileAccess, Fmt, FmtDictData, \
    FmtDictRow, FmtListData, FmtListRow, ListData, OptionalArgs, \
    ValueFmt, create_tableio
from .cmd_for_examples import cmd_parse_and_run_example


# This example mainly demonstrates writing, formatting and highlights.
#
# The formatting related capabilities are marked as ignorable so the same
# example can still run on backends that support writing but cannot show
# every formatting detail.
#
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
    """Write several tables that demonstrate formatting features."""
    #
    # This example is write-only.
    #
    # Its purpose is to show several ways to represent formatted data
    # before passing that data to tableio.
    #
    with create_tableio(format_name=format_name,
                        file_name=output_file_name,
                        file_access=FileAccess.CREATE,
                        implementation=implementation_name,
                        capabilities=CAPS,
                        args=optional_args) as tableio:
        #
        # The headings divide the output file into sections so it is easier
        # for a beginner to compare the different input styles.
        #
        tableio.write_heading('Example of how to write formatted data.')
        tableio.write_heading('Formatted List data.')
        #
        # In this first section every single cell carries its own format.
        #
        # ValueFmt combines a value and a Fmt object. This is the most
        # explicit style: you decide formatting cell by cell.
        #
        data1: ListData[ValueFmt] = [
            [ValueFmt(value='Jira key', fmt=Fmt(bold=True)),
             ValueFmt(value='Type', fmt=Fmt(bold=True)),
             ValueFmt(value='Status', fmt=Fmt(bold=True, italic=True))],
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
        #
        # filtered_data_range=True asks backends that support it to mark the
        # actual table range. For spreadsheet formats this can help when a
        # user later opens the file and wants the written table area to be
        # recognized clearly.
        #
        tableio.write_table_listdata(data1, filtered_data_range=True)
        tableio.write_heading('Formatted Dict data.')
        #
        # Here each row is a dictionary keyed by column name.
        #
        # This style is useful when it is more natural to refer to columns
        # by name than by position.
        #
        data2: DictData[ValueFmt] = [
            {'Jira key': ValueFmt(value='TIO-123', fmt=Fmt(italic=True)),
             'Reporter': ValueFmt(value='John Doe', fmt=Fmt(bold=True)),
             'Assignee': ValueFmt(value='Jane Doe', fmt=Fmt(italic=True,
                                                            bold=True))},
            {'Jira key': ValueFmt(value='TIO-456', fmt=Fmt()),
             'Reporter': ValueFmt(value='Jane Doe', fmt=Fmt()),
             'Assignee': ValueFmt(value='John Doe',
                                  fmt=Fmt(italic=True,
                                          bold=True,
                                          highlight=Color.GREEN))},
            {'Jira key': ValueFmt(value='TIO-789', fmt=Fmt()),
             'Reporter': ValueFmt(value='John Doe', fmt=Fmt()),
             'Assignee': ValueFmt(value='Unassigned',
                                  fmt=Fmt(italic=True,
                                          bold=True,
                                          highlight=Color.RED))}]
        #
        # When writing dict rows, column_order decides both which columns
        # appear and in what order they are written.
        #
        column_order2: list[str] = ['Jira key', 'Assignee', 'Reporter']
        #
        # first_row_format styles the generated header row that tableio
        # creates from the dictionary keys.
        #
        tableio.write_table_dictdata(data=data2,
                                     column_order=column_order2,
                                     filtered_data_range=True,
                                     first_row_format=Fmt(bold=True))
        tableio.write_heading('Formatted List data with FmtListRow.')
        #
        # FmtListRow moves the formatting to the row level instead.
        #
        # This is useful when the whole row should share the same look and
        # you do not want to repeat the same Fmt for every cell.
        #
        today: datetime = datetime.now()
        today = today.replace(hour=13, minute=0, second=0, microsecond=0)
        data3: FmtListData = [
            FmtListRow(values=['Jira key', 'Story Points', 'report date'],
                       fmt=Fmt(bold=True)),
            FmtListRow(values=['TIO-123', 13, today],
                       fmt=Fmt(italic=True, highlight=Color.GREEN)),
            FmtListRow(values=['TIO-456', 5,
                               today - timedelta(days=30)],
                       fmt=Fmt()),
            FmtListRow(values=['TIO-789', 3,
                               datetime.fromisoformat('2010-12-25')],
                       fmt=Fmt(italic=True, highlight=Color.RED))
        ]
        #
        # The values here also show that tableio can write more than just
        # strings. The example includes integers and datetime objects.
        #
        tableio.write_table_fmtlistdata(data3, filtered_data_range=True)
        tableio.write_heading('Formatted Dict data with FmtDictRow.')
        #
        # FmtDictRow combines the ideas from the previous two sections:
        # dictionary-shaped rows together with one format per whole row.
        #
        data4: FmtDictData = [
            FmtDictRow(values={'Jira key': 'TIO-123', 'Story Points': 13,
                               'report date': today},
                       fmt=Fmt(bold=True, highlight=Color.GREEN)),
            FmtDictRow(values={'Jira key': 'TIO-456', 'Story Points': 5,
                               'report date':
                               today - timedelta(days=30)},
                       fmt=Fmt(italic=True, highlight=Color.YELLOW)),
            FmtDictRow(values={'Jira key': 'TIO-789', 'Story Points': 3,
                               'report date':
                               datetime.fromisoformat('2010-12-25')},
                       fmt=Fmt(bold=True, italic=True, highlight=Color.RED))
        ]
        #
        # We use a different column order here to show that the written
        # table layout does not have to follow the dictionary insertion
        # order used when the rows were created.
        #
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
