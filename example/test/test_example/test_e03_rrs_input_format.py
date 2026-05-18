#! /usr/bin/env python3
"""Tests for more write example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest
from tableio import Value
from example.e03_rrs_input_format import e03_rrs_input_format
from .spreadsheet_checkers import SheetContentExpectation, \
    RelativeStyleExpectation, AnchoredStyleExpectation, PLAIN_STYLE
from .example_checkers import check_example_spreadsheet, Example, change_sheet


SHEET_ROW_FRAGMENTS: list[list[Value]] = [
    ['Class', 'Division', 'Nationality', 'MNA No.', 'Sail Number',
     'Boat Name', 'First Name', 'Last Name', 'Club Name', 'Email',
     'Phone', 'Whats App Number'],
    ['ILCA', '', 'SWE', 134567, '13456',
     'Sjöbjörn', 'Örjan', 'Äldalsåker', 'Älvsborgs Segelsällskap',
     'ingen.mottagare@exempel.se', '+46701234567', '+46701234567'
     ],
    ['ILCA', '', 'USA', 123456, '12345',
     "Daddy's Money", 'John', 'Doe', 'New York Yacht Club',
     'no.receiver@example.com', '+12234567890', '+123456789'],
    ['Europe', '', 'GER', 145678, '145', 'Viel Spaß',
     'Thöß', 'Müller', 'Hamburger Segelclub',
     'keiner.empfaenger@beispiel.de', '+491234567', '+491234567']
]

EXPECTED_STYLES: list[AnchoredStyleExpectation] = [
    AnchoredStyleExpectation(
        sheet_name='Sheet', anchor_row_fragment=['Class', 'Division'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=PLAIN_STYLE,
                                     number_of_rows=3, number_of_columns=12),
        ])
]

# pylint: disable=duplicate-code
EXPECTED_STYLES1: list[AnchoredStyleExpectation] = \
    change_sheet(anchored_style_expectations=EXPECTED_STYLES,
                 sheet_name='Sheet1')


SHEET_OPX: SheetContentExpectation = SheetContentExpectation(
    sheet_name='Sheet', row_fragments=SHEET_ROW_FRAGMENTS)

SHEET_REST: SheetContentExpectation = SheetContentExpectation(
    sheet_name='Sheet1', row_fragments=SHEET_ROW_FRAGMENTS)
# pylint: enable=duplicate-code


@pytest.mark.parametrize('fmt, impl, expected, styles',
                         [('ods', 'odfdo', SHEET_REST, EXPECTED_STYLES1),
                          ('excel', 'openpyxl', SHEET_OPX, EXPECTED_STYLES),
                          ('excel', 'xlsxwriter', SHEET_REST,
                           EXPECTED_STYLES1)])
def test_e03_spreadsheet(capsys: pytest.CaptureFixture[str], fmt: str,
                         impl: str, expected: SheetContentExpectation,
                         styles: list[AnchoredStyleExpectation]) -> None:
    """Test e03 for spreadsheet formats and implementations."""
    example3 = Example(example_function=e03_rrs_input_format, format_name=fmt,
                       implementation_name=impl)
    check_example_spreadsheet(example3, capture=capsys,
                              expected_fragments=[expected],
                              style_expectations=styles)
