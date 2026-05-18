#! /usr/local/bin/python3
"""Tests for FactoryFormatInfo."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest

from tableio.factory import FactoryFormatInfo
from tableio.factory import TableIOFactoryConflictError, \
    TableIOFactoryNoSuchError, TableIOFactoryNoCapabilityMatch
from tableio.tableio import TableIO
from tableio.capability import Capabilities, SingleCapability, Strictness
from tableio.tableio_types import Descriptor
from .check_capsys import check_capsys
from .test_factory import StubAlphaHigh, StubAlphaLow, _SUP, \
    _make_format_info_alpha

# -- FactoryFormatInfo ---------------------------------------------------


class TestFactoryFormatInfo:
    """Tests for FactoryFormatInfo."""

    def test_init_none(self) -> None:
        """Init with None creates empty registry."""
        info = FactoryFormatInfo()
        bm = info.best_match_names(empty_is_ok=True)
        assert len(bm) == 0

    def test_init_with_class(self) -> None:
        """Init with a format class registers it."""
        info = FactoryFormatInfo(format_class=StubAlphaHigh)
        bm = info.best_match_names()
        assert len(bm) == 1
        assert bm.strict_matches[0].implementation == 'high'

    def test_add_implementation(self) -> None:
        """Adding a second implementation succeeds."""
        info = FactoryFormatInfo(format_class=StubAlphaHigh)
        info.add_implementation(StubAlphaLow)
        bm = info.best_match_names()
        assert len(bm) == 2

    def test_add_duplicate_raises(self) -> None:
        """Adding the same implementation twice raises."""
        info = FactoryFormatInfo(format_class=StubAlphaHigh)
        with pytest.raises(TableIOFactoryConflictError,
                           match='already registered'):
            info.add_implementation(StubAlphaHigh)

    def test_add_case_conflict_raises(self) -> None:
        """Implementation with case-only name difference raises."""
        class StubConflict(StubAlphaHigh):
            """Stub with case-conflicting implementation name."""

            _desc = Descriptor(format_name='Alpha', implementation='High',
                               capabilities=Capabilities(can_write=_SUP),
                               mandatory_args=[], optional_args=[])
        info = FactoryFormatInfo(format_class=StubAlphaHigh)
        with pytest.raises(TableIOFactoryConflictError):
            info.add_implementation(StubConflict)

    def test_best_match_no_capabilities(self) -> None:
        """Without capabilities all implementations are strict."""
        info = _make_format_info_alpha()
        bm = info.best_match_names()
        assert len(bm.strict_matches) == 2
        assert len(bm.nonstrict_matches) == 0

    def test_best_match_strict_and_nonstrict(self) -> None:
        """Capabilities separate strict from nonstrict matches."""
        info = _make_format_info_alpha()
        caps = Capabilities(
            can_write=SingleCapability(True, Strictness.STRICT),
            can_read=SingleCapability(True, Strictness.STRICT))
        bm = info.best_match_names(capabilities=caps, empty_is_ok=True)
        strict = [m.implementation
                  for m in bm.strict_matches]
        assert 'high' in strict
        assert 'low' not in strict

    def test_best_match_nonstrict_only(self) -> None:
        """Request that only matches nonstrictly."""
        info = _make_format_info_alpha()
        caps = Capabilities(
            can_write=SingleCapability(True, Strictness.STRICT),
            can_fmt_row=SingleCapability(True, Strictness.IGNORE))
        bm = info.best_match_names(capabilities=caps, empty_is_ok=True)
        assert len(bm.strict_matches) == 0
        assert len(bm.nonstrict_matches) == 2

    def test_best_match_no_match_raises(self) -> None:
        """No match with empty_is_ok=False raises."""
        info = FactoryFormatInfo(format_class=StubAlphaHigh)
        caps = Capabilities(
            can_fmt_row=SingleCapability(True, Strictness.STRICT))
        with pytest.raises(TableIOFactoryNoCapabilityMatch):
            info.best_match_names(capabilities=caps)

    def test_best_match_no_match_empty_ok(self) -> None:
        """No match with empty_is_ok=True returns empty."""
        info = FactoryFormatInfo(format_class=StubAlphaHigh)
        caps = Capabilities(
            can_fmt_row=SingleCapability(True, Strictness.STRICT))
        bm = info.best_match_names(capabilities=caps, empty_is_ok=True)
        assert len(bm) == 0


# ---- Test FactoryFormatInfo case insensitivity -----------------------------


class FormatInfoMock(TableIO):
    """Mock TableIO for FactoryFormatInfo testing."""

    _desc = Descriptor(format_name='Mock', implementation='mock',
                       capabilities=Capabilities(), mandatory_args=[],
                       optional_args=[])

    @classmethod
    def get_description(cls) -> Descriptor:
        """Get the description of the reader/writer class."""
        return cls._desc

    @classmethod
    def get_capabilities(cls) -> Capabilities:
        """Get the capabilities of the reader/writer class."""
        return cls._desc.capabilities

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the extension of the file name."""
        return '.ext'


@pytest.mark.parametrize('implnames,lookupname,correctname',
                         [(['Abc', 'deF'], 'ABC', 'Abc'),
                          (['OpenPyXL', 'pylightxl',
                            'XlsxWriter'], 'openpyxl', 'OpenPyXL'),
                          (['OpenPyXL', 'pylightxl',
                            'XlsxWriter'], 'xLSXwRITER', 'XlsxWriter')])
def test_factory_fi_correct_impl_name(capsys: pytest.CaptureFixture[str],
                                      implnames: list[str], lookupname: str,
                                      correctname: str) -> None:
    """Test FactoryFormatInfo.correct_implementation_name."""
    f = FactoryFormatInfo()
    for implname in implnames:
        # pylint: disable=protected-access
        FormatInfoMock._desc = \
            FormatInfoMock._desc._replace(implementation=implname)
        f.add_implementation(FormatInfoMock)
    assert f.correct_implementation_name(lookupname) == correctname
    check_capsys(capsys)


@pytest.mark.parametrize('implnames,lookupname',
                         [(['Abc', 'deF'], 'Abcc'),
                          (['OpenPyXL', 'pylightxl',
                            'XlsxWriter'], 'openpyxx'),
                          (['OpenPyXL', 'pylightxl',
                            'XlsxWriter'], 'nonexistent')])
def test_factory_fi_correct_impl_nok(capsys: pytest.CaptureFixture[str],
                                     implnames: list[str],
                                     lookupname: str) -> None:
    """Test not OK usage of FactoryFormatInfo.correct_implementation_name."""
    f = FactoryFormatInfo()
    for implname in implnames:
        # pylint: disable=protected-access
        FormatInfoMock._desc = \
            FormatInfoMock._desc._replace(implementation=implname)
        f.add_implementation(FormatInfoMock)
    with pytest.raises(TableIOFactoryNoSuchError) as exc:
        f.correct_implementation_name(lookupname)
    err1 = f'Implementation "{lookupname}" is not registered.'
    err2 = 'Available implementations:'
    assert err1 in str(exc.value)
    assert err2 in str(exc.value)
    for implname in implnames:
        assert implname in str(exc.value)
    check_capsys(capsys)
