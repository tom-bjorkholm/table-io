#! /usr/bin/env python3
"""Tests for capability-driven selection example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
import pytest
from tableio import Value
from example.e10_capability_driven_selection import \
    e10_capability_driven_selection
from .spreadsheet_checkers import SheetContentExpectation, \
    RelativeStyleExpectation, AnchoredStyleExpectation, BOLD_STYLE, \
    ITALIC_STYLE, YELLOW_BOLD
from .example_checkers import check_example_md_csv, \
    check_example_spreadsheet, Example, change_sheet


example_function = e10_capability_driven_selection


COMMON_SHEET_ROWS: list[list[Value]] = [
    ['Preferred capability request.'],
    ['Capability', 'Request'],
    ['can_write', 'needed'],
    ['can_fmt_row', 'wanted, but ignorable'],
    ['filtered_data_range', 'wanted, but ignorable'],
    ['can_write_highlight', 'wanted, but ignorable'],
    ['Formats matching the preferred request.'],
    ['Matching formats'],
    ['CSV'],
    ['Excel'],
    ['ODS'],
    ['txt'],
    ['Implementations matching the preferred request.'],
    ['Matching implementations'],
    ['OpenPyXL'],
    ['XlsxWriter'],
    ['csv'],
    ['mformat'],
    ['odfdo'],
    ['pylightxl'],
    ['Stricter capability request for comparison.'],
    ['Capability', 'Request'],
    ['can_write', 'needed'],
    ['can_fmt_row', 'needed'],
    ['filtered_data_range', 'needed'],
    ['can_write_highlight', 'needed'],
    ['Formats matching the stricter request.'],
    ['Strict matching formats'],
    ['Excel'],
    ['ODS'],
    ['Implementations matching the stricter request.'],
    ['Strict matching implementations'],
    ['OpenPyXL'],
    ['XlsxWriter'],
    ['odfdo'],
    ['Information about the writer used in this run.'],
    ['A table written with the preferred request.'],
    ['Task', 'Status', 'Why this row is interesting'],
    ['Create writer', 'Works everywhere',
     'Only can_write is strictly required'],
    ['Use formatting', 'Best effort',
     'Bold and highlight may be ignored'],
    ['Use filtered range', 'Best effort',
     'Spreadsheet backends can honor it']
]


def build_sheet_rows(writer_rows: list[list[Value]]) -> list[list[Value]]:
    """Build expected sheet row fragments for one e10 backend."""
    before_writer = COMMON_SHEET_ROWS[:-5]
    after_writer = COMMON_SHEET_ROWS[-5:]
    return before_writer + writer_rows + after_writer


SHEET_ODS = SheetContentExpectation(
    sheet_name='Sheet1',
    row_fragments=build_sheet_rows([
        ['Attribute', 'Value', 'Requested value'],
        ['Type name', 'ODS', 'ods'],
        ['Implementation', 'odfdo', 'odfdo'],
        ['Priority', 10],
        ['Mandatory arguments', '(none)'],
        ['Optional argument', 'lang'],
        ['Capability can_write', 'supported (strict)'],
        ['Capability can_read', 'supported (strict)'],
        ['Capability can_fmt_row', 'supported (strict)'],
        ['Capability filtered_data_range', 'supported (strict)'],
        ['Capability can_write_highlight', 'supported (strict)'],
        ['Capability multi_sheet', 'supported (strict)'],
        ['Capability can_find_value_position', 'supported (strict)']
    ]))

SHEET_OPX = SheetContentExpectation(
    sheet_name='Sheet',
    row_fragments=build_sheet_rows([
        ['Attribute', 'Value', 'Requested value'],
        ['Type name', 'Excel', 'excel'],
        ['Implementation', 'OpenPyXL', 'openpyxl'],
        ['Priority', 10],
        ['Mandatory arguments', '(none)'],
        ['Optional arguments', '(none)'],
        ['Capability can_write', 'supported (strict)'],
        ['Capability can_read', 'supported (strict)'],
        ['Capability can_fmt_row', 'supported (strict)'],
        ['Capability filtered_data_range', 'supported (strict)'],
        ['Capability can_write_highlight', 'supported (strict)'],
        ['Capability multi_sheet', 'supported (strict)'],
        ['Capability can_find_value_position', 'supported (strict)']
    ]))

SHEET_PYXL = SheetContentExpectation(
    sheet_name='Sheet1',
    row_fragments=build_sheet_rows([
        ['Attribute', 'Value', 'Requested value'],
        ['Type name', 'Excel', 'excel'],
        ['Implementation', 'pylightxl', 'pylightxl'],
        ['Priority', 8],
        ['Mandatory arguments', '(none)'],
        ['Optional arguments', '(none)'],
        ['Capability can_write', 'supported (strict)'],
        ['Capability can_read', 'supported (strict)'],
        ['Capability can_fmt_row', 'not supported (ignore)'],
        ['Capability filtered_data_range', 'not supported (ignore)'],
        ['Capability can_write_highlight', 'not supported (ignore)'],
        ['Capability multi_sheet', 'supported (strict)'],
        ['Capability can_find_value_position', 'supported (strict)']
    ]))

SHEET_XW = SheetContentExpectation(
    sheet_name='Sheet1',
    row_fragments=build_sheet_rows([
        ['Attribute', 'Value', 'Requested value'],
        ['Type name', 'Excel', 'excel'],
        ['Implementation', 'XlsxWriter', 'xlsxwriter'],
        ['Priority', 20],
        ['Mandatory arguments', '(none)'],
        ['Optional arguments', '(none)'],
        ['Capability can_write', 'supported (strict)'],
        ['Capability can_read', 'not supported (strict)'],
        ['Capability can_fmt_row', 'supported (strict)'],
        ['Capability filtered_data_range', 'supported (strict)'],
        ['Capability can_write_highlight', 'supported (strict)'],
        ['Capability multi_sheet', 'supported (strict)'],
        ['Capability can_find_value_position', 'not supported (strict)']
    ]))


# pylint: disable=duplicate-code
EXPECTED_STYLES: list[AnchoredStyleExpectation] = [
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['Task', 'Status'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=BOLD_STYLE,
                                     number_of_columns=3),
        ]),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['Use formatting', 'Best effort'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=YELLOW_BOLD,
                                     number_of_columns=3),
        ]),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['Use filtered range', 'Best effort'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=ITALIC_STYLE,
                                     number_of_columns=3),
        ])
]

EXPECTED_STYLES1: list[AnchoredStyleExpectation] = \
    change_sheet(anchored_style_expectations=EXPECTED_STYLES,
                 sheet_name='Sheet1')
# pylint: enable=duplicate-code


CSV_FRAGMENTS: list[str] = [
    '# Preferred capability request.',
    '"Capability","Request"',
    '"can_write","needed"',
    '"can_fmt_row","wanted, but ignorable"',
    '"filtered_data_range","wanted, but ignorable"',
    '## Formats matching the preferred request.',
    '"Matching formats"',
    '"CSV"',
    '"ODS"',
    '"txt"',
    '## Implementations matching the preferred request.',
    '"Matching implementations"',
    '"OpenPyXL"',
    '"XlsxWriter"',
    '"csv"',
    '"mformat"',
    '"odfdo"',
    '"pylightxl"',
    '## Stricter capability request for comparison.',
    '"can_fmt_row","needed"',
    '"filtered_data_range","needed"',
    '"can_write_highlight","needed"',
    '## Implementations matching the stricter request.',
    '"Strict matching implementations"',
    '"OpenPyXL"',
    '"XlsxWriter"',
    '"odfdo"',
    '## Information about the writer used in this run.',
    '"Type name","CSV","csv"',
    '"Implementation","csv","csv"',
    '"Capability can_read","supported (ignore)",""',
    '"Capability can_fmt_row","not supported (ignore)",""',
    '## A table written with the preferred request.',
    '"Task","Status","Why this row is interesting"',
    '"Use formatting","Best effort","Bold and highlight may be ignored"',
    '"Use filtered range","Best effort",'
]

MD_FRAGMENTS: list[str] = [
    '# Preferred capability request.',
    '| Capability | Request |',
    '| can_write  | needed',
    '| can_fmt_row | wanted, but ignorable',
    '| filtered_data_range | wanted, but ignorable',
    '## Formats matching the preferred request.',
    '| Matching formats |',
    '| CSV',
    '| ODS',
    '| txt',
    '## Implementations matching the preferred request.',
    '| Matching implementations |',
    '| OpenPyXL',
    '| XlsxWriter',
    '| csv',
    '| mformat',
    '| odfdo',
    '| pylightxl',
    '## Stricter capability request for comparison.',
    '| can_fmt_row | needed',
    '| filtered_data_range | needed',
    '| can_write_highlight | needed',
    '## Implementations matching the stricter request.',
    '| Strict matching implementations |',
    '| OpenPyXL',
    '| XlsxWriter',
    '| odfdo',
    '## Information about the writer used in this run.',
    '| Type name | md    | md',
    '| Implementation | mformat | mformat',
    '| Capability can_read  | not supported (strict)',
    '| Capability can_fmt_row | supported (ignore)',
    '## A table written with the preferred request.',
    '| **Task** | **Status** | **Why this row is interesting** |',
    '| **Use formatting** | **Best effort**',
    '| *Use filtered range* | *Best effort*'
]


@pytest.mark.parametrize('example, expected_fragments, expected_styles',
                         [(Example(
                             example_function=example_function,
                             format_name='ods',
                             implementation_name='odfdo'),
                           [SHEET_ODS], EXPECTED_STYLES1),
                          (Example(
                              example_function=example_function,
                              format_name='excel',
                              implementation_name='openpyxl'),
                           [SHEET_OPX], EXPECTED_STYLES),
                          (Example(
                              example_function=example_function,
                              format_name='excel',
                              implementation_name='pylightxl'),
                           [SHEET_PYXL], None),
                          (Example(
                              example_function=example_function,
                              format_name='excel',
                              implementation_name='xlsxwriter'),
                           [SHEET_XW], EXPECTED_STYLES1)])
def test_e10_capability_driven_selection_spreadsheet(
        capsys: pytest.CaptureFixture[str],
        example: Example,
        expected_fragments: list[SheetContentExpectation],
        expected_styles: Optional[list[AnchoredStyleExpectation]]) -> None:
    """Test e10 for spreadsheet formats and implementations."""
    check_example_spreadsheet(example=example, capture=capsys,
                              expected_fragments=expected_fragments,
                              style_expectations=expected_styles)


@pytest.mark.parametrize('example, expected_fragments',
                         [(Example(
                             example_function=example_function,
                             format_name='csv',
                             implementation_name='csv'),
                           CSV_FRAGMENTS),
                          (Example(
                              example_function=example_function,
                              format_name='md',
                              implementation_name='mformat'),
                           MD_FRAGMENTS)])
def test_e10_capability_driven_selection_text(
        capsys: pytest.CaptureFixture[str],
        example: Example,
        expected_fragments: list[str]) -> None:
    """Test e10 for text formats and implementations."""
    check_example_md_csv(example=example, capture=capsys,
                         expected_fragments=expected_fragments)
