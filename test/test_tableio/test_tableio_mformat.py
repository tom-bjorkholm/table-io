#! /usr/local/bin/python3
"""Tests for the tableio_mformat module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
from pytest import CaptureFixture
from tableio.capability import CapabilityNotSupported, SingleCapability
from tableio.tableio import Box, Descriptor, FileAccess
from tableio.tableio_mformat import (
    TableIOMformatMd, TableIOMformatHtml,
    TableIOMformatTxt, TableIOMformatLatex,
    TableIOMformatRst, TableIOMformatDocx,
    TableIOMformatOdt, TableIOMformatPdf,
    TableIOMformatRtf)
from tableio.tableio_mformatbased import TableIOMformatBased
from tableio.value_type import Fmt, FmtDictRow, FmtListRow, Value

from .check_capsys import check_capsys

type _MformatCls = type[TableIOMformatBased]

_ALL_CLASSES: list[tuple[_MformatCls, str]] = [
    (TableIOMformatMd, '.md'),
    (TableIOMformatHtml, '.html'),
    (TableIOMformatTxt, '.txt'),
    (TableIOMformatLatex, '.tex'),
    (TableIOMformatRst, '.rst'),
    (TableIOMformatDocx, '.docx'),
    (TableIOMformatOdt, '.odt'),
    (TableIOMformatPdf, '.pdf'),
    (TableIOMformatRtf, '.rtf'),
]


# ── file extension tests ────────────────────────────────────────────


@pytest.mark.parametrize(
    ('cls', 'expected'),
    [pytest.param(c, e, id=e.lstrip('.')) for c, e in _ALL_CLASSES])
def test_file_name_extension(
        cls: _MformatCls, expected: str,
        capsys: CaptureFixture[str]) -> None:
    """Test file name extension for each mformat class."""
    assert cls.file_name_extension() == expected
    check_capsys(capsys)


# ── get_description tests ─────────────────────────────────────────────


_DESCRIPTION_PARAMS: list[tuple[_MformatCls, str, list[str]]] = [
    (TableIOMformatMd, 'md',
     ['file_exists_callback', 'character_encoding']),
    (TableIOMformatHtml, 'HTML',
     ['file_exists_callback', 'character_encoding',
      'title', 'css_file', 'lang']),
    (TableIOMformatTxt, 'txt',
     ['file_exists_callback', 'character_encoding',
      'line_length', 'table_max_line_length', 'table_alignment']),
    (TableIOMformatLatex, 'LaTeX',
     ['file_exists_callback', 'character_encoding',
      'document_class', 'paper_size', 'title', 'latex_preamble',
      'latex_heading_levels', 'latex_replacements']),
    (TableIOMformatRst, 'rst',
     ['file_exists_callback', 'character_encoding',
      'line_length', 'table_max_line_length', 'table_alignment']),
    (TableIOMformatDocx, 'docx',
     ['file_exists_callback', 'paper_size']),
    (TableIOMformatOdt, 'odt',
     ['file_exists_callback', 'lang', 'paper_size']),
    (TableIOMformatPdf, 'pdf',
     ['file_exists_callback', 'paper_size', 'title']),
    (TableIOMformatRtf, 'rtf',
     ['file_exists_callback', 'paper_size']),
]


@pytest.mark.parametrize(
    ('cls', 'fmt_name', 'opt_args'),
    [pytest.param(c, f, o, id=f) for c, f, o in _DESCRIPTION_PARAMS])
def test_get_description(
        cls: _MformatCls, fmt_name: str, opt_args: list[str],
        capsys: CaptureFixture[str]) -> None:
    """Test get_description returns correct Descriptor for each class."""
    desc = cls.get_description()
    assert isinstance(desc, Descriptor)
    assert desc.format_name == fmt_name
    assert desc.implementation == 'mformat'
    assert desc.capabilities == cls.get_capabilities()
    assert desc.mandatory_args == []
    assert desc.optional_args == opt_args
    assert desc.priority == 10
    check_capsys(capsys)


# ── row format capability tests ──────────────────────────────────────


@pytest.mark.parametrize(
    ('cls', 'supported'),
    [
        pytest.param(TableIOMformatMd, True, id='md'),
        pytest.param(TableIOMformatHtml, True, id='html'),
        pytest.param(TableIOMformatTxt, False, id='txt'),
        pytest.param(TableIOMformatLatex, True, id='latex'),
        pytest.param(TableIOMformatRst, False, id='rst'),
        pytest.param(TableIOMformatDocx, True, id='docx'),
        pytest.param(TableIOMformatOdt, True, id='odt'),
        pytest.param(TableIOMformatPdf, True, id='pdf'),
        pytest.param(TableIOMformatRtf, True, id='rtf'),
    ])
def test_row_format_capability(
        cls: _MformatCls, supported: bool,
        capsys: CaptureFixture[str]) -> None:
    """Test row format capability for each mformat class."""
    cap = cls.get_row_format_capability()
    assert cap == SingleCapability(supported=supported)
    check_capsys(capsys)


# ── common capabilities tests ────────────────────────────────────────


@pytest.mark.parametrize(
    ('cls', 'ext'),
    [pytest.param(c, e, id=e.lstrip('.')) for c, e in _ALL_CLASSES])
def test_common_capabilities(
        cls: _MformatCls, ext: str,
        capsys: CaptureFixture[str]) -> None:
    """Test capabilities common to all mformat-based classes."""
    _ = ext
    caps = cls.get_capabilities()
    assert caps.can_write.supported is True
    assert caps.can_read.supported is False
    assert caps.can_write_box.supported is False
    assert caps.can_read_box.supported is False
    assert caps.filtered_data_range.supported is False
    assert caps.can_fmt_value.supported is False
    assert caps.can_write_highlight.supported is False
    assert caps.multi_sheet.supported is False
    check_capsys(capsys)


# ── access mode tests ────────────────────────────────────────────────


@pytest.mark.parametrize(
    'file_access',
    [
        pytest.param(FileAccess.READ, id='read'),
        pytest.param(FileAccess.UPDATE, id='update'),
    ])
def test_rejects_non_create_access(
        file_access: FileAccess,
        capsys: CaptureFixture[str]) -> None:
    """Test that non-CREATE access raises CapabilityNotSupported."""
    with TemporaryDirectory() as td:
        (Path(td) / 'test.md').write_text('', encoding='utf-8')
        with pytest.raises(CapabilityNotSupported):
            TableIOMformatMd(
                Path(td) / 'test', file_access, None)
    check_capsys(capsys)


# ── reading not supported ────────────────────────────────────────────


def test_reading_not_supported(
        capsys: CaptureFixture[str]) -> None:
    """Test that reading raises CapabilityNotSupported."""
    with TemporaryDirectory() as td:
        path = Path(td) / 'test'
        with TableIOMformatMd(
                path, FileAccess.CREATE, None) as w:
            w.write_table_listdata([['a', 'b'], ['c', 'd']])
            with pytest.raises(CapabilityNotSupported):
                w.read_table_listdata()
            with pytest.raises(CapabilityNotSupported):
                w.read_table_dictdata()
    check_capsys(capsys)


# ── box not supported ────────────────────────────────────────────────


def test_box_not_supported_for_listdata(
        capsys: CaptureFixture[str]) -> None:
    """Test that box is rejected for list data writes."""
    data = [
        FmtListRow(values=['a', 'b'], fmt=Fmt()),
        FmtListRow(values=['c', 'd'], fmt=Fmt())
    ]
    with TemporaryDirectory() as td:
        with TableIOMformatMd(
                Path(td) / 'test', FileAccess.CREATE,
                None) as w:
            with pytest.raises(CapabilityNotSupported):
                w.write_table_fmtlistdata(
                    data, box=Box(0, 0, 5, 5))
    check_capsys(capsys)


def test_box_not_supported_for_fmtdictdata(
        capsys: CaptureFixture[str]) -> None:
    """Test that box is rejected for formatted dict data writes."""
    data = [
        FmtDictRow(
            values={'a': '1', 'b': '2'}, fmt=Fmt())
    ]
    with TemporaryDirectory() as td:
        with TableIOMformatMd(
                Path(td) / 'test', FileAccess.CREATE,
                None) as w:
            with pytest.raises(CapabilityNotSupported):
                w.write_table_fmtdictdata(
                    data, ['a', 'b'],
                    box=Box(0, 0, 5, 5))
    check_capsys(capsys)


# ── context manager test ─────────────────────────────────────────────


def test_context_manager_opens_and_closes(
        capsys: CaptureFixture[str]) -> None:
    """Test that the context manager opens and closes the file."""
    with TemporaryDirectory() as td:
        obj = TableIOMformatMd(
            Path(td) / 'test', FileAccess.CREATE, None)
        assert not obj.is_open
        with obj:
            assert obj.is_open
        assert not obj.is_open
    check_capsys(capsys)


# ── file_exists_callback test ────────────────────────────────────────


def test_file_exists_callback_is_called(
        capsys: CaptureFixture[str]) -> None:
    """Test file_exists_callback is called for existing files."""
    called: list[str] = []

    def callback(name: str) -> None:
        called.append(name)

    with TemporaryDirectory() as td:
        file_path = Path(td) / 'test.md'
        file_path.write_text('', encoding='utf-8')
        with TableIOMformatMd(
                Path(td) / 'test',
                FileAccess.CREATE, callback) as w:
            w.write_table_listdata(
                [['a', 'b'], ['c', 'd']])
        assert len(called) == 1
    check_capsys(capsys)


# ── Markdown content tests ───────────────────────────────────────────


def test_md_write_heading_and_listdata(
        capsys: CaptureFixture[str]) -> None:
    """Test Markdown output with heading and plain list data."""
    data: list[list[Value]] = [
        ['Name', 'Age'],
        ['Alice', '30']
    ]
    with TemporaryDirectory() as td:
        path = Path(td) / 'test'
        with TableIOMformatMd(
                path, FileAccess.CREATE, None) as w:
            w.write_heading('Report')
            w.write_table_listdata(data)
        content = (Path(td) / 'test.md').read_text(
            encoding='utf-8')
        assert '# Report' in content
        assert '| Name' in content
        assert '| Alice' in content
        assert '|' in content
    check_capsys(capsys)


def test_md_write_fmtlistdata_bold(
        capsys: CaptureFixture[str]) -> None:
    """Test Markdown output with bold formatted list data."""
    data = [
        FmtListRow(values=['Name', 'Age'],
                   fmt=Fmt(bold=True)),
        FmtListRow(values=['Alice', '30'], fmt=Fmt())
    ]
    with TemporaryDirectory() as td:
        path = Path(td) / 'test'
        with TableIOMformatMd(
                path, FileAccess.CREATE, None) as w:
            w.write_table_fmtlistdata(data)
        content = (Path(td) / 'test.md').read_text(
            encoding='utf-8')
        assert '**Name**' in content
        assert '**Age**' in content
        assert 'Alice' in content
    check_capsys(capsys)


def test_md_write_dictdata(
        capsys: CaptureFixture[str]) -> None:
    """Test Markdown output with plain dict data."""
    data: list[dict[str, Value]] = [
        {'name': 'Alice', 'age': '30'},
        {'name': 'Bob', 'age': '25'}
    ]
    with TemporaryDirectory() as td:
        path = Path(td) / 'test'
        with TableIOMformatMd(
                path, FileAccess.CREATE, None) as w:
            w.write_table_dictdata(data, ['name', 'age'])
        content = (Path(td) / 'test.md').read_text(
            encoding='utf-8')
        assert '| name' in content
        assert 'Alice' in content
        assert 'Bob' in content
    check_capsys(capsys)


def test_md_write_dictdata_applies_first_row_format(
        capsys: CaptureFixture[str]) -> None:
    """Markdown dict writes apply first_row_format to column names."""
    data: list[dict[str, Value]] = [
        {'name': 'Alice', 'age': '30'}
    ]
    with TemporaryDirectory() as td:
        path = Path(td) / 'test'
        with TableIOMformatMd(
                path, FileAccess.CREATE, None) as w:
            w.write_table_dictdata(
                data, ['name', 'age'],
                first_row_format=Fmt(bold=True))
        content = (Path(td) / 'test.md').read_text(
            encoding='utf-8')
        assert '**name**' in content
        assert '**age**' in content
        assert 'Alice' in content
    check_capsys(capsys)


def test_md_write_fmtdictdata(
        capsys: CaptureFixture[str]) -> None:
    """Test Markdown output with formatted dict data."""
    data = [
        FmtDictRow(
            values={'name': 'Alice', 'age': '30'},
            fmt=Fmt(bold=True)),
        FmtDictRow(
            values={'name': 'Bob', 'age': '25'},
            fmt=Fmt())
    ]
    with TemporaryDirectory() as td:
        path = Path(td) / 'test'
        with TableIOMformatMd(
                path, FileAccess.CREATE, None) as w:
            w.write_table_fmtdictdata(
                data, ['name', 'age'])
        content = (Path(td) / 'test.md').read_text(
            encoding='utf-8')
        assert '| name' in content
        assert '**Alice**' in content
        assert 'Bob' in content
    check_capsys(capsys)


def test_md_write_multiple_tables_with_headings(
        capsys: CaptureFixture[str]) -> None:
    """Test Markdown output with multiple tables and headings."""
    t1: list[list[Value]] = [['a', 'b'], ['1', '2']]
    t2: list[list[Value]] = [['c', 'd'], ['3', '4']]
    with TemporaryDirectory() as td:
        path = Path(td) / 'test'
        with TableIOMformatMd(
                path, FileAccess.CREATE, None) as w:
            w.write_heading('First')
            w.write_table_listdata(t1)
            w.write_heading('Second')
            w.write_table_listdata(t2)
        content = (Path(td) / 'test.md').read_text(
            encoding='utf-8')
        assert '# First' in content
        assert '## Second' in content
        assert '| a' in content
        assert '| c' in content
    check_capsys(capsys)


def test_md_write_none_values(
        capsys: CaptureFixture[str]) -> None:
    """Test Markdown output with None values."""
    data: list[list[Value]] = [['a', 'b'], [None, '2']]
    with TemporaryDirectory() as td:
        path = Path(td) / 'test'
        with TableIOMformatMd(
                path, FileAccess.CREATE, None) as w:
            w.write_table_listdata(data)
        content = (Path(td) / 'test.md').read_text(
            encoding='utf-8')
        assert '| a' in content
        assert '| 2' in content or '2' in content
    check_capsys(capsys)


# ── non-empty output for all other formats ───────────────────────────


_NON_MD_TEXT_CLASSES: list[tuple[_MformatCls, str]] = [
    (TableIOMformatHtml, '.html'),
    (TableIOMformatTxt, '.txt'),
    (TableIOMformatLatex, '.tex'),
    (TableIOMformatRst, '.rst'),
]

_BINARY_CLASSES: list[tuple[_MformatCls, str]] = [
    (TableIOMformatDocx, '.docx'),
    (TableIOMformatOdt, '.odt'),
    (TableIOMformatPdf, '.pdf'),
    (TableIOMformatRtf, '.rtf'),
]


@pytest.mark.parametrize(
    ('cls', 'ext'),
    [pytest.param(c, e, id=e.lstrip('.'))
     for c, e in _NON_MD_TEXT_CLASSES])
def test_text_format_creates_nonempty_file(
        cls: _MformatCls, ext: str,
        capsys: CaptureFixture[str]) -> None:
    """Test that text format writers create non-empty files."""
    data: list[list[Value]] = [
        ['Name', 'Age'], ['Alice', '30']]
    with TemporaryDirectory() as td:
        path = Path(td) / 'test'
        with cls(path, FileAccess.CREATE, None) as w:
            w.write_heading('Report')
            w.write_table_listdata(data)
        file_path = Path(td) / f'test{ext}'
        assert file_path.exists()
        assert file_path.stat().st_size > 0
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('cls', 'ext'),
    [pytest.param(c, e, id=e.lstrip('.'))
     for c, e in _BINARY_CLASSES])
def test_binary_format_creates_nonempty_file(
        cls: _MformatCls, ext: str,
        capsys: CaptureFixture[str]) -> None:
    """Test that binary format writers create non-empty files."""
    data: list[list[Value]] = [
        ['Name', 'Age'], ['Alice', '30']]
    with TemporaryDirectory() as td:
        path = Path(td) / 'test'
        with cls(path, FileAccess.CREATE, None) as w:
            w.write_heading('Report')
            w.write_table_listdata(data)
        file_path = Path(td) / f'test{ext}'
        assert file_path.exists()
        assert file_path.stat().st_size > 0
    check_capsys(capsys)


# ── dictdata for all formats ─────────────────────────────────────────


@pytest.mark.parametrize(
    ('cls', 'ext'),
    [pytest.param(c, e, id=e.lstrip('.'))
     for c, e in _ALL_CLASSES])
def test_dictdata_creates_nonempty_file(
        cls: _MformatCls, ext: str,
        capsys: CaptureFixture[str]) -> None:
    """Test that writing dict data creates non-empty files."""
    data: list[dict[str, Value]] = [
        {'name': 'Alice', 'age': '30'}]
    with TemporaryDirectory() as td:
        path = Path(td) / 'test'
        with cls(path, FileAccess.CREATE, None) as w:
            w.write_table_dictdata(data, ['name', 'age'])
        file_path = Path(td) / f'test{ext}'
        assert file_path.exists()
        assert file_path.stat().st_size > 0
    check_capsys(capsys)


# ── fmtdictdata for all formats ──────────────────────────────────────


@pytest.mark.parametrize(
    ('cls', 'ext'),
    [pytest.param(c, e, id=e.lstrip('.'))
     for c, e in _ALL_CLASSES])
def test_fmtdictdata_creates_nonempty_file(
        cls: _MformatCls, ext: str,
        capsys: CaptureFixture[str]) -> None:
    """Test that writing formatted dict data creates non-empty files."""
    data = [
        FmtDictRow(
            values={'name': 'Alice', 'age': '30'},
            fmt=Fmt(bold=True)),
        FmtDictRow(
            values={'name': 'Bob', 'age': '25'},
            fmt=Fmt())
    ]
    with TemporaryDirectory() as td:
        path = Path(td) / 'test'
        with cls(path, FileAccess.CREATE, None) as w:
            w.write_table_fmtdictdata(
                data, ['name', 'age'])
        file_path = Path(td) / f'test{ext}'
        assert file_path.exists()
        assert file_path.stat().st_size > 0
    check_capsys(capsys)


# ── fmtlistdata for all formats ──────────────────────────────────────


@pytest.mark.parametrize(
    ('cls', 'ext'),
    [pytest.param(c, e, id=e.lstrip('.'))
     for c, e in _ALL_CLASSES])
def test_fmtlistdata_creates_nonempty_file(
        cls: _MformatCls, ext: str,
        capsys: CaptureFixture[str]) -> None:
    """Test that writing formatted list data creates non-empty files."""
    data = [
        FmtListRow(values=['Name', 'Age'],
                   fmt=Fmt(bold=True)),
        FmtListRow(values=['Alice', '30'], fmt=Fmt())
    ]
    with TemporaryDirectory() as td:
        path = Path(td) / 'test'
        with cls(path, FileAccess.CREATE, None) as w:
            w.write_table_fmtlistdata(data)
        file_path = Path(td) / f'test{ext}'
        assert file_path.exists()
        assert file_path.stat().st_size > 0
    check_capsys(capsys)
