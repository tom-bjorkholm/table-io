#! /usr/local/bin/python3
"""Support functions for timedelta values in the tableio package.

Implementations without native timedelta support use ``format_timedelta``
(via ``fallback_value``) to write timedelta values as text or seconds.
Applications use ``parse_timedelta`` to read such values back.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import re
from datetime import timedelta
from typing import Optional
from tableio.optional_args import TimeDeltaFallback
from tableio.value_type import Value

DEFAULT_TIMEDELTA_FALLBACK = TimeDeltaFallback.HMS_STRING
"""The fallback used when no timedelta fallback is specified."""

_DAY_UNITS: dict[TimeDeltaFallback, tuple[tuple[int, str, str], ...]] = {
    TimeDeltaFallback.HMS_STRING: (),
    TimeDeltaFallback.DHMS_STRING: ((1, 'd', 'd'),),
    TimeDeltaFallback.DHMS_STRING_LONG: ((1, 'day', 'days'),),
    TimeDeltaFallback.WDHMS_STRING: ((7, 'w', 'w'), (1, 'd', 'd')),
    TimeDeltaFallback.WDHMS_STRING_LONG: ((7, 'week', 'weeks'),
                                          (1, 'day', 'days'))}
"""Units written before 'HH:MM:SS': (size in days, singular, plural)."""

_HMS_PATTERN = r'(?P<hours>\d+):(?P<minutes>[0-5]\d):' \
    r'(?P<seconds>[0-5]\d)(?:\.(?P<fraction>\d{1,6}))?'
_FALLBACK_RE = re.compile(r'(?P<sign>-?)(?:(?P<weeks>\d+) ?w(?:eeks?)? )?'
                          r'(?:(?P<days>\d+) ?d(?:ays?)? )?' + _HMS_PATTERN,
                          re.IGNORECASE)
"""Matches every string format written by the TimeDeltaFallback values."""
_PYTHON_STR_RE = re.compile(r'(?P<days>-?\d+) days?, ' + _HMS_PATTERN)
"""Matches ``str(timedelta)`` with days, like '-1 day, 23:00:00'."""


def _day_parts(days: int, units: tuple[tuple[int, str, str], ...]) -> \
        tuple[list[str], int]:
    """Split days into unit texts, and return them with remaining days."""
    parts: list[str] = []
    for size, singular, plural in units:
        count, days = divmod(days, size)
        if count:
            parts.append(f'{count} {singular if count == 1 else plural}')
    return parts, days


def hms_parts(days: int, seconds: int,
              microseconds: int) -> tuple[int, int, int, str]:
    """Split a non-negative duration into hours, minutes and seconds.

    Args:
        days: The number of days, included in the returned hours.
        seconds: The number of seconds (less than one day).
        microseconds: The number of microseconds (less than one second).
    Returns:
        The hours, minutes, whole seconds and the fraction text. The
        fraction text is '' if microseconds is zero, otherwise a '.' and
        up to six decimals without trailing zeros (for example '.5').
    """
    minutes, secs = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    fraction = f'.{microseconds:06d}'.rstrip('0') if microseconds else ''
    return days * 24 + hours, minutes, secs, fraction


def _hms_text(days: int, seconds: int, microseconds: int) -> str:
    """Return 'HH:MM:SS' with days as hours and fraction only if non-zero."""
    hours, minutes, secs, fraction = hms_parts(days, seconds, microseconds)
    return f'{hours:02d}:{minutes:02d}:{secs:02d}{fraction}'


def format_timedelta(td: timedelta, fallback: TimeDeltaFallback) -> \
        str | float:
    """Format a timedelta value according to the specified fallback behavior.

    To be called by an implementation that needs to format timedelta values
    according to the specified fallback behavior, because the implementation
    does not have native support for timedelta values.
    Negative values get a leading '-' for the whole duration (for example
    '-01:00:00' or '-1 d 02:00:00'). Fractional seconds are written with
    up to six decimals, only when non-zero (for example '00:00:01.5').
    The result can be converted back exactly with ``parse_timedelta``.
    Args:
        td: The timedelta value to format.
        fallback: The fallback behavior to use if native support is not
                  available.
    Returns:
        The formatted timedelta as a string or float, depending on the
        fallback enum value.
    """
    if fallback == TimeDeltaFallback.FLOATSECONDS:
        return td.total_seconds()
    sign = '-' if td < timedelta(0) else ''
    magnitude = abs(td)
    parts, days = _day_parts(magnitude.days, _DAY_UNITS[fallback])
    parts.append(_hms_text(days, magnitude.seconds, magnitude.microseconds))
    return sign + ' '.join(parts)


def fallback_value(value: Value,
                   fallback: Optional[TimeDeltaFallback]) -> Value:
    """Return value with a timedelta replaced by its fallback format.

    Args:
        value: The value to write. Only timedelta values are changed.
        fallback: The fallback behavior, or None for the default
                  (``DEFAULT_TIMEDELTA_FALLBACK``).
    Returns:
        The value to write instead of the original value.
    """
    if not isinstance(value, timedelta):
        return value
    if fallback is None:
        fallback = DEFAULT_TIMEDELTA_FALLBACK
    return format_timedelta(value, fallback)


def _hms_delta(match: re.Match[str]) -> timedelta:
    """Return the timedelta of the hours, minutes and seconds groups."""
    fraction = match['fraction'] or ''
    return timedelta(hours=int(match['hours']), minutes=int(match['minutes']),
                     seconds=int(match['seconds']),
                     microseconds=int(fraction.ljust(6, '0')))


def _parse_str(text: str) -> timedelta:
    """Parse a fallback string, a Python timedelta string or seconds."""
    match = _FALLBACK_RE.fullmatch(text)
    if match is not None:
        delta = timedelta(weeks=int(match['weeks'] or 0),
                          days=int(match['days'] or 0)) + _hms_delta(match)
        return -delta if match['sign'] else delta
    match = _PYTHON_STR_RE.fullmatch(text)
    if match is not None:
        # Python semantics: only the day count is signed.
        return timedelta(days=int(match['days'])) + _hms_delta(match)
    return timedelta(seconds=float(text))


def parse_timedelta(value: str | int | float | timedelta) -> timedelta:
    """Parse a value into a timedelta object.

    To be called by an application that knows that a value represents a
    timedelta, when the implementation for reading might not provide native
    support for timedelta values.
    Accepted values:
      - timedelta: returned unchanged.
      - int or float (not bool): a number of seconds.
      - str: any string written by the ``TimeDeltaFallback`` formats (for
        example '26:03:04', '-1 d 02:03:04', '1 week 2 days 00:00:01.5'),
        the ``str(timedelta)`` format (for example '-1 day, 23:00:00'), or
        a number of seconds (for example '93784.0'). Surrounding whitespace
        is ignored and unit names are case-insensitive.
    Args:
        value: The value to parse, which can be a string, int, float, or
               timedelta.
    Returns:
        The parsed timedelta object.
    Raises:
        TypeError: If the value is not a string, int, float, or timedelta.
        ValueError: If the value cannot be parsed into a timedelta, or is
                    out of the range of timedelta.
    """
    if isinstance(value, timedelta):
        return value
    if isinstance(value, bool) or \
            not isinstance(value, (str, int, float)):
        raise TypeError(
            f'Unsupported type for parsing timedelta: {type(value)}')
    try:
        if isinstance(value, str):
            return _parse_str(value.strip())
        return timedelta(seconds=value)
    except (ValueError, OverflowError) as err:
        raise ValueError(f'Cannot parse timedelta from: {value!r}') from err
