#! /usr/local/bin/python3
"""Shared ImplMeta helpers for TableIO implementation-hook tests."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional

from tableio.border_helper import BorderHelper
from tableio.capability import Capabilities
from tableio.tableio import Box, TableIO
from tableio.tableio_types import TableBorderStyle
from tableio.value_type import Fmt


def make_no_border_helper() -> BorderHelper:
    """Build the default no-border helper used in tests."""
    return BorderHelper(TableBorderStyle.NONE, Capabilities())


def make_boxed_write_impl_meta(box: Box) -> TableIO.ImplMetaForWrite:
    """Build write metadata for a boxed write used in tests."""
    return TableIO.ImplMetaForWrite(filtered_data_range=False, box=box,
                                    borders=make_no_border_helper())


def make_boxed_dict_write_impl_meta(
        column_order: list[str], box: Box,
        first_row_format: Optional[Fmt] = None) -> \
        TableIO.ImplMetaForDictWrite:
    """Build dict-write metadata for a boxed write used in tests."""
    return TableIO.ImplMetaForDictWrite(
        common_impl=make_boxed_write_impl_meta(box), column_order=column_order,
        first_row_format=first_row_format)
