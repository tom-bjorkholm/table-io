#! /usr/bin/env python3
"""Tests that close() is idempotent for all built-in TableIO classes."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from pytest import CaptureFixture

from tableio.tableio import FileAccess, TableIO
from tableio.tableio_csv import TableIOCsv
from tableio.tableio_excel_openpyxl import TableIOExcelOpenPyXL
from tableio.tableio_excel_pylightxl import TableIOExcelPylightxl
from tableio.tableio_excel_xlsxwriter import TableIOExcelXlsxWriter
from tableio.tableio_mformat import TableIOMformatDocx, TableIOMformatHtml, \
    TableIOMformatLatex, TableIOMformatMd, TableIOMformatOdt, \
    TableIOMformatPdf, TableIOMformatRst, TableIOMformatRtf, \
    TableIOMformatTxt
from tableio.tableio_ods_odfdo import TableIOOdsOdfdo
from tableio.value_type import Value

from .check_capsys import check_capsys


_CLASSES: list[type[TableIO]] = [
    TableIOCsv, TableIOExcelOpenPyXL, TableIOExcelPylightxl,
    TableIOExcelXlsxWriter, TableIOOdsOdfdo, TableIOMformatDocx,
    TableIOMformatHtml, TableIOMformatLatex, TableIOMformatMd,
    TableIOMformatOdt, TableIOMformatPdf, TableIOMformatRst,
    TableIOMformatRtf, TableIOMformatTxt]
_DATA: list[list[Value]] = [['a', 'b'], ['c', 'd']]


def _readable_classes() -> list[type[TableIO]]:
    """Return the built-in classes that support reading."""
    return [cls for cls in _CLASSES
            if cls.get_capabilities().can_read.supported]


def _updatable_classes() -> list[type[TableIO]]:
    """Return the built-in classes that support reading and writing."""
    return [cls for cls in _readable_classes()
            if cls.get_capabilities().can_write.supported]


def _create_file(tableio_class: type[TableIO], file_name: Path) -> Path:
    """Create one file with a small table and return its full path."""
    with tableio_class(file_name, FileAccess.CREATE) as table_io:
        table_io.write_table_listdata(_DATA)
    return Path(table_io.file_name)


@pytest.mark.parametrize('tableio_class', _CLASSES,
                         ids=lambda cls: cls.__name__)
def test_create_close_twice(tableio_class: type[TableIO],
                            capsys: CaptureFixture[str]) -> None:
    """A second close() after CREATE does nothing and keeps the file."""
    with TemporaryDirectory() as temp_dir:
        with tableio_class(Path(temp_dir) / 'twice',
                           FileAccess.CREATE) as table_io:
            table_io.write_table_listdata(_DATA)
            table_io.close()
        written = Path(table_io.file_name).read_bytes()
        table_io.close()
        assert Path(table_io.file_name).read_bytes() == written
    check_capsys(capsys)


@pytest.mark.parametrize('tableio_class', _readable_classes(),
                         ids=lambda cls: cls.__name__)
def test_read_close_twice(tableio_class: type[TableIO],
                          capsys: CaptureFixture[str]) -> None:
    """A second close() after READ does nothing."""
    with TemporaryDirectory() as temp_dir:
        file_path = _create_file(tableio_class, Path(temp_dir) / 'read')
        with tableio_class(file_path, FileAccess.READ) as table_io:
            assert table_io.read_table_listdata().data == _DATA
            table_io.close()
        table_io.close()
    check_capsys(capsys)


@pytest.mark.parametrize('tableio_class', _updatable_classes(),
                         ids=lambda cls: cls.__name__)
def test_update_close_twice(tableio_class: type[TableIO],
                            capsys: CaptureFixture[str]) -> None:
    """A second close() after UPDATE does nothing and keeps the update."""
    with TemporaryDirectory() as temp_dir:
        file_path = _create_file(tableio_class, Path(temp_dir) / 'update')
        with tableio_class(file_path, FileAccess.UPDATE) as table_io:
            table_io.write_table_listdata([['e', 'f'], ['g', 'h']])
            table_io.close()
        table_io.close()
        with tableio_class(file_path, FileAccess.READ) as table_io:
            assert table_io.read_table_listdata().data == _DATA
            assert table_io.read_table_listdata().data == \
                [['e', 'f'], ['g', 'h']]
    check_capsys(capsys)


@pytest.mark.parametrize('tableio_class', _CLASSES,
                         ids=lambda cls: cls.__name__)
def test_close_hook_unopened(tableio_class: type[TableIO],
                             capsys: CaptureFixture[str]) -> None:
    """The _close() hook does nothing for an instance never opened."""
    with TemporaryDirectory() as temp_dir:
        table_io = tableio_class(Path(temp_dir) / 'never', FileAccess.CREATE)
        table_io._close()  # pylint: disable=protected-access
        assert not Path(table_io.file_name).exists()
    check_capsys(capsys)
