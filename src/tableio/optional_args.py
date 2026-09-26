#! /usr/bin/env python3
"""Optional arguments for the tableio package."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional, cast
from enum import IntEnum, auto
from mformat.factory import OptArgsDict


class CsvDialect(IntEnum):
    """The type of CSV file to write."""

    EXCEL = auto()
    """Excel CSV file type/dialect."""
    UNIX = auto()
    """Unix CSV file type/dialect."""


class TimeDeltaFallback(IntEnum):
    """The fallback behavior for timedelta values.

    How a timedelta value is written when an implementation does not support
    writing timedelta values. If an implementation does support timedelta
    values, the fallback behavior specified by this enum will be ignored.

    For all string formats: A negative value gets a leading '-' that applies
    to the whole duration (for example '-01:00:00' is minus one hour).
    Fractional seconds are written with up to six decimals, and only when
    non-zero (for example '00:00:01.5'). The 'HH' part is always at least two
    digits. Use ``tableio.parse_timedelta`` to read the values back.
    """

    FLOATSECONDS = auto()
    """Convert the timedelta to a float of the total number of seconds.

    Microsecond precision is lost for very large durations (roughly
    above 100 years), as a float has limited precision.
    """

    HMS_STRING = auto()
    """Convert the timedelta to a string in the format 'HH:MM:SS'.

    Days are included in the hours, so 'HH' may exceed 24 (for example
    '26:03:04').
    This is the default fallback.
    """

    DHMS_STRING = auto()
    """Convert the timedelta to a string in the format 'D d HH:MM:SS'.

    The 'D d' part will only be included if the number of days is non-zero.
    """

    DHMS_STRING_LONG = auto()
    """Convert the timedelta to a string in the format 'D days HH:MM:SS'.

    The 'D days' part will only be included if the number of days is non-zero.
    If the number of days is one, it will be written as '1 day'.
    """

    WDHMS_STRING = auto()
    """Convert the timedelta to a string in the format 'W w D d HH:MM:SS'.

    The 'W w' part will only be included if the number of weeks is non-zero.
    The 'D d' part will only be included if the number of days is non-zero.
    """

    WDHMS_STRING_LONG = auto()
    """Convert the timedelta to a string as 'W weeks D days HH:MM:SS'.

    The 'W weeks' part will only be included if the number of weeks is
    non-zero. If the number of weeks is one, it will be written as '1 week'.
    The 'D days' part will only be included if the number of days is non-zero.
    If the number of days is one, it will be written as '1 day'.
    """


class OptionalArgsDict(OptArgsDict, total=False):
    """Optional arguments for the tableio package.

    This is a TypedDict that describes the optional arguments that can be
    passed to the factory in the tableio package.
    For description of the arguments, see the class derived from TableIO
    that uses the arguments.
    The possible optional arguments includ the arguments in
    mformat.factory.OptArgsDict plus the arguments specific to the tableio
    package.
    """

    csv_dialect: Optional[CsvDialect]
    """The type/dialect of CSV file to write. None for default type."""

    csv_delimiter: Optional[str]
    """The delimiter to use for CSV files. None for default delimiter."""

    csv_quoting: Optional[str]
    """The quoting style to use for CSV files.

    Allowed values (case-insensitive): 'all', 'minimal',
    'nonnumeric', 'none', 'strings', 'notnull'.
    None for default quoting."""

    csv_quotechar: Optional[str]
    """The quote character to use for CSV files. None for default."""

    csv_lineterminator: Optional[str]
    """The line terminator to use for CSV files. None for default."""

    csv_escapechar: Optional[str]
    """The escape character to use for CSV files. None for default."""

    timedelta_fallback: Optional[TimeDeltaFallback]
    """The fallback format to use for timedelta, when no native support.

    Silently ignored if the implementation provides native support for
    timedelta values. None for default (TimeDeltaFallback.HMS_STRING).
    """


type OptionalArgs = Optional[OptionalArgsDict]
"""Optional arguments for the factory in the tableio package."""

_MFORMAT_OPTARG_NAMES: set[str] = set(OptArgsDict.__annotations__)


def mformat_optargs_from_optionalargs(optional_args: OptionalArgs) \
        -> Optional[OptArgsDict]:
    """Convert the optional arguments to a dictionary of arguments for mformat.

    Args:
        optional_args: The optional arguments to convert.
    Returns:
        A dictionary of arguments for mformat.
    """
    if optional_args is None:
        return None
    ret = {
        key: value for key, value in optional_args.items()
        if key in _MFORMAT_OPTARG_NAMES and value is not None
    }
    return cast(OptArgsDict, ret)
