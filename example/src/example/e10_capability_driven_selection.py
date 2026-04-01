#! /usr/bin/env python3
"""Show how capability requests influence factory matching."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
from tableio import CAP_IGNORABLE, CAP_NEEDED, CAP_NOT_USED, \
    Capabilities, Color, FileAccess, Fmt, FmtListData, FmtListRow, \
    ListData, OptionalArgs, Value, create_tableio, \
    list_implementations_tableio, list_registered_tableio
from tableio.capability import SingleCapability, Strictness
from .cmd_for_examples import cmd_parse_and_run_example
from .write_writer_info import write_writer_info


PREFERRED_CAPS = Capabilities(
    can_write=CAP_NEEDED,
    can_read=CAP_NOT_USED,
    can_fmt_row=CAP_IGNORABLE,
    can_fmt_value=CAP_NOT_USED,
    filtered_data_range=CAP_IGNORABLE,
    can_write_box=CAP_NOT_USED,
    can_read_box=CAP_NOT_USED,
    can_write_highlight=CAP_IGNORABLE,
    multi_sheet=CAP_NOT_USED
)

STRICT_COMPARISON_CAPS = Capabilities(
    can_write=CAP_NEEDED,
    can_read=CAP_NOT_USED,
    can_fmt_row=CAP_NEEDED,
    can_fmt_value=CAP_NOT_USED,
    filtered_data_range=CAP_NEEDED,
    can_write_box=CAP_NOT_USED,
    can_read_box=CAP_NOT_USED,
    can_write_highlight=CAP_NEEDED,
    multi_sheet=CAP_NOT_USED
)


def capability_request_text(capability: SingleCapability) -> str:
    """Describe a capability request from the caller's point of view."""
    if not capability.supported:
        return 'not used'
    if capability.strictness == Strictness.STRICT:
        return 'needed'
    return 'wanted, but ignorable'


def build_capability_request_table(caps: Capabilities) -> ListData[Value]:
    """Build a table that describes one capability request."""
    data: ListData[Value] = [['Capability', 'Request']]
    for name, capability in zip(caps._fields, caps):
        data.append([name, capability_request_text(capability)])
    return data


def build_name_table(title: str, names: list[str]) -> ListData[Value]:
    """Build a simple one-column table from a list of names."""
    data: ListData[Value] = [[title]]
    if not names:
        data.append(['(none)'])
        return data
    for name in names:
        data.append([name])
    return data


def build_demo_table() -> FmtListData:
    """Build a small row-formatted table for the preferred-capability demo."""
    return [
        FmtListRow(values=['Task', 'Status', 'Why this row is interesting'],
                   fmt=Fmt(bold=True)),
        FmtListRow(values=['Create writer', 'Works everywhere',
                           'Only can_write is strictly required'],
                   fmt=Fmt()),
        FmtListRow(values=['Use formatting', 'Best effort',
                           'Bold and highlight may be ignored'],
                   fmt=Fmt(bold=True, highlight=Color.YELLOW)),
        FmtListRow(values=['Use filtered range', 'Best effort',
                           'Spreadsheet backends can honor it'],
                   fmt=Fmt(italic=True))]


# pylint: disable=duplicate-code
def e10_capability_driven_selection(
        format_name: str, output_file_name: str,
        implementation_name: Optional[str],
        optional_args: OptionalArgs) -> int:
    """Show how capability requests affect factory matching.

    This example uses two related capability sets:
    - PREFERRED_CAPS: capabilities we would like to use, but some of them
      are allowed to be ignored.
    - STRICT_COMPARISON_CAPS: the same extra features, but now they are
      all required.

    By comparing the matching formats for these two requests, a new
    programmer can see how CAP_NEEDED and CAP_IGNORABLE change the factory's
    matching behavior.
    """
    preferred_formats = list_registered_tableio(
        capabilities=PREFERRED_CAPS, empty_is_ok=True)
    preferred_impls = list_implementations_tableio(
        capabilities=PREFERRED_CAPS, empty_is_ok=True)
    strict_formats = list_registered_tableio(
        capabilities=STRICT_COMPARISON_CAPS, empty_is_ok=True)
    strict_impls = list_implementations_tableio(
        capabilities=STRICT_COMPARISON_CAPS, empty_is_ok=True)
    with create_tableio(format_name=format_name,
                        file_name=output_file_name,
                        file_access=FileAccess.CREATE,
                        implementation=implementation_name,
                        capabilities=PREFERRED_CAPS,
                        args=optional_args) as tableio:
        #
        # First explain the capability request that this example actually
        # uses when it creates the writer.
        #
        tableio.write_heading('Preferred capability request.')
        tableio.write_table_listdata(
            build_capability_request_table(PREFERRED_CAPS))
        #
        # Then show which formats and implementations match that request.
        #
        tableio.write_heading('Formats matching the preferred request.')
        tableio.write_table_listdata(
            build_name_table('Matching formats', preferred_formats))
        tableio.write_heading(
            'Implementations matching the preferred request.')
        tableio.write_table_listdata(
            build_name_table('Matching implementations', preferred_impls))
        #
        # Now compare that with a stricter request. This is the same general
        # idea, but the extra features are now mandatory instead of optional.
        #
        tableio.write_heading('Stricter capability request for comparison.')
        tableio.write_table_listdata(
            build_capability_request_table(STRICT_COMPARISON_CAPS))
        tableio.write_heading('Formats matching the stricter request.')
        tableio.write_table_listdata(
            build_name_table('Strict matching formats', strict_formats))
        tableio.write_heading(
            'Implementations matching the stricter request.')
        tableio.write_table_listdata(
            build_name_table('Strict matching implementations',
                             strict_impls))
        #
        # Also show which writer the factory actually created for this run.
        #
        tableio.write_heading('Information about the writer used in this run.')
        write_writer_info(tableio,
                          requested_format_name=format_name,
                          requested_implementation=implementation_name)
        #
        # Finally write a small table using the same preferred capabilities.
        #
        # Some formats will show bold text, highlight and a filtered data
        # range. Other formats may ignore parts of that request. That is
        # exactly what CAP_IGNORABLE is for.
        #
        tableio.write_heading('A table written with the preferred request.')
        tableio.write_table_fmtlistdata(build_demo_table(),
                                        filtered_data_range=True)
    return 0
# pylint: enable=duplicate-code


if __name__ == '__main__':
    cmd_parse_and_run_example(
        example_name='e10_capability_driven_selection',
        func=e10_capability_driven_selection, caps=PREFERRED_CAPS)
