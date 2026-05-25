#! /usr/bin/env python3
"""Helpers that connect file access modes to capability requests."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from enum import Enum, auto
from typing import NoReturn, TextIO

from tableio.capability import CAP_NEEDED, Capabilities
from tableio.tableio_types import FileAccess


class NoErrorOutput(Enum):
    """Text stream marker when helper errors should not be printed."""

    NO_OUTPUT = auto()
    """Text stream marker when helper errors should not be printed."""


NO_ERROR_OUTPUT = NoErrorOutput.NO_OUTPUT
"""Text stream marker used when helper errors should not be printed."""


class InsufficientCapabilities(ValueError):
    """Raised when requested capabilities contradict requested file access.

    Error raised when the caller supplies file access and explicit
    Capabilities, but the requested capabilities do not include the capability
    implied by that access mode. For example, READ requires can_read, CREATE
    requires can_write, and UPDATE requires both.
    """

    def __init__(self, message: str, capability_names: tuple[str, ...] =
                 ()) -> None:
        """Initialize the exception."""
        self.capability_names = capability_names
        super().__init__(message)


def _raise_error(error_file: TextIO | NoErrorOutput,
                 error: Exception) -> NoReturn:
    """Write an error message and raise the error."""
    if isinstance(error_file, NoErrorOutput):
        raise error
    error_file.write(str(error) + '\n')
    raise error


def _check_access_value(file_access: FileAccess,
                        error_file: TextIO | NoErrorOutput) -> None:
    """Raise if file access is not a supported FileAccess value."""
    if not isinstance(file_access, FileAccess):
        error = TypeError('file_access must be a FileAccess value.')
        _raise_error(error_file, error)
    valid_access = (FileAccess.READ, FileAccess.CREATE, FileAccess.UPDATE)
    if file_access not in valid_access:
        error = ValueError(f'unsupported file access: {file_access!r}.')
        _raise_error(error_file, error)


def _check_capabilities_value(capabilities: Capabilities,
                              error_file: TextIO | NoErrorOutput) -> None:
    """Raise if capabilities is not a Capabilities object."""
    if not isinstance(capabilities, Capabilities):
        error = TypeError('capabilities must be a Capabilities object.')
        _raise_error(error_file, error)


def access_capabilities(file_access: FileAccess,
                        error_file: TextIO | NoErrorOutput =
                        NO_ERROR_OUTPUT) -> Capabilities:
    """Return the capabilities implied by a file access mode.

    Args:
        file_access: File access mode to convert to capability requirements.
        error_file: Text stream receiving error messages before exceptions.
    Raises:
        TypeError: If file_access is not a FileAccess value.
        ValueError: If file_access is an unsupported FileAccess value.
    Returns:
        Capabilities needed for the requested file access.
    """
    _check_access_value(file_access, error_file)
    if file_access == FileAccess.READ:
        return Capabilities(can_read=CAP_NEEDED)
    if file_access == FileAccess.CREATE:
        return Capabilities(can_write=CAP_NEEDED)
    return Capabilities(can_read=CAP_NEEDED, can_write=CAP_NEEDED)


def add_access_capabilities(file_access: FileAccess,
                            capabilities: Capabilities,
                            error_file: TextIO | NoErrorOutput =
                            NO_ERROR_OUTPUT) \
        -> Capabilities:
    """Return capabilities with file access requirements added.

    The original capabilities object is not mutated.

    Args:
        file_access: File access mode to add capability requirements for.
        capabilities: Existing capability requirements to extend.
        error_file: Text stream receiving error messages before exceptions.
    Raises:
        TypeError: If file_access or capabilities has an invalid type.
        ValueError: If file_access is an unsupported FileAccess value.
    Returns:
        New Capabilities object including the file access requirements.
    """
    _check_access_value(file_access, error_file)
    _check_capabilities_value(capabilities, error_file)
    if file_access == FileAccess.READ:
        return capabilities._replace(can_read=CAP_NEEDED)
    if file_access == FileAccess.CREATE:
        return capabilities._replace(can_write=CAP_NEEDED)
    return capabilities._replace(can_read=CAP_NEEDED, can_write=CAP_NEEDED)


def _missing_access_caps(file_access: FileAccess,
                         capabilities: Capabilities) -> tuple[str, ...]:
    """Return capability names missing for the requested access mode."""
    if file_access == FileAccess.READ and not capabilities.can_read.supported:
        return ('can_read',)
    if file_access == FileAccess.CREATE and \
            not capabilities.can_write.supported:
        return ('can_write',)
    if file_access == FileAccess.UPDATE:
        missing: list[str] = []
        if not capabilities.can_read.supported:
            missing.append('can_read')
        if not capabilities.can_write.supported:
            missing.append('can_write')
        return tuple(missing)
    return ()


def _access_error_message(file_access: FileAccess) -> str:
    """Return the error message for missing access capabilities."""
    if file_access == FileAccess.READ:
        return 'FileAccess.READ requires can_read capability.'
    if file_access == FileAccess.CREATE:
        return 'FileAccess.CREATE requires can_write capability.'
    return 'FileAccess.UPDATE requires both can_read and can_write ' + \
        'capabilities.'


def check_access_capabilities(file_access: FileAccess,
                              capabilities: Capabilities,
                              error_file: TextIO | NoErrorOutput =
                              NO_ERROR_OUTPUT) -> None:
    """Raise if capabilities are not enough for requested access mode.

    Args:
        file_access: File access mode to check capability requirements for.
        capabilities: Capability requirements to check.
        error_file: Text stream receiving error messages before exceptions.
    Raises:
        TypeError: If file_access or capabilities has an invalid type.
        ValueError: If file_access is an unsupported FileAccess value.
        InsufficientCapabilities: If capabilities do not support file_access.
    """
    _check_access_value(file_access, error_file)
    _check_capabilities_value(capabilities, error_file)
    missing_caps = _missing_access_caps(file_access, capabilities)
    if missing_caps:
        message = _access_error_message(file_access)
        error = InsufficientCapabilities(message, missing_caps)
        _raise_error(error_file, error)
