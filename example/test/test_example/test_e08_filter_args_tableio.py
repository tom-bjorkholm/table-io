#! /usr/bin/env python3
"""Tests for filter args tableio example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from dataclasses import dataclass

import pytest
from tableio import Value
from example.e08_filter_args_tableio import e08_filter_args_tableio
from .spreadsheet_checkers import SheetContentExpectation
from .example_checkers import check_example_md_csv, \
    check_example_spreadsheet, Example


ALL_REMOVED_ARGS: list[str] = [
    'character_encoding',
    'csv_delimiter',
    'csv_quoting',
    'document_class',
    'lang',
    'line_length',
    'paper_size',
    'table_max_line_length',
    'title'
]


@dataclass(frozen=True)
class WriterExpectation:
    """Expected writer metadata for one e08 spreadsheet output."""

    type_name: str
    writer_implementation: str
    requested_implementation: str
    priority: int
    optional_arg_names: list[str]
    capability_rows: list[tuple[str, str]]


@dataclass(frozen=True)
class BackendExpectation:
    """Expected backend-specific rows for one e08 spreadsheet output."""

    actual_implementation: str
    filtered_arg_count: int
    kept_args: list[tuple[str, str]]
    removed_args: list[str]
    writer: WriterExpectation


def build_optional_arg_rows(
        optional_arg_names: list[str]) -> list[list[Value]]:
    """Build expected writer-info rows for optional arguments."""
    if not optional_arg_names:
        return [['Optional arguments', '(none)']]
    return [['Optional argument', name] for name in optional_arg_names]


def build_sheet_row_fragments(
        backend: BackendExpectation) -> list[list[Value]]:
    """Build expected spreadsheet row fragments for one e08 backend."""
    rows: list[list[Value]] = [
        ['Summary of the filtering.'],
        ['Property', 'Value'],
        ['Implementation', backend.actual_implementation],
        ['Filtered arg count', backend.filtered_arg_count],
        ['Arguments kept for this backend.'],
        ['Argument', 'Value'],
    ]
    if backend.kept_args:
        for key, value in backend.kept_args:
            rows.append([key, value])
    else:
        rows.append(['(none)', ''])
    rows.extend([
        ['Arguments removed by the filter.'],
        ['Removed arguments'],
    ])
    for key in backend.removed_args:
        rows.append([key])
    rows.extend([
        ['Information about the writer we created.'],
        ['Attribute', 'Value', 'Requested value'],
        ['Type name', backend.writer.type_name,
         backend.writer.type_name.lower()],
        ['Implementation', backend.writer.writer_implementation,
         backend.writer.requested_implementation],
        ['Priority', backend.writer.priority],
        ['Mandatory arguments', '(none)'],
    ])
    rows.extend(build_optional_arg_rows(backend.writer.optional_arg_names))
    for capability_name, capability_value in backend.writer.capability_rows:
        rows.append([f'Capability {capability_name}', capability_value])
    rows.extend([
        ['A small table written with the filtered args.'],
        ['message', 'value'],
        ['writer implementation', backend.actual_implementation],
        ['arg count', backend.filtered_arg_count],
    ])
    return rows


# pylint: disable=duplicate-code
SHEET_ODS: SheetContentExpectation = SheetContentExpectation(
    sheet_name='Sheet1',
    row_fragments=build_sheet_row_fragments(
        BackendExpectation(
            actual_implementation='odfdo', filtered_arg_count=1,
            kept_args=[('lang', 'en')],
            removed_args=[
                'character_encoding',
                'csv_delimiter',
                'csv_quoting',
                'document_class',
                'line_length',
                'paper_size',
                'table_max_line_length',
                'title'
            ],
            writer=WriterExpectation(
                type_name='ODS', writer_implementation='odfdo',
                requested_implementation='odfdo', priority=10,
                optional_arg_names=['lang'],
                capability_rows=[
                    ('can_read', 'supported (strict)'),
                    ('can_find_value_position', 'supported (strict)'),
                ]))))

SHEET_OPX: SheetContentExpectation = SheetContentExpectation(
    sheet_name='Sheet',
    row_fragments=build_sheet_row_fragments(
        BackendExpectation(
            actual_implementation='OpenPyXL', filtered_arg_count=0,
            kept_args=[], removed_args=ALL_REMOVED_ARGS,
            writer=WriterExpectation(
                type_name='Excel', writer_implementation='OpenPyXL',
                requested_implementation='openpyxl', priority=10,
                optional_arg_names=[],
                capability_rows=[
                    ('can_read', 'supported (strict)'),
                    ('can_write_highlight', 'supported (strict)'),
                ]))))

SHEET_PYXL: SheetContentExpectation = SheetContentExpectation(
    sheet_name='Sheet1',
    row_fragments=build_sheet_row_fragments(
        BackendExpectation(
            actual_implementation='pylightxl', filtered_arg_count=0,
            kept_args=[], removed_args=ALL_REMOVED_ARGS,
            writer=WriterExpectation(
                type_name='Excel', writer_implementation='pylightxl',
                requested_implementation='pylightxl', priority=8,
                optional_arg_names=[],
                capability_rows=[
                    ('can_read', 'supported (strict)'),
                    ('can_fmt_row', 'not supported (ignore)'),
                    ('can_write_highlight', 'not supported (ignore)'),
                ]))))

SHEET_XW: SheetContentExpectation = SheetContentExpectation(
    sheet_name='Sheet1',
    row_fragments=build_sheet_row_fragments(
        BackendExpectation(
            actual_implementation='XlsxWriter', filtered_arg_count=0,
            kept_args=[], removed_args=ALL_REMOVED_ARGS,
            writer=WriterExpectation(
                type_name='Excel', writer_implementation='XlsxWriter',
                requested_implementation='xlsxwriter', priority=20,
                optional_arg_names=[],
                capability_rows=[
                    ('can_read', 'not supported (strict)'),
                    ('can_find_value_position', 'not supported (strict)'),
                ]))))
# pylint: enable=duplicate-code


CSV_FRAGMENTS: list[str] = [
    '# Summary of the filtering.',
    'Property;Value',
    'Implementation;csv',
    'Filtered arg count;3',
    '## Arguments kept for this backend.',
    'Argument;Value',
    'character_encoding;utf-8',
    'csv_delimiter;";"',
    'csv_quoting;minimal',
    '## Arguments removed by the filter.',
    'Removed arguments',
    'document_class',
    'lang',
    'line_length',
    'paper_size',
    'table_max_line_length',
    'title',
    '## Information about the writer we created.',
    'Attribute;Value;Requested value',
    'Type name;CSV;csv',
    'Implementation;csv;csv',
    'Priority;10;',
    'Mandatory arguments;(none);',
    'Optional argument;character_encoding;',
    'Optional argument;csv_delimiter;',
    'Capability can_read;supported (ignore);',
    'Capability can_write_box;not supported (strict);',
    '## A small table written with the filtered args.',
    'message;value',
    'writer implementation;csv',
    'arg count;3'
]

CSV_AUTO_FRAGMENTS: list[str] = [
    '# Summary of the filtering.',
    'Implementation;csv',
    'Filtered arg count;3',
    '## Arguments kept for this backend.',
    'character_encoding;utf-8',
    'csv_delimiter;";"',
    'csv_quoting;minimal',
    '## Information about the writer we created.',
    'Implementation;csv;(none)',
    '## A small table written with the filtered args.',
    'writer implementation;csv',
    'arg count;3'
]

MD_FRAGMENTS: list[str] = [
    '# Summary of the filtering.',
    '| Property | Value |',
    '| Implementation | mformat |',
    '| Filtered arg count | 1',
    '## Arguments kept for this backend.',
    '| Argument | Value |',
    '| character_encoding | utf-8 |',
    '## Arguments removed by the filter.',
    '| Removed arguments |',
    '| csv_delimiter',
    '| csv_quoting',
    '| document_class',
    '| lang',
    '| line_length',
    '| paper_size',
    '| table_max_line_length',
    '| title',
    '## Information about the writer we created.',
    '| Attribute | Value | Requested value |',
    '| Type name | md    | md',
    '| Implementation | mformat | mformat',
    '| Priority       | 10',
    '| Mandatory arguments | (none)',
    '| Optional argument   | character_encoding',
    '| Capability can_read  | not supported (strict)',
    '| Capability can_fmt_row | supported (ignore)',
    '## A small table written with the filtered args.',
    '| message | value |',
    '| writer implementation | mformat |',
    '| arg count             | 1'
]


@pytest.mark.parametrize('example, expected',
                         [(Example(example_function=e08_filter_args_tableio,
                                   format_name='ods',
                                   implementation_name='odfdo'),
                           SHEET_ODS),
                          (Example(example_function=e08_filter_args_tableio,
                                   format_name='excel',
                                   implementation_name='openpyxl'),
                           SHEET_OPX),
                          (Example(example_function=e08_filter_args_tableio,
                                   format_name='excel',
                                   implementation_name='pylightxl'),
                           SHEET_PYXL),
                          (Example(example_function=e08_filter_args_tableio,
                                   format_name='excel',
                                   implementation_name='xlsxwriter'),
                           SHEET_XW)])
def test_e08_filter_args_tableio_spreadsheet(
        capsys: pytest.CaptureFixture[str], example: Example,
        expected: SheetContentExpectation) -> None:
    """Test e08 for spreadsheet formats and implementations."""
    check_example_spreadsheet(example=example, capture=capsys,
                              expected_fragments=[expected])


@pytest.mark.parametrize('example, expected',
                         [(Example(example_function=e08_filter_args_tableio,
                                   format_name='csv',
                                   implementation_name='csv'),
                           CSV_FRAGMENTS),
                          (Example(example_function=e08_filter_args_tableio,
                                   format_name='csv'),
                           CSV_AUTO_FRAGMENTS),
                          (Example(example_function=e08_filter_args_tableio,
                                   format_name='md',
                                   implementation_name='mformat'),
                           MD_FRAGMENTS)])
def test_e08_filter_args_text(capsys: pytest.CaptureFixture[str],
                              example: Example, expected: list[str]) -> None:
    """Test e08 for text formats and implementations."""
    check_example_md_csv(example=example, capture=capsys,
                         expected_fragments=expected)
