#! /usr/bin/env python3
"""Capabilities of the reader/writer class for a file format."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import NamedTuple
from enum import IntEnum, auto


class Strictness(IntEnum):
    """Strictness of a capability."""

    STRICT = auto()
    """Strictly enforce, raise if not supported."""
    IGNORE = auto()
    """Ignored if not supported."""


class SingleCapability(NamedTuple):
    """Single capability of aspect of reader/writer class.

    Describes if a reader/writer class for a file format can handle a
    specific aspect when reading or writing a file.

    A reader/writer class will provide information about its capabilities in a
    Capabilities object. For the single capability this says if it is
    supported, but also how the class behaves if it is requested and not
    supported.
    If supported is True, the strictness is not used.
    If supported is False, and the strictness is STRICT, an exception is raised
    when a call to the reader/writer class is made that requires the
    capability.
    If supported is False, and the strictness is IGNORE, the call is ignored.

    When requesting reader/writer class from the factory, the requester can
    specify that only reader/writer classes that support the requested
    capabilities are returned.
    If the requester sets supported to True for a capability, it means that
    the requester will be making calls to the reader/writer class that requires
    the capability.
    If the requester sets supported to False for a capability, it means that
    the requester will not be making calls to the reader/writer class that
    requires the capability. (If the requester sets supported to false, the
    strictness will not be used.)
    If the requester sets supported to True and strictness to STRICT, it means
    that the requester is only accepting reader/writer classes that support
    the capability.
    If the requester sets supported to True and strictness to IGNORE, it means
    that the requester is accepting reader/writer classes that may ignore
    calls using the capability.
    """

    supported: bool = False
    """If the capability is supported."""
    strictness: Strictness = Strictness.IGNORE
    """How the capability is handled if not supported. Default is to ignore."""


class Capabilities(NamedTuple):
    """Capabilities of a reader/writer class for a file format."""

    can_write: SingleCapability = SingleCapability()
    """The reader/writer class can write to the file format."""
    can_read: SingleCapability = SingleCapability()
    """The reader/writer class can read from the file format."""
