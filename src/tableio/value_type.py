#! /usr/bin/env python3
"""Value types for the tableio package."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional, cast, Sequence, Mapping, TypeVar, \
    NamedTuple, overload, TypeGuard, Generic
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
DataT = TypeVar('DataT', bound='ListData[Value] | DictData[Value]')


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


class ReadResult(NamedTuple, Generic[DataT]):
    """Result of reading data from a file."""

    data: DataT
    """The data read from the table in the file."""

    headings: list[str]
    """The headings read from the file before the table with the data."""


# ----------------------------------------------------------------------------
# helper functions to convert between different types of data
# ----------------------------------------------------------------------------


def fmt_set_in_both(fmt1: Fmt, fmt2: Fmt) -> Fmt:
    """Return the format attributes that are set the same in both formats.

    Bold and italic remain enabled only when they are enabled in both input
    formats. Highlight is preserved only when both input formats use the same
    highlight color; otherwise the result uses Color.NONE.

    Args:
        fmt1: The first argument format.
        fmt2: The second argument format.
    Returns:
        The format that is set in both argument formats.
    """
    return Fmt(bold=fmt1.bold and fmt2.bold,
               italic=fmt1.italic and fmt2.italic,
               highlight=fmt1.highlight if fmt1.highlight == fmt2.highlight
               else Color.NONE)


def fmt_set_in_all(fmts: Sequence[Fmt]) -> Fmt:
    """Return a new format that is set in all argument formats.

    Bold and italic remain enabled only when they are enabled in every input
    format. Highlight is preserved only when every input format uses the same
    highlight color; otherwise the result uses Color.NONE.

    Args:
        fmts: The sequence of formats to merge.
    Returns:
        The format that is set in all argument formats.
    Raises:
        ValueError: If the sequence is empty.
    """
    if not fmts:
        raise ValueError('fmts must not be empty.')
    ret = fmts[0]
    for fmt in fmts[1:]:
        ret = fmt_set_in_both(ret, fmt)
    return ret


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


def row_fmt_from_cell_fmt_list(data: ListData[ValueFmt]) -> FmtListData:
    """Create a list of formatted rows from a list of cell formatted rows.

    For each row in the input data, create a new formatted row with the
    format of the row. The format is the merge of the formats of the cells
    in the row. The merge is done so that a formatting is applied to the row
    if and only if that formatting is applied to all cells in the row.

    Args:
        data: The list of cell formatted rows to create formatted rows from.
    Returns:
        A list of formatted rows.
    Raises:
        ValueError: If any row is empty.
    """
    ret: list[FmtListRow] = []
    for row_index, row in enumerate(data):
        if not row:
            _raise_empty_row_error(row_index)
        vals = [cell.value for cell in row]
        fmt = fmt_set_in_all([cell.fmt for cell in row])
        ret.append(FmtListRow(values=vals, fmt=fmt))
    return ret


def row_fmt_from_cell_fmt_dict(data: DictData[ValueFmt]) -> FmtDictData:
    """Create formatted dict rows from cell-formatted dict rows.

    For each row in the input data, create a new formatted row with the
    format of the row. The format is the merge of the formats of the cells
    in the row. The merge is done so that a formatting is applied to the row
    if and only if that formatting is applied to all cells in the row.

    Args:
        data: The dict rows with cell formatting to convert.
    Returns:
        A list of formatted dict rows.
    Raises:
        ValueError: If any row is empty.
    """
    ret: list[FmtDictRow] = []
    for row_index, row in enumerate(data):
        if not row:
            _raise_empty_row_error(row_index)
        vals = {key: cell.value for key, cell in row.items()}
        fmt = fmt_set_in_all([cell.fmt for cell in row.values()])
        ret.append(FmtDictRow(values=vals, fmt=fmt))
    return ret


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


def _validate_column_order(column_order: list[str]) -> None:
    """Raise if column_order is empty or contains duplicate names."""
    if not column_order:
        raise ValueError('column_order must not be empty.')
    seen_columns: set[str] = set()
    for column_name in column_order:
        if column_name in seen_columns:
            err = f'Duplicate column name in column_order: {column_name}.'
            raise ValueError(err)
        seen_columns.add(column_name)


def _raise_empty_row_error(row_index: int) -> None:
    """Raise the empty-row error with the row index in the message."""
    err = f'Empty rows are not allowed. Found empty row at index {row_index}.'
    raise ValueError(err)


def _first_row_is_plain_dict_data(
        data: DictDataMap[Value] | DictDataMap[ValueFmt]
) -> TypeGuard[DictDataMap[Value]]:
    """Return whether the first cell in the first row is a plain value."""
    first_row = data[0]
    first_cell = next(iter(first_row.values()))
    return not isinstance(first_cell, ValueFmt)


def _first_row_is_formatted_dict_data(
        data: DictDataMap[Value] | DictDataMap[ValueFmt]
) -> TypeGuard[DictDataMap[ValueFmt]]:
    """Return whether the first cell in the first row is formatted."""
    first_row = data[0]
    first_cell = next(iter(first_row.values()))
    return isinstance(first_cell, ValueFmt)


def _normalize_dict_data_with_missing_cell(data: DictDataMap[CellT],
                                           column_order: list[str],
                                           missing_ok: bool,
                                           extra_ok: bool,
                                           missing_cell: CellT) -> \
        DictDataMap[CellT]:
    """Normalize dict data using the provided missing-cell value."""
    column_names = set(column_order)
    needs_normalization = False
    expect_formatted = isinstance(missing_cell, ValueFmt)
    for row_index, row in enumerate(data):
        if not row:
            _raise_empty_row_error(row_index)
        for key, value in row.items():
            if isinstance(value, ValueFmt) != expect_formatted:
                expected = 'ValueFmt' if expect_formatted else 'plain value'
                err = 'Mixed plain and formatted cells are not allowed. ' \
                    f'Found {type(value).__name__} when expecting ' \
                    f'{expected} in row {row_index}.'
                raise TypeError(err)
            if key not in column_names:
                if not extra_ok:
                    raise DataForExtraColumn(key)
                needs_normalization = True
        for column_name in column_order:
            if column_name not in row:
                if not missing_ok:
                    raise MissingDataForColumn(column_name)
                needs_normalization = True
                break
    if not needs_normalization:
        return data
    return [{key: row[key] if key in row else missing_cell
             for key in column_order}
            for row in data]


def _normalize_dict_data_impl(data: DictDataMap[Value] | DictDataMap[ValueFmt],
                              column_order: list[str],
                              missing_ok: bool = False,
                              extra_ok: bool = False) -> \
        DictDataMap[Value] | DictDataMap[ValueFmt]:
    """Normalize dict data for one concrete cell-kind input."""
    _validate_column_order(column_order)
    if not data:
        return data
    if not data[0]:
        _raise_empty_row_error(0)
    if _first_row_is_plain_dict_data(data):
        return _normalize_dict_data_with_missing_cell(
            data,
            column_order,
            missing_ok,
            extra_ok,
            None
        )
    if _first_row_is_formatted_dict_data(data):
        return _normalize_dict_data_with_missing_cell(
            data,
            column_order,
            missing_ok,
            extra_ok,
            ValueFmt(value=None, fmt=Fmt())
        )
    raise AssertionError('Unreachable code reached in normalize_dict_data.')


def normalize_dict_data(data: DictDataMap[CellT],
                        column_order: list[str],
                        missing_ok: bool = False,
                        extra_ok: bool = False) -> DictDataMap[CellT]:
    """Check and normalize a dict data to have specified columns.

    The column_order must not be empty.
    Empty rows are not allowed.
    If all columns in column_order are present as keys in every row,
    and no other keys are present, the original data is returned unchanged.
    If missing_ok is False and data is missing for a column in the
    column_order then an exception is raised.
    If extra_ok is False and data is present for a key not in the
    column_order, an exception is raised.
    The data is normalized by adding None values for missing columns if
    missing_ok is True. For formatted data, missing cells are added as
    ValueFmt(value=None, fmt=Fmt()).
    The data is normalized by removing extra columns if extra_ok is True.
    When normalizing the data, the order of the rows is preserved.
    When data is added of removed, the modification are done on a copy of the
    data and the original data object in argument list is not modified.
    Args:
        data: The dict data to normalize.
        column_order: The order of the columns, that will be present in the
                      keys of the normalized data. Must not be empty.
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
        ValueError: If column_order is empty, contains duplicate column
                    names, or if any row is empty.
        MissingDataForColumn: If missing_ok is False and data is missing for a
                              key (column name) in the column_order in any row.
        DataForExtraColumn: If extra_ok is False and data is present for a
                            key (column name) not in the column_order in any
                            row.
        TypeError: If plain and formatted cells are mixed in the same input.
    Returns:
        The normalized data that may be the same object as the input data.
    """
    return cast(
        DictDataMap[CellT],
        _normalize_dict_data_impl(data, column_order, missing_ok, extra_ok)
    )
