#! /usr/local/bin/python3
"""Tests for the value_type module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import inspect
from datetime import datetime

import pytest
from pytest import CaptureFixture

from tableio.value_type import Fmt, ValueFmt, \
    FmtListRow, FmtDictRow, Value, dict_row_to_str_dict, \
    get_checked_type, list_row_to_str_list, strip_format_list, \
    str_list_to_list_row

from .check_capsys import check_capsys


@pytest.mark.parametrize(
    ('row', 'expected'),
    [
        pytest.param([], [], id='empty'),
        pytest.param(('text', 1, 2.5), ['text', '1', '2.5'], id='scalars'),
        pytest.param(
            ('row', datetime(2026, 3, 16, 7, 8, 9)),
            ['row', '2026-03-16 07:08:09'],
            id='datetime',
        ),
    ],
)
def test_list_row_to_str_list_converts_values(
        row: tuple[str | int | float | datetime, ...] |
        list[str | int | float | datetime], expected: list[str],
        capsys: CaptureFixture[str]) -> None:
    """Test that list_row_to_str_list converts supported values to strings."""
    assert list_row_to_str_list(row) == expected
    check_capsys(capsys)


def test_list_row_to_str_list_rejects_none(
        capsys: CaptureFixture[str]) -> None:
    """Test that list_row_to_str_list raises for None values."""
    with pytest.raises(ValueError, match='Found None when expecting str.'):
        list_row_to_str_list(['value', None])
    check_capsys(capsys)


def test_list_row_to_str_list_converts_formatted_values(
        capsys: CaptureFixture[str]) -> None:
    """Test that list_row_to_str_list unwraps formatted values."""
    fmt = Fmt(bold=True)
    row = [ValueFmt(value='text', fmt=fmt), ValueFmt(value=2, fmt=fmt)]
    assert list_row_to_str_list(row) == ['text', '2']
    check_capsys(capsys)


def test_list_row_to_str_list_converts_none_to_empty_string(
        capsys: CaptureFixture[str]) -> None:
    """Test that list_row_to_str_list can convert None to empty strings."""
    fmt = Fmt(italic=True)
    row = [ValueFmt(value='value', fmt=fmt), ValueFmt(value=None, fmt=fmt)]
    assert list_row_to_str_list(row, none_is_empty=True) == ['value', '']
    check_capsys(capsys)


def test_dict_row_to_str_dict_converts_values(
        capsys: CaptureFixture[str]) -> None:
    """Test that dict_row_to_str_dict converts supported values."""
    fmt = Fmt(bold=True)
    row = {
        'name': ValueFmt(value='cell', fmt=fmt),
        'count': ValueFmt(value=2, fmt=fmt)
    }
    assert dict_row_to_str_dict(row) == {'name': 'cell', 'count': '2'}
    check_capsys(capsys)


def test_dict_row_to_str_dict_rejects_none(
        capsys: CaptureFixture[str]) -> None:
    """Test that dict_row_to_str_dict raises for None values."""
    with pytest.raises(ValueError, match='Found None when expecting str.'):
        dict_row_to_str_dict({'value': None})
    check_capsys(capsys)


def test_dict_row_to_str_dict_converts_none_to_empty_string(
        capsys: CaptureFixture[str]) -> None:
    """Test that dict_row_to_str_dict can convert None to empty strings."""
    fmt = Fmt(italic=True)
    row = {'value': ValueFmt(value=None, fmt=fmt)}
    assert dict_row_to_str_dict(row, none_is_empty=True) == {'value': ''}
    check_capsys(capsys)


def test_str_list_to_list_row_returns_same_list_object(
        capsys: CaptureFixture[str]) -> None:
    """Test that str_list_to_list_row preserves the original list object."""
    row = ['first', 'second']
    converted = str_list_to_list_row(row)
    assert converted is row
    assert converted == ['first', 'second']
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('value', 'expected_type'),
    [
        pytest.param('text', str, id='matching-str'),
        pytest.param(1, int, id='matching-int'),
    ]
)
def test_get_checked_type_ok(
        value: object | None, expected_type: type[object],
        capsys: CaptureFixture[str]) -> None:
    """Test that get_checked_type returns the original value unchanged."""
    assert get_checked_type(value, expected_type) == value
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('value', 'expected_type'),
    [
        pytest.param(None, str, id='none'),
        pytest.param(datetime(2026, 3, 16, 7, 8, 9), str, id='mismatch'),
    ]
)
def test_get_checked_type_nok(
        value: object | None, expected_type: type[object],
        capsys: CaptureFixture[str]) -> None:
    """Test that get_checked_type returns the original value unchanged."""
    with pytest.raises(AssertionError):
        _ = get_checked_type(value, expected_type)
    check_capsys(capsys)


def test_value_type_named_tuples_store_runtime_values(
        capsys: CaptureFixture[str]) -> None:
    """Test that the public NamedTuple types preserve their stored values."""
    fmt = Fmt(bold=True, italic=False)
    value_fmt = ValueFmt(value='cell', fmt=fmt)
    fmt_num_row = FmtListRow(values=('cell', 2), fmt=fmt)
    fmt_name_row = FmtDictRow(values={'first': 'cell'}, fmt=fmt)
    assert fmt.bold is True
    assert fmt.italic is False
    assert value_fmt.value == 'cell'
    assert value_fmt.fmt is fmt
    assert fmt_num_row.values == ('cell', 2)
    assert fmt_num_row.fmt is fmt
    assert fmt_name_row.values == {'first': 'cell'}
    assert fmt_name_row.fmt is fmt
    check_capsys(capsys)


def test_value_type_named_tuples_require_explicit_values(
        capsys: CaptureFixture[str]) -> None:
    """Test that the public NamedTuple types define no runtime defaults."""
    value_fmt_signature = inspect.signature(ValueFmt)
    fmt_num_row_signature = inspect.signature(FmtListRow)
    fmt_name_row_signature = inspect.signature(FmtDictRow)
    assert value_fmt_signature.parameters['value'].default is \
        inspect.Parameter.empty
    assert value_fmt_signature.parameters['fmt'].default is \
        inspect.Parameter.empty
    assert fmt_num_row_signature.parameters['values'].default is \
        inspect.Parameter.empty
    assert fmt_num_row_signature.parameters['fmt'].default is \
        inspect.Parameter.empty
    assert fmt_name_row_signature.parameters['values'].default is \
        inspect.Parameter.empty
    assert fmt_name_row_signature.parameters['fmt'].default is \
        inspect.Parameter.empty
    check_capsys(capsys)


def test_strip_format_list_returns_plain_data_unchanged(
        capsys: CaptureFixture[str]) -> None:
    """Test that strip_format_list preserves plain list data objects."""
    data: list[list[Value]] = [['cell', 1], [None, 2.5]]
    stripped = strip_format_list(data)
    assert stripped is data
    assert stripped == [['cell', 1], [None, 2.5]]
    check_capsys(capsys)


def test_strip_format_list_strips_formatted_data(
        capsys: CaptureFixture[str]) -> None:
    """Test that strip_format_list unwraps formatted list data."""
    fmt = Fmt(bold=True)
    data = (
        (ValueFmt(value='cell', fmt=fmt), ValueFmt(value=None, fmt=fmt)),
        (ValueFmt(value=2, fmt=fmt), ValueFmt(value=3.5, fmt=fmt)),
    )
    stripped = strip_format_list(data)
    assert stripped == [['cell', None], [2, 3.5]]
    assert id(stripped) != id(data)
    assert isinstance(stripped, list)
    assert isinstance(stripped[0], list)
    check_capsys(capsys)
