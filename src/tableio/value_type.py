#! /usr/bin/env python3
"""Value types for the tableio package."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional, cast, Sequence, Mapping, TypeVar, \
    NamedTuple
from datetime import datetime

# types used to describe input and output data
type Value = Optional[str | int | float | datetime]
type NumRow = list[Value]
type NumRowSeq = Sequence[Value]
type NameRow = dict[str, Value]
Row = TypeVar('Row', NumRow, NameRow)
type NameRowMap = Mapping[str, Value]
type NumData = list[NumRow]
type NumDataSeq = Sequence[NumRowSeq]
type NameData = list[NameRow]
type NameDataMap = Sequence[NameRowMap]
type Data[Row] = list[Row]
DataCov = TypeVar('DataCov', NumDataSeq, NameDataMap)


class Fmt(NamedTuple):
    """Format specification for value(s)."""

    bold: bool
    """If the value(s) should be bold."""
    italic: bool
    """If the value(s) should be italic."""


class ValueFmt(NamedTuple):
    """Value with format specification."""

    value: Value
    """The value."""
    fmt: Fmt
    """The format specification."""


type NumRowFmt = Sequence[ValueFmt]
type NameRowFmt = Mapping[str, ValueFmt]
type NumDataFmt = Sequence[NumRowFmt]
type NameDataFmt = Sequence[NameRowFmt]


class FmtNumRow(NamedTuple):
    """Formatted number row."""

    values: NumRowSeq
    """The sequence of values in the row."""
    fmt: Fmt
    """The format specification for the row."""


class FmtNameRow(NamedTuple):
    """Formatted name row."""

    values: NameRowMap
    """The mapping of value names to values in the row."""
    fmt: Fmt
    """The format specification for the row."""


type FmtNumData = Sequence[FmtNumRow]
type FmtNameData = Sequence[FmtNameRow]


def num_row_to_str_list(row: NumRowSeq) -> list[str]:
    """Convert NumRow to list of str."""
    ret: list[str] = []
    for i in row:
        if isinstance(i, str):
            ret.append(i)
        elif i is None:
            raise TypeError('Found None when expecting str.')
        else:
            ret.append(str(i))
    return ret


def str_list_to_num_row(row: list[str]) -> NumRow:
    """Convert list of str to NumRow."""
    return cast(NumRow, row)


# flake8-docstrings/pydocstyle misses the docstring on `def func[T](...)`.
T = TypeVar('T')


def get_checked_type(value: Optional[object],
                     expected_type: type[T]) -> T:
    """Return value unchanged while narrowing it to the expected type.

    This helper is a non-raising cast for code that has already established
    the runtime type by other means. The expected_type argument exists so
    static type checkers can infer the target type.
    Any runtime mismatch will raise an AssertionError as this will be
    an internal programming error.

    Args:
        value: The value to check. Must not be None.
        expected_type: The expected type.
    Returns:
        The value unchanged, narrowed to the expected type.
    """
    assert value is not None
    assert isinstance(value, expected_type)
    return value
