#! /usr/local/bin/python3
"""Tests for the border_helper module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest

from tableio.border_helper import BorderHelper, BorderWeight, CellBorder
from tableio.capability import Capabilities, CapabilityNotSupported, \
    SingleCapability, Strictness
from tableio.tableio_types import TableBorderStyle


def _capability(supported: bool,
                strictness: Strictness = Strictness.IGNORE) -> \
        SingleCapability:
    """Build one single capability value for tests."""
    return SingleCapability(supported=supported, strictness=strictness)


def test_border_helper_keeps_shared_first_row_separator_consistent() -> None:
    """The border below row 0 matches the border above row 1."""
    helper = BorderHelper(
        TableBorderStyle.OUTER_FIRST_ROW_THICK_INNER_THIN,
        Capabilities(can_write_borders=_capability(True, Strictness.STRICT)))
    assert helper.cell_border(0, 0, 3, 2) == CellBorder(
        top=BorderWeight.THICK, right=BorderWeight.THIN,
        bottom=BorderWeight.THICK, left=BorderWeight.THICK)
    assert helper.cell_border(1, 0, 3, 2) == CellBorder(
        top=BorderWeight.THICK, right=BorderWeight.THIN,
        bottom=BorderWeight.THIN, left=BorderWeight.THICK)


def test_border_helper_uses_thicker_outer_border_for_one_row_table() -> None:
    """A one-row table keeps the thicker outer edge on its bottom border."""
    helper = BorderHelper(
        TableBorderStyle.OUTER_THICK_FIRST_ROW_THIN,
        Capabilities(can_write_borders=_capability(True, Strictness.STRICT)))
    assert helper.cell_border(0, 0, 1, 1) == CellBorder(
        top=BorderWeight.THICK, right=BorderWeight.THICK,
        bottom=BorderWeight.THICK, left=BorderWeight.THICK)


def test_border_helper_ignores_unsupported_style_when_allowed() -> None:
    """Unsupported border styles degrade to no borders when ignorable."""
    helper = BorderHelper(
        TableBorderStyle.ALL_THICK,
        Capabilities(can_write_borders=_capability(False, Strictness.IGNORE)))
    assert helper.border_style == TableBorderStyle.NONE
    assert helper.has_borders() is False


def test_border_helper_rejects_unsupported_style_when_strict() -> None:
    """Unsupported border styles raise when the capability is strict."""
    with pytest.raises(CapabilityNotSupported,
                       match='write borders to the table'):
        BorderHelper(
            TableBorderStyle.ALL_THICK,
            Capabilities(can_write_borders=_capability(False,
                                                       Strictness.STRICT)))


@pytest.mark.parametrize(
    ('row_index', 'column_index', 'row_count', 'column_count'),
    [
        pytest.param(-1, 0, 1, 1, id='negative-row'),
        pytest.param(0, -1, 1, 1, id='negative-column'),
        pytest.param(1, 0, 1, 1, id='row-outside-table'),
        pytest.param(0, 1, 1, 1, id='column-outside-table'),
        pytest.param(0, 0, 0, 1, id='empty-rows'),
        pytest.param(0, 0, 1, 0, id='empty-columns')
    ])
def test_border_helper_rejects_invalid_cell_requests(
        row_index: int, column_index: int, row_count: int,
        column_count: int) -> None:
    """Invalid table sizes and positions are rejected."""
    helper = BorderHelper(
        TableBorderStyle.OUTER_THIN,
        Capabilities(can_write_borders=_capability(True, Strictness.STRICT)))
    with pytest.raises(ValueError):
        helper.cell_border(row_index, column_index, row_count, column_count)
