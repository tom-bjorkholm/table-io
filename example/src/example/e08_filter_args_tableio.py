#! /usr/bin/env python3
"""Show how filter_args_tableio() can trim a mixed OptionalArgsDict."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from enum import IntEnum
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional
from mformat.paper_size import PaperSize
from mformat.document_class import DocumentClass
from tableio.factory import create_tableio, filter_args_tableio
from tableio.optional_args import OptionalArgs, OptionalArgsDict
from tableio.tableio import FileAccess
from tableio.value_type import Value, ListData
from tableio.capability import Capabilities, CAP_NEEDED, CAP_NOT_USED
from .cmd_for_examples import cmd_parse_and_run_example
from .write_writer_info import write_writer_info


# pylint: disable=duplicate-code
CAPS = Capabilities(
    can_write=CAP_NEEDED,
    can_read=CAP_NOT_USED,
    can_fmt_row=CAP_NOT_USED,
    can_fmt_value=CAP_NOT_USED,
    filtered_data_range=CAP_NOT_USED,
    can_write_box=CAP_NOT_USED,
    can_read_box=CAP_NOT_USED,
    can_write_highlight=CAP_NOT_USED,
    multi_sheet=CAP_NOT_USED
)
# pylint: enable=duplicate-code


def build_mixed_optional_args(
        optional_args: OptionalArgs) -> OptionalArgsDict:
    """Build one dictionary that contains arguments for several formats.

    The point of this example is that the dictionary intentionally mixes
    arguments that belong to different backends. The later call to
    filter_args_tableio() will keep only the arguments that make sense for
    the concrete backend we are about to create.
    """
    result = OptionalArgsDict(
        character_encoding='utf-8',
        title='Filter args demo',
        lang='en',
        paper_size=PaperSize.A4,
        document_class=DocumentClass.ARTICLE,
        line_length=72,
        table_max_line_length=72,
        csv_delimiter=';',
        csv_quoting='minimal')
    if optional_args is not None:
        result.update(optional_args)
    return result


def stringify_optional_arg_value(value: object) -> str:
    """Convert an optional argument value into readable text."""
    if isinstance(value, IntEnum):
        return value.name
    return str(value)


def resolve_implementation_name(format_name: str,
                                implementation_name: Optional[str],
                                capabilities: Capabilities) -> str:
    """Resolve the concrete implementation name to use for filtering.

    filter_args_tableio() needs both a format name and an implementation
    name. When the caller did not specify an implementation, we discover the
    implementation the factory would choose by creating a temporary writer in
    a temporary directory and reading its descriptor.
    """
    if implementation_name is not None:
        return implementation_name
    with TemporaryDirectory() as temp_dir:
        probe_output = Path(temp_dir) / 'probe_output'
        with create_tableio(format_name=format_name,
                            file_name=probe_output,
                            file_access=FileAccess.CREATE,
                            capabilities=capabilities) as tableio:
            return tableio.get_description().implementation
    msg = 'Could not resolve the implementation name.'
    raise RuntimeError(msg)


def build_summary_table(actual_implementation: str,
                        filtered_args: OptionalArgs) -> ListData[Value]:
    """Build a short summary table for the filtering result."""
    return [
        ['Property', 'Value'],
        ['Implementation', actual_implementation],
        ['Filtered arg count',
         len(filtered_args) if filtered_args is not None else 0]]


def build_filtered_args_table(filtered_args: OptionalArgs) -> ListData[Value]:
    """Build a two-column table with the kept arguments."""
    data: ListData[Value] = [['Argument', 'Value']]
    if filtered_args is None or not filtered_args:
        data.append(['(none)', ''])
        return data
    for key, value in sorted(filtered_args.items()):
        assert value is not None
        data.append([key, stringify_optional_arg_value(value)])
    return data


def build_removed_args_table(mixed_args: OptionalArgsDict,
                             filtered_args: OptionalArgs) -> ListData[Value]:
    """Build a one-column table with the removed argument names."""
    filtered_keys = set()
    if filtered_args is not None:
        filtered_keys = set(filtered_args.keys())
    data: ListData[Value] = [['Removed arguments']]
    removed = sorted(
        key for key in mixed_args.keys()
        if key not in filtered_keys)
    if not removed:
        data.append(['(none)'])
        return data
    for key in removed:
        data.append([key])
    return data


# pylint: disable=duplicate-code
def e08_filter_args_tableio(format_name: str, output_file_name: str,
                            implementation_name: Optional[str],
                            optional_args: OptionalArgs) -> int:
    """Create one backend from a mixed OptionalArgsDict.

    This example demonstrates a common pattern:
    1. Build one dictionary with arguments for several possible formats.
    2. Resolve the concrete implementation that will actually be used.
    3. Filter the dictionary for that backend.
    4. Create the final writer with only the valid arguments.
    """
    mixed_args = build_mixed_optional_args(optional_args)
    actual_implementation = resolve_implementation_name(
        format_name=format_name,
        implementation_name=implementation_name,
        capabilities=CAPS)
    filtered_args = filter_args_tableio(
        args=mixed_args,
        format_name=format_name,
        implementation=actual_implementation)
    with create_tableio(format_name=format_name,
                        file_name=output_file_name,
                        file_access=FileAccess.CREATE,
                        implementation=implementation_name,
                        capabilities=CAPS,
                        args=filtered_args) as tableio:
        #
        # First write a short summary so the reader sees the resolved
        # implementation and how many arguments survived the filtering.
        #
        tableio.write_heading('Summary of the filtering.')
        tableio.write_table_listdata(
            build_summary_table(actual_implementation, filtered_args))
        #
        # Then show the arguments that were kept.
        #
        tableio.write_heading('Arguments kept for this backend.')
        tableio.write_table_listdata(
            build_filtered_args_table(filtered_args))
        #
        # And separately show the arguments that were removed.
        #
        tableio.write_heading('Arguments removed by the filter.')
        tableio.write_table_listdata(
            build_removed_args_table(mixed_args, filtered_args))
        #
        # The next table shows the actual writer that was created.
        #
        tableio.write_heading('Information about the writer we created.')
        write_writer_info(tableio,
                          requested_format_name=format_name,
                          requested_implementation=implementation_name)
        #
        # Finally we write a tiny normal data table to show that the
        # filtered arguments were enough to create and use the writer.
        #
        tableio.write_heading('A small table written with the filtered args.')
        demo_table: ListData[Value] = [
            ['message', 'value'],
            ['writer implementation', actual_implementation],
            ['arg count',
             len(filtered_args) if filtered_args is not None else 0]]
        tableio.write_table_listdata(demo_table)
    return 0
# pylint: enable=duplicate-code


if __name__ == '__main__':
    cmd_parse_and_run_example(example_name='e08_filter_args_tableio',
                              func=e08_filter_args_tableio, caps=CAPS)
