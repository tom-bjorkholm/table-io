#! /usr/bin/env python3
"""Helpers for converting one stored ``Value`` to an expected type.

When a ``Value`` is stored in a file format with weaker typing, the original
type may be lost. A ``datetime`` written to CSV, for example, is usually read
back as a string. These helpers perform explicit and predictable conversions
from one public ``Value`` representation to another expected concrete type.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import datetime, date, time
from typing import Optional
from tableio.value_type import Value, value_to_str

_TRUE_STRINGS = frozenset({'true', '1', 'yes', 'on'})
_FALSE_STRINGS = frozenset({'false', '0', 'no', 'off'})


class UnreasonableTypeConversion(TypeError):
    """Exception for when a value's conversion types are unreasonable."""

    def __init__(self, value: Value, expected_type: type[object]):
        """Initialize the exception."""
        self.value = value
        self.expected_type = expected_type
        msg = 'Unreasonable type conversion: from type: '
        msg += f'{type(value).__name__} to type: {expected_type.__name__}.'
        msg += f' Value: {str(value)}.'
        super().__init__(msg)


class UnreasonableValueConversion(ValueError):
    """Exception for when a value's conversion values are unreasonable."""

    def __init__(self, value: Value, expected_type: type[object]):
        """Initialize the exception."""
        self.value = value
        self.expected_type = expected_type
        msg = 'Unreasonable value conversion: from value: '
        msg += f'{str(value)} of type {type(value).__name__} '
        msg += f'to type: {expected_type.__name__}.'
        super().__init__(msg)


def value2str(value: Value, none_is_empty: bool = False) -> str:
    """Convert a value to a string.

    Datetime values are converted with ``isoformat()`` so the result remains
    easy to parse back to a datetime when needed.

    Args:
        value: The value to convert.
        none_is_empty: If True, None values are converted to empty strings.
                       If False, None values raise
                       UnreasonableValueConversion.
    Raises:
        UnreasonableValueConversion: If none_is_empty is False and value is
            None.
    Returns:
        The converted value.
    """
    if isinstance(value, datetime):
        return value.isoformat()
    try:
        return value_to_str(value, none_is_empty=none_is_empty)
    except ValueError as err:
        raise UnreasonableValueConversion(value, str) from err


def value2bool(value: Value, none_is_false: bool = False) -> bool:
    """Convert a value to a boolean.

    Strings are accepted only when they match one of the documented boolean
    spellings, case-insensitively and with surrounding whitespace ignored.
    Integer values are accepted only when they are exactly 0 or 1.

    Args:
        value: The value to convert.
        none_is_false: If True, None values are converted to False.
                       If False, None values raise UnreasonableValueConversion.
    Raises:
        UnreasonableTypeConversion: If the source type cannot reasonably be
            converted to bool.
        UnreasonableValueConversion: If the source value is of a reasonable
            type but does not represent a boolean.
    Returns:
        The converted boolean value.
    """
    if isinstance(value, bool):
        return value
    if value is None:
        if none_is_false:
            return False
        raise UnreasonableValueConversion(value, bool)
    if isinstance(value, int):
        if value in (0, 1):
            return bool(value)
        raise UnreasonableValueConversion(value, bool)
    if isinstance(value, str):
        normalized_value = value.strip().casefold()
        if normalized_value in _TRUE_STRINGS:
            return True
        if normalized_value in _FALSE_STRINGS:
            return False
        raise UnreasonableValueConversion(value, bool)
    raise UnreasonableTypeConversion(value, bool)


def value2int(value: Value, none_is_zero: bool = False,
              format_string: Optional[str] = None) -> int:
    """Convert a value to an integer.

    Strings are parsed with ``int()``. When ``format_string`` is provided, the
    parsed integer must reproduce the original string with ``format()``. This
    keeps parsing deterministic while supporting common integer formats such as
    zero-padded decimal strings.

    Args:
        value: The value to convert.
        none_is_zero: If True, None values are converted to 0.
                      If False, None values raise
                      UnreasonableValueConversion.
        format_string: Optional Python integer format specification used to
                       validate string input after parsing.
    Raises:
        UnreasonableTypeConversion: If the source type cannot reasonably be
            converted to int.
        UnreasonableValueConversion: If the source value is of a reasonable
            type but does not represent an integer.
    Returns:
        The converted integer value.
    """
    if isinstance(value, bool):
        raise UnreasonableTypeConversion(value, int)
    if isinstance(value, int):
        return value
    if value is None:
        if none_is_zero:
            return 0
        raise UnreasonableValueConversion(value, int)
    if isinstance(value, float):
        if value.is_integer():
            return int(value)
        raise UnreasonableValueConversion(value, int)
    if isinstance(value, str):
        try:
            int_value = int(value)
        except ValueError as err:
            raise UnreasonableValueConversion(value, int) from err
        if format_string is not None and \
                format(int_value, format_string) != value:
            raise UnreasonableValueConversion(value, int)
        return int_value
    raise UnreasonableTypeConversion(value, int)


def value2float(value: Value, none_is_zero: bool = False) -> float:
    """Convert a value to a float.

    Args:
        value: The value to convert.
        none_is_zero: If True, None values are converted to 0.0.
                      If False, None values raise
                      UnreasonableValueConversion.
    Raises:
        UnreasonableTypeConversion: If the source type cannot reasonably be
            converted to float.
        UnreasonableValueConversion: If the source value is of a reasonable
            type but does not represent a float.
    Returns:
        The converted float value.
    """
    if isinstance(value, bool):
        raise UnreasonableTypeConversion(value, float)
    if isinstance(value, float):
        return value
    if isinstance(value, int):
        return float(value)
    if value is None:
        if none_is_zero:
            return 0.0
        raise UnreasonableValueConversion(value, float)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError as err:
            raise UnreasonableValueConversion(value, float) from err
    raise UnreasonableTypeConversion(value, float)


def value2datetime(value: Value,
                   format_string: Optional[str] = None) -> datetime:
    """Convert a value to a datetime.

    Without ``format_string``, string input must use one of the formats
    accepted by ``datetime.fromisoformat()``. With ``format_string``, parsing
    is delegated to ``datetime.strptime()``.

    Args:
        value: The value to convert.
        format_string: Optional ``strptime`` format for string input.
    Raises:
        UnreasonableTypeConversion: If the source type cannot reasonably be
            converted to datetime.
        UnreasonableValueConversion: If the source value is of a reasonable
            type but does not represent a datetime.
    Returns:
        The converted datetime value.
    """
    if isinstance(value, datetime):
        return value
    if value is None:
        raise UnreasonableValueConversion(value, datetime)
    if isinstance(value, str):
        try:
            if format_string is None:
                return datetime.fromisoformat(value)
            return datetime.strptime(value, format_string)
        except ValueError as err:
            raise UnreasonableValueConversion(value, datetime) from err
    raise UnreasonableTypeConversion(value, datetime)


def value2date(value: Value,
               format_string: Optional[str] = None) -> date:
    """Convert a value to a date.

    Datetime values are reduced to their calendar date. Without
    ``format_string``, string input is parsed first as an ISO date and then as
    an ISO datetime if needed. With ``format_string``, parsing is delegated to
    ``datetime.strptime()`` and the date part is returned.

    Args:
        value: The value to convert.
        format_string: Optional ``strptime`` format for string input.
    Raises:
        UnreasonableTypeConversion: If the source type cannot reasonably be
            converted to date.
        UnreasonableValueConversion: If the source value is of a reasonable
            type but does not represent a date.
    Returns:
        The converted date value.
    """
    if isinstance(value, datetime):
        return value.date()
    if value is None:
        raise UnreasonableValueConversion(value, date)
    if isinstance(value, str):
        try:
            if format_string is not None:
                return datetime.strptime(value, format_string).date()
            try:
                return date.fromisoformat(value)
            except ValueError:
                return datetime.fromisoformat(value).date()
        except ValueError as err:
            raise UnreasonableValueConversion(value, date) from err
    raise UnreasonableTypeConversion(value, date)


def value2time(value: Value,
               format_string: Optional[str] = None) -> time:
    """Convert a value to a time.

    Datetime values are reduced to their time-of-day. Without
    ``format_string``, string input is parsed first as an ISO time and then as
    an ISO datetime if needed. With ``format_string``, parsing is delegated to
    ``datetime.strptime()`` and the time part is returned.

    Args:
        value: The value to convert.
        format_string: Optional ``strptime`` format for string input.
    Raises:
        UnreasonableTypeConversion: If the source type cannot reasonably be
            converted to time.
        UnreasonableValueConversion: If the source value is of a reasonable
            type but does not represent a time.
    Returns:
        The converted time value.
    """
    if isinstance(value, datetime):
        return value.timetz()
    if value is None:
        raise UnreasonableValueConversion(value, time)
    if isinstance(value, str):
        try:
            if format_string is not None:
                return datetime.strptime(value, format_string).time()
            try:
                return time.fromisoformat(value)
            except ValueError as err:
                if 'T' not in value and ' ' not in value:
                    raise UnreasonableValueConversion(value, time) from err
                return datetime.fromisoformat(value).timetz()
        except ValueError as err:
            raise UnreasonableValueConversion(value, time) from err
    raise UnreasonableTypeConversion(value, time)
