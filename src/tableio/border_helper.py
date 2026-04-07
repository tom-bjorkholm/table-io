#! /usr/bin/env python3
"""Helpers for working with normalized table borders."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from enum import IntEnum
from typing import NamedTuple, Optional

from tableio.capability import Capabilities, CapabilityNotSupported, \
    Strictness
from tableio.tableio_types import TableBorderStyle
from tableio.value_type import Fmt


class BorderWeight(IntEnum):
    """Semantic weight for one border edge."""

    NONE = 0
    THIN = 1
    THICK = 2


class CellBorder(NamedTuple):
    """Border weights for the four edges of one cell."""

    top: BorderWeight
    right: BorderWeight
    bottom: BorderWeight
    left: BorderWeight


NO_BORDERS = CellBorder(
    BorderWeight.NONE,
    BorderWeight.NONE,
    BorderWeight.NONE,
    BorderWeight.NONE)
"""The absence of borders on all four cell edges."""


class CellStyleState(NamedTuple):
    """Combined cell formatting state used by style-caching backends."""

    fmt: Fmt = Fmt()
    font_size: Optional[int] = None
    borders: CellBorder = NO_BORDERS


DEFAULT_CELL_STYLE = CellStyleState()
"""The default cell formatting state with no extra styling."""


class _BorderComponents(NamedTuple):
    """Normalized border weights for one table style."""

    outer: BorderWeight
    first_row_separator: BorderWeight
    inner_horizontal: BorderWeight
    inner_vertical: BorderWeight


def _thicker(first: BorderWeight, second: BorderWeight) -> BorderWeight:
    """Return the thicker of two border weights."""
    if first >= second:
        return first
    return second


_STYLE_COMPONENTS: dict[TableBorderStyle, _BorderComponents] = {
    TableBorderStyle.NONE: _BorderComponents(
        outer=BorderWeight.NONE,
        first_row_separator=BorderWeight.NONE,
        inner_horizontal=BorderWeight.NONE,
        inner_vertical=BorderWeight.NONE),
    TableBorderStyle.OUTER_THIN: _BorderComponents(
        outer=BorderWeight.THIN,
        first_row_separator=BorderWeight.NONE,
        inner_horizontal=BorderWeight.NONE,
        inner_vertical=BorderWeight.NONE),
    TableBorderStyle.OUTER_THICK: _BorderComponents(
        outer=BorderWeight.THICK,
        first_row_separator=BorderWeight.NONE,
        inner_horizontal=BorderWeight.NONE,
        inner_vertical=BorderWeight.NONE),
    TableBorderStyle.OUTER_FIRST_ROW_THIN: _BorderComponents(
        outer=BorderWeight.THIN,
        first_row_separator=BorderWeight.THIN,
        inner_horizontal=BorderWeight.NONE,
        inner_vertical=BorderWeight.NONE),
    TableBorderStyle.OUTER_FIRST_ROW_THICK: _BorderComponents(
        outer=BorderWeight.THICK,
        first_row_separator=BorderWeight.THICK,
        inner_horizontal=BorderWeight.NONE,
        inner_vertical=BorderWeight.NONE),
    TableBorderStyle.OUTER_THICK_FIRST_ROW_THIN: _BorderComponents(
        outer=BorderWeight.THICK,
        first_row_separator=BorderWeight.THIN,
        inner_horizontal=BorderWeight.NONE,
        inner_vertical=BorderWeight.NONE),
    TableBorderStyle.OUTER_FIRST_ROW_THICK_VERTICAL_THIN:
        _BorderComponents(
            outer=BorderWeight.THICK,
            first_row_separator=BorderWeight.THICK,
            inner_horizontal=BorderWeight.NONE,
            inner_vertical=BorderWeight.THIN),
    TableBorderStyle.OUTER_FIRST_ROW_THICK_INNER_THIN: _BorderComponents(
        outer=BorderWeight.THICK,
        first_row_separator=BorderWeight.THICK,
        inner_horizontal=BorderWeight.THIN,
        inner_vertical=BorderWeight.THIN),
    TableBorderStyle.OUTER_THICK_INNER_THIN: _BorderComponents(
        outer=BorderWeight.THICK,
        first_row_separator=BorderWeight.NONE,
        inner_horizontal=BorderWeight.THIN,
        inner_vertical=BorderWeight.THIN),
    TableBorderStyle.ALL_THIN: _BorderComponents(
        outer=BorderWeight.THIN,
        first_row_separator=BorderWeight.NONE,
        inner_horizontal=BorderWeight.THIN,
        inner_vertical=BorderWeight.THIN),
    TableBorderStyle.ALL_THICK: _BorderComponents(
        outer=BorderWeight.THICK,
        first_row_separator=BorderWeight.NONE,
        inner_horizontal=BorderWeight.THICK,
        inner_vertical=BorderWeight.THICK)
}


class BorderHelper:
    """Normalize one public table-border style for backend use."""

    def __init__(self, border_style: TableBorderStyle,
                 capabilities: Capabilities):
        """Initialize the normalized table-border helper."""
        self.border_style = self._checked_style(border_style, capabilities)
        components = _STYLE_COMPONENTS[self.border_style]
        self.outer = components.outer
        self.first_row_separator = components.first_row_separator
        self.inner_horizontal = components.inner_horizontal
        self.inner_vertical = components.inner_vertical

    @staticmethod
    def _checked_style(border_style: TableBorderStyle,
                       capabilities: Capabilities) -> TableBorderStyle:
        """Return the effective border style after capability handling."""
        if border_style == TableBorderStyle.NONE:
            return border_style
        capability = capabilities.can_write_borders
        if capability.supported:
            return border_style
        if capability.strictness == Strictness.IGNORE:
            return TableBorderStyle.NONE
        raise CapabilityNotSupported('write borders to the table')

    def has_borders(self) -> bool:
        """Return whether any border is active in this normalized style."""
        return (
            self.outer != BorderWeight.NONE or
            self.first_row_separator != BorderWeight.NONE or
            self.inner_horizontal != BorderWeight.NONE or
            self.inner_vertical != BorderWeight.NONE)

    def _horizontal_boundary(self, boundary_index: int,
                             row_count: int) -> BorderWeight:
        """Return the weight of one horizontal table boundary."""
        if boundary_index in (0, row_count):
            weight = self.outer
        else:
            weight = self.inner_horizontal
        if boundary_index == 1:
            weight = _thicker(weight, self.first_row_separator)
        return weight

    def _vertical_boundary(self, boundary_index: int,
                           column_count: int) -> BorderWeight:
        """Return the weight of one vertical table boundary."""
        if boundary_index in (0, column_count):
            return self.outer
        return self.inner_vertical

    def cell_border(self, row_index: int, column_index: int, row_count: int,
                    column_count: int) -> CellBorder:
        """Return the four border edges for one cell in a table."""
        if row_count < 1:
            raise ValueError('row_count must be at least 1.')
        if column_count < 1:
            raise ValueError('column_count must be at least 1.')
        if not 0 <= row_index < row_count:
            raise ValueError('row_index is outside the table.')
        if not 0 <= column_index < column_count:
            raise ValueError('column_index is outside the table.')
        return CellBorder(
            top=self._horizontal_boundary(row_index, row_count),
            right=self._vertical_boundary(column_index + 1, column_count),
            bottom=self._horizontal_boundary(row_index + 1, row_count),
            left=self._vertical_boundary(column_index, column_count))
