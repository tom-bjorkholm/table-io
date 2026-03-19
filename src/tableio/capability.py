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

    can_fmt_row: SingleCapability = SingleCapability()
    """The writer class can apply a format to a row."""

    can_fmt_value: SingleCapability = SingleCapability()
    """The writer class can apply a format to a value."""

    filtered_data_range: SingleCapability = SingleCapability()
    """The writer class can mark a table as a filterable data range."""

    can_write_box: SingleCapability = SingleCapability()
    """The writer class can write to position given by a box."""

    can_read_box: SingleCapability = SingleCapability()
    """The reader class can read from position given by a box."""

    can_write_highlight: SingleCapability = SingleCapability()
    """The writer class can write highlight according to format."""


def single_capability_match(offered: SingleCapability,
                            will_use: SingleCapability,
                            ignore_allowed: bool = True) -> bool:
    """Check if the offered single capability matches the will use.

    Args:
        offered: The offered single capability. Does the reader/writer
                 class support this capability?
        will_use: The will use single capability. Does the requester intend to
                  use this capability?
        ignore_allowed: If False: when the offered single capability would
                        ignore the will use single capability it is
                        considered a mismatch, and will return False.
                        If False: when the offered single capability would
                        ignore the will use single capability it is
                        considered a match, and will return True.
    Returns:
        True if the offered single capability matches the will use,
        False otherwise.
    """
    if not will_use.supported:
        return True
    if offered.supported:
        return True
    if Strictness.STRICT in (offered.strictness, will_use.strictness):
        return False
    if ignore_allowed:
        return True
    return False


def capability_match(offered: Capabilities,
                     will_use: Capabilities,
                     ignore_allowed: bool = False) -> bool:
    """Check if the offered capabilities match the required capabilities.

    Args:
        offered: The offered capabilities. What capabilities does the
                 reader/writer class support?
        will_use: The recuested capabilities. What capabilities
                  does the requester intend to use?
        ignore_allowed: If False: when an offered capability would ignore a
                        will use capability it is considered a mismatch, and
                        considered a mismatch, and will return False.
                        If True: when an offered capability would ignore a
                        will use capability it is considered a match, and
                        will return True.
    Returns:
        True if the offered capabilities match the will_use capabilities,
        False otherwise.
    """
    for single_offered, single_will_use in zip(offered, will_use):
        if not single_capability_match(single_offered, single_will_use,
                                       ignore_allowed):
            return False
    return True


class CapabilityNotSupported(ValueError):
    """Exception raised when a capability is not supported."""

    def __init__(self, action: str):
        """Initialize the exception.

        Args:
            action: The requested action that is not supported.
        """
        self.action = action
        super().__init__(f'The class does not support {action}.')
