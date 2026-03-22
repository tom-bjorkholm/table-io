#! /usr/bin/env python3
"""Tests for cmd_for_examples module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
from typing import Any
from unittest.mock import patch, MagicMock
import pytest
from mformat.paper_size import PaperSize
from tableio.optional_args import CsvDialect
from example.cmd_for_examples import (
    cmd_parse_and_run_example, _build_optional_args,
    _unpack_and_run_example)

_PATCH_REG = 'example.cmd_for_examples.list_registered_tableio'
_PATCH_IMPL = (
    'example.cmd_for_examples.list_implementations_tableio')


class TestBuildOptionalArgs:
    """Tests for _build_optional_args."""

    # pylint: disable=unsubscriptable-object

    def test_no_optional_args_returns_none(self) -> None:
        """Empty namespace produces None."""
        ns = argparse.Namespace()
        assert _build_optional_args(ns) is None

    def test_string_arg(self) -> None:
        """A single string argument is unpacked correctly."""
        ns = argparse.Namespace(lang=['en'])
        result = _build_optional_args(ns)
        assert isinstance(result, dict)
        assert result['lang'] == 'en'

    def test_int_arg(self) -> None:
        """A single int argument is unpacked correctly."""
        ns = argparse.Namespace(line_length=[80])
        result = _build_optional_args(ns)
        assert isinstance(result, dict)
        assert result['line_length'] == 80

    @pytest.mark.parametrize('input_str,expected', [
        ('EXCEL', CsvDialect.EXCEL),
        ('excel', CsvDialect.EXCEL),
        ('Excel', CsvDialect.EXCEL),
        ('UNIX', CsvDialect.UNIX)])
    def test_enum_csv_type(self, input_str: str,
                           expected: CsvDialect) -> None:
        """Enum values for CsvDialect are parsed from strings."""
        ns = argparse.Namespace(csv_type=[input_str])
        result = _build_optional_args(ns)
        assert isinstance(result, dict)
        assert result['csv_type'] == expected

    def test_enum_paper_size(self) -> None:
        """Enum value for PaperSize is parsed from string."""
        ns = argparse.Namespace(paper_size=['A4'])
        result = _build_optional_args(ns)
        assert isinstance(result, dict)
        assert result['paper_size'] == PaperSize.A4

    def test_multiple_args(self) -> None:
        """Multiple arguments of mixed types are all included."""
        ns = argparse.Namespace(
            lang=['en'], line_length=[80],
            csv_type=['EXCEL'])
        result = _build_optional_args(ns)
        assert isinstance(result, dict)
        assert result['lang'] == 'en'
        assert result['line_length'] == 80
        assert result['csv_type'] == CsvDialect.EXCEL


class TestUnpackAndRunExample:
    """Tests for _unpack_and_run_example."""

    @patch(_PATCH_IMPL)
    @patch(_PATCH_REG)
    def test_single_format_no_impl(
            self, _mock_reg: MagicMock,
            _mock_impl: MagicMock) -> None:
        """Single format, no implementation specified."""
        func: Any = MagicMock(return_value=0)
        ns = argparse.Namespace(
            format=['CSV'], output=['out'],
            implementation=None)
        ret = _unpack_and_run_example(
            'test', func, None, ns)
        assert ret == 0
        func.assert_called_once_with(
            'CSV', 'out', None, None)

    @patch(_PATCH_IMPL)
    @patch(_PATCH_REG)
    def test_single_format_specific_impl(
            self, _mock_reg: MagicMock,
            _mock_impl: MagicMock) -> None:
        """Single format with a specific implementation."""
        func: Any = MagicMock(return_value=0)
        ns = argparse.Namespace(
            format=['CSV'], output=['out'],
            implementation=['PyCsv'])
        ret = _unpack_and_run_example(
            'test', func, None, ns)
        assert ret == 0
        func.assert_called_once_with(
            'CSV', 'out', 'PyCsv', None)

    @patch(_PATCH_IMPL)
    @patch(_PATCH_REG)
    def test_all_formats(self, mock_reg: MagicMock,
                         _mock_impl: MagicMock) -> None:
        """Format 'all' iterates over all registered formats."""
        mock_reg.return_value = ['CSV', 'HTML']
        func: Any = MagicMock(return_value=0)
        ns = argparse.Namespace(
            format=['all'], output=['out'],
            implementation=None)
        ret = _unpack_and_run_example(
            'test', func, None, ns)
        assert ret == 0
        assert func.call_count == 2
        func.assert_any_call('CSV', 'out_CSV', None, None)
        func.assert_any_call(
            'HTML', 'out_HTML', None, None)

    @patch(_PATCH_IMPL)
    @patch(_PATCH_REG)
    def test_all_implementations(
            self, _mock_reg: MagicMock,
            mock_impl: MagicMock) -> None:
        """Implementation 'all' iterates per-format."""
        mock_impl.return_value = ['PyCsv', 'AltCsv']
        func: Any = MagicMock(return_value=0)
        ns = argparse.Namespace(
            format=['CSV'], output=['out'],
            implementation=['all'])
        ret = _unpack_and_run_example(
            'test', func, None, ns)
        assert ret == 0
        assert func.call_count == 2
        func.assert_any_call(
            'CSV', 'out_PyCsv', 'PyCsv', None)
        func.assert_any_call(
            'CSV', 'out_AltCsv', 'AltCsv', None)

    @patch(_PATCH_IMPL)
    @patch(_PATCH_REG)
    def test_all_formats_all_impls(
            self, mock_reg: MagicMock,
            mock_impl: MagicMock) -> None:
        """Both format and impl 'all': sparse matrix."""
        mock_reg.return_value = ['CSV', 'HTML']

        def impl_side_effect(
                format_name: str | None = None,
                **_kwargs: object) -> list[str]:
            """Return per-format implementations."""
            impls = {'CSV': ['PyCsv'],
                     'HTML': ['MfHtml', 'Alt']}
            return impls.get(format_name or '', [])
        mock_impl.side_effect = impl_side_effect
        func: Any = MagicMock(return_value=0)
        ns = argparse.Namespace(
            format=['all'], output=['out'],
            implementation=['all'])
        ret = _unpack_and_run_example(
            'test', func, None, ns)
        assert ret == 0
        assert func.call_count == 3
        func.assert_any_call(
            'CSV', 'out_CSV_PyCsv', 'PyCsv', None)
        func.assert_any_call(
            'HTML', 'out_HTML_MfHtml', 'MfHtml', None)
        func.assert_any_call(
            'HTML', 'out_HTML_Alt', 'Alt', None)

    @patch(_PATCH_IMPL)
    @patch(_PATCH_REG)
    def test_all_impls_empty_skips(
            self, _mock_reg: MagicMock,
            mock_impl: MagicMock) -> None:
        """No implementations for a format: func not called."""
        mock_impl.return_value = []
        func: Any = MagicMock(return_value=0)
        ns = argparse.Namespace(
            format=['CSV'], output=['out'],
            implementation=['all'])
        ret = _unpack_and_run_example(
            'test', func, None, ns)
        assert ret == 0
        func.assert_not_called()

    @pytest.mark.parametrize('returns,expected', [
        ([0, 0], 0),
        ([1, 0], 1),
        ([0, 2], 2),
        ([3, 5], 3)])
    @patch(_PATCH_IMPL)
    @patch(_PATCH_REG)
    def test_error_propagation(
            self, mock_reg: MagicMock,
            _mock_impl: MagicMock,
            returns: list[int],
            expected: int) -> None:
        """First non-zero return code is propagated."""
        mock_reg.return_value = ['CSV', 'HTML']
        func: Any = MagicMock(side_effect=returns)
        ns = argparse.Namespace(
            format=['all'], output=['out'],
            implementation=None)
        ret = _unpack_and_run_example(
            'test', func, None, ns)
        assert ret == expected


class TestCmdParseAndRunExample:
    """Tests for cmd_parse_and_run_example."""

    @patch(_PATCH_IMPL)
    @patch(_PATCH_REG)
    def test_exit_code_zero(self, mock_reg: MagicMock,
                            mock_impl: MagicMock
                            ) -> None:
        """Successful run produces exit code 0."""
        mock_reg.side_effect = lambda **kw: ['CSV']
        mock_impl.side_effect = lambda **kw: []
        func: Any = MagicMock(return_value=0)
        with pytest.raises(SystemExit) as exc_info:
            cmd_parse_and_run_example(
                'test', func,
                args=['-f', 'CSV', '-o', 'out'])
        assert exc_info.value.code == 0
        func.assert_called_once()

    @patch(_PATCH_IMPL)
    @patch(_PATCH_REG)
    def test_exit_code_nonzero(
            self, mock_reg: MagicMock,
            mock_impl: MagicMock) -> None:
        """Failed run produces non-zero exit code."""
        mock_reg.side_effect = lambda **kw: ['CSV']
        mock_impl.side_effect = lambda **kw: []
        func: Any = MagicMock(return_value=1)
        with pytest.raises(SystemExit) as exc_info:
            cmd_parse_and_run_example(
                'test', func,
                args=['-f', 'CSV', '-o', 'out'])
        assert exc_info.value.code == 1

    @patch(_PATCH_IMPL)
    @patch(_PATCH_REG)
    def test_optional_args_passed(
            self, mock_reg: MagicMock,
            mock_impl: MagicMock) -> None:
        """Optional arguments reach the example function."""
        mock_reg.side_effect = lambda **kw: ['CSV']
        mock_impl.side_effect = lambda **kw: []
        func: Any = MagicMock(return_value=0)
        with pytest.raises(SystemExit):
            cmd_parse_and_run_example(
                'test', func,
                args=['-f', 'CSV', '-o', 'out',
                      '--lang', 'en'])
        func.assert_called_once()
        _, _, _, opt_args = func.call_args[0]
        assert opt_args is not None
        assert opt_args['lang'] == 'en'
