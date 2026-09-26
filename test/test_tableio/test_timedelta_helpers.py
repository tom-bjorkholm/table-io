#! /usr/local/bin/python3
"""Tests for the timedelta_helpers module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import datetime, timedelta
from typing import Optional, cast
import pytest
from pytest import CaptureFixture
import tableio
from tableio.optional_args import TimeDeltaFallback
from tableio.timedelta_helpers import DEFAULT_TIMEDELTA_FALLBACK, \
    fallback_value, format_timedelta, parse_timedelta
from tableio.value_type import Value
from .check_capsys import check_capsys

_F = TimeDeltaFallback
_DURATION = timedelta(weeks=2, days=1, hours=2, minutes=3, seconds=4)
_ROUND_TRIP_VALUES = [
    timedelta(0), timedelta(microseconds=1), timedelta(seconds=1.5),
    timedelta(hours=-1), timedelta(days=1), timedelta(weeks=1),
    timedelta(days=-8, microseconds=1), _DURATION,
    timedelta(days=1000, hours=23, microseconds=999999),
    timedelta.max, timedelta.min]


@pytest.mark.parametrize(
    ('fallback', 'value', 'expected'),
    [
        (_F.FLOATSECONDS, _DURATION, 1303384.0),
        (_F.FLOATSECONDS, timedelta(milliseconds=-1500), -1.5),
        (_F.HMS_STRING, _DURATION, '362:03:04'),
        (_F.HMS_STRING, timedelta(0), '00:00:00'),
        (_F.HMS_STRING, timedelta(seconds=1.5), '00:00:01.5'),
        (_F.HMS_STRING, timedelta(microseconds=7), '00:00:00.000007'),
        (_F.HMS_STRING, timedelta(hours=-1), '-01:00:00'),
        (_F.HMS_STRING, timedelta(hours=100), '100:00:00'),
        (_F.DHMS_STRING, _DURATION, '15 d 02:03:04'),
        (_F.DHMS_STRING, timedelta(hours=5), '05:00:00'),
        (_F.DHMS_STRING, timedelta(days=-1, hours=-2), '-1 d 02:00:00'),
        (_F.DHMS_STRING_LONG, _DURATION, '15 days 02:03:04'),
        (_F.DHMS_STRING_LONG, timedelta(days=1), '1 day 00:00:00'),
        (_F.WDHMS_STRING, _DURATION, '2 w 1 d 02:03:04'),
        (_F.WDHMS_STRING, timedelta(weeks=1, hours=1), '1 w 01:00:00'),
        (_F.WDHMS_STRING, timedelta(days=6), '6 d 00:00:00'),
        (_F.WDHMS_STRING_LONG, _DURATION, '2 weeks 1 day 02:03:04'),
        (_F.WDHMS_STRING_LONG, timedelta(weeks=1, days=2),
         '1 week 2 days 00:00:00'),
        (_F.WDHMS_STRING_LONG, -timedelta(weeks=3, seconds=0.25),
         '-3 weeks 00:00:00.25')
    ])
def test_format_timedelta(fallback: TimeDeltaFallback, value: timedelta,
                          expected: str | float,
                          capsys: CaptureFixture[str]) -> None:
    """format_timedelta writes each fallback format as documented."""
    assert format_timedelta(value, fallback) == expected
    check_capsys(capsys)


@pytest.mark.parametrize('fallback', list(TimeDeltaFallback))
@pytest.mark.parametrize('value', _ROUND_TRIP_VALUES)
def test_round_trip(fallback: TimeDeltaFallback, value: timedelta,
                    capsys: CaptureFixture[str]) -> None:
    """parse_timedelta reads back every string fallback format exactly."""
    formatted = format_timedelta(value, fallback)
    if fallback == TimeDeltaFallback.FLOATSECONDS:
        assert isinstance(formatted, float)
        if abs(value) < timedelta(days=36500):
            assert parse_timedelta(formatted) == value
            assert parse_timedelta(str(formatted)) == value
    else:
        assert isinstance(formatted, str)
        assert parse_timedelta(formatted) == value
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        (_DURATION, _DURATION),
        (90, timedelta(seconds=90)),
        (-1.25, timedelta(seconds=-1.25)),
        ('1:02:03', timedelta(hours=1, minutes=2, seconds=3)),
        ('  26:03:04\n', timedelta(hours=26, minutes=3, seconds=4)),
        ('1d 00:00:00', timedelta(days=1)),
        ('2 DAYS 00:00:00', timedelta(days=2)),
        ('1 Week 00:00:00', timedelta(weeks=1)),
        ('1 day, 2:03:04', timedelta(days=1, hours=2, minutes=3, seconds=4)),
        ('-1 day, 23:00:00', timedelta(hours=-1)),
        ('2 days, 0:00:00.500000', timedelta(days=2, seconds=0.5)),
        ('3600', timedelta(hours=1)),
        ('-93784.5', -timedelta(days=1, hours=2, minutes=3, seconds=4.5))
    ])
def test_parse_timedelta(value: str | int | float | timedelta,
                         expected: timedelta,
                         capsys: CaptureFixture[str]) -> None:
    """parse_timedelta accepts all documented input forms."""
    assert parse_timedelta(value) == expected
    check_capsys(capsys)


@pytest.mark.parametrize(
    'value',
    ['', 'soon', '1:60:00', '00:00:60', '1:2:3', '00:00:00.1234567',
     '1.5 d 00:00:00', '1 d', '- 01:00:00', 'nan', 'inf', 'infinity',
     '1e20', float('nan'), float('inf'), 10 ** 20])
def test_parse_bad_value(value: str | int | float,
                         capsys: CaptureFixture[str]) -> None:
    """parse_timedelta raises ValueError for unparsable values."""
    with pytest.raises(ValueError, match='Cannot parse timedelta'):
        parse_timedelta(value)
    check_capsys(capsys)


@pytest.mark.parametrize('value', [None, True, False,
                                   datetime(2026, 1, 1), ['1']])
def test_parse_bad_type(value: object, capsys: CaptureFixture[str]) -> None:
    """parse_timedelta raises TypeError for unsupported types."""
    with pytest.raises(TypeError, match='Unsupported type'):
        parse_timedelta(cast(str, value))
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('value', 'fallback', 'expected'),
    [
        (None, None, None),
        ('text', _F.FLOATSECONDS, 'text'),
        (3, _F.FLOATSECONDS, 3),
        (True, None, True),
        (datetime(2026, 1, 1), _F.FLOATSECONDS, datetime(2026, 1, 1)),
        (timedelta(days=1), None, '24:00:00'),
        (timedelta(days=1), _F.FLOATSECONDS, 86400.0),
        (timedelta(days=1), _F.DHMS_STRING_LONG, '1 day 00:00:00')
    ])
def test_fallback_value(value: Value, fallback: Optional[TimeDeltaFallback],
                        expected: Value, capsys: CaptureFixture[str]) -> None:
    """fallback_value only replaces timedelta values."""
    assert fallback_value(value, fallback) == expected
    check_capsys(capsys)


def test_public_exports(capsys: CaptureFixture[str]) -> None:
    """The timedelta API is exported from the tableio package."""
    assert tableio.format_timedelta is format_timedelta
    assert tableio.parse_timedelta is parse_timedelta
    assert tableio.TimeDeltaFallback is TimeDeltaFallback
    assert DEFAULT_TIMEDELTA_FALLBACK == TimeDeltaFallback.HMS_STRING
    check_capsys(capsys)
