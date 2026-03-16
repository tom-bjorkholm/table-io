#! /usr/local/bin/python3
"""Tests for the capability module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest
from pytest import CaptureFixture

from tableio.capability import Capabilities, SingleCapability, Strictness, \
    capability_match, single_capability_match

from .check_capsys import check_capsys


def make_capability(
        supported: bool = False,
        strictness: Strictness = Strictness.IGNORE) -> SingleCapability:
    """Build a SingleCapability value for tests."""
    return SingleCapability(supported=supported, strictness=strictness)


def make_capabilities(
        can_write: SingleCapability = SingleCapability(),
        can_read: SingleCapability = SingleCapability(),
        can_fmt_row: SingleCapability = SingleCapability(),
        can_fmt_value: SingleCapability = SingleCapability(),
        filtered_data_range: SingleCapability = SingleCapability(),
        ) -> Capabilities:
    """Build a Capabilities value for tests."""
    return Capabilities(
        can_write=can_write,
        can_read=can_read,
        can_fmt_row=can_fmt_row,
        can_fmt_value=can_fmt_value,
        filtered_data_range=filtered_data_range,
    )


def expected_single_capability_match(
        offered: SingleCapability, will_use: SingleCapability,
        ignore_allowed: bool) -> bool:
    """Return the documented expected result for a capability pair."""
    strict_mismatch = Strictness.STRICT in (
        offered.strictness,
        will_use.strictness,
    )
    return (
        not will_use.supported
        or offered.supported
        or (ignore_allowed and not strict_mismatch)
    )


SINGLE_CAPABILITY_CASES = tuple(
    pytest.param(
        make_capability(offered_supported, offered_strictness),
        make_capability(will_use_supported, will_use_strictness),
        ignore_allowed,
        expected_single_capability_match(
            make_capability(offered_supported, offered_strictness),
            make_capability(will_use_supported, will_use_strictness),
            ignore_allowed,
        ),
        id=(
            f'offered-{offered_supported}-{offered_strictness.name.lower()}_'
            f'will-use-{will_use_supported}_'
            f'{will_use_strictness.name.lower()}_'
            f'ignore-{ignore_allowed}'
        ),
    )
    for offered_supported in (False, True)
    for offered_strictness in Strictness
    for will_use_supported in (False, True)
    for will_use_strictness in Strictness
    for ignore_allowed in (False, True)
)


@pytest.mark.parametrize(
    ('offered', 'will_use', 'ignore_allowed', 'expected'),
    SINGLE_CAPABILITY_CASES,
)
def test_single_capability_match_covers_all_supported_and_strictness_cases(
        offered: SingleCapability, will_use: SingleCapability,
        ignore_allowed: bool, expected: bool,
        capsys: CaptureFixture[str]) -> None:
    """Test single_capability_match for the full decision matrix."""
    assert single_capability_match(offered, will_use, ignore_allowed) is \
        expected
    check_capsys(capsys)


def test_single_capability_runtime_defaults(
        capsys: CaptureFixture[str]) -> None:
    """Test the runtime defaults of SingleCapability."""
    default_capability = SingleCapability()
    assert default_capability.supported is False
    assert default_capability.strictness is Strictness.IGNORE
    assert default_capability == SingleCapability(
        supported=False,
        strictness=Strictness.IGNORE,
    )
    check_capsys(capsys)


def test_capabilities_runtime_defaults(capsys: CaptureFixture[str]) -> None:
    """Test the runtime defaults of Capabilities."""
    default_single = SingleCapability()
    capabilities = Capabilities()
    assert capabilities == Capabilities(
        can_write=default_single,
        can_read=default_single,
        can_fmt_row=default_single,
        can_fmt_value=default_single,
        filtered_data_range=default_single,
    )
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('offered', 'will_use', 'ignore_allowed', 'expected'),
    [
        pytest.param(
            Capabilities(
                can_write=SingleCapability(
                    supported=True,
                    strictness=Strictness.IGNORE,
                ),
                can_read=SingleCapability(
                    supported=True,
                    strictness=Strictness.IGNORE,
                ),
            ),
            Capabilities(
                can_write=SingleCapability(
                    supported=True,
                    strictness=Strictness.STRICT,
                ),
            ),
            False,
            True,
            id='writer-supports-requested-write',
        ),
        pytest.param(
            Capabilities(
                can_write=SingleCapability(
                    supported=True,
                    strictness=Strictness.IGNORE,
                ),
                can_fmt_row=SingleCapability(
                    supported=False,
                    strictness=Strictness.STRICT,
                ),
            ),
            Capabilities(
                can_write=SingleCapability(
                    supported=True,
                    strictness=Strictness.IGNORE,
                ),
                can_fmt_row=SingleCapability(
                    supported=True,
                    strictness=Strictness.IGNORE,
                ),
            ),
            False,
            False,
            id='strict-row-format-mismatch',
        ),
        pytest.param(
            Capabilities(
                can_fmt_value=SingleCapability(
                    supported=False,
                    strictness=Strictness.IGNORE,
                ),
            ),
            Capabilities(
                can_fmt_value=SingleCapability(
                    supported=True,
                    strictness=Strictness.IGNORE,
                ),
            ),
            True,
            True,
            id='ignored-value-format-is-allowed',
        ),
    ],
)
def test_capability_match_has_readable_examples(
        offered: Capabilities, will_use: Capabilities,
        ignore_allowed: bool, expected: bool,
        capsys: CaptureFixture[str]) -> None:
    """Test capability_match with a few explicit easy-to-read examples."""
    assert capability_match(offered, will_use, ignore_allowed) is expected
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('offered', 'will_use', 'ignore_allowed', 'expected'),
    [
        pytest.param(
            make_capabilities(),
            make_capabilities(),
            False,
            True,
            id='all-defaults',
        ),
        pytest.param(
            make_capabilities(
                can_write=make_capability(False, Strictness.STRICT),
            ),
            make_capabilities(
                can_write=make_capability(True, Strictness.IGNORE),
            ),
            False,
            False,
            id='strict-write-mismatch',
        ),
        pytest.param(
            make_capabilities(
                can_read=make_capability(True, Strictness.IGNORE),
            ),
            make_capabilities(
                can_read=make_capability(True, Strictness.STRICT),
            ),
            False,
            True,
            id='supported-read',
        ),
        pytest.param(
            make_capabilities(
                can_fmt_row=make_capability(False, Strictness.IGNORE),
            ),
            make_capabilities(
                can_fmt_row=make_capability(True, Strictness.IGNORE),
            ),
            False,
            False,
            id='ignore-row-mismatch-disallowed',
        ),
        pytest.param(
            make_capabilities(
                can_fmt_value=make_capability(False, Strictness.IGNORE),
            ),
            make_capabilities(
                can_fmt_value=make_capability(True, Strictness.IGNORE),
            ),
            True,
            True,
            id='ignore-value-mismatch-allowed',
        ),
        pytest.param(
            make_capabilities(),
            make_capabilities(
                filtered_data_range=make_capability(
                    False, Strictness.STRICT,
                ),
            ),
            False,
            True,
            id='unused-filter-capability',
        ),
    ],
)
def test_capability_match_handles_defaults_and_each_public_field(
        offered: Capabilities, will_use: Capabilities,
        ignore_allowed: bool, expected: bool,
        capsys: CaptureFixture[str]) -> None:
    """Test capability_match across defaults and field-specific cases."""
    assert capability_match(offered, will_use, ignore_allowed) is expected
    check_capsys(capsys)
