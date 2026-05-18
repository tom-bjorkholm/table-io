#! /usr/local/bin/python3
"""Tests for the valueconversion module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import date, datetime, time
from types import NoneType

import pytest
from pytest import CaptureFixture

from tableio.valueconversion import UnreasonableTypeConversion, \
    UnreasonableValueConversion, value2bool, value2date, value2datetime, \
    value2float, value2int, value2none, value2str, value2time, value2type, \
    value2type_of

from .check_capsys import check_capsys


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        pytest.param('text', 'text', id='string'),
        pytest.param(True, 'True', id='bool'),
        pytest.param(7, '7', id='int'),
        pytest.param(2.5, '2.5', id='float'),
        pytest.param(datetime(2026, 3, 25, 7, 8, 9), '2026-03-25T07:08:09',
                     id='datetime'),
    ],)
def test_value2str_converts_supported_values(
        value: str | bool | int | float | datetime, expected: str,
        capsys: CaptureFixture[str]) -> None:
    """Test that value2str converts supported values to strings."""
    assert value2str(value) == expected
    check_capsys(capsys)


def test_value2str_rejects_none(capsys: CaptureFixture[str]) -> None:
    """Test that value2str raises for None by default."""
    with pytest.raises(UnreasonableValueConversion, match='to type: str'):
        value2str(None)
    check_capsys(capsys)


def test_value2str_converts_none_to_empty_string(
        capsys: CaptureFixture[str]) -> None:
    """Test that value2str can convert None to an empty string."""
    assert value2str(None, none_is_empty=True) == ''
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        pytest.param(True, True, id='bool-true'),
        pytest.param(False, False, id='bool-false'),
        pytest.param(1, True, id='int-one'),
        pytest.param(0, False, id='int-zero'),
        pytest.param('true', True, id='true'),
        pytest.param(' FALSE ', False, id='false'),
        pytest.param('Yes', True, id='yes'),
        pytest.param('no', False, id='no'),
        pytest.param('On', True, id='on'),
        pytest.param('0', False, id='zero'),
    ],)
def test_value2bool_converts_supported_values(
        value: str | bool | int, expected: bool,
        capsys: CaptureFixture[str]) -> None:
    """Test that value2bool converts accepted spellings to booleans."""
    assert value2bool(value) is expected
    check_capsys(capsys)


def test_value2bool_converts_none_to_false(
        capsys: CaptureFixture[str]) -> None:
    """Test that value2bool can convert None to False."""
    assert value2bool(None, none_is_false=True) is False
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('value', 'expected_exception'),
    [
        pytest.param(None, UnreasonableValueConversion, id='none'),
        pytest.param('', UnreasonableValueConversion, id='empty-string'),
        pytest.param('maybe', UnreasonableValueConversion, id='bad-string'),
        pytest.param(2, UnreasonableValueConversion, id='int-two'),
        pytest.param(-1, UnreasonableValueConversion, id='int-negative'),
        pytest.param(1.0, UnreasonableTypeConversion, id='float'),
        pytest.param(datetime(2026, 3, 25, 7, 8, 9),
                     UnreasonableTypeConversion, id='datetime'),
    ],)
def test_value2bool_rejects_unreasonable_values(
        value: str | int | float | datetime | None,
        expected_exception: type[Exception],
        capsys: CaptureFixture[str]) -> None:
    """Test that value2bool rejects invalid values and types."""
    with pytest.raises(expected_exception):
        value2bool(value)
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        pytest.param(7, 7, id='int'),
        pytest.param(7.0, 7, id='whole-float'),
        pytest.param('7', 7, id='string'),
        pytest.param(' 7', 7, id='string-with-space'),
        pytest.param('-3', -3, id='negative-string'),
    ],)
def test_value2int_converts_supported_values(
        value: int | float | str, expected: int,
        capsys: CaptureFixture[str]) -> None:
    """Test that value2int converts accepted values to integers."""
    assert value2int(value) == expected
    check_capsys(capsys)


def test_value2int_validates_format_string(
        capsys: CaptureFixture[str]) -> None:
    """Test that value2int can require a specific string format."""
    assert value2int('0007', format_string='04d') == 7
    with pytest.raises(UnreasonableValueConversion):
        value2int('7', format_string='04d')
    check_capsys(capsys)


def test_value2int_none_to_zero(capsys: CaptureFixture[str]) -> None:
    """Test that value2int can convert None to zero."""
    assert value2int(None, none_is_zero=True) == 0
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('value', 'expected_exception'),
    [
        pytest.param(None, UnreasonableValueConversion, id='none'),
        pytest.param(True, UnreasonableTypeConversion, id='bool'),
        pytest.param(3.5, UnreasonableValueConversion, id='fractional-float'),
        pytest.param('', UnreasonableValueConversion, id='empty-string'),
        pytest.param('3.5', UnreasonableValueConversion, id='float-string'),
        pytest.param(datetime(2026, 3, 25, 7, 8, 9),
                     UnreasonableTypeConversion, id='datetime'),
    ],)
def test_value2int_rejects_unreasonable_values(
        value: bool | float | str | datetime | None,
        expected_exception: type[Exception],
        capsys: CaptureFixture[str]) -> None:
    """Test that value2int rejects invalid values and types."""
    with pytest.raises(expected_exception):
        value2int(value)
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        pytest.param(2.5, 2.5, id='float'),
        pytest.param(2, 2.0, id='int'),
        pytest.param('2', 2.0, id='int-string'),
        pytest.param('2.5', 2.5, id='float-string'),
    ],)
def test_value2float_converts_supported_values(
        value: int | float | str, expected: float,
        capsys: CaptureFixture[str]) -> None:
    """Test that value2float converts accepted values to floats."""
    assert value2float(value) == expected
    check_capsys(capsys)


def test_value2float_converts_none_to_zero(
        capsys: CaptureFixture[str]) -> None:
    """Test that value2float can convert None to zero."""
    assert value2float(None, none_is_zero=True) == 0.0
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('value', 'expected_exception'),
    [
        pytest.param(None, UnreasonableValueConversion, id='none'),
        pytest.param(True, UnreasonableTypeConversion, id='bool'),
        pytest.param('', UnreasonableValueConversion, id='empty-string'),
        pytest.param('x', UnreasonableValueConversion, id='bad-string'),
        pytest.param(datetime(2026, 3, 25, 7, 8, 9),
                     UnreasonableTypeConversion, id='datetime'),
    ],)
def test_value2float_rejects_unreasonable_values(
        value: bool | str | datetime | None,
        expected_exception: type[Exception],
        capsys: CaptureFixture[str]) -> None:
    """Test that value2float rejects invalid values and types."""
    with pytest.raises(expected_exception):
        value2float(value)
    check_capsys(capsys)


def test_value2datetime_preserves_datetime_identity(
        capsys: CaptureFixture[str]) -> None:
    """Test that value2datetime returns a datetime unchanged."""
    value = datetime(2026, 3, 25, 7, 8, 9)
    assert value2datetime(value) is value
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('value', 'format_string', 'expected'),
    [
        pytest.param('2026-03-25T07:08:09', None,
                     datetime(2026, 3, 25, 7, 8, 9), id='iso-datetime'),
        pytest.param('2026-03-25', None, datetime(2026, 3, 25, 0, 0, 0),
                     id='iso-date'),
        pytest.param('25/03/2026 07:08', '%d/%m/%Y %H:%M',
                     datetime(2026, 3, 25, 7, 8, 0), id='custom-format'),
    ],)
def test_value2datetime_parses_strings(
        value: str, format_string: str | None, expected: datetime,
        capsys: CaptureFixture[str]) -> None:
    """Test that value2datetime parses supported string formats."""
    assert value2datetime(value, format_string=format_string) == expected
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('value', 'expected_exception'),
    [
        pytest.param(None, UnreasonableValueConversion, id='none'),
        pytest.param(True, UnreasonableTypeConversion, id='bool'),
        pytest.param(2, UnreasonableTypeConversion, id='int'),
        pytest.param('25/03/2026', UnreasonableValueConversion,
                     id='bad-string'),
    ],)
def test_value2datetime_rejects_unreasonable_values(
        value: bool | int | str | None, expected_exception: type[Exception],
        capsys: CaptureFixture[str]) -> None:
    """Test that value2datetime rejects invalid values and types."""
    with pytest.raises(expected_exception):
        value2datetime(value)
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('value', 'format_string', 'expected'),
    [
        pytest.param(datetime(2026, 3, 25, 7, 8, 9), None, date(2026, 3, 25),
                     id='datetime'),
        pytest.param('2026-03-25', None, date(2026, 3, 25), id='iso-date'),
        pytest.param('2026-03-25T07:08:09', None, date(2026, 3, 25),
                     id='iso-datetime'),
        pytest.param('25/03/2026', '%d/%m/%Y', date(2026, 3, 25),
                     id='custom-format'),
    ],)
def test_value2date_converts_supported_values(
        value: datetime | str, format_string: str | None, expected: date,
        capsys: CaptureFixture[str]) -> None:
    """Test that value2date converts supported values to dates."""
    assert value2date(value, format_string=format_string) == expected
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('value', 'expected_exception'),
    [
        pytest.param(None, UnreasonableValueConversion, id='none'),
        pytest.param(True, UnreasonableTypeConversion, id='bool'),
        pytest.param(2, UnreasonableTypeConversion, id='int'),
        pytest.param('07:08:09', UnreasonableValueConversion,
                     id='time-string'),
    ],)
def test_value2date_rejects_unreasonable_values(
        value: bool | int | str | None, expected_exception: type[Exception],
        capsys: CaptureFixture[str]) -> None:
    """Test that value2date rejects invalid values and types."""
    with pytest.raises(expected_exception):
        value2date(value)
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('value', 'format_string', 'expected'),
    [
        pytest.param(datetime(2026, 3, 25, 7, 8, 9), None, time(7, 8, 9),
                     id='datetime'),
        pytest.param('07:08:09', None, time(7, 8, 9), id='iso-time'),
        pytest.param('2026-03-25T07:08:09', None, time(7, 8, 9),
                     id='iso-datetime'),
        pytest.param('07.08.09', '%H.%M.%S', time(7, 8, 9),
                     id='custom-format'),
    ],)
def test_value2time_converts_supported_values(
        value: datetime | str, format_string: str | None, expected: time,
        capsys: CaptureFixture[str]) -> None:
    """Test that value2time converts supported values to times."""
    assert value2time(value, format_string=format_string) == expected
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('value', 'expected_exception'),
    [
        pytest.param(None, UnreasonableValueConversion, id='none'),
        pytest.param(True, UnreasonableTypeConversion, id='bool'),
        pytest.param(2, UnreasonableTypeConversion, id='int'),
        pytest.param('2026-03-25', UnreasonableValueConversion,
                     id='date-string'),
        pytest.param('not-a-time', UnreasonableValueConversion,
                     id='bad-string'),
    ],)
def test_value2time_rejects_unreasonable_values(
        value: bool | int | str | None, expected_exception: type[Exception],
        capsys: CaptureFixture[str]) -> None:
    """Test that value2time rejects invalid values and types."""
    with pytest.raises(expected_exception):
        value2time(value)
    check_capsys(capsys)


@pytest.mark.parametrize(
    'value',
    [
        pytest.param(None, id='none'),
        pytest.param(False, id='bool-false'),
        pytest.param(0, id='int-zero'),
        pytest.param('', id='empty-string'),
    ],)
def test_value2none_converts_supported_values(
        value: None | bool | int | str, capsys: CaptureFixture[str]) -> None:
    """Test that value2none converts supported falsey values to None."""
    value2none(value)
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('value', 'expected_exception'),
    [
        pytest.param(True, UnreasonableValueConversion, id='bool-true'),
        pytest.param(1, UnreasonableValueConversion, id='int-one'),
        pytest.param('text', UnreasonableValueConversion, id='string'),
        pytest.param(0.0, UnreasonableTypeConversion, id='float'),
        pytest.param(datetime(2026, 3, 25, 7, 8, 9),
                     UnreasonableTypeConversion, id='datetime'),
    ],)
def test_value2none_rejects_unreasonable_values(
        value: bool | int | float | str | datetime,
        expected_exception: type[Exception],
        capsys: CaptureFixture[str]) -> None:
    """Test that value2none rejects non-empty values and bad types."""
    with pytest.raises(expected_exception):
        value2none(value)
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('value', 'to_type', 'expected'),
    [
        pytest.param('text', str, 'text', id='str'),
        pytest.param('yes', bool, True, id='bool'),
        pytest.param('7', int, 7, id='int'),
        pytest.param('2.5', float, 2.5, id='float'),
        pytest.param('2026-03-25T07:08:09', datetime,
                     datetime(2026, 3, 25, 7, 8, 9), id='datetime'),
        pytest.param('', NoneType, None, id='none'),
    ],)
def test_value2type_converts_supported_values(
        value: str, to_type: type[object],
        expected: str | bool | int | float | datetime | None,
        capsys: CaptureFixture[str]) -> None:
    """Test that value2type dispatches to the right converter."""
    assert value2type(value, to_type) == expected
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('value', 'to_type', 'expected'),
    [
        pytest.param(None, str, '', id='none-to-str'),
        pytest.param(None, bool, False, id='none-to-bool'),
        pytest.param(None, int, 0, id='none-to-int'),
        pytest.param(None, float, 0.0, id='none-to-float'),
    ],)
def test_value2type_accept_none_passthrough(
        value: None, to_type: type[object], expected: str | bool | int | float,
        capsys: CaptureFixture[str]) -> None:
    """Test that value2type forwards accept_none to converters."""
    assert value2type(value, to_type, accept_none=True) == expected
    check_capsys(capsys)


def test_value2type_passes_datetime_format_string(
        capsys: CaptureFixture[str]) -> None:
    """Test that value2type forwards datetime format strings."""
    value = '25/03/2026 07:08'
    expected = datetime(2026, 3, 25, 7, 8, 0)
    assert value2type(value, datetime,
                      datetime_format_string='%d/%m/%Y %H:%M') == expected
    check_capsys(capsys)


def test_value2type_passes_int_format_string(
        capsys: CaptureFixture[str]) -> None:
    """Test that value2type forwards integer format validation."""
    assert value2type('0007', int, int_format_string='04d') == 7
    with pytest.raises(UnreasonableValueConversion):
        value2type('7', int, int_format_string='04d')
    check_capsys(capsys)


@pytest.mark.parametrize(
    'to_type',
    [
        pytest.param(date, id='date'),
        pytest.param(time, id='time'),
    ],)
def test_value2type_rejects_unsupported_target_types(
        to_type: type[object], capsys: CaptureFixture[str]) -> None:
    """Test that value2type rejects unsupported target types."""
    with pytest.raises(UnreasonableTypeConversion):
        value2type('2026-03-25', to_type)
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('value', 'to_type_of', 'expected'),
    [
        pytest.param('text', 'other', 'text', id='str'),
        pytest.param('on', False, True, id='bool'),
        pytest.param('7', 99, 7, id='int'),
        pytest.param('2.5', 1.25, 2.5, id='float'),
        pytest.param('2026-03-25T07:08:09', datetime(2030, 1, 1, 0, 0, 0),
                     datetime(2026, 3, 25, 7, 8, 9), id='datetime'),
        pytest.param('', None, None, id='none'),
    ],)
def test_value2type_of_converts_supported_values(
        value: str, to_type_of: str | bool | int | float | datetime | None,
        expected: str | bool | int | float | datetime | None,
        capsys: CaptureFixture[str]) -> None:
    """Test that value2type_of uses the example value's type."""
    assert value2type_of(value, to_type_of) == expected
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('value', 'to_type_of', 'expected'),
    [
        pytest.param(None, '', '', id='none-to-str'),
        pytest.param(None, False, False, id='none-to-bool'),
        pytest.param(None, 0, 0, id='none-to-int'),
        pytest.param(None, 0.0, 0.0, id='none-to-float'),
    ],)
def test_value2type_of_accept_none_passthrough(
        value: None, to_type_of: str | bool | int | float,
        expected: str | bool | int | float,
        capsys: CaptureFixture[str]) -> None:
    """Test that value2type_of forwards accept_none to converters."""
    assert value2type_of(value, to_type_of, accept_none=True) == expected
    check_capsys(capsys)


def test_value2type_of_passes_datetime_format_string(
        capsys: CaptureFixture[str]) -> None:
    """Test that value2type_of forwards datetime format strings."""
    value = '25/03/2026 07:08'
    expected = datetime(2026, 3, 25, 7, 8, 0)
    assert value2type_of(value, expected,
                         datetime_format_string='%d/%m/%Y %H:%M') == expected
    check_capsys(capsys)


def test_value2type_of_passes_int_format_string(
        capsys: CaptureFixture[str]) -> None:
    """Test that value2type_of forwards integer format validation."""
    assert value2type_of('0007', 0, int_format_string='04d') == 7
    with pytest.raises(UnreasonableValueConversion):
        value2type_of('7', 0, int_format_string='04d')
    check_capsys(capsys)


@pytest.mark.parametrize(
    'to_type_of',
    [
        pytest.param(date(2026, 3, 25), id='date'),
        pytest.param(time(7, 8, 9), id='time'),
    ],)
def test_value2type_of_rejects_unsupported_target_types(
        to_type_of: date | time, capsys: CaptureFixture[str]) -> None:
    """Test that value2type_of rejects unsupported target types."""
    with pytest.raises(UnreasonableTypeConversion):
        value2type_of('2026-03-25', to_type_of)
    check_capsys(capsys)
