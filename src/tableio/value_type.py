#! /usr/bin/env python3
"""Value types for the tableio package."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional, cast, Sequence, Mapping, TypeVar, \
    NamedTuple
from datetime import datetime
from tableio.color import Color


class Fmt(NamedTuple):
    """Format specification for value(s)."""

    bold: bool = False
    """If the value(s) should be bold."""
    italic: bool = False
    """If the value(s) should be italic."""
    highlight: Color = Color.NONE
    """The highlight color."""


class ValueFmt(NamedTuple):
    """Value with format specification."""

    value: Value
    """The value."""
    fmt: Fmt
    """The format specification."""


# types used to describe input and output data
type Value = Optional[str | int | float | datetime]
Valuetype = TypeVar('Valuetype', Value, ValueFmt)
type ListRow[Valuetype] = list[Valuetype]
type ListRowSeq[Valuetype] = Sequence[Valuetype]
type DictRow[Valuetype] = dict[str, Valuetype]
# Row = TypeVar('Row', ListRow[Valuetype], DictRow[Valuetype])
type DictRowMap[Valuetype] = Mapping[str, Valuetype]
type ListData[Valuetype] = list[ListRow[Valuetype]]
type ListDataSeq[Valuetype] = Sequence[ListRowSeq[Valuetype]]
type DictData[Valuetype] = list[DictRow[Valuetype]]
type DictDataMap[Valuetype] = Sequence[DictRowMap[Valuetype]]
# type Data = list[Row[Valuetype]]
# DataCov = TypeVar('DataCov', ListDataSeq[Valuetype],
#                  DictDataMap[Valuetype])


class FmtListRow(NamedTuple):
    """Formatted Listber row."""

    values: ListRowSeq[Value]
    """The sequence of values in the row."""
    fmt: Fmt
    """The format specification for the row."""


class FmtDictRow(NamedTuple):
    """Formatted Dict row."""

    values: DictRowMap[Value]
    """The mapping of value names to values in the row."""
    fmt: Fmt
    """The format specification for the row."""


type FmtListData = Sequence[FmtListRow]
type FmtDictData = Sequence[FmtDictRow]


def list_row_to_str_list(row: ListRowSeq[Value]) -> list[str]:
    """Convert ListRow to list of str."""
    ret: list[str] = []
    for i in row:
        if isinstance(i, str):
            ret.append(i)
        elif i is None:
            raise TypeError('Found None when expecting str.')
        else:
            ret.append(str(i))
    return ret


def str_list_to_list_row(row: list[str]) -> ListRow[Value]:
    """Convert list of str to ListRow."""
    return cast(ListRow[Value], row)


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
