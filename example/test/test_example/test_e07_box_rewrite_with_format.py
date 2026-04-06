#! /usr/bin/env python3
"""Tests for box rewrite with format example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest
from tableio import Value
from example.e07_box_rewrite_with_format import e07_box_rewrite_with_format
from .spreadsheet_checkers import SheetContentExpectation, \
    RelativeStyleExpectation, AnchoredStyleExpectation, PLAIN_STYLE, RED_BOLD
from .example_checkers import check_example_spreadsheet, Example, \
    change_sheet


# pylint: disable=duplicate-code
def build_sheet_row_fragments() -> list[list[Value]]:
    """Build expected row fragments for the e07 spreadsheet."""
    fragments: list[list[Value]] = []
    for row in range(10):
        fragment: list[Value] = []
        for column in range(10):
            fragment.append(f'r{row}c{column}')
        fragments.append(fragment)
    return fragments


SHEET_ROW_FRAGMENTS: list[list[Value]] = build_sheet_row_fragments()

EXPECTED_STYLES: list[AnchoredStyleExpectation] = [
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['r0c0', 'r0c1'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=PLAIN_STYLE,
                                     number_of_rows=8,
                                     number_of_columns=10),
        ]),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['r8c0', 'r8c1'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=RED_BOLD,
                                     number_of_rows=2,
                                     number_of_columns=2),
            RelativeStyleExpectation(expected_style=PLAIN_STYLE,
                                     col_offset=2,
                                     number_of_rows=2,
                                     number_of_columns=8),
        ])
]

EXPECTED_STYLES1: list[AnchoredStyleExpectation] = \
    change_sheet(anchored_style_expectations=EXPECTED_STYLES,
                 sheet_name='Sheet1')

SHEET_OPX: SheetContentExpectation = SheetContentExpectation(
    sheet_name='Sheet',
    row_fragments=SHEET_ROW_FRAGMENTS
)

SHEET_ODS: SheetContentExpectation = SheetContentExpectation(
    sheet_name='Sheet1',
    row_fragments=SHEET_ROW_FRAGMENTS
)


@pytest.mark.parametrize('example, expected, expected_styles',
                         [(Example(
                             example_function=e07_box_rewrite_with_format,
                             format_name='ods',
                             implementation_name='odfdo'),
                           SHEET_ODS, EXPECTED_STYLES1),
                          (Example(
                              example_function=e07_box_rewrite_with_format,
                              format_name='excel',
                              implementation_name='openpyxl'),
                           SHEET_OPX, EXPECTED_STYLES)])
def test_e07_box_rewrite_with_format_spreadsheet(
        capsys: pytest.CaptureFixture[str],
        example: Example,
        expected: SheetContentExpectation,
        expected_styles: list[AnchoredStyleExpectation]) -> None:
    """Test e07 for spreadsheet formats and implementations."""
    check_example_spreadsheet(example=example, capture=capsys,
                              expected_fragments=[expected],
                              style_expectations=expected_styles)
# pylint: enable=duplicate-code
