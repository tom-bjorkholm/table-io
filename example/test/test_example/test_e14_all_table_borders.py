#! /usr/bin/env python3
"""Tests for all table borders example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest
from tableio import TableBorderStyle, Value
from example.e14_all_table_borders import e14_all_table_borders
from .spreadsheet_checkers import SheetContentExpectation, \
    RelativeStyleExpectation, AnchoredStyleExpectation, \
    RelativeBorderExpectation, AnchoredBorderExpectation, BOLD_STYLE, \
    YELLOW_BOLD, RED_BOLD, GREEN_PLAIN
from .example_checkers import check_example_spreadsheet, Example, \
    change_sheet, change_sheet_borders


example_function = e14_all_table_borders


def build_sheet_rows() -> list[list[Value]]:
    """Build expected row fragments for the e14 spreadsheet."""
    rows: list[list[Value]] = [['Showing all table border styles']]
    for border_style in TableBorderStyle:
        rows.extend([
            [f'write_table_listdata() with {border_style.name}'],
            ['A-Column', 'B-Column', 'C-Column'],
            [3.1415, 2.7182, 'Yellow bold'],
            [True, False, 'Red bold'],
            ['ListData[ValueFmt]', border_style.name, 'Green']
        ])
    return rows


def build_expected_styles() -> list[AnchoredStyleExpectation]:
    """Build expected style checks for the e14 spreadsheet."""
    expectations: list[AnchoredStyleExpectation] = [
        AnchoredStyleExpectation(
            sheet_name='Sheet',
            anchor_row_fragment=['Showing all table border styles'],
            relative_expectations=[
                RelativeStyleExpectation(expected_style=BOLD_STYLE)
            ]
        )
    ]
    for border_style in TableBorderStyle:
        expectations.append(AnchoredStyleExpectation(
            sheet_name='Sheet',
            anchor_row_fragment=[
                f'write_table_listdata() with {border_style.name}'
            ],
            relative_expectations=[
                RelativeStyleExpectation(expected_style=BOLD_STYLE),
                RelativeStyleExpectation(expected_style=BOLD_STYLE,
                                         row_offset=2,
                                         col_offset=1,
                                         number_of_columns=3),
                RelativeStyleExpectation(expected_style=YELLOW_BOLD,
                                         row_offset=3,
                                         col_offset=3),
                RelativeStyleExpectation(expected_style=RED_BOLD,
                                         row_offset=4,
                                         col_offset=3),
                RelativeStyleExpectation(expected_style=GREEN_PLAIN,
                                         row_offset=5,
                                         col_offset=3)
            ]
        ))
    return expectations


def build_expected_borders() -> list[AnchoredBorderExpectation]:
    """Build expected border checks for the e14 spreadsheet."""
    expectations: list[AnchoredBorderExpectation] = []
    for border_style in TableBorderStyle:
        expectations.append(AnchoredBorderExpectation(
            sheet_name='Sheet',
            anchor_row_fragment=[
                f'write_table_listdata() with {border_style.name}'
            ],
            relative_expectations=[
                RelativeBorderExpectation(border_style=border_style,
                                          row_offset=2,
                                          col_offset=1,
                                          number_of_rows=4,
                                          number_of_columns=3)
            ]
        ))
    return expectations


# pylint: disable=duplicate-code
SHEET_ROWS: list[list[Value]] = build_sheet_rows()
EXPECTED_STYLES: list[AnchoredStyleExpectation] = build_expected_styles()
EXPECTED_BORDERS: list[AnchoredBorderExpectation] = \
    build_expected_borders()
EXPECTED_STYLES1: list[AnchoredStyleExpectation] = \
    change_sheet(anchored_style_expectations=EXPECTED_STYLES,
                 sheet_name='Sheet1')
EXPECTED_BORDERS1: list[AnchoredBorderExpectation] = \
    change_sheet_borders(anchored_border_expectations=EXPECTED_BORDERS,
                         sheet_name='Sheet1')
SHEET_OPX = SheetContentExpectation(sheet_name='Sheet',
                                    row_fragments=SHEET_ROWS)
SHEET_REST = SheetContentExpectation(sheet_name='Sheet1',
                                     row_fragments=SHEET_ROWS)


@pytest.mark.parametrize('example, expected, expected_styles, '
                         'expected_borders',
                         [(Example(example_function=example_function,
                                   format_name='ods',
                                   implementation_name='odfdo'),
                           SHEET_REST, EXPECTED_STYLES1,
                           EXPECTED_BORDERS1),
                          (Example(example_function=example_function,
                                   format_name='excel',
                                   implementation_name='openpyxl'),
                           SHEET_OPX, EXPECTED_STYLES,
                           EXPECTED_BORDERS),
                          (Example(example_function=example_function,
                                   format_name='excel',
                                   implementation_name='xlsxwriter'),
                           SHEET_REST, EXPECTED_STYLES1,
                           EXPECTED_BORDERS1)])
def test_e14_all_table_borders_spreadsheet(
        capsys: pytest.CaptureFixture[str],
        example: Example,
        expected: SheetContentExpectation,
        expected_styles: list[AnchoredStyleExpectation],
        expected_borders: list[AnchoredBorderExpectation]) -> None:
    """Test e14 for spreadsheet formats and implementations."""
    check_example_spreadsheet(example=example, capture=capsys,
                              expected_fragments=[expected],
                              style_expectations=expected_styles,
                              border_expectations=expected_borders)
# pylint: enable=duplicate-code
