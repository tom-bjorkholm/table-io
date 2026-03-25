#! /usr/bin/env python3
"""Helper functions to change type of single data cell Value.

When storing a Value in some file formats, the actual type of the value
may get lost. For example when storing a datatime value in CSV format,
the value that is read back will most likely be a string. These are helper
functions to change the type of the value to the expected type.
"""

# flake8: noqa
# TODO: remove flake8 disable and noqa when functions are implemented. # pylint: disable=fixme

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import datetime, date, time
from typing import Optional
from tableio.value_type import Value


class UnreasonableTypeConversion(TypeError):
    """Exception for when a value's conversion types are unreasonable."""

    def __init__(self, value: Value, expected_type: type[Value]):
        """Initialize the exception."""
        self.value = value
        self.expected_type = expected_type
        msg = 'Unreasonable type conversion: from type: '
        msg += f'{type(value).__name__} to type: {expected_type.__name__}.'
        msg += f' Value: {str(value)}.'
        super().__init__(msg)


class UnreasonableValueConversion(ValueError):
    """Exception for when a value's conversion values are unreasonable."""

    def __init__(self, value: Value, expected_type: type[Value]):
        """Initialize the exception."""
        self.value = value
        self.expected_type = expected_type
        msg = 'Unreasonable value conversion: from value: '
        msg += f'{str(value)} of type {type(value).__name__} '
        msg += f'to type: {expected_type.__name__}.'
        super().__init__(msg)


def value2str(value: Value, none_is_empty: bool = False) -> str:
    """Convert a value to a string.

    When storing a Value in some file formats, the actual type of the value
    may get lost. Use this function to convert the value to a string if the
    the code logic knows that the value should be a string.
    Args:
        value: The value to convert.
        none_is_empty: If True, None values are converted to empty strings.
                       If False, None values will raise ValueError.
    Raises:
        ValueError: If none_is_empty is False and value is None.
    Returns:
        The converted value.
    """
    if isinstance(value, str):
        return value
    if value is None:
        if none_is_empty:
            return ''
        raise UnreasonableValueConversion(value, str)
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value)
    # TODO: add tests for this function. # pylint: disable=fixme


# pylint: disable=fixme,line-too-long,missing-function-docstring,unused-argument
# TODO: remove pylint disable and noqa when functions are implemented.
def value2bool(value: Value, none_is_false: bool = False) -> bool:
    # TODO write docstring, code and tests for this function.
    raise NotImplementedError('value2bool not implemented')
    return False  # pylint: disable=unreachable # TODO: remove this line when function is implemented.


def value2int(value: Value, none_is_zero: bool = False,
              format_string: Optional[str] = None) -> int:
    # TODO write docstring, code and tests for this function.
    # TODO: is format_string is given it shold be used for conversion from string.
    raise NotImplementedError('value2int not implemented')
    return 0  # pylint: disable=unreachable # TODO: remove this line when function is implemented.


def value2float(value: Value, none_is_zero: bool = False) -> float:
    # TODO write docstring, code and tests for this function.
    raise NotImplementedError('value2float not implemented')
    return 0.0  # pylint: disable=unreachable # TODO: remove this line when function is implemented.


def value2datetime(value: Value,
                   format_string: Optional[str] = None) -> datetime:
    # TODO write docstring, code and tests for this function.
    # TODO: if format_string is given it shold be used for conversion from string.
    # TODO: if format_string is not given and value is a string, the code should try to parse the string as a datetime - trying isoformat and locale dependent parsing.
    raise NotImplementedError('value2datetime not implemented')
    return datetime.now()  # pylint: disable=unreachable # TODO: remove this line when function is implemented.


def value2date(value: Value,
               format_string: Optional[str] = None) -> date:
    # TODO write docstring, code and tests for this function.
    # TODO: if format_string is given it shold be used for conversion from string.
    # TODO: if format_string is not given and value is a string, the code should try to parse the string as a date - trying isoformat and locale dependent parsing.
    raise NotImplementedError('value2date not implemented')
    return date.today()  # pylint: disable=unreachable # TODO: remove this line when function is implemented.


def value2time(value: Value,
               format_string: Optional[str] = None) -> time:
    # TODO write docstring, code and tests for this function.
    # TODO: if format_string is given it shold be used for conversion from string.
    # TODO: if format_string is not given and value is a string, the code should try to parse the string as a time - trying isoformat and locale dependent parsing.
    raise NotImplementedError('value2time not implemented')
    return time(0, 0, 0)  # pylint: disable=unreachable # TODO: remove this line when function is implemented.
