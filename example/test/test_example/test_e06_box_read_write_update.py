#! /usr/bin/env python3
"""Tests for box read and write update example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest
from tableio import Value
from example.e06_box_read_write_update import e06_box_read_write_update
from .spreadsheet_checkers import SheetContentExpectation, \
    RelativeStyleExpectation, AnchoredStyleExpectation, PLAIN_STYLE
from .example_checkers import check_example_spreadsheet, Example, \
    change_sheet


# pylint: disable=duplicate-code
def build_sheet_row_fragments() -> list[list[Value]]:
    """Build expected row fragments for the e06 spreadsheet."""
    fragments: list[list[Value]] = []
    for row in range(10):
        fragment: list[Value] = []
        for value in range(row * 10, row * 10 + 10):
            fragment.append(value)
        if row == 2:
            fragment.extend([23, 24])
        if row == 3:
            fragment.extend([33, 34])
        fragments.append(fragment)
    return fragments


SHEET_ROW_FRAGMENTS: list[list[Value]] = build_sheet_row_fragments()

EXPECTED_STYLES: list[AnchoredStyleExpectation] = [
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=[0, 1],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=PLAIN_STYLE,
                                     number_of_rows=10,
                                     number_of_columns=10),
        ]),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=[20, 21],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=PLAIN_STYLE,
                                     col_offset=13,
                                     number_of_rows=2,
                                     number_of_columns=2),
        ])
]

EXPECTED_STYLES1: list[AnchoredStyleExpectation] = \
    change_sheet(anchored_style_expectations=EXPECTED_STYLES,
                 sheet_name='Sheet1')

SHEET_OPX: SheetContentExpectation = SheetContentExpectation(
    sheet_name='Sheet',
    row_fragments=SHEET_ROW_FRAGMENTS
)

SHEET_REST: SheetContentExpectation = SheetContentExpectation(
    sheet_name='Sheet1',
    row_fragments=SHEET_ROW_FRAGMENTS
)


@pytest.mark.parametrize('example, expected, expected_styles',
                         [(Example(example_function=e06_box_read_write_update,
                                   format_name='ods',
                                   implementation_name='odfdo'),
                           SHEET_REST, EXPECTED_STYLES1),
                          (Example(example_function=e06_box_read_write_update,
                                   format_name='excel',
                                   implementation_name='openpyxl'),
                           SHEET_OPX, EXPECTED_STYLES),
                          (Example(example_function=e06_box_read_write_update,
                                   format_name='excel',
                                   implementation_name='pylightxl'),
                           SHEET_REST, EXPECTED_STYLES1)])
def test_e06_box_read_write_update_spreadsheet(
        capsys: pytest.CaptureFixture[str],
        example: Example,
        expected: SheetContentExpectation,
        expected_styles: list[AnchoredStyleExpectation]) -> None:
    """Test e06 for spreadsheet formats and implementations."""
    check_example_spreadsheet(example=example, capture=capsys,
                              expected_fragments=[expected],
                              style_expectations=expected_styles)
# pylint: enable=duplicate-code
