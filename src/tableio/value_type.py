#! /usr/bin/env python3
"""Value types for the tableio package."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional, cast, Sequence, Mapping, TypeVar, \
    NamedTuple, overload, TypeGuard
from datetime import datetime
from tableio.color import Color

# ----------------------------------------------------------------------------
# types used to describe input and output data
# ----------------------------------------------------------------------------

type Value = Optional[str | int | float | datetime]


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


CellT = TypeVar('CellT', Value, ValueFmt)
type ListRow[CellValue: (Value, ValueFmt)] = list[CellValue]
type ListRowSeq[CellValue: (Value, ValueFmt)] = Sequence[CellValue]
type DictRow[CellValue: (Value, ValueFmt)] = dict[str, CellValue]
type DictRowMap[CellValue: (Value, ValueFmt)] = Mapping[str, CellValue]
type ListData[CellValue: (Value, ValueFmt)] = list[ListRow[CellValue]]
type ListDataSeq[CellValue: (Value, ValueFmt)] = \
    Sequence[ListRowSeq[CellValue]]
type DictData[CellValue: (Value, ValueFmt)] = list[DictRow[CellValue]]
type DictDataMap[CellValue: (Value, ValueFmt)] = \
    Sequence[DictRowMap[CellValue]]


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


# ----------------------------------------------------------------------------
# helper functions to convert between different types of data
# ----------------------------------------------------------------------------

def get_plain_value(cell: CellT) -> Value:
    """Return the plain value stored in a cell."""
    if isinstance(cell, ValueFmt):
        return cell.value
    return cell


def value_to_str(value: Value, none_is_empty: bool = False) -> str:
    """Convert a plain value to its string representation.

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
        raise ValueError('Found None when expecting str.')
    return str(value)


def list_row_to_str_list(row: ListRowSeq[CellT],
                         none_is_empty: bool = False) -> list[str]:
    """Convert ListRow to list of str.

    Args:
        row: The row to convert.
        none_is_empty: If True, None values are converted to empty strings.
                       If False, None values will raise ValueError.
    Raises:
        ValueError: If none_is_empty is False and a None value is found.
    Returns:
        The converted row.
    """
    return [value_to_str(get_plain_value(cell), none_is_empty)
            for cell in row]


def dict_row_to_str_dict(row: DictRowMap[CellT],
                         none_is_empty: bool = False) -> dict[str, str]:
    """Convert DictRow to dict of str.

    Args:
        row: The row to convert.
        none_is_empty: If True, None values are converted to empty strings.
                       If False, None values will raise ValueError.
    Raises:
        ValueError: If none_is_empty is False and a None value is found.
    Returns:
        The converted row.
    """
    return {key: value_to_str(get_plain_value(value), none_is_empty)
            for key, value in row.items()}


def str_list_to_list_row(row: list[str]) -> ListRow[Value]:
    """Convert list of str to ListRow."""
    return cast(ListRow[Value], row)


# flake8-docstrings/pydocstyle misses docstrings on PEP 695 functions.
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


def has_format_list(data: ListDataSeq[CellT]) -> bool:
    """Return whether any cell in the list data carries formatting."""
    for row in data:
        for cell in row:
            if isinstance(cell, ValueFmt):
                return True
    return False


def is_plain_list_data(
        data: ListDataSeq[CellT]) -> TypeGuard[ListDataSeq[Value]]:
    """Return whether the list data contains plain values only."""
    return not has_format_list(data)


@overload
def strip_format_list(data: ListDataSeq[Value]) -> ListDataSeq[Value]:
    ...


@overload
def strip_format_list(data: ListDataSeq[ValueFmt]) -> ListData[Value]:
    ...


def strip_format_list(data: ListDataSeq[CellT]) -> ListDataSeq[Value]:
    """Return list data with any cell formatting removed.

    If the input already contains plain values only, the original data object
    is returned unchanged. Formatted data is converted to a new list of lists
    containing the plain values.

    Args:
        data: The list data to convert.
    Returns:
        The plain-value list data.
    """
    if is_plain_list_data(data):
        return data
    return [[get_plain_value(cell) for cell in row] for row in data]
