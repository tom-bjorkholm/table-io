#! /usr/bin/env python3
"""Tests for more write example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest
from example.e04_rrs_input_format_list import e04_rrs_input_format_list
from .spreadsheet_checkers import SheetContentExpectation, \
    AnchoredStyleExpectation
from .example_checkers import check_example_spreadsheet, Example
from .test_e03_rrs_input_format import \
    EXPECTED_STYLES, EXPECTED_STYLES1, SHEET_OPX, SHEET_REST


@pytest.mark.parametrize('fmt, impl, expected, styles',
                         [('ods', 'odfdo', SHEET_REST, EXPECTED_STYLES1),
                          ('excel', 'openpyxl', SHEET_OPX, EXPECTED_STYLES),
                          ('excel', 'xlsxwriter', SHEET_REST,
                           EXPECTED_STYLES1)])
def test_e04_spreadsheet(capsys: pytest.CaptureFixture[str], fmt: str,
                         impl: str, expected: SheetContentExpectation,
                         styles: list[AnchoredStyleExpectation]) -> None:
    """Test e03 for spreadsheet formats and implementations."""
    example4 = Example(example_function=e04_rrs_input_format_list,
                       format_name=fmt, implementation_name=impl)
    check_example_spreadsheet(example4, capture=capsys,
                              expected_fragments=[expected],
                              style_expectations=styles)
