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


def capability_to_str(capability: SingleCapability) -> str:
    """Convert a single capability to a string.

    Args:
        capability: The single capability to convert.
    Returns:
        A string representation of the single capability.
    """
    result = ''
    if capability.supported:
        result += 'supported'
    else:
        result += 'not supported'
    if capability.strictness == Strictness.STRICT:
        result += ' (strict)'
    else:
        result += ' (ignore)'
    return result


# ----------------------------------------------------------------------------
# Capability constants from the point of view of the requester
# ----------------------------------------------------------------------------

CAP_NOT_USED = SingleCapability(supported=False, strictness=Strictness.IGNORE)
"""A capability that is not used.

   The requester promises to not use this capability, so it does not
   matter if the implementation supports it or not.
   """

CAP_NEEDED = SingleCapability(supported=True, strictness=Strictness.STRICT)
"""A capability that is used and must be supported.

   In the selection of reader/writer class it is a must that the selected
   class supports this capability. If no matching reader/writer class is
   found to fulfill the request, an exception is raised.
   """

CAP_IGNORABLE = SingleCapability(supported=True, strictness=Strictness.IGNORE)
"""A capability that can be ignored if not supported.

   An example might be that prefer to be able to write a value in bold,
   but the request can accept that the implementation ignores the bold
   formatting."""

# ----------------------------------------------------------------------------
# Capability constants from the point of view of the reader/writer class
# ----------------------------------------------------------------------------

CAP_IMPLEMENTED = SingleCapability(supported=True,
                                   strictness=Strictness.STRICT)
"""A capability that is fully implemented and supported."""

CAP_IGNORED = SingleCapability(supported=False, strictness=Strictness.IGNORE)
"""A capability that is not supported and will be ignored if requested.

   The implementation cannot fulfill the request, but it makes sense to
   ignore this feature and continue anyway. A typical example would be
   a request to format a written value in bold. Here ignoring the bold
   formatting makes sense as there is still a value written to the file.
   """

CAP_UNSUPPORTED = SingleCapability(supported=False,
                                   strictness=Strictness.STRICT)
"""A capability that is not supported and will raise an exception if requested.

   This is a for a feature that cannot be supported but it would not make
   sense to ignore. A typical example would be a request request to write
   a value in a specific location in the file. Writing the value to a
   different location would not make sense. Thus the only sensible thing
   to do is to raise an exception.
   """
