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


def has_format_dict(data: DictDataMap[CellT]) -> bool:
    """Return whether any cell in the dict data carries formatting."""
    for row in data:
        for cell in row.values():
            if isinstance(cell, ValueFmt):
                return True
    return False


def is_plain_dict_data(
        data: DictDataMap[CellT]) -> TypeGuard[DictDataMap[Value]]:
    """Return whether the dict data contains plain values only."""
    return not has_format_dict(data)


@overload
def strip_format_dict(data: DictDataMap[Value]) -> DictDataMap[Value]:
    ...


@overload
def strip_format_dict(data: DictDataMap[ValueFmt]) -> DictData[Value]:
    ...


def strip_format_dict(data: DictDataMap[CellT]) -> DictDataMap[Value]:
    """Return dict data with any cell formatting removed.

    If the input already contains plain values only, the original data object
    is returned unchanged. Formatted data is converted to a new list of dicts
    containing the plain values.

    Args:
        data: The dict data to convert.
    Returns:
        The plain-value dict data.
    """
    if is_plain_dict_data(data):
        return data
    return [{key: get_plain_value(value) for key, value in row.items()}
            for row in data]


def row_strip_format_list(data: FmtListData) -> ListDataSeq[Value]:
    """Return list row data without the row format wrappers.

    Args:
        data: The list data to strip.
    Returns:
        A new outer list containing the original row value sequences.
    """
    return [row.values for row in data]


def row_strip_format_dict(data: FmtDictData) -> DictDataMap[Value]:
    """Return dict row data without the row format wrappers.

    Args:
        data: The dict data to strip.
    Returns:
        A new outer list containing the original row value mappings.
    """
    return [row.values for row in data]


def row_format_each_cell_list(data: FmtListData) -> ListData[ValueFmt]:
    """Format each cell individually with the format of the row.

    For each each row in the input data use the format of the row to format
    the value of each cell in the row. Return the formatted data as a list of
    lists of ValueFmt.
    Args:
        data: The list data to format.
    Returns:
        The formatted list data.
    """
    return [[ValueFmt(value=cell, fmt=row.fmt) for cell in row.values]
            for row in data]


def row_format_each_cell_dict(data: FmtDictData) -> DictData[ValueFmt]:
    """Format each cell individually with the format of the row.

    For each each row in the input data use the format of the row to format
    the value of each cell in the row. Return the formatted data as a list of
    dicts of ValueFmt.
    Args:
        data: The dict data to format.
    Returns:
        The formatted dict data.
    """
    return [{key: ValueFmt(value=value, fmt=row.fmt)
             for key, value in row.values.items()}
            for row in data]


def format_each_cell_list(data: ListDataSeq[Value],
                          fmt: Fmt = Fmt()) -> ListData[ValueFmt]:
    """Format each cell in the list data with the specified format.

    Args:
        data: The list data to format.
        fmt: The format to apply to the cells.
    Returns:
        The formatted list data.
    """
    return [[ValueFmt(value=cell, fmt=fmt) for cell in row] for row in data]


def format_each_cell_dict(data: DictDataMap[Value],
                          fmt: Fmt = Fmt()) -> DictData[ValueFmt]:
    """Format each cell in the dict data with the specified format.

    Args:
        data: The dict data to format.
        fmt: The format to apply to the cells.
    Returns:
        The formatted dict data.
    """
    return [{key: ValueFmt(value=value, fmt=fmt) for key, value in row.items()}
            for row in data]


class MissingDataForColumn(ValueError):
    """Exception for when data is missing for a needed key (column name)."""

    def __init__(self, key: str):
        """Initialize the exception."""
        self.key = key
        super().__init__(f'Data is missing for key (column name) {key}.')


class DataForExtraColumn(ValueError):
    """Exception for when data is present for key not in the column_order."""

    def __init__(self, key: str):
        """Initialize the exception."""
        self.key = key
        super().__init__(f'Data is present for extra key (column name) {key}.')


def normalize_dict_data(data: DictDataMap[CellT],
                        column_order: list[str],
                        missing_ok: bool = False,
                        extra_ok: bool = False) -> DictDataMap[CellT]:
    """Check and normalize a dict data to have specified columns.

    If all columns in column_order are present as keys in every row,
    and no other keys are present, the original data is returned unchanged.
    If missing_ok is False and data is missing for a column in the
    column_order then an exception is raised.
    If extra_ok is False and data is present for a key not in the
    column_order, an exception is raised.
    The data is normalized by adding None values for missing columns if
    missing_ok is True.
    The data is normalized by removing extra columns if extra_ok is True.
    When normalizing the data, the order of the rows is preserved.
    When data is added of removed, the modification are done on a copy of the
    data and the original data object in argument list is not modified.
    Args:
        data: The dict data to normalize.
        column_order: The order of the columns, that will be present in the
                      keys of the normalized data.
        missing_ok: If True, missing data for a column in the column_order
                    is OK, and None is added for the key (column name) in the
                    row.
                    If False, an exception is raised if data is missing for a
                    key (column name) in the column_order in any row.
        extra_ok: If True, data for a key (column name) not in the column_order
                  is OK, and the key (column name) is removed from the row.
                  If False, an exception is raised if data is present for a
                  key (column name) not in the column_order in any row.
    Raises:
        MissingDataForColumn: If missing_ok is False and data is missing for a
                              key (column name) in the column_order in any row.
        DataForExtraColumn: If extra_ok is False and data is present for a
                            key (column name) not in the column_order in any
                            row.
    Returns:
        The normalized data that may be the same object as the input data.
    """
    # TODO: Implement this function and write comprehensive tests for it.
    return data  # to keep the linter happy until the function is implemented.
