#! /usr/local/bin/python3
"""Curated top-level public API for the tableio package."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from tableio.capability import CAP_IGNORABLE, CAP_NEEDED, CAP_NOT_USED, \
    Capabilities
from tableio.color import Color
from tableio.factory import create_tableio, filter_args_tableio, \
    list_implementations_tableio, list_registered_tableio
from tableio.optional_args import CsvDialect, OptionalArgs, OptionalArgsDict
from tableio.tableio import TableIO
from tableio.tableio_types import TableBorderStyle, Box, FileAccess, Position
from tableio.value_type import CellT, DictData, DictDataMap, Fmt, \
    FmtDictData, FmtDictRow, FmtListData, FmtListRow, ListData, \
    ListDataSeq, ReadResult, Value, ValueFmt

__all__ = ['create_tableio',
           'TableIO',
           'FileAccess',
           'Box',
           'TableBorderStyle',
           'Position',
           'OptionalArgs',
           'OptionalArgsDict',
           'Value',
           'ListData',
           'ListDataSeq',
           'DictData',
           'DictDataMap',
           'ReadResult',
           'Fmt',
           'ValueFmt',
           'FmtListRow',
           'FmtDictRow',
           'FmtListData',
           'FmtDictData',
           'CellT',
           'Color',
           'Capabilities',
           'CAP_NEEDED',
           'CAP_NOT_USED',
           'CAP_IGNORABLE',
           'filter_args_tableio',
           'list_registered_tableio',
           'list_implementations_tableio',
           'CsvDialect']
