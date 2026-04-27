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
