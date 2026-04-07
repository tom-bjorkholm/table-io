#! /usr/bin/env python3
"""Tests for table borders example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest
from tableio import TableBorderStyle, Value
from example.e13_table_borders import e13_table_borders
from .spreadsheet_checkers import SheetContentExpectation, \
    RelativeStyleExpectation, AnchoredStyleExpectation, \
    RelativeBorderExpectation, AnchoredBorderExpectation, BOLD_STYLE, \
    ITALIC_STYLE, RED_PLAIN, YELLOW_PLAIN, GREEN_PLAIN
from .example_checkers import check_example_spreadsheet, Example, \
    change_sheet, change_sheet_borders


example_function = e13_table_borders


SHEET_ROWS: list[list[Value]] = [
    ['Table border API examples'],
    ['write_table_listdata() with OUTER_FIRST_ROW_THICK_INNER_THIN'],
    ['A-Column', 'B-Column', 'C-Column'],
    [3.1415, 2.7182, 1.4142],
    [True, False, 'Lower right'],
    ['write_table_dictdata() with OUTER_THICK_INNER_THIN'],
    ['A-Col', 'B-Col', 'C-Col'],
    ['Upper left', 1.4142, 'Upper right'],
    [3.1415, 2.7182, 'Right middle'],
    [True, False, 'Lower right'],
    ['write_table_fmtlistdata() with ALL_THIN'],
    ['A-Column', 'B-Column', 'C-Column'],
    [3.1415, 2.7182, 1.4142],
    [True, False, 'Lower right'],
    ['write_table_fmtdictdata() with OUTER_THICK'],
    ['A-Col', 'B-Col', 'C-Col'],
    ['Upper left', 1.4142, 'Upper right'],
    [3.1415, 2.7182, 'Right middle'],
    [True, False, 'Lower right']
]


EXPECTED_STYLES: list[AnchoredStyleExpectation] = [
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['Table border API examples'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=BOLD_STYLE)
        ]
    ),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=[
            'write_table_listdata() with OUTER_FIRST_ROW_THICK_INNER_THIN'
        ],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=BOLD_STYLE),
            RelativeStyleExpectation(expected_style=BOLD_STYLE,
                                     row_offset=2,
                                     number_of_columns=3),
            RelativeStyleExpectation(expected_style=ITALIC_STYLE,
                                     row_offset=3),
            RelativeStyleExpectation(expected_style=YELLOW_PLAIN,
                                     row_offset=3,
                                     col_offset=2),
            RelativeStyleExpectation(expected_style=BOLD_STYLE,
                                     row_offset=4),
            RelativeStyleExpectation(expected_style=RED_PLAIN,
                                     row_offset=4,
                                     col_offset=2)
        ]
    ),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['write_table_dictdata() with '
                             'OUTER_THICK_INNER_THIN'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=BOLD_STYLE),
            RelativeStyleExpectation(expected_style=BOLD_STYLE,
                                     row_offset=2,
                                     number_of_columns=3),
            RelativeStyleExpectation(expected_style=ITALIC_STYLE,
                                     row_offset=3),
            RelativeStyleExpectation(expected_style=GREEN_PLAIN,
                                     row_offset=3,
                                     col_offset=2),
            RelativeStyleExpectation(expected_style=ITALIC_STYLE,
                                     row_offset=4),
            RelativeStyleExpectation(expected_style=YELLOW_PLAIN,
                                     row_offset=4,
                                     col_offset=2),
            RelativeStyleExpectation(expected_style=BOLD_STYLE,
                                     row_offset=5),
            RelativeStyleExpectation(expected_style=RED_PLAIN,
                                     row_offset=5,
                                     col_offset=2)
        ]
    ),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['write_table_fmtlistdata() with ALL_THIN'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=BOLD_STYLE),
            RelativeStyleExpectation(expected_style=BOLD_STYLE,
                                     row_offset=2,
                                     number_of_columns=3),
            RelativeStyleExpectation(expected_style=ITALIC_STYLE,
                                     row_offset=3,
                                     number_of_columns=3),
            RelativeStyleExpectation(expected_style=RED_PLAIN,
                                     row_offset=4,
                                     number_of_columns=3)
        ]
    ),
    AnchoredStyleExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['write_table_fmtdictdata() with OUTER_THICK'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=BOLD_STYLE),
            RelativeStyleExpectation(expected_style=BOLD_STYLE,
                                     row_offset=2,
                                     number_of_columns=3),
            RelativeStyleExpectation(expected_style=ITALIC_STYLE,
                                     row_offset=3,
                                     number_of_columns=3),
            RelativeStyleExpectation(expected_style=RED_PLAIN,
                                     row_offset=5,
                                     number_of_columns=3)
        ]
    )
]


EXPECTED_BORDERS: list[AnchoredBorderExpectation] = [
    AnchoredBorderExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=[
            'write_table_listdata() with OUTER_FIRST_ROW_THICK_INNER_THIN'
        ],
        relative_expectations=[
            RelativeBorderExpectation(
                border_style=TableBorderStyle.OUTER_FIRST_ROW_THICK_INNER_THIN,
                row_offset=2,
                number_of_rows=3,
                number_of_columns=3
            )
        ]
    ),
    AnchoredBorderExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['write_table_dictdata() with '
                             'OUTER_THICK_INNER_THIN'],
        relative_expectations=[
            RelativeBorderExpectation(
                border_style=TableBorderStyle.OUTER_THICK_INNER_THIN,
                row_offset=2,
                number_of_rows=4,
                number_of_columns=3
            )
        ]
    ),
    AnchoredBorderExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['write_table_fmtlistdata() with ALL_THIN'],
        relative_expectations=[
            RelativeBorderExpectation(
                border_style=TableBorderStyle.ALL_THIN,
                row_offset=2,
                number_of_rows=3,
                number_of_columns=3
            )
        ]
    ),
    AnchoredBorderExpectation(
        sheet_name='Sheet',
        anchor_row_fragment=['write_table_fmtdictdata() with OUTER_THICK'],
        relative_expectations=[
            RelativeBorderExpectation(
                border_style=TableBorderStyle.OUTER_THICK,
                row_offset=2,
                number_of_rows=4,
                number_of_columns=3
            )
        ]
    )
]

# pylint: disable=duplicate-code
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
def test_e13_table_borders_spreadsheet(
        capsys: pytest.CaptureFixture[str],
        example: Example,
        expected: SheetContentExpectation,
        expected_styles: list[AnchoredStyleExpectation],
        expected_borders: list[AnchoredBorderExpectation]) -> None:
    """Test e13 for spreadsheet formats and implementations."""
    check_example_spreadsheet(example=example, capture=capsys,
                              expected_fragments=[expected],
                              style_expectations=expected_styles,
                              border_expectations=expected_borders)
# pylint: enable=duplicate-code
