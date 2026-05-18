#! /usr/bin/env python3
"""Tests for repeated multi-cell find_value example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest
from tableio import Value
from example.e12_find_value_multiple_matches import \
    e12_find_value_multiple_matches
from .spreadsheet_checkers import SheetContentExpectation
from .example_checkers import check_example_spreadsheet, Example


example_function = e12_find_value_multiple_matches


SHEET_ROWS: list[list[Value]] = [
    ['Group/artist', 'Year', 'Remark', 'Single'],
    ['David Bowie', 1974, '', 'Rebel Rebel'],
    ['ABBA', 1974, 'found and edited 1', 'Waterloo'],
    ['Queen', 1974, '', 'Killer Queen'],
    ['ABBA', 1975, '', 'Mamma Mia'],
    ['The Rubettes', 1974, '', 'Sugar Baby Love'],
    ['ABBA', 1974, 'found and edited 2', 'Honey, Honey'],
    ['Mud', 1974, '', 'Tiger Feet'],
    ['ABBA', 1976, '', 'Fernando'],
    ['Sweet', 1974, '', 'Fox on the Run'],
    ['ABBA', 1974, 'found and edited 3', 'So Long'],
    ['Bee Gees', 1977, '', 'Stayin Alive'],
    ['ABBA', 1977, '', 'Knowing Me, Knowing You']
]


SHEET_OPX = SheetContentExpectation(sheet_name='Sheet',
                                    row_fragments=SHEET_ROWS)
SHEET_REST = SheetContentExpectation(sheet_name='Sheet1',
                                     row_fragments=SHEET_ROWS)


@pytest.mark.parametrize('example, expected_fragments',
                         [(Example(example_function=example_function,
                                   format_name='ods',
                                   implementation_name='odfdo'),
                           [SHEET_REST]),
                          (Example(example_function=example_function,
                                   format_name='excel',
                                   implementation_name='openpyxl'),
                           [SHEET_OPX]),
                          (Example(example_function=example_function,
                                   format_name='excel',
                                   implementation_name='pylightxl'),
                           [SHEET_REST])])
def test_e12_find_value_multiple_matches_spreadsheet(
        capsys: pytest.CaptureFixture[str], example: Example,
        expected_fragments: list[SheetContentExpectation]) -> None:
    """Test e12 for spreadsheet formats and implementations."""
    check_example_spreadsheet(example=example, capture=capsys,
                              expected_fragments=expected_fragments)
