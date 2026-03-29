#! /usr/bin/env python3
"""Shared public types used by the tableio package."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from enum import IntEnum, auto
from typing import NamedTuple, Optional

from tableio.capability import Capabilities


class Descriptor(NamedTuple):
    """Metadata describing one TableIO implementation."""

    format_name: str
    """The name of the file format."""

    implementation: str
    """The implementation name for the file format."""

    capabilities: Capabilities
    """The capabilities of the reader/writer class."""

    mandatory_args: list[str]
    """Mandatory constructor arguments besides file name and access."""

    optional_args: list[str]
    """Optional constructor arguments."""

    priority: int = 10
    """The implementation priority. Higher means more preferred."""


class Box(NamedTuple):
    """A rectangular area in a sheet or file."""

    top: int
    left: int
    bottom: Optional[int]
    right: Optional[int]


class Position(NamedTuple):
    """A zero-based row and column position in one sheet."""

    row: int
    column: int


class FileAccess(IntEnum):
    """What access is requested to a file."""

    READ = auto()
    """The file must exist and is opened for reading."""

    CREATE = auto()
    """The file is created and opened for writing and reading."""

    UPDATE = auto()
    """The file must exist and is opened for reading and writing."""
