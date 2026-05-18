#! /usr/local/bin/python3
"""Tests for factory implementation selection helpers."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import cast

import pytest
import tableio.factory as factory_module
from tableio.capability import Capabilities, SingleCapability, Strictness
from tableio.factory import TableIOFactory, TableIOFactoryNoCapabilityMatch, \
    filter_args_tableio, list_implementations_tableio
from tableio.optional_args import OptionalArgsDict
from tableio.tableio import Descriptor
from .test_factory import _SUP, _StubBase, StubAlphaHigh, StubAlphaLow, \
    StubBeta


class _AlphaFmtStrict(_StubBase):
    """Alpha format, low priority, but strict row-format support."""

    _desc = Descriptor(
        format_name='Alpha', implementation='fmt_strict',
        capabilities=Capabilities(can_write=_SUP, can_read=_SUP,
                                  can_fmt_row=_SUP),
        mandatory_args=[], optional_args=['opt_c'], priority=1)


def _shared_descriptor(format_name: str, implementation: str,
                       priority: int) -> Descriptor:
    """Return a descriptor for one shared-name test implementation."""
    return Descriptor(format_name=format_name, implementation=implementation,
                      capabilities=Capabilities(can_write=_SUP),
                      mandatory_args=[], optional_args=[], priority=priority)


class _SharedHigh(_StubBase):
    """High-priority implementation name shared with another format."""

    _desc = _shared_descriptor('SharedHigh', 'shared', 30)


class _SharedLow(_StubBase):
    """Low-priority implementation name shared with another format."""

    _desc = _shared_descriptor('SharedLow', 'shared', 5)


class _OtherSharedGroup(_StubBase):
    """Mid-priority implementation in the shared-name test group."""

    _desc = _shared_descriptor('SharedOther', 'other', 20)


def _make_empty_factory() -> TableIOFactory:
    """Create a factory with no package formats registered."""
    factory = TableIOFactory()
    factory._formats = {}  # pylint: disable=protected-access
    factory._lower2correct = {}  # pylint: disable=protected-access
    return factory


def _make_selection_factory() -> TableIOFactory:
    """Create a factory with only the selection test stubs."""
    factory = _make_empty_factory()
    factory.i_register(StubAlphaHigh)
    factory.i_register(StubAlphaLow)
    factory.i_register(StubBeta)
    return factory


def test_filter_args_none_implementation_uses_best_priority() -> None:
    """None implementation filters for the highest-priority backend."""
    factory = _make_selection_factory()
    args = cast(OptionalArgsDict, {
        'opt_a': 'a',
        'opt_b': 'b',
        'file_exists_callback': None
    })
    result = factory.i_filter_args(args, 'Alpha', None)
    assert result == {
        'opt_a': 'a',
        'file_exists_callback': None
    }


def test_filter_args_none_implementation_prefers_strict_match() -> None:
    """Strict matches are selected before tolerant higher priority ones."""
    factory = _make_selection_factory()
    factory.i_register(_AlphaFmtStrict)
    args = cast(OptionalArgsDict, {
        'opt_a': 'a',
        'opt_b': 'b',
        'opt_c': 'c'
    })
    caps = Capabilities(can_fmt_row=_SUP)
    result = factory.i_filter_args(args, 'alpha', None, capabilities=caps)
    assert result == {'opt_c': 'c'}


def test_filter_args_explicit_implementation_validates_caps() -> None:
    """Explicit implementation filtering validates capabilities."""
    factory = _make_selection_factory()
    args = cast(OptionalArgsDict, {'opt_b': 'b'})
    caps = Capabilities(can_read=SingleCapability(True, Strictness.STRICT))
    with pytest.raises(TableIOFactoryNoCapabilityMatch):
        factory.i_filter_args(args, 'Alpha', 'low', capabilities=caps)


def test_filter_args_none_implementation_no_match_raises() -> None:
    """None implementation still raises if no backend can match."""
    factory = _make_selection_factory()
    args = cast(OptionalArgsDict, {'opt_a': 'a'})
    caps = Capabilities(
        can_write_box=SingleCapability(True, Strictness.STRICT))
    with pytest.raises(TableIOFactoryNoCapabilityMatch):
        factory.i_filter_args(args, 'Alpha', None, capabilities=caps)


def test_implementation_listing_not_alphabetical_orders_by_priority() -> None:
    """alphabetical=False returns factory selection order."""
    factory = _make_selection_factory()
    names = factory.i_get_reg_impls(alphabetical=False)
    assert names == ['high', 'beta_impl', 'low']


def test_implementation_listing_keeps_strict_before_nonstrict() -> None:
    """Strict capability matches are listed before tolerant matches."""
    factory = _make_selection_factory()
    caps = Capabilities(can_fmt_row=_SUP)
    names = factory.i_get_reg_impls(capabilities=caps, alphabetical=False)
    assert names == ['beta_impl', 'high', 'low']


def test_implementation_listing_deduplicates_by_first_match() -> None:
    """Duplicate implementation names keep the first best match."""
    factory = _make_empty_factory()
    factory.i_register(_SharedLow)
    factory.i_register(_OtherSharedGroup)
    factory.i_register(_SharedHigh)
    names = factory.i_get_reg_impls(alphabetical=False)
    assert names == ['shared', 'other']


def test_implementation_listing_format_name_is_case_insensitive() -> None:
    """Implementation listing accepts case-insensitive format names."""
    factory = _make_selection_factory()
    names = factory.i_get_reg_impls(format_name='alpha')
    assert names == ['high', 'low']


def test_list_implementations_tableio_not_alphabetical(
        monkeypatch: pytest.MonkeyPatch) -> None:
    """list_implementations_tableio forwards alphabetical=False."""
    monkeypatch.setattr(factory_module, '_the_factory',
                        _make_selection_factory())
    names = list_implementations_tableio(alphabetical=False)
    assert names == ['high', 'beta_impl', 'low']


def test_filter_args_tableio_none_implementation() -> None:
    """filter_args_tableio can select the implementation to filter."""
    args: OptionalArgsDict = {'csv_delimiter': ';'}
    caps = Capabilities(can_write=_SUP)
    result = filter_args_tableio(args, 'CSV', None, capabilities=caps)
    assert result is not None
    assert 'csv_delimiter' in result
