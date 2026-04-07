#! /usr/bin/env python3
"""Tests for more write example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import datetime, timedelta
import pytest
from tableio import Value
from example.e02_more_write import e02_more_write
from .spreadsheet_checkers import SheetContentExpectation, \
    RelativeStyleExpectation, AnchoredStyleExpectation, PLAIN_STYLE, \
    BOLD_STYLE, ITALIC_STYLE, BOLD_ITALIC_STYLE, YELLOW_ITALIC, RED_BOLD, \
    RED_BOLD_ITALIC, RED_ITALIC, GREEN_BOLD_ITALIC, GREEN_BOLD, GREEN_ITALIC
from .example_checkers import check_example_md_csv, \
    check_example_spreadsheet, Example, change_sheet

today: datetime = datetime.now()
today = today.replace(hour=13, minute=0, second=0, microsecond=0)
THIRTY_DAYS_AGO = today - timedelta(days=30)
TODAY_TEXT = today.strftime('%Y-%m-%d %H:%M:%S')
THIRTY_DAYS_AGO_TEXT = THIRTY_DAYS_AGO.strftime('%Y-%m-%d %H:%M:%S')

SHEET_ROW_FRAGMENTS: list[list[Value]] = [
    ['Example of how to write formatted data.'],
    ['Formatted List data.'],
    ['Jira key', 'Type', 'Status'],
    ['TIO-123', 'Task', 'In Progress'],
    ['TIO-456', 'Bug', 'To Do'],
    ['TIO-789', 'Story', 'Delayed'],
    ['TIO-101', 'Epic', 'Done'],
    ['Formatted Dict data.'],
    ['Jira key', 'Assignee', 'Reporter'],
    ['TIO-123', 'Jane Doe', 'John Doe'],
    ['TIO-456', 'John Doe', 'Jane Doe'],
    ['TIO-789', 'Unassigned', 'John Doe'],
    ['Formatted List data with FmtListRow.'],
    ['Jira key', 'Story Points', 'report date'],
    ['TIO-123', 13, today],
    ['TIO-456', 5, THIRTY_DAYS_AGO],
    ['TIO-789', 3, datetime(year=2010, month=12, day=25)],
    ['Formatted Dict data with FmtDictRow.'],
    ['Jira key', 'report date', 'Story Points'],
    ['TIO-123', today, 13],
    ['TIO-456', THIRTY_DAYS_AGO, 5],
    ['TIO-789', datetime(year=2010, month=12, day=25), 3],
]

EXPECTED_STYLES: list[AnchoredStyleExpectation] = [
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['Example of how to write formatted data.'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=BOLD_STYLE),
        ]),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['Formatted List data.'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=BOLD_STYLE),
        ]),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['Jira key', 'Type', 'Status'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=BOLD_STYLE,
                                     number_of_columns=2),
            RelativeStyleExpectation(expected_style=BOLD_ITALIC_STYLE,
                                     col_offset=2),
        ]),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['Jira key', 'Assignee', 'Reporter'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=BOLD_STYLE,
                                     number_of_columns=3),
        ]),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['Jira key', 'Story Points', 'report date'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=BOLD_STYLE,
                                     number_of_columns=3),
        ]),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['Jira key', 'report date', 'Story Points'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=BOLD_STYLE,
                                     number_of_columns=3),
        ]),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['TIO-123', 'Task', 'In Progress'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=ITALIC_STYLE,
                                     number_of_columns=3),
        ]),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['TIO-456', 'Bug', 'To Do'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=YELLOW_ITALIC,
                                     number_of_columns=3),
        ]),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['TIO-789', 'Story', 'Delayed'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=RED_BOLD,
                                     col_offset=2),
            RelativeStyleExpectation(expected_style=PLAIN_STYLE,
                                     col_offset=0, number_of_columns=2),
        ]),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['TIO-101', 'Epic', 'Done'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=GREEN_BOLD_ITALIC,
                                     col_offset=2),
            RelativeStyleExpectation(expected_style=PLAIN_STYLE,
                                     col_offset=0, number_of_columns=2),
        ]),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['TIO-123', 'Jane Doe', 'John Doe'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=ITALIC_STYLE),
            RelativeStyleExpectation(expected_style=BOLD_ITALIC_STYLE,
                                     col_offset=1),
            RelativeStyleExpectation(expected_style=BOLD_STYLE,
                                     col_offset=2)
        ]),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['TIO-456', 'John Doe', 'Jane Doe'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=GREEN_BOLD_ITALIC,
                                     col_offset=1),
            RelativeStyleExpectation(expected_style=PLAIN_STYLE,
                                     col_offset=0),
            RelativeStyleExpectation(expected_style=PLAIN_STYLE,
                                     col_offset=2)
        ]),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['TIO-789', 'Unassigned', 'John Doe'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=RED_BOLD_ITALIC,
                                     col_offset=1),
            RelativeStyleExpectation(expected_style=PLAIN_STYLE,
                                     col_offset=0),
            RelativeStyleExpectation(expected_style=PLAIN_STYLE,
                                     col_offset=2)
        ]),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['Jira key', 'Story Points', 'report date'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=BOLD_STYLE,
                                     number_of_columns=3),
        ]),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['TIO-123', 13, today],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=GREEN_ITALIC,
                                     number_of_columns=3),
        ]),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['TIO-456', 5, THIRTY_DAYS_AGO],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=PLAIN_STYLE,
                                     number_of_columns=3),
        ]),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['TIO-789', 3,
                             datetime(year=2010, month=12, day=25)],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=RED_ITALIC,
                                     number_of_columns=3),
        ]),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['Jira key', 'report date', 'Story Points'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=BOLD_STYLE,
                                     number_of_columns=3),
        ]),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['TIO-123', today, 13],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=GREEN_BOLD,
                                     number_of_columns=3),
        ]),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['TIO-456', THIRTY_DAYS_AGO, 5],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=YELLOW_ITALIC,
                                     number_of_columns=3),
        ]),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['TIO-789',
                             datetime(year=2010, month=12, day=25), 3],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=RED_BOLD_ITALIC,
                                     number_of_columns=3),
        ])
]

# pylint: disable=duplicate-code
EXPECTED_STYLES1: list[AnchoredStyleExpectation] = \
    change_sheet(anchored_style_expectations=EXPECTED_STYLES,
                 sheet_name='Sheet1')
# pylint: enable=duplicate-code


MD_FRAGMENTS: list[str] = [
    '# Example of how to write formatted data.',
    '## Formatted List data.',
    '| **Jira key** | **Type** | **Status** |',
    '|--------------|----------|------------|',
    '| *TIO-123*    | *Task*   | *In Progress* |',
    '| *TIO-456*    | *Bug*    | *To Do*       |',
    '| TIO-789      | Story    | Delayed       |',
    '| TIO-101      | Epic     | Done          |',
    '## Formatted Dict data.',
    '| **Jira key** | **Assignee** | **Reporter** |',
    '|--------------|--------------|--------------|',
    '| TIO-123      | Jane Doe     | John Doe     |',
    '| TIO-456      | John Doe     | Jane Doe     |',
    '| TIO-789      | Unassigned   | John Doe     |',
    '## Formatted List data with FmtListRow.',
    '**Jira key**', '**Story Points**', '**report date**',
    '*TIO-123*', '*13*',
    'TIO-456', '5',
    '*TIO-789*', '*3*',
    '## Formatted Dict data with FmtDictRow.',
    '**Jira key**', '**report date**', '**Story Points**',
    '**TIO-123**', '**13**',
    '*TIO-456*', '*5*',
    '***TIO-789***', '***3***'
]

CSV_FRAGMENTS: list[str] = [
    '# Example of how to write formatted data.',
    '## Formatted List data.',
    '"Jira key","Type","Status"',
    '"TIO-123","Task","In Progress"',
    '"TIO-456","Bug","To Do"',
    '"TIO-789","Story","Delayed"',
    '"TIO-101","Epic","Done"',
    '## Formatted Dict data.',
    '"Jira key","Assignee","Reporter"',
    '"TIO-123","Jane Doe","John Doe"',
    '"TIO-456","John Doe","Jane Doe"',
    '"TIO-789","Unassigned","John Doe"',
    '## Formatted List data with FmtListRow.',
    '"Jira key","Story Points","report date"',
    f'"TIO-123","13","{TODAY_TEXT}"',
    f'"TIO-456","5","{THIRTY_DAYS_AGO_TEXT}"',
    '"TIO-789","3","2010-12-25 00:00:00"',
    '## Formatted Dict data with FmtDictRow.',
    '"Jira key","report date","Story Points"',
    f'"TIO-123","{TODAY_TEXT}","13"',
    f'"TIO-456","{THIRTY_DAYS_AGO_TEXT}","5"',
    '"TIO-789","2010-12-25 00:00:00","3"',
]


# pylint: disable=duplicate-code
SHEET_OPX: SheetContentExpectation = SheetContentExpectation(
    sheet_name='Sheet',
    row_fragments=SHEET_ROW_FRAGMENTS)

SHEET_REST: SheetContentExpectation = SheetContentExpectation(
    sheet_name='Sheet1',
    row_fragments=SHEET_ROW_FRAGMENTS)
# pylint: enable=duplicate-code


@pytest.mark.parametrize('fmt, impl, expected, expected_styles',
                         [('ods', 'odfdo', SHEET_REST, EXPECTED_STYLES1),
                          ('excel', 'openpyxl', SHEET_OPX, EXPECTED_STYLES),
                          ('excel', 'pylightxl', SHEET_REST, None),
                          ('excel', 'xlsxwriter', SHEET_REST,
                           EXPECTED_STYLES1)])
def test_e02_more_write_spreadsheet(
        capsys: pytest.CaptureFixture[str],
        fmt: str,
        impl: str, expected: SheetContentExpectation,
        expected_styles: list[AnchoredStyleExpectation]) -> None:
    """Test e02 for spreadsheet formats and implementations."""
    example = Example(example_function=e02_more_write,
                      format_name=fmt, implementation_name=impl)
    check_example_spreadsheet(example, capture=capsys,
                              expected_fragments=[expected],
                              style_expectations=expected_styles)


@pytest.mark.parametrize('fmt, expected',
                         [('md', MD_FRAGMENTS),
                          ('csv', CSV_FRAGMENTS)])
def test_e02_more_write_text(capsys: pytest.CaptureFixture[str],
                             fmt: str, expected: list[str]) -> None:
    """Test e02 for CSV text format."""
    example = Example(example_function=e02_more_write,
                      format_name=fmt)
    check_example_md_csv(example, capture=capsys,
                         expected_fragments=expected)
