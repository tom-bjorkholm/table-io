#! /usr/local/bin/python3
"""Tests for the value_type module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import inspect
from datetime import datetime
from types import MappingProxyType
from typing import Any, Mapping, cast

import pytest
from pytest import CaptureFixture

import tableio.value_type as value_type_module
from tableio.color import Color
from tableio.value_type import Fmt, ValueFmt, \
    FmtListRow, FmtDictRow, Value, DataForExtraColumn, \
    MissingDataForColumn, dict_row_to_str_dict, fmt_set_in_all, \
    fmt_set_in_both, format_each_cell_dict, format_each_cell_list, \
    get_checked_type, list_row_to_str_list, normalize_dict_data, \
    row_fmt_from_cell_fmt_dict, row_fmt_from_cell_fmt_list, \
    row_format_each_cell_dict, row_format_each_cell_list, \
    row_strip_format_dict, row_strip_format_list, strip_format_dict, \
    strip_format_list, str_list_to_list_row

from .check_capsys import check_capsys


@pytest.mark.parametrize(
    ('row', 'expected'),
    [
        pytest.param([], [], id='empty'),
        pytest.param(('text', True, 2.5), ['text', 'True', '2.5'],
                     id='scalars'),
        pytest.param(('row', datetime(2026, 3, 16, 7, 8, 9)),
                     ['row', '2026-03-16T07:08:09'], id='datetime',),
    ],)
def test_list_row_to_str_list_converts_values(
        row: tuple[str | bool | int | float | datetime, ...] |
        list[str | bool | int | float | datetime], expected: list[str],
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
        pytest.param(True, bool, id='matching-bool'),
        pytest.param(1, int, id='matching-int'),
    ])
def test_get_checked_type_ok(value: object | None, expected_type: type[object],
                             capsys: CaptureFixture[str]) -> None:
    """Test that get_checked_type returns the original value unchanged."""
    assert get_checked_type(value, expected_type) == value
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('value', 'expected_type'),
    [
        pytest.param(None, str, id='none'),
        pytest.param(datetime(2026, 3, 16, 7, 8, 9), str, id='mismatch'),
    ])
def test_get_checked_type_nok(value: object | None,
                              expected_type: type[object],
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


def test_strip_format_dict_returns_plain_data_unchanged(
        capsys: CaptureFixture[str]) -> None:
    """Test that strip_format_dict preserves plain dict data objects."""
    data: list[dict[str, Value]] = [
        {'name': 'cell', 'count': 1},
        {'name': None, 'count': 2.5}
    ]
    stripped = strip_format_dict(data)
    assert stripped is data
    assert stripped == [
        {'name': 'cell', 'count': 1},
        {'name': None, 'count': 2.5}
    ]
    check_capsys(capsys)


def test_strip_format_dict_strips_formatted_data(
        capsys: CaptureFixture[str]) -> None:
    """Test that strip_format_dict unwraps formatted dict data."""
    fmt = Fmt(bold=True)
    data = (
        {
            'name': ValueFmt(value='cell', fmt=fmt),
            'count': ValueFmt(value=None, fmt=fmt)
        },
        {
            'name': ValueFmt(value='next', fmt=fmt),
            'count': ValueFmt(value=3.5, fmt=fmt)
        }
    )
    stripped = strip_format_dict(data)
    assert stripped == [
        {'name': 'cell', 'count': None},
        {'name': 'next', 'count': 3.5}
    ]
    assert id(stripped) != id(data)
    assert isinstance(stripped, list)
    assert isinstance(stripped[0], dict)
    check_capsys(capsys)


def test_row_strip_format_list_returns_empty_list(
        capsys: CaptureFixture[str]) -> None:
    """Test that row_strip_format_list returns an empty outer list."""
    data: tuple[FmtListRow, ...] = ()
    stripped = row_strip_format_list(data)
    assert stripped == []
    assert isinstance(stripped, list)
    check_capsys(capsys)


def test_row_strip_format_list_preserves_inner_row_objects(
        capsys: CaptureFixture[str]) -> None:
    """Test that row_strip_format_list preserves each row value sequence."""
    tuple_values: tuple[Value, ...] = ('left', 1)
    list_values: list[Value] = [None, 2.5]
    data = (
        FmtListRow(values=tuple_values, fmt=Fmt(bold=True)),
        FmtListRow(values=list_values, fmt=Fmt(italic=True))
    )
    stripped = row_strip_format_list(data)
    assert stripped == [tuple_values, list_values]
    assert isinstance(stripped, list)
    assert id(stripped) != id(data)
    assert stripped[0] is tuple_values
    assert stripped[1] is list_values
    check_capsys(capsys)


def test_row_strip_format_dict_returns_empty_list(
        capsys: CaptureFixture[str]) -> None:
    """Test that row_strip_format_dict returns an empty outer list."""
    data: tuple[FmtDictRow, ...] = ()
    stripped = row_strip_format_dict(data)
    assert stripped == []
    assert isinstance(stripped, list)
    check_capsys(capsys)


def test_row_strip_format_dict_preserves_inner_mapping_objects(
        capsys: CaptureFixture[str]) -> None:
    """Test that row_strip_format_dict preserves each row value mapping."""
    dict_values: dict[str, Value] = {'beta': 2, 'alpha': 'cell'}
    proxy_values: Mapping[str, Value] = MappingProxyType({'only': None})
    data = (
        FmtDictRow(values=dict_values, fmt=Fmt(bold=True)),
        FmtDictRow(values=proxy_values, fmt=Fmt(italic=True))
    )
    stripped = row_strip_format_dict(data)
    assert [dict(row) for row in stripped] == [
        {'beta': 2, 'alpha': 'cell'},
        {'only': None}
    ]
    assert isinstance(stripped, list)
    assert id(stripped) != id(data)
    assert stripped[0] is dict_values
    assert stripped[1] is proxy_values
    assert list(stripped[0].keys()) == ['beta', 'alpha']
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('data', 'expected'),
    [
        pytest.param([], [], id='empty'),
        pytest.param(
            [
                FmtListRow(values=('left', 1), fmt=Fmt(bold=True)),
                FmtListRow(values=(None,), fmt=Fmt(italic=True))
            ],
            [
                [
                    ValueFmt(value='left', fmt=Fmt(bold=True)),
                    ValueFmt(value=1, fmt=Fmt(bold=True))
                ],
                [ValueFmt(value=None, fmt=Fmt(italic=True))]
            ],
            id='rows')
    ])
def test_row_format_each_cell_list(data: list[FmtListRow],
                                   expected: list[list[ValueFmt]],
                                   capsys: CaptureFixture[str]) -> None:
    """Test that row_format_each_cell_list applies each row format."""
    assert row_format_each_cell_list(data) == expected
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('data', 'expected'),
    [
        pytest.param([], [], id='empty'),
        pytest.param(
            [
                FmtDictRow(values={'beta': 2, 'alpha': 'cell'},
                           fmt=Fmt(bold=True)),
                FmtDictRow(values={'only': None}, fmt=Fmt(italic=True))
            ],
            [
                {
                    'beta': ValueFmt(value=2, fmt=Fmt(bold=True)),
                    'alpha': ValueFmt(value='cell', fmt=Fmt(bold=True))
                },
                {'only': ValueFmt(value=None, fmt=Fmt(italic=True))}
            ],
            id='rows')
    ])
def test_row_format_each_cell_dict(data: list[FmtDictRow],
                                   expected: list[dict[str, ValueFmt]],
                                   capsys: CaptureFixture[str]) -> None:
    """Test that row_format_each_cell_dict applies each row format."""
    formatted = row_format_each_cell_dict(data)
    assert formatted == expected
    if formatted:
        assert list(formatted[0].keys()) == ['beta', 'alpha']
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('data', 'fmt', 'expected'),
    [
        pytest.param([], Fmt(), [], id='empty'),
        pytest.param(
            [('left', 1), (None,)], Fmt(bold=True),
            [
                [
                    ValueFmt(value='left', fmt=Fmt(bold=True)),
                    ValueFmt(value=1, fmt=Fmt(bold=True))
                ],
                [ValueFmt(value=None, fmt=Fmt(bold=True))]
            ],
            id='values')
    ])
def test_format_each_cell_list(
        data: list[tuple[Value, ...]], fmt: Fmt,
        expected: list[list[ValueFmt]], capsys: CaptureFixture[str]) -> None:
    """Test that format_each_cell_list applies the provided format."""
    assert format_each_cell_list(data, fmt) == expected
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('data', 'fmt', 'expected'),
    [
        pytest.param([], Fmt(), [], id='empty'),
        pytest.param(
            [
                {'beta': 2, 'alpha': 'cell'},
                {'only': None}
            ],
            Fmt(italic=True),
            [
                {
                    'beta': ValueFmt(value=2, fmt=Fmt(italic=True)),
                    'alpha': ValueFmt(value='cell', fmt=Fmt(italic=True))
                },
                {'only': ValueFmt(value=None, fmt=Fmt(italic=True))}
            ],
            id='values')
    ])
def test_format_each_cell_dict(data: list[dict[str, Value]], fmt: Fmt,
                               expected: list[dict[str, ValueFmt]],
                               capsys: CaptureFixture[str]) -> None:
    """Test that format_each_cell_dict applies the provided format."""
    formatted = format_each_cell_dict(data, fmt)
    assert formatted == expected
    if formatted:
        assert list(formatted[0].keys()) == ['beta', 'alpha']
    check_capsys(capsys)


def test_normalize_dict_data_returns_matching_data_unchanged(
        capsys: CaptureFixture[str]) -> None:
    """Test that normalize_dict_data keeps already matching data unchanged."""
    data: list[dict[str, Value]] = [
        {'beta': 2, 'alpha': 'cell'},
        {'alpha': None, 'beta': 3.5}
    ]
    normalized = normalize_dict_data(data, ['alpha', 'beta'])
    assert normalized is data
    assert normalized == data
    check_capsys(capsys)


def test_normalize_dict_data_rejects_duplicate_column_order(
        capsys: CaptureFixture[str]) -> None:
    """Test that normalize_dict_data rejects duplicate column names."""
    data: list[dict[str, Value]] = []
    with pytest.raises(ValueError, match='Duplicate column name'):
        normalize_dict_data(data, ['alpha', 'alpha'])
    check_capsys(capsys)


def test_normalize_dict_data_rejects_empty_column_order(
        capsys: CaptureFixture[str]) -> None:
    """Test that normalize_dict_data rejects empty column_order."""
    data: list[dict[str, Value]] = []
    with pytest.raises(ValueError, match='column_order'):
        normalize_dict_data(data, [])
    check_capsys(capsys)


def test_normalize_dict_data_rejects_missing_column(
        capsys: CaptureFixture[str]) -> None:
    """Test that normalize_dict_data rejects missing required columns."""
    data: list[dict[str, Value]] = [{'alpha': 'cell'}]
    with pytest.raises(MissingDataForColumn, match='beta') as exc_info:
        normalize_dict_data(data, ['alpha', 'beta'])
    assert exc_info.value.key == 'beta'
    check_capsys(capsys)


def test_normalize_dict_data_rejects_extra_column(
        capsys: CaptureFixture[str]) -> None:
    """Test that normalize_dict_data rejects extra columns."""
    data: list[dict[str, Value]] = [{'alpha': 'cell', 'beta': 2}]
    with pytest.raises(DataForExtraColumn, match='beta') as exc_info:
        normalize_dict_data(data, ['alpha'])
    assert exc_info.value.key == 'beta'
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('data', 'row_index'),
    [
        pytest.param([{}, {'alpha': 'cell'}], 0, id='first-row'),
        pytest.param([{'alpha': 'cell'}, {}], 1, id='later-row')
    ])
def test_normalize_dict_data_rejects_empty_rows(
        data: list[dict[str, Value]], row_index: int,
        capsys: CaptureFixture[str]) -> None:
    """Test that normalize_dict_data rejects empty rows."""
    with pytest.raises(ValueError, match=f'index {row_index}'):
        normalize_dict_data(data, ['alpha'], missing_ok=True, extra_ok=True)
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('data', 'row_index'),
    [
        pytest.param(
            [
                {'alpha': 'cell'},
                {'alpha': ValueFmt(value='next', fmt=Fmt(bold=True))}
            ],
            1, id='plain-then-formatted'),
        pytest.param(
            [
                {'alpha': ValueFmt(value='cell', fmt=Fmt(bold=True))},
                {'alpha': 'next'}
            ],
            1, id='formatted-then-plain')
    ])
def test_normalize_dict_data_rejects_mixed_cell_types(
        data: list[dict[str, object]], row_index: int,
        capsys: CaptureFixture[str]) -> None:
    """Test that normalize_dict_data rejects mixed plain and formatted rows."""
    mixed_data = cast(list[dict[str, Value]] | list[dict[str, ValueFmt]], data)
    with pytest.raises(TypeError, match=f'row {row_index}'):
        normalize_dict_data(cast(Any, mixed_data), ['alpha'])
    check_capsys(capsys)


def test_normalize_dict_data_normalizes_plain_rows(
        capsys: CaptureFixture[str]) -> None:
    """Test that normalize_dict_data adds and removes plain row cells."""
    data: list[dict[str, Value]] = [
        {'alpha': 'cell', 'extra': 2},
        {'beta': 3.5}
    ]
    normalized = normalize_dict_data(data, ['alpha', 'beta'], missing_ok=True,
                                     extra_ok=True)
    assert normalized == [
        {'alpha': 'cell', 'beta': None},
        {'alpha': None, 'beta': 3.5}
    ]
    assert normalized is not data
    check_capsys(capsys)


def test_normalize_dict_data_normalizes_formatted_rows(
        capsys: CaptureFixture[str]) -> None:
    """Test that normalize_dict_data fills formatted missing cells."""
    fmt = Fmt(bold=True)
    missing_cell = ValueFmt(value=None, fmt=Fmt())
    data: list[dict[str, ValueFmt]] = [
        {
            'alpha': ValueFmt(value='cell', fmt=fmt),
            'extra': ValueFmt(value=2, fmt=fmt)
        },
        {'beta': ValueFmt(value=3.5, fmt=fmt)}
    ]
    normalized = normalize_dict_data(data, ['alpha', 'beta'], missing_ok=True,
                                     extra_ok=True)
    assert normalized == [
        {'alpha': ValueFmt(value='cell', fmt=fmt), 'beta': missing_cell},
        {'alpha': missing_cell, 'beta': ValueFmt(value=3.5, fmt=fmt)}
    ]
    assert normalized is not data
    check_capsys(capsys)


def test_normalize_dict_data_impl_asserts_if_type_guards_disagree(
        monkeypatch: pytest.MonkeyPatch, capsys: CaptureFixture[str]) -> None:
    """The internal normalize helper keeps a defensive assertion."""
    monkeypatch.setattr(value_type_module, '_first_row_is_plain_dict_data',
                        lambda data: False)
    monkeypatch.setattr(value_type_module, '_first_row_is_formatted_dict_data',
                        lambda data: False)
    normalize_impl = getattr(value_type_module, '_normalize_dict_data_impl')
    with pytest.raises(AssertionError, match='Unreachable code reached'):
        normalize_impl([{'alpha': 'cell'}], ['alpha'])
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('fmt1', 'fmt2', 'expected'),
    [
        pytest.param(Fmt(bold=True, italic=True, highlight=Color.RED),
                     Fmt(bold=True, italic=False, highlight=Color.RED),
                     Fmt(bold=True, italic=False, highlight=Color.RED),
                     id='shared-highlight'),
        pytest.param(Fmt(bold=False, italic=True, highlight=Color.GREEN),
                     Fmt(bold=True, italic=True, highlight=Color.YELLOW),
                     Fmt(bold=False, italic=True, highlight=Color.NONE),
                     id='different-highlight')
    ])
def test_fmt_set_in_both(fmt1: Fmt, fmt2: Fmt, expected: Fmt,
                         capsys: CaptureFixture[str]) -> None:
    """Test that fmt_set_in_both keeps only shared formatting."""
    assert fmt_set_in_both(fmt1, fmt2) == expected
    check_capsys(capsys)


def test_fmt_set_in_all_rejects_empty_sequence(
        capsys: CaptureFixture[str]) -> None:
    """Test that fmt_set_in_all rejects an empty sequence."""
    with pytest.raises(ValueError, match='fmts must not be empty'):
        fmt_set_in_all([])
    check_capsys(capsys)


def test_fmt_set_in_all_merges_all_formats(
        capsys: CaptureFixture[str]) -> None:
    """Test that fmt_set_in_all keeps only formatting shared by all."""
    fmts = [
        Fmt(bold=True, italic=True, highlight=Color.YELLOW),
        Fmt(bold=True, italic=True, highlight=Color.YELLOW),
        Fmt(bold=True, italic=False, highlight=Color.GREEN)
    ]
    assert fmt_set_in_all(fmts) == Fmt(bold=True, italic=False,
                                       highlight=Color.NONE)
    check_capsys(capsys)


def test_row_fmt_from_cell_fmt_list_returns_empty_list(
        capsys: CaptureFixture[str]) -> None:
    """Test that row_fmt_from_cell_fmt_list preserves an empty outer list."""
    assert not row_fmt_from_cell_fmt_list([])
    check_capsys(capsys)


def test_row_fmt_from_cell_fmt_list_merges_formats(
        capsys: CaptureFixture[str]) -> None:
    """Test that row_fmt_from_cell_fmt_list merges each row format."""
    data: list[list[ValueFmt]] = [
        [
            ValueFmt(value='left', fmt=Fmt(bold=True, highlight=Color.RED)),
            ValueFmt(value=1, fmt=Fmt(bold=True, highlight=Color.RED))
        ],
        [
            ValueFmt(value='next', fmt=Fmt(italic=True, highlight=Color.RED)),
            ValueFmt(value=None, fmt=Fmt(italic=True, highlight=Color.GREEN))
        ]
    ]
    assert row_fmt_from_cell_fmt_list(data) == [
        FmtListRow(values=['left', 1],
                   fmt=Fmt(bold=True, highlight=Color.RED)),
        FmtListRow(values=['next', None],
                   fmt=Fmt(italic=True, highlight=Color.NONE))
    ]
    check_capsys(capsys)


def test_row_fmt_from_cell_fmt_list_rejects_empty_row(
        capsys: CaptureFixture[str]) -> None:
    """Test that row_fmt_from_cell_fmt_list rejects empty rows."""
    with pytest.raises(ValueError, match='index 1'):
        row_fmt_from_cell_fmt_list([
            [ValueFmt(value='left', fmt=Fmt())],
            []
        ])
    check_capsys(capsys)


def test_row_fmt_from_cell_fmt_list_plain_values(
        capsys: CaptureFixture[str]) -> None:
    """Test row_fmt_from_cell_fmt_list with plain values."""
    data: list[list[Value]] = [
        ['Alice', 30],
        [None, 'text']
    ]
    assert row_fmt_from_cell_fmt_list(data) == [
        FmtListRow(values=['Alice', 30], fmt=Fmt()),
        FmtListRow(values=[None, 'text'], fmt=Fmt())
    ]
    check_capsys(capsys)


def test_row_fmt_from_cell_fmt_list_plain_rejects_empty_row(
        capsys: CaptureFixture[str]) -> None:
    """Test that row_fmt_from_cell_fmt_list rejects empty plain rows."""
    with pytest.raises(ValueError, match='index 0'):
        row_fmt_from_cell_fmt_list([[]])
    check_capsys(capsys)


def test_row_fmt_from_cell_fmt_dict_returns_empty_list(
        capsys: CaptureFixture[str]) -> None:
    """Test that row_fmt_from_cell_fmt_dict preserves an empty outer list."""
    assert not row_fmt_from_cell_fmt_dict([])
    check_capsys(capsys)


def test_row_fmt_from_cell_fmt_dict_merges_formats(
        capsys: CaptureFixture[str]) -> None:
    """Test that row_fmt_from_cell_fmt_dict merges each row format."""
    data: list[dict[str, ValueFmt]] = [
        {
            'beta': ValueFmt(value=2,
                             fmt=Fmt(bold=True, highlight=Color.YELLOW)),
            'alpha': ValueFmt(value='cell',
                              fmt=Fmt(bold=True, highlight=Color.YELLOW))
        },
        {
            'only': ValueFmt(value=None,
                             fmt=Fmt(italic=True, highlight=Color.GREEN)),
            'other': ValueFmt(value='text',
                              fmt=Fmt(italic=True, highlight=Color.RED))
        }
    ]
    merged = row_fmt_from_cell_fmt_dict(data)
    assert merged == [
        FmtDictRow(values={'beta': 2, 'alpha': 'cell'},
                   fmt=Fmt(bold=True, highlight=Color.YELLOW)),
        FmtDictRow(values={'only': None, 'other': 'text'},
                   fmt=Fmt(italic=True, highlight=Color.NONE))
    ]
    assert list(cast(dict[str, Value], merged[0].values).keys()) == [
        'beta',
        'alpha'
    ]
    check_capsys(capsys)


def test_row_fmt_from_cell_fmt_dict_rejects_empty_row(
        capsys: CaptureFixture[str]) -> None:
    """Test that row_fmt_from_cell_fmt_dict rejects empty rows."""
    with pytest.raises(ValueError, match='index 0'):
        row_fmt_from_cell_fmt_dict([{}])
    check_capsys(capsys)


def test_row_fmt_from_cell_fmt_dict_plain_values(
        capsys: CaptureFixture[str]) -> None:
    """Test row_fmt_from_cell_fmt_dict with plain values."""
    data: list[dict[str, Value]] = [
        {'name': 'Alice', 'age': 30},
        {'name': None, 'age': 0}
    ]
    merged = row_fmt_from_cell_fmt_dict(data)
    assert merged == [
        FmtDictRow(values={'name': 'Alice', 'age': 30}, fmt=Fmt()),
        FmtDictRow(values={'name': None, 'age': 0}, fmt=Fmt())
    ]
    assert list(cast(dict[str, Value], merged[0].values).keys()) == [
        'name', 'age']
    check_capsys(capsys)


def test_row_fmt_from_cell_fmt_dict_plain_rejects_empty_row(
        capsys: CaptureFixture[str]) -> None:
    """Test row_fmt_from_cell_fmt_dict rejects empty plain rows."""
    with pytest.raises(ValueError, match='index 0'):
        row_fmt_from_cell_fmt_dict([{}])
    check_capsys(capsys)
