#! /usr/bin/env python3
"""Tests for read and write with value conversion example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import datetime, timedelta
from unittest.mock import Mock
import pytest
from tableio import Value
import example.e05_read_write_valueconversion as example_module
from .spreadsheet_checkers import SheetContentExpectation, \
    RelativeStyleExpectation, AnchoredStyleExpectation, PLAIN_STYLE
from .example_checkers import check_example_md_csv, \
    check_example_spreadsheet, Example, change_sheet


FIXED_NOW: datetime = datetime(year=2026, month=4, day=6, hour=13, minute=14,
                               second=15)
example_function = example_module.e05_read_write_valueconversion


@pytest.fixture(autouse=True)
def freeze_datetime_now(monkeypatch: pytest.MonkeyPatch) -> None:
    """Freeze datetime.now() used by the example."""
    patched_datetime = Mock(wraps=datetime)
    patched_datetime.now.return_value = FIXED_NOW
    monkeypatch.setattr(example_module, 'datetime', patched_datetime)


SHEET_ROW_FRAGMENTS: list[list[Value]] = [
    ['name', 'value', 'rounded', 'valid', 'when'],
    ['real', 3.14159, 3, True, FIXED_NOW],
    ['fake', 2.71828, 3, False,
     datetime(year=2036, month=3, day=26, hour=12, minute=5, second=49)],
    ['name', 'answer', 'part', 'valid', 'when'],
    ['magic', 42, 0.5, True, FIXED_NOW - timedelta(seconds=1)],
    ['show', 100, 0.25, False,
     datetime(year=2026, month=12, day=25, hour=8, minute=5, second=49)]
]

# pylint: disable=duplicate-code
EXPECTED_STYLES: list[AnchoredStyleExpectation] = [
    AnchoredStyleExpectation(
        sheet_name='Sheet', anchor_row_fragment=['name', 'value'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=PLAIN_STYLE,
                                     number_of_rows=3, number_of_columns=5),
        ]),
    AnchoredStyleExpectation(
        sheet_name='Sheet', anchor_row_fragment=['name', 'answer'],
        relative_expectations=[
            RelativeStyleExpectation(expected_style=PLAIN_STYLE,
                                     number_of_rows=3, number_of_columns=5),
        ])
]

EXPECTED_STYLES1: list[AnchoredStyleExpectation] = \
    change_sheet(anchored_style_expectations=EXPECTED_STYLES,
                 sheet_name='Sheet1')

SHEET_OPX: SheetContentExpectation = SheetContentExpectation(
    sheet_name='Sheet', row_fragments=SHEET_ROW_FRAGMENTS)

SHEET_REST: SheetContentExpectation = SheetContentExpectation(
    sheet_name='Sheet1', row_fragments=SHEET_ROW_FRAGMENTS)
# pylint: enable=duplicate-code


CSV_FRAGMENTS: list[str] = [
    '"name","value","rounded","valid","when"',
    '"real","3.14159","3","True","2026-04-06 13:14:15"',
    '"fake","2.71828","3","False","2036-03-26 12:05:49"',
    '"name","answer","part","valid","when"',
    '"magic","42","0.5","True","2026-04-06 13:14:14"',
    '"show","100","0.25","False","2026-12-25 08:05:49"'
]


@pytest.mark.parametrize('example, expected, expected_styles',
                         [(Example(example_function=example_function,
                                   format_name='ods',
                                   implementation_name='odfdo'),
                           SHEET_REST, EXPECTED_STYLES1),
                          (Example(example_function=example_function,
                                   format_name='excel',
                                   implementation_name='openpyxl'),
                           SHEET_OPX, EXPECTED_STYLES),
                          (Example(example_function=example_function,
                                   format_name='excel',
                                   implementation_name='pylightxl'),
                           SHEET_REST, EXPECTED_STYLES1)])
def test_e05_read_write_valueconversion_spreadsheet(
        capsys: pytest.CaptureFixture[str], example: Example,
        expected: SheetContentExpectation,
        expected_styles: list[AnchoredStyleExpectation]) -> None:
    """Test e05 for spreadsheet formats and implementations."""
    check_example_spreadsheet(example=example, capture=capsys,
                              expected_fragments=[expected],
                              style_expectations=expected_styles)


@pytest.mark.parametrize('example, expected',
                         [(Example(example_function=example_function,
                                   format_name='csv'),
                           CSV_FRAGMENTS)])
def test_e05_text(capsys: pytest.CaptureFixture[str], example: Example,
                  expected: list[str]) -> None:
    """Test e05 for CSV text format."""
    check_example_md_csv(example=example, capture=capsys,
                         expected_fragments=expected)
