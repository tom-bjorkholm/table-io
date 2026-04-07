#! /usr/local/bin/python3
"""Tests for the factory module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Callable, cast
import pytest
from tableio.capability import Capabilities, SingleCapability, Strictness
from tableio.tableio import TableIO, Descriptor, FileAccess
from tableio.factory import (
    ImplPrio, BestMatch, FactoryFormatInfo, TableIOFactory,
    TableIOFactoryConflictError, TableIOFactoryNoSuchError,
    TableIOFactoryNoCapabilityMatch, InsufficientCapabilities,
    create_tableio, filter_args_tableio, list_registered_tableio,
    list_implementations_tableio, usage_tableio, register_tableio)
from tableio.optional_args import OptionalArgsDict

_SUP = SingleCapability(supported=True)
_STRICT_NO = SingleCapability(supported=False,
                              strictness=Strictness.STRICT)
_IGNORE_NO = SingleCapability(supported=False,
                              strictness=Strictness.IGNORE)


# -- Test doubles --------------------------------------------------------

class _StubBase(TableIO):
    """Minimal TableIO stub for factory testing."""

    _desc = Descriptor(
        format_name='_base', implementation='_base',
        capabilities=Capabilities(),
        mandatory_args=[], optional_args=[])

    @classmethod
    def get_description(cls) -> Descriptor:
        """Return the stub descriptor."""
        return cls._desc

    @classmethod
    def get_capabilities(cls) -> Capabilities:
        """Return the stub capabilities."""
        return cls._desc.capabilities

    @classmethod
    def file_name_extension(cls) -> str:
        """Return file extension for stubs."""
        return 'stub'


class StubAlphaHigh(_StubBase):
    """Alpha format, high priority, read+write, tolerates fmt_row."""

    _desc = Descriptor(
        format_name='Alpha', implementation='high',
        capabilities=Capabilities(
            can_write=_SUP, can_read=_SUP,
            can_fmt_row=_IGNORE_NO),
        mandatory_args=[], optional_args=['opt_a'],
        priority=20)

    def __init__(self, file_name: str | Path,
                 file_access: FileAccess = FileAccess.CREATE,
                 file_exists_callback:
                 Callable[[str], None] | None = None,
                 opt_a: str | None = None):
        """Initialize with optional opt_a."""
        super().__init__(file_name, file_access,
                         file_exists_callback)
        self.opt_a = opt_a


class StubAlphaLow(_StubBase):
    """Alpha format, low priority, write-only, tolerates fmt_row."""

    _desc = Descriptor(
        format_name='Alpha', implementation='low',
        capabilities=Capabilities(
            can_write=_SUP, can_read=_STRICT_NO,
            can_fmt_row=_IGNORE_NO),
        mandatory_args=[], optional_args=['opt_b'],
        priority=5)

    def __init__(self, file_name: str | Path,
                 file_access: FileAccess = FileAccess.CREATE,
                 file_exists_callback:
                 Callable[[str], None] | None = None,
                 opt_b: str | None = None):
        """Initialize with optional opt_b."""
        super().__init__(file_name, file_access,
                         file_exists_callback)
        self.opt_b = opt_b


class StubBeta(_StubBase):
    """Beta format, mid priority, read+write, supports fmt_row."""

    _desc = Descriptor(
        format_name='Beta', implementation='beta_impl',
        capabilities=Capabilities(
            can_write=_SUP, can_read=_SUP,
            can_fmt_row=_SUP),
        mandatory_args=[], optional_args=[],
        priority=10)


class StubGammaMandatory(_StubBase):
    """Gamma format used to exercise mandatory and mixed-case args."""

    _desc = Descriptor(
        format_name='Gamma', implementation='CamelCase',
        capabilities=Capabilities(can_write=_SUP),
        mandatory_args=['required_arg'], optional_args=[])

    def __init__(self, file_name: str | Path,
                 file_access: FileAccess = FileAccess.CREATE,
                 required_arg: str = 'required',
                 file_exists_callback:
                 Callable[[str], None] | None = None):
        """Initialize with a descriptor-declared mandatory argument."""
        super().__init__(file_name, file_access, file_exists_callback)
        self.required_arg = required_arg


# -- Helpers -------------------------------------------------------------

def _make_format_info_alpha() -> FactoryFormatInfo:
    """Create a FactoryFormatInfo with two Alpha implementations."""
    info = FactoryFormatInfo(format_class=StubAlphaHigh)
    info.add_implementation(StubAlphaLow)
    return info


def _make_factory_stubs() -> TableIOFactory:
    """Create a fresh factory with test stubs plus package formats."""
    factory = TableIOFactory()
    factory.i_register(StubAlphaHigh)
    factory.i_register(StubAlphaLow)
    factory.i_register(StubBeta)
    return factory


# -- Error classes -------------------------------------------------------

class TestErrorClasses:
    """Tests for custom exception hierarchy."""

    def test_conflict_is_value_error(self) -> None:
        """Verify conflict error subclasses ValueError."""
        assert issubclass(TableIOFactoryConflictError, ValueError)

    def test_no_such_is_key_error(self) -> None:
        """Verify no-such error subclasses KeyError."""
        assert issubclass(TableIOFactoryNoSuchError, KeyError)

    def test_no_capability_is_value_error(self) -> None:
        """Verify capability-match error subclasses ValueError."""
        assert issubclass(
            TableIOFactoryNoCapabilityMatch, ValueError)

    def test_insufficient_capabilities_is_value_error(self) -> None:
        """Verify insufficient-capabilities error subclasses ValueError."""
        assert issubclass(InsufficientCapabilities, ValueError)


# -- ImplPrio ------------------------------------------------------------

class TestImplPrio:
    """Tests for ImplPrio comparison and ordering."""

    @pytest.mark.parametrize('left, right, expected', [
        (ImplPrio('A', 'x', 10), ImplPrio('A', 'x', 20), True),
        (ImplPrio('A', 'x', 20), ImplPrio('A', 'x', 10), False),
        (ImplPrio('A', 'x', 10), ImplPrio('B', 'x', 10), True),
        (ImplPrio('B', 'x', 10), ImplPrio('A', 'x', 10), False),
        (ImplPrio('A', 'x', 10), ImplPrio('A', 'y', 10), True),
        (ImplPrio('A', 'y', 10), ImplPrio('A', 'x', 10), False),
        (ImplPrio('A', 'x', 10), ImplPrio('A', 'x', 10), False),
    ], ids=['lower-prio', 'higher-prio',
            'lower-fmt', 'higher-fmt',
            'lower-impl', 'higher-impl', 'equal'])
    def test_lt(self, left: ImplPrio, right: ImplPrio,
                expected: bool) -> None:
        """Test __lt__ for various orderings."""
        assert (left < right) == expected

    @pytest.mark.parametrize('left, right, expected', [
        (ImplPrio('A', 'x', 10), ImplPrio('A', 'x', 10), True),
        (ImplPrio('A', 'x', 10), ImplPrio('A', 'x', 20), False),
        (ImplPrio('A', 'x', 10), ImplPrio('B', 'x', 10), False),
    ], ids=['equal', 'diff-prio', 'diff-fmt'])
    def test_eq(self, left: ImplPrio, right: ImplPrio,
                expected: bool) -> None:
        """Test __eq__ for equal and unequal pairs."""
        assert (left == right) == expected

    def test_lt_non_implprio(self) -> None:
        """Comparison with non-ImplPrio returns NotImplemented."""
        impl = ImplPrio('A', 'x', 10)
        assert impl.__lt__(42) is NotImplemented  # pylint: disable=unnecessary-dunder-call # noqa: E501

    def test_eq_non_implprio(self) -> None:
        """Equality with non-ImplPrio returns NotImplemented."""
        impl = ImplPrio('A', 'x', 10)
        assert impl.__eq__(42) is NotImplemented  # pylint: disable=unnecessary-dunder-call # noqa: E501

    def test_sorting_reverse(self) -> None:
        """Sorted reverse gives highest priority first."""
        items = [
            ImplPrio('B', 'y', 5),
            ImplPrio('A', 'x', 20),
            ImplPrio('A', 'z', 10)]
        result = sorted(items, reverse=True)
        assert [r.priority for r in result] == [20, 10, 5]

    def test_total_ordering_derived(self) -> None:
        """@total_ordering provides le, gt, ge from lt and eq."""
        low = ImplPrio('A', 'x', 5)
        high = ImplPrio('A', 'x', 20)
        equal = ImplPrio('A', 'x', 5)
        assert low <= high
        assert high >= low
        assert high > low
        assert low <= high
        assert low <= equal
        assert low >= equal


# -- BestMatch -----------------------------------------------------------

class TestBestMatch:
    """Tests for BestMatch creation and operations."""

    def test_from_lists_sorts_desc(self) -> None:
        """from_lists sorts each group by priority descending."""
        strict = [ImplPrio('A', 'x', 5), ImplPrio('A', 'y', 20)]
        nonstrict = [ImplPrio('B', 'z', 1),
                     ImplPrio('B', 'w', 10)]
        bm = BestMatch.from_lists(strict, nonstrict)
        assert bm.strict_matches[0].priority == 20
        assert bm.strict_matches[1].priority == 5
        assert bm.nonstrict_matches[0].priority == 10
        assert bm.nonstrict_matches[1].priority == 1

    def test_from_lists_empty(self) -> None:
        """from_lists with empty lists gives empty BestMatch."""
        bm = BestMatch.from_lists([], [])
        assert bm.strict_matches == ()
        assert bm.nonstrict_matches == ()
        assert len(bm) == 0

    def test_len(self) -> None:
        """__len__ returns combined count."""
        bm = BestMatch.from_lists(
            [ImplPrio('A', 'x', 10)],
            [ImplPrio('B', 'y', 5), ImplPrio('C', 'z', 1)])
        assert len(bm) == 3

    def test_combined_strict_first(self) -> None:
        """combined() returns strict matches before nonstrict."""
        bm = BestMatch.from_lists(
            [ImplPrio('A', 'x', 10)],
            [ImplPrio('B', 'y', 5)])
        c = bm.combined()
        assert c[0] == ImplPrio('A', 'x', 10)
        assert c[1] == ImplPrio('B', 'y', 5)

    def test_add_merges(self) -> None:
        """Merge two BestMatch objects via add."""
        bm1 = BestMatch.from_lists(
            [ImplPrio('A', 'x', 20)],
            [ImplPrio('B', 'y', 5)])
        bm2 = BestMatch.from_lists(
            [ImplPrio('C', 'z', 10)], [])
        result = BestMatch.add(bm1, bm2)
        assert len(result.strict_matches) == 2
        assert result.strict_matches[0].priority == 20
        assert result.strict_matches[1].priority == 10
        assert len(result.nonstrict_matches) == 1

    def test_add_list_empty(self) -> None:
        """add_list with empty list returns empty BestMatch."""
        result = BestMatch.add_list([])
        assert len(result) == 0

    def test_add_list_single(self) -> None:
        """add_list with one element returns that element."""
        bm = BestMatch.from_lists(
            [ImplPrio('A', 'x', 10)], [])
        result = BestMatch.add_list([bm])
        assert len(result) == 1

    def test_add_list_multiple(self) -> None:
        """add_list merges several BestMatch objects."""
        bms = [
            BestMatch.from_lists(
                [ImplPrio('A', 'x', 20)], []),
            BestMatch.from_lists(
                [], [ImplPrio('B', 'y', 5)]),
            BestMatch.from_lists(
                [ImplPrio('C', 'z', 10)], [])]
        result = BestMatch.add_list(bms)
        assert len(result.strict_matches) == 2
        assert len(result.nonstrict_matches) == 1


# -- TableIOFactory: registration ----------------------------------------


class TestTableIOFactoryRegister:
    """Tests for TableIOFactory registration."""

    def test_init_has_package_formats(self) -> None:
        """Factory init registers known package formats."""
        factory = TableIOFactory()
        names = list(factory._formats.keys())  # pylint: disable=protected-access # noqa: E501
        assert 'CSV' in names
        assert 'HTML' in names

    def test_register_not_subclass(self) -> None:
        """Registering a non-subclass raises ValueError."""
        factory = TableIOFactory()
        with pytest.raises(ValueError, match='subclass of TableIO'):
            factory.i_register(object)  # type: ignore[arg-type]

    def test_register_format_case_conflict(self) -> None:
        """Format name with case-only difference raises."""
        class StubConflict(_StubBase):
            """Stub with case-conflicting format name."""

            _desc = Descriptor(
                format_name='alpha', implementation='conflict',
                capabilities=Capabilities(can_write=_SUP),
                mandatory_args=[], optional_args=[])
        factory = TableIOFactory()
        factory.i_register(StubAlphaHigh)
        with pytest.raises(TableIOFactoryConflictError):
            factory.i_register(StubConflict)

    def test_register_same_format_different_impl(self) -> None:
        """Two implementations of same format can be registered."""
        factory = TableIOFactory()
        factory.i_register(StubAlphaHigh)
        factory.i_register(StubAlphaLow)
        finfo = factory._formats['Alpha']  # pylint: disable=protected-access # noqa: E501
        names = list(finfo._registry.keys())  # pylint: disable=protected-access # noqa: E501
        assert 'high' in names
        assert 'low' in names

    def test_singleton_same_instance(self) -> None:
        """i_get_factory returns the same instance each time."""
        f1 = TableIOFactory.i_get_factory()
        f2 = TableIOFactory.i_get_factory()
        assert f1 is f2


# -- TableIOFactory: create ----------------------------------------------

class TestTableIOFactoryCreate:
    """Tests for TableIOFactory.i_create."""

    def test_by_name(self, tmp_path: Path) -> None:
        """Create picks highest-priority implementation."""
        f = _make_factory_stubs()
        result = f.i_create(
            'Alpha', tmp_path / 'f', FileAccess.CREATE)
        assert isinstance(result, StubAlphaHigh)

    def test_case_insensitive(self, tmp_path: Path) -> None:
        """Format name lookup is case insensitive."""
        f = _make_factory_stubs()
        result = f.i_create(
            'alpha', tmp_path / 'f', FileAccess.CREATE)
        assert isinstance(result, StubAlphaHigh)

    def test_unknown_format(self, tmp_path: Path) -> None:
        """Unknown format name raises."""
        f = _make_factory_stubs()
        with pytest.raises(TableIOFactoryNoSuchError):
            f.i_create(
                'NoSuch', tmp_path / 'f', FileAccess.CREATE)

    def test_with_implementation(self, tmp_path: Path) -> None:
        """Specific implementation is used when requested."""
        f = _make_factory_stubs()
        result = f.i_create(
            'Alpha', tmp_path / 'f', FileAccess.CREATE,
            implementation='low')
        assert isinstance(result, StubAlphaLow)

    def test_unknown_implementation(
            self, tmp_path: Path) -> None:
        """Unknown implementation name raises."""
        f = _make_factory_stubs()
        with pytest.raises(TableIOFactoryNoSuchError):
            f.i_create(
                'Alpha', tmp_path / 'f', FileAccess.CREATE,
                implementation='no_such')

    def test_impl_capability_mismatch(
            self, tmp_path: Path) -> None:
        """Implementation not matching capabilities raises."""
        f = _make_factory_stubs()
        caps = Capabilities(
            can_write=SingleCapability(
                True, Strictness.STRICT),
            can_read=SingleCapability(
                True, Strictness.STRICT))
        with pytest.raises(TableIOFactoryNoCapabilityMatch):
            f.i_create(
                'Alpha', tmp_path / 'f', FileAccess.CREATE,
                implementation='low', capabilities=caps)

    def test_picks_best_strict(self, tmp_path: Path) -> None:
        """Without implementation picks highest-priority strict."""
        f = _make_factory_stubs()
        caps = Capabilities(
            can_write=SingleCapability(
                True, Strictness.STRICT),
            can_read=SingleCapability(
                True, Strictness.STRICT))
        result = f.i_create(
            'Alpha', tmp_path / 'f', FileAccess.CREATE,
            capabilities=caps)
        assert isinstance(result, StubAlphaHigh)

    def test_falls_back_to_nonstrict(
            self, tmp_path: Path) -> None:
        """Falls back to nonstrict when no strict match."""
        f = _make_factory_stubs()
        caps = Capabilities(
            can_write=SingleCapability(
                True, Strictness.STRICT),
            can_fmt_row=SingleCapability(
                True, Strictness.IGNORE))
        result = f.i_create(
            'Alpha', tmp_path / 'f', FileAccess.CREATE,
            capabilities=caps)
        assert isinstance(result, StubAlphaHigh)

    def test_with_args(self, tmp_path: Path) -> None:
        """Args are forwarded to the constructor."""
        f = _make_factory_stubs()
        args: OptionalArgsDict = {}
        args['opt_a'] = 'hello'  # type: ignore[typeddict-unknown-key]
        result = f.i_create(
            'Alpha', tmp_path / 'f', FileAccess.CREATE,
            args=args, implementation='high')
        assert isinstance(result, StubAlphaHigh)
        assert result.opt_a == 'hello'

    def test_none_args(self, tmp_path: Path) -> None:
        """None args creates instance without extra arguments."""
        f = _make_factory_stubs()
        result = f.i_create(
            'Alpha', tmp_path / 'f', FileAccess.CREATE,
            args=None)
        assert isinstance(result, StubAlphaHigh)

    def test_create_rejects_capabilities_without_write(
            self, tmp_path: Path) -> None:
        """CREATE rejects explicit capabilities that omit write support."""
        f = _make_factory_stubs()
        caps = Capabilities(can_read=_SUP)
        with pytest.raises(InsufficientCapabilities,
                           match='FileAccess.CREATE'):
            f.i_create('Alpha', tmp_path / 'f', FileAccess.CREATE,
                       capabilities=caps)

    def test_read_rejects_capabilities_without_read(
            self, tmp_path: Path) -> None:
        """READ rejects explicit capabilities that omit read support."""
        f = _make_factory_stubs()
        caps = Capabilities(can_write=_SUP)
        with pytest.raises(InsufficientCapabilities,
                           match='FileAccess.READ'):
            f.i_create('Alpha', tmp_path / 'f', FileAccess.READ,
                       capabilities=caps)

    @pytest.mark.parametrize('caps', [
        pytest.param(Capabilities(can_read=_SUP), id='read-only'),
        pytest.param(Capabilities(can_write=_SUP), id='write-only'),
        pytest.param(Capabilities(), id='neither')
    ])
    def test_update_rejects_capabilities_without_read_and_write(
            self, tmp_path: Path, caps: Capabilities) -> None:
        """UPDATE requires both read and write in explicit capabilities."""
        f = _make_factory_stubs()
        with pytest.raises(InsufficientCapabilities,
                           match='FileAccess.UPDATE'):
            f.i_create('Alpha', tmp_path / 'f', FileAccess.UPDATE,
                       capabilities=caps)

    def test_inconsistent_request_raises_before_format_lookup(
            self, tmp_path: Path) -> None:
        """Capability-vs-access errors are raised before format lookup."""
        f = _make_factory_stubs()
        caps = Capabilities(can_write=_SUP)
        with pytest.raises(InsufficientCapabilities,
                           match='FileAccess.READ'):
            f.i_create('NoSuch', tmp_path / 'f', FileAccess.READ,
                       capabilities=caps)


# -- TableIOFactory: filter_args -----------------------------------------

class TestTableIOFactoryFilterArgs:
    """Tests for TableIOFactory.i_filter_args."""

    def test_keeps_mandatory_and_common_args(self) -> None:
        """Mandatory args and COMMON_ARGS are preserved."""
        f = _make_factory_stubs()
        f.i_register(StubGammaMandatory)
        args = {
            'required_arg': 'value',
            'file_exists_callback': None,
            'ignored': 'x'
        }
        result = f.i_filter_args(
            cast(OptionalArgsDict, args), 'Gamma', 'CamelCase')
        assert result == {
            'required_arg': 'value',
            'file_exists_callback': None
        }

    def test_keeps_valid(self) -> None:
        """Valid optional args are kept."""
        f = _make_factory_stubs()
        args: OptionalArgsDict = {'csv_delimiter': ';'}
        result = f.i_filter_args(args, 'CSV', 'csv')
        assert result is not None
        assert 'csv_delimiter' in result

    def test_removes_unknown(self) -> None:
        """Unknown args are filtered out."""
        f = _make_factory_stubs()
        args = {'csv_delimiter': ';', 'bogus': 'val'}
        result = f.i_filter_args(
            args, 'CSV', 'csv')  # type: ignore[arg-type]
        assert result is not None
        assert 'csv_delimiter' in result
        assert 'bogus' not in result

    def test_keeps_common(self) -> None:
        """COMMON_ARGS (file_exists_callback) are kept."""
        f = _make_factory_stubs()
        args: OptionalArgsDict = {
            'file_exists_callback': None}
        result = f.i_filter_args(args, 'CSV', 'csv')
        assert result is not None
        assert 'file_exists_callback' in result

    def test_none_returns_none(self) -> None:
        """None args returns None."""
        f = _make_factory_stubs()
        result = f.i_filter_args(None, 'CSV', 'csv')
        assert result is None


# -- TableIOFactory: listing formats -------------------------------------

class TestTableIOFactoryFormats:
    """Tests for TableIOFactory.i_get_registered_formats."""

    def test_sorted(self) -> None:
        """Format names are sorted alphabetically."""
        f = _make_factory_stubs()
        names = f.i_get_registered_formats()
        assert names == sorted(names)

    def test_includes_stubs(self) -> None:
        """Registered stubs appear in the format list."""
        f = _make_factory_stubs()
        names = f.i_get_registered_formats()
        assert 'Alpha' in names
        assert 'Beta' in names

    def test_with_lower(self) -> None:
        """lower=True adds lowercase variant."""
        f = _make_factory_stubs()
        names = f.i_get_registered_formats(lower=True)
        assert 'Alpha' in names
        assert 'alpha' in names

    def test_with_upper(self) -> None:
        """upper=True adds uppercase variant."""
        f = _make_factory_stubs()
        names = f.i_get_registered_formats(upper=True)
        assert 'Alpha' in names
        assert 'ALPHA' in names

    def test_caps_strict_excludes_tolerant(self) -> None:
        """Strict capability filters out tolerant-only formats."""
        f = _make_factory_stubs()
        caps = Capabilities(
            can_fmt_row=SingleCapability(
                True, Strictness.STRICT))
        names = f.i_get_registered_formats(
            capabilities=caps, empty_is_ok=True)
        assert 'Beta' in names
        assert 'Alpha' not in names

    def test_caps_tolerant_includes_both(self) -> None:
        """Tolerant capability includes strict and nonstrict."""
        f = _make_factory_stubs()
        caps = Capabilities(
            can_fmt_row=SingleCapability(
                True, Strictness.IGNORE))
        names = f.i_get_registered_formats(
            capabilities=caps, empty_is_ok=True)
        assert 'Beta' in names
        assert 'Alpha' in names

    def test_caps_sorted(self) -> None:
        """Capability-filtered names are still sorted."""
        f = _make_factory_stubs()
        caps = Capabilities(
            can_write=SingleCapability(
                True, Strictness.STRICT))
        names = f.i_get_registered_formats(
            capabilities=caps)
        assert names == sorted(names)

    def test_box_capability_matches_spreadsheet_formats(self) -> None:
        """Requesting box support includes the spreadsheet formats."""
        f = _make_factory_stubs()
        caps = Capabilities(
            can_write_box=SingleCapability(
                True, Strictness.STRICT))
        names = f.i_get_registered_formats(capabilities=caps)
        assert 'Excel' in names
        assert 'ODS' in names

    def test_box_capability_empty_ok_still_returns_match(self) -> None:
        """empty_is_ok keeps returning matching formats when they exist."""
        f = _make_factory_stubs()
        caps = Capabilities(
            can_write_box=SingleCapability(
                True, Strictness.STRICT))
        names = f.i_get_registered_formats(
            capabilities=caps, empty_is_ok=True)
        assert 'Excel' in names
        assert 'ODS' in names

    def test_multi_sheet_capability_matches_spreadsheet_formats(self) -> None:
        """Requesting multi-sheet support includes spreadsheet formats."""
        f = _make_factory_stubs()
        caps = Capabilities(
            multi_sheet=SingleCapability(
                True, Strictness.STRICT))
        names = f.i_get_registered_formats(capabilities=caps)
        assert 'Excel' in names
        assert 'ODS' in names
        assert 'CSV' not in names

    def test_multi_sheet_capability_empty_ok_still_returns_match(self) -> \
            None:
        """empty_is_ok keeps returning multi-sheet-capable formats."""
        f = _make_factory_stubs()
        caps = Capabilities(
            multi_sheet=SingleCapability(
                True, Strictness.STRICT))
        names = f.i_get_registered_formats(
            capabilities=caps, empty_is_ok=True)
        assert 'Excel' in names
        assert 'ODS' in names

    def test_border_capability_matches_spreadsheet_formats(self) -> None:
        """Requesting border support matches the capable sheet formats."""
        f = _make_factory_stubs()
        caps = Capabilities(
            can_write_borders=SingleCapability(
                True, Strictness.STRICT))
        names = f.i_get_registered_formats(capabilities=caps)
        assert 'Excel' in names
        assert 'ODS' in names
        assert 'CSV' not in names

    def test_no_matching_formats_raise_when_empty_is_not_allowed(self) -> \
            None:
        """Capability filtering raises when no configured format can match."""
        f = _make_factory_stubs()
        f._formats = {  # pylint: disable=protected-access
            'Alpha': f._formats['Alpha'],  # pylint: disable=protected-access
            'Beta': f._formats['Beta']  # pylint: disable=protected-access
        }
        f._lower2correct = {  # pylint: disable=protected-access
            'alpha': 'Alpha',
            'beta': 'Beta'
        }
        caps = Capabilities(
            can_write_box=SingleCapability(
                True, Strictness.STRICT))
        with pytest.raises(TableIOFactoryNoCapabilityMatch,
                           match='No formats match the capabilities'):
            f.i_get_registered_formats(capabilities=caps)


# -- TableIOFactory: listing implementations -----------------------------

class TestTableIOFactoryImplementations:
    """Tests for TableIOFactory.i_get_registered_implementations."""

    def test_basic(self) -> None:
        """All stub implementations are returned."""
        f = _make_factory_stubs()
        names = f.i_get_registered_implementations()
        assert 'high' in names
        assert 'low' in names
        assert 'beta_impl' in names

    def test_sorted(self) -> None:
        """Implementation names are sorted."""
        f = _make_factory_stubs()
        names = f.i_get_registered_implementations()
        assert names == sorted(names)

    def test_by_format(self) -> None:
        """Filter by format name returns only that format."""
        f = _make_factory_stubs()
        names = f.i_get_registered_implementations(
            format_name='Alpha')
        assert 'high' in names
        assert 'low' in names
        assert 'beta_impl' not in names

    def test_with_lower(self) -> None:
        """lower=True adds lowercase variant."""
        f = _make_factory_stubs()
        names = f.i_get_registered_implementations(
            format_name='Alpha', lower=True)
        assert 'high' in names

    def test_with_lower_adds_variant_for_mixed_case_implementation(self) -> \
            None:
        """lower=True adds a lowercase alias for mixed-case names."""
        f = _make_factory_stubs()
        f.i_register(StubGammaMandatory)
        names = f.i_get_registered_implementations(
            format_name='Gamma', lower=True)
        assert 'CamelCase' in names
        assert 'camelcase' in names

    def test_with_upper(self) -> None:
        """upper=True adds uppercase variant."""
        f = _make_factory_stubs()
        names = f.i_get_registered_implementations(
            format_name='Alpha', upper=True)
        assert 'HIGH' in names

    def test_with_caps(self) -> None:
        """Capability filter limits implementations."""
        f = _make_factory_stubs()
        caps = Capabilities(
            can_read=SingleCapability(
                True, Strictness.STRICT))
        names = f.i_get_registered_implementations(
            capabilities=caps, empty_is_ok=True)
        assert 'high' in names
        assert 'beta_impl' in names
        assert 'low' not in names

    def test_no_match_raises(self) -> None:
        """No match with empty_is_ok=False raises."""
        f = _make_factory_stubs()
        caps = Capabilities(
            can_write_box=SingleCapability(
                True, Strictness.STRICT))
        with pytest.raises(TableIOFactoryNoCapabilityMatch):
            f.i_get_registered_implementations(
                format_name='Alpha', capabilities=caps)

    def test_no_match_empty_ok(self) -> None:
        """No match with empty_is_ok=True returns []."""
        f = _make_factory_stubs()
        caps = Capabilities(
            can_write_box=SingleCapability(
                True, Strictness.STRICT))
        names = f.i_get_registered_implementations(
            format_name='Alpha', capabilities=caps,
            empty_is_ok=True)
        assert not names

    def test_multi_sheet_with_caps(self) -> None:
        """Capability filtering finds only multi-sheet implementations."""
        f = _make_factory_stubs()
        caps = Capabilities(
            multi_sheet=SingleCapability(
                True, Strictness.STRICT))
        names = f.i_get_registered_implementations(
            capabilities=caps, empty_is_ok=True)
        assert 'OpenPyXL' in names
        assert 'odfdo' in names
        assert 'high' not in names


# -- TableIOFactory: usage -----------------------------------------------

class TestTableIOFactoryUsage:
    """Tests for TableIOFactory.i_get_usage."""

    def test_exact(self) -> None:
        """Get usage by exact format and implementation name."""
        f = _make_factory_stubs()
        desc = f.i_get_usage('Alpha', 'high')
        assert desc.format_name == 'Alpha'
        assert desc.implementation == 'high'

    def test_case_insensitive_format(self) -> None:
        """Format name lookup is case insensitive."""
        f = _make_factory_stubs()
        desc = f.i_get_usage('alpha', 'high')
        assert desc.format_name == 'Alpha'

    def test_case_insensitive_impl(self) -> None:
        """Implementation name lookup is case insensitive."""
        f = _make_factory_stubs()
        desc = f.i_get_usage('Alpha', 'HIGH')
        assert desc.implementation == 'high'

    def test_unknown_format(self) -> None:
        """Unknown format name raises."""
        f = _make_factory_stubs()
        with pytest.raises(TableIOFactoryNoSuchError):
            f.i_get_usage('NoSuch', 'high')

    def test_unknown_impl(self) -> None:
        """Unknown implementation name raises."""
        f = _make_factory_stubs()
        with pytest.raises(TableIOFactoryNoSuchError):
            f.i_get_usage('Alpha', 'no_such')


# -- Shortcut functions --------------------------------------------------

class TestShortcutFunctions:
    """Tests for module-level shortcut functions."""

    def test_list_registered_tableio(self) -> None:
        """list_registered_tableio returns known formats."""
        names = list_registered_tableio()
        assert 'CSV' in names
        assert 'HTML' in names
        assert 'ODS' in names

    def test_list_implementations_tableio(self) -> None:
        """list_implementations_tableio returns known impls."""
        names = list_implementations_tableio()
        assert 'csv' in names
        assert 'mformat' in names

    def test_usage_tableio(self) -> None:
        """usage_tableio returns correct descriptor."""
        desc = usage_tableio('CSV', 'csv')
        assert desc.format_name == 'CSV'
        assert desc.implementation == 'csv'

    def test_create_tableio(self, tmp_path: Path) -> None:
        """create_tableio creates a TableIO instance."""
        result = create_tableio(
            'CSV', tmp_path / 'test', FileAccess.CREATE)
        assert isinstance(result, TableIO)

    def test_filter_args_tableio(self) -> None:
        """filter_args_tableio filters correctly."""
        args: OptionalArgsDict = {'csv_delimiter': ';'}
        result = filter_args_tableio(args, 'CSV', 'csv')
        assert result is not None
        assert 'csv_delimiter' in result

    def test_register_tableio(self) -> None:
        """register_tableio adds a class to the singleton."""
        import tableio.factory as fmod  # pylint: disable=import-outside-toplevel # noqa: E501
        saved = fmod._the_factory  # pylint: disable=protected-access
        fmod._the_factory = None  # pylint: disable=protected-access
        try:
            register_tableio(StubBeta)
            names = list_registered_tableio()
            assert 'Beta' in names
        finally:
            fmod._the_factory = saved  # pylint: disable=protected-access
