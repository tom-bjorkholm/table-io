#! /usr/bin/env python3
"""Tests for the timedelta example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import timedelta
import pytest
from tableio import OptionalArgsDict, TimeDeltaFallback, Value
import example.e15_timedelta as example_module
from .spreadsheet_checkers import SheetContentExpectation
from .example_checkers import check_example_md_csv, \
    check_example_spreadsheet, Example

example_function = example_module.e15_timedelta
HEADING = 'Total late: 1 day 06:26:02.5'

EXCEL_ROW_FRAGMENTS: list[list[Value]] = [
    ['task', 'estimate', 'actual'],
    ['design', timedelta(hours=6), timedelta(hours=7, minutes=30)],
    ['build', timedelta(days=2, hours=3), timedelta(days=3)],
    ['test', timedelta(minutes=45), timedelta(minutes=41, seconds=2.5)],
    [HEADING],
    ['task', 'late'],
    ['design', timedelta(hours=1, minutes=30)],
    ['build', timedelta(days=1, hours=5)],
    ['test', timedelta(minutes=-3, seconds=-57.5)]
]
"""Excel durations are checked with an independent reader (calamine)."""

ODS_ROW_FRAGMENTS: list[list[Value]] = [
    ['task', 'estimate', 'actual'], ['design'], ['build'], ['test'],
    [HEADING], ['task', 'late'], ['design'], ['build'], ['test']
]
"""calamine cannot read ODS durations, so only the text cells are checked.

(calamine returns ODS durations as a time of day, or as a string when the
duration is negative or at least 24 hours.) The ODS duration values are
checked by the example itself and in test_tableio_timedelta.py.
"""


@pytest.mark.parametrize(
    'example, expected',
    [(Example(example_function=example_function, format_name='ods',
              implementation_name='odfdo'),
      SheetContentExpectation(sheet_name='Sheet1',
                              row_fragments=ODS_ROW_FRAGMENTS)),
     (Example(example_function=example_function, format_name='excel',
              implementation_name='openpyxl'),
      SheetContentExpectation(sheet_name='Sheet',
                              row_fragments=EXCEL_ROW_FRAGMENTS)),
     (Example(example_function=example_function, format_name='excel',
              implementation_name='pylightxl'),
      SheetContentExpectation(sheet_name='Sheet1',
                              row_fragments=EXCEL_ROW_FRAGMENTS))])
def test_e15_spreadsheet(capsys: pytest.CaptureFixture[str], example: Example,
                         expected: SheetContentExpectation) -> None:
    """Test e15 for spreadsheet formats with native timedelta."""
    check_example_spreadsheet(example=example, capture=capsys,
                              expected_fragments=[expected])


_FLOAT_ARGS: OptionalArgsDict = {
    'timedelta_fallback': TimeDeltaFallback.FLOATSECONDS}
_LONG_ARGS: OptionalArgsDict = {
    'timedelta_fallback': TimeDeltaFallback.WDHMS_STRING_LONG}


@pytest.mark.parametrize(
    'example, expected',
    [(Example(example_function=example_function, format_name='csv'),
      ['"task","estimate","actual"', '"design","06:00:00","07:30:00"',
       '"build","51:00:00","72:00:00"', '"test","00:45:00","00:41:02.5"',
       f'# {HEADING}', '"task","late"', '"design","01:30:00"',
       '"build","29:00:00"', '"test","-00:03:57.5"']),
     (Example(example_function=example_function, format_name='csv',
              optional_args=_FLOAT_ARGS),
      ['"design","21600.0","27000.0"', '"build","183600.0","259200.0"',
       '"test","2700.0","2462.5"', '"test","-237.5"']),
     (Example(example_function=example_function, format_name='csv',
              optional_args=_LONG_ARGS),
      ['"build","2 days 03:00:00","3 days 00:00:00"',
       '"build","1 day 05:00:00"'])])
def test_e15_text(capsys: pytest.CaptureFixture[str], example: Example,
                  expected: list[str]) -> None:
    """Test e15 for CSV with default and chosen timedelta fallbacks."""
    check_example_md_csv(example=example, capture=capsys,
                         expected_fragments=expected)
