#! /usr/bin/env python3
"""Tests for find-value, read-cells and write-cells example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest
from tableio import Value
from example.e11_find_value_read_cells_write_cells import \
    e11_find_value_read_cells_write_cells
from .spreadsheet_checkers import SheetContentExpectation, \
    RelativeStyleExpectation, AnchoredStyleExpectation, GREEN_BOLD, \
    PLAIN_STYLE
from .example_checkers import check_example_spreadsheet, Example, \
    change_sheet


example_function = e11_find_value_read_cells_write_cells


SHEET_ROWS: list[list[Value]] = [
    ['Economic entity', 2024, 2025],
    ['Revenue', 1250000, 1390000],
    ['Operating costs', 830000, 900000],
    ['Operating profit', 420000, 490000]
]


EXPECTED_STYLES: list[AnchoredStyleExpectation] = [
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['Revenue', 1250000, 1390000],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=GREEN_BOLD,
                                     col_offset=1,
                                     number_of_columns=2),
        ]),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['Operating costs', 830000, 900000],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=PLAIN_STYLE,
                                     col_offset=1,
                                     number_of_columns=2),
        ])
]

EXPECTED_STYLES1: list[AnchoredStyleExpectation] = \
    change_sheet(anchored_style_expectations=EXPECTED_STYLES,
                 sheet_name='Sheet1')

SHEET_OPX = SheetContentExpectation(sheet_name='Sheet',
                                    row_fragments=SHEET_ROWS)
SHEET_ODS = SheetContentExpectation(sheet_name='Sheet1',
                                    row_fragments=SHEET_ROWS)


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
                           [SHEET_OPX], EXPECTED_STYLES)])
def test_e11_find_value_read_cells_write_cells_spreadsheet(
        capsys: pytest.CaptureFixture[str],
        example: Example,
        expected_fragments: list[SheetContentExpectation],
        expected_styles: list[AnchoredStyleExpectation]) -> None:
    """Test e11 for spreadsheet formats and implementations."""
    check_example_spreadsheet(example=example, capture=capsys,
                              expected_fragments=expected_fragments,
                              style_expectations=expected_styles)
