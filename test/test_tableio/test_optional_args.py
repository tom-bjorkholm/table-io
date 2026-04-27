#! /usr/local/bin/python3
"""Tests for the optional_args module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pytest import CaptureFixture

from tableio.optional_args import CsvDialect, OptionalArgsDict, \
    mformat_optargs_from_optionalargs

from .check_capsys import check_capsys


def allow_existing_file(file_name: str) -> None:
    """Accept an existing file in optional-argument tests."""
    _ = file_name


def test_mformat_optargs_from_optionalargs_returns_none(
        capsys: CaptureFixture[str]) -> None:
    """Test conversion of missing optional arguments."""
    assert mformat_optargs_from_optionalargs(None) is None
    check_capsys(capsys)


def test_mformat_optargs_from_optionalargs_filters_tableio_args_and_none(
        capsys: CaptureFixture[str]) -> None:
    """Test filtering to mformat keys with non-None values."""
    optional_args: OptionalArgsDict = {
        'file_exists_callback': allow_existing_file,
        'title': 'Report',
        'line_length': 72,
        'css_file': None,
        'csv_dialect': CsvDialect.EXCEL,
        'csv_delimiter': ';',
        'csv_quotechar': None
    }
    result = mformat_optargs_from_optionalargs(optional_args)
    assert result is not None
    assert result == {
        'file_exists_callback': allow_existing_file,
        'title': 'Report',
        'line_length': 72
    }
    assert result['file_exists_callback'] is allow_existing_file
    check_capsys(capsys)


def test_mformat_optargs_from_optionalargs_returns_empty_dict(
        capsys: CaptureFixture[str]) -> None:
    """Test conversion when no mformat values remain after filtering."""
    optional_args: OptionalArgsDict = {
        'title': None,
        'csv_dialect': CsvDialect.UNIX,
        'csv_delimiter': ';',
        'csv_escapechar': None
    }
    result = mformat_optargs_from_optionalargs(optional_args)
    assert result == {}
    check_capsys(capsys)
