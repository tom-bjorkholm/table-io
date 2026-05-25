#! /usr/bin/env python3
"""Tests for file access capability helpers."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from io import StringIO
from typing import cast

import pytest

from tableio import CAP_IGNORABLE, CAP_NEEDED, Capabilities, FileAccess, \
    InsufficientCapabilities, NO_ERROR_OUTPUT, access_capabilities, \
    add_access_capabilities, check_access_capabilities

from .file_access_test_helper import unsupported_file_access


@pytest.mark.parametrize(('file_access', 'expected'), [
    pytest.param(FileAccess.READ, Capabilities(can_read=CAP_NEEDED),
                 id='read'),
    pytest.param(FileAccess.CREATE, Capabilities(can_write=CAP_NEEDED),
                 id='create'),
    pytest.param(FileAccess.UPDATE,
                 Capabilities(can_read=CAP_NEEDED, can_write=CAP_NEEDED),
                 id='update')
])
def test_access_capabilities(file_access: FileAccess,
                             expected: Capabilities) -> None:
    """File access maps to the capabilities it requires."""
    assert access_capabilities(file_access) == expected


def test_access_caps_bad_type() -> None:
    """File access type errors can be written before raising."""
    error_file = StringIO()
    with pytest.raises(TypeError, match='file_access'):
        access_capabilities(cast(FileAccess, object()), error_file)
    assert error_file.getvalue() == \
        'file_access must be a FileAccess value.\n'


def test_access_caps_unknown_value() -> None:
    """Unsupported future FileAccess values are reported clearly."""
    error_file = StringIO()
    with pytest.raises(ValueError, match='unsupported file access'):
        access_capabilities(unsupported_file_access(), error_file)
    assert error_file.getvalue() == \
        'unsupported file access: <FileAccess.UNKNOWN: 99>.\n'


def test_add_access_caps_new() -> None:
    """Adding access requirements returns a new Capabilities object."""
    caps = Capabilities(can_fmt_row=CAP_IGNORABLE)
    result = add_access_capabilities(FileAccess.UPDATE, caps)
    expected = Capabilities(can_write=CAP_NEEDED, can_read=CAP_NEEDED,
                            can_fmt_row=CAP_IGNORABLE)
    assert result == expected
    assert caps == Capabilities(can_fmt_row=CAP_IGNORABLE)


def test_add_access_caps_bad_caps() -> None:
    """Capability type errors can be written before raising."""
    error_file = StringIO()
    with pytest.raises(TypeError, match='capabilities'):
        add_access_capabilities(FileAccess.READ, cast(Capabilities, object()),
                                error_file)
    assert error_file.getvalue() == \
        'capabilities must be a Capabilities object.\n'


def test_check_access_caps_ok() -> None:
    """Checks pass when the capabilities support the file access."""
    caps = Capabilities(can_read=CAP_NEEDED, can_write=CAP_NEEDED)
    check_access_capabilities(FileAccess.UPDATE, caps)


def test_check_access_caps_writes() -> None:
    """Checks raise and optionally write for insufficient capabilities."""
    error_file = StringIO()
    with pytest.raises(InsufficientCapabilities) as exc_info:
        check_access_capabilities(FileAccess.UPDATE, Capabilities(),
                                  error_file)
    assert exc_info.value.capability_names == ('can_read', 'can_write')
    assert error_file.getvalue() == (
        'FileAccess.UPDATE requires both can_read and can_write '
        'capabilities.\n')


def test_no_error_output_suppresses() -> None:
    """The no-output marker suppresses helper error messages."""
    with pytest.raises(TypeError, match='file_access'):
        access_capabilities(cast(FileAccess, object()), NO_ERROR_OUTPUT)
