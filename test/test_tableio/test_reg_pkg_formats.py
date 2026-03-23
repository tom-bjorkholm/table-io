#! /usr/local/bin/python3
"""Tests for the reg_pkg_formats module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest
from tableio.reg_pkg_formats import register_formats_in_pkg
from tableio.tableio import TableIO
from tableio.tableio_csv import TableIOCsv
from tableio.tableio_excel_openpyxl import TableIOExcelOpenPyXL
from tableio.tableio_mformat import (
    TableIOMformatHtml, TableIOMformatMd, TableIOMformatRst,
    TableIOMformatTxt, TableIOMformatLatex, TableIOMformatDocx,
    TableIOMformatOdt, TableIOMformatPdf, TableIOMformatRtf)


def test_returns_nonempty_list() -> None:
    """The function returns a non-empty list."""
    result = register_formats_in_pkg()
    assert isinstance(result, list)
    assert len(result) > 0


def test_all_are_tableio_subclasses() -> None:
    """Every element is a subclass of TableIO."""
    for cls in register_formats_in_pkg():
        assert issubclass(cls, TableIO), \
            f'{cls.__name__} is not a subclass of TableIO'


_KNOWN_CLASSES: list[type[TableIO]] = [
    TableIOMformatHtml, TableIOMformatMd, TableIOMformatRst,
    TableIOMformatTxt, TableIOMformatLatex, TableIOMformatDocx,
    TableIOMformatOdt, TableIOMformatPdf, TableIOMformatRtf,
    TableIOCsv, TableIOExcelOpenPyXL]


@pytest.mark.parametrize(
    'cls', _KNOWN_CLASSES,
    ids=[c.__name__ for c in _KNOWN_CLASSES])
def test_known_format_present(cls: type[TableIO]) -> None:
    """Each known format class is in the returned list."""
    assert cls in register_formats_in_pkg()


def test_unique_format_implementation_pairs() -> None:
    """Each (format_name, implementation) pair is unique."""
    descs = [cls.get_description()
             for cls in register_formats_in_pkg()]
    keys = [(d.format_name, d.implementation) for d in descs]
    assert len(keys) == len(set(keys))


def test_descriptions_have_valid_fields() -> None:
    """Each descriptor has non-empty names and valid priority."""
    for cls in register_formats_in_pkg():
        desc = cls.get_description()
        assert desc.format_name, \
            f'{cls.__name__} has empty format_name'
        assert desc.implementation, \
            f'{cls.__name__} has empty implementation'
        assert isinstance(desc.priority, int)
        assert 0 <= desc.priority <= 100
