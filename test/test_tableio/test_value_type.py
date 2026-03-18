#! /usr/local/bin/python3
"""Tests for the value_type module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import inspect
from datetime import datetime

import pytest
from pytest import CaptureFixture

from tableio.value_type import Fmt, ValueFmt, \
    FmtListRow, FmtDictRow, \
    get_checked_type, list_row_to_str_list, str_list_to_list_row

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
    with pytest.raises(TypeError, match='Found None when expecting str.'):
        list_row_to_str_list(['value', None])
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
