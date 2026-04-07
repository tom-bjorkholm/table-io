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


class TableBorderStyle(IntEnum):
    """Border style of a table.

    Used to describe the borders of a table. Borders are defined at the
    table level, not at the cell level. A table may have borders on all
    sides and also internally in the table. In the styles the words
    'thin' and 'thick' describe the semantic weight of the borders; they
    may be mapped to different physical border styles in the file format.
    When several parts of one style affect the same cell edge, the
    thickest weight is used. For example, if the separator below the
    first row should be thick and inner lines should be thin, the cell
    edge below the first row is thick.
    """

    NONE = auto()
    """No borders."""

    OUTER_THIN = auto()
    """Thin border around the table. No inner borders."""

    OUTER_THICK = auto()
    """Thick border around the table. No inner borders."""

    OUTER_FIRST_ROW_THIN = auto()
    """Thin border around the table and thin separator below the first row.

    Thin lines on the outside of the table and under (the column names
    on) the first row. No other inner borders.
    """

    OUTER_FIRST_ROW_THICK = auto()
    """Thick border around the table and thick separator below the first row.

    Thick lines on the outside of the table and under (the column names
    on) the first row. No other inner borders.
    """

    OUTER_THICK_FIRST_ROW_THIN = auto()
    """Thick border around the table and thin separator below the first row.

    Thick lines on the outside of the table and a thin line under (the
    column names on) the first row. No other lines inside the table.
    """

    OUTER_FIRST_ROW_THICK_VERTICAL_THIN = auto()
    """Thick border around the table, thick separator below the first
    row, and thin vertical inner borders.

    Thick lines on the outside of the table and under (the column names
    on) the first row. Thin vertical lines between the columns. No other
    inner borders.
    """

    OUTER_FIRST_ROW_THICK_INNER_THIN = auto()
    """Thick border around the table, thick separator below the first
    row, and thin inner borders.

    Thick lines on the outside of the table and under (the column names
    on) the first row. All other inner cell borders are thin.
    """

    OUTER_THICK_INNER_THIN = auto()
    """Thick border around the table and thin inner borders."""

    ALL_THIN = auto()
    """All cell borders in the table have thin lines."""

    ALL_THICK = auto()
    """All cell borders in the table have thick lines."""
