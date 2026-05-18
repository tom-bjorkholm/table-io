#! /usr/bin/env python3
"""Show how to work with more than one sheet in a spreadsheet file."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
from tableio import CAP_NEEDED, CAP_NOT_USED, Capabilities, FileAccess, \
    ListData, OptionalArgs, Value, create_tableio
from .cmd_for_examples import cmd_parse_and_run_example


# pylint: disable=duplicate-code
CAPS = Capabilities(can_write=CAP_NEEDED, can_read=CAP_NEEDED,
                    can_fmt_row=CAP_NOT_USED, can_fmt_value=CAP_NOT_USED,
                    filtered_data_range=CAP_NOT_USED,
                    can_write_box=CAP_NOT_USED, can_read_box=CAP_NOT_USED,
                    can_write_highlight=CAP_NOT_USED, multi_sheet=CAP_NEEDED)
# pylint: enable=duplicate-code


def build_main_sheet_table() -> ListData[Value]:
    """Build the main table for the first sheet."""
    return [
        ['Name', 'Role', 'Hours'],
        ['Alice', 'Developer', 38],
        ['Bob', 'Tester', 35],
        ['Carla', 'Project manager', 40]]


def build_sheet_info_table(first_sheet_name: str, current_sheet_name: str,
                           all_sheet_names: list[str]) -> ListData[Value]:
    """Build a small summary table about the workbook sheets."""
    return [
        ['Property', 'Value'],
        ['First sheet name', first_sheet_name],
        ['Current sheet after select_sheet()', current_sheet_name],
        ['Sheets in workbook', ', '.join(all_sheet_names)]]


# pylint: disable=duplicate-code
def e09_multi_sheet(format_name: str, output_file_name: str,
                    implementation_name: Optional[str],
                    optional_args: OptionalArgs) -> int:
    """Write to two sheets and move back and forth between them.

    This example demonstrates the basic multi-sheet workflow:
    1. Start on the default first sheet and write a table.
    2. Create and select another sheet.
    3. Write something there.
    4. Switch back to the first sheet and read from it.
    5. Switch to the second sheet again and keep writing there.

    The interesting detail is that read and write positions are tracked per
    sheet, so each sheet remembers where the next sequential operation should
    happen.
    """
    main_table = build_main_sheet_table()
    with create_tableio(format_name=format_name, file_name=output_file_name,
                        file_access=FileAccess.CREATE,
                        implementation=implementation_name, capabilities=CAPS,
                        args=optional_args) as tableio:
        #
        # Every workbook starts with one current sheet already selected.
        #
        first_sheet_name = tableio.current_sheet_name()
        tableio.write_table_listdata(main_table)
        #
        # Create and select a second sheet.
        #
        # The create=True argument means "create this sheet if it does not
        # already exist".
        #
        tableio.select_sheet('Summary', create=True)
        tableio.write_heading('Information about the workbook sheets.')
        tableio.write_table_listdata(
            build_sheet_info_table(
                first_sheet_name=first_sheet_name,
                current_sheet_name=tableio.current_sheet_name(),
                all_sheet_names=tableio.list_sheets()))
        #
        # Switch back to the original sheet and read the table we wrote
        # there earlier.
        #
        tableio.select_sheet(first_sheet_name)
        read_back = tableio.read_table_listdata()
        #
        # Switch again to the Summary sheet.
        #
        # Because write positions are remembered per sheet, the next write on
        # Summary continues after the table we already wrote there.
        #
        tableio.select_sheet('Summary')
        tableio.write_heading('Data read back from the first sheet.')
        tableio.write_table_listdata(read_back.data)
    return 0
# pylint: enable=duplicate-code


if __name__ == '__main__':
    cmd_parse_and_run_example(example_name='e09_multi_sheet',
                              func=e09_multi_sheet, caps=CAPS)
