#! /usr/local/bin/python3
"""Tests for the tableio_csv module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import csv
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from pytest import CaptureFixture

from tableio.capability import CapabilityNotSupported
from tableio.optional_args import CsvDialect
from tableio.tableio import Box, FileAccess
from tableio.tableio_csv import (
    CsvDefinitions, TableIOCsv,
    _get_csv_dialect, _get_csv_dialect_type, _is_heading_line,
    _validate_quoting
)
from tableio.value_type import Fmt, FmtDictRow, FmtListRow, Value

from .check_capsys import check_capsys


# ── module-level helper function tests ───────────────────────────────


def test_get_csv_dialect_type_unix(
        capsys: CaptureFixture[str]) -> None:
    """Test that UNIX dialect enum maps to csv.unix_dialect."""
    assert _get_csv_dialect_type(CsvDialect.UNIX) is csv.unix_dialect
    check_capsys(capsys)


def test_get_csv_dialect_type_excel(
        capsys: CaptureFixture[str]) -> None:
    """Test that EXCEL dialect enum maps to csv.excel."""
    assert _get_csv_dialect_type(CsvDialect.EXCEL) is csv.excel
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('quoting_str', 'expected'),
    [
        pytest.param('all', csv.QUOTE_ALL, id='all'),
        pytest.param('minimal', csv.QUOTE_MINIMAL, id='minimal'),
        pytest.param(
            'nonnumeric', csv.QUOTE_NONNUMERIC, id='nonnumeric'
        ),
        pytest.param('none', csv.QUOTE_NONE, id='none'),
        pytest.param('strings', csv.QUOTE_STRINGS, id='strings'),
        pytest.param('notnull', csv.QUOTE_NOTNULL, id='notnull'),
        pytest.param('ALL', csv.QUOTE_ALL, id='uppercase'),
        pytest.param(
            'Minimal', csv.QUOTE_MINIMAL, id='mixed-case'
        )
    ]
)
def test_validate_quoting_valid_values(
        quoting_str: str, expected: int,
        capsys: CaptureFixture[str]) -> None:
    """Test that all valid quoting strings are accepted."""
    assert _validate_quoting(quoting_str) == expected
    check_capsys(capsys)


def test_validate_quoting_rejects_unknown(
        capsys: CaptureFixture[str]) -> None:
    """Test that an unknown quoting string raises ValueError."""
    with pytest.raises(ValueError, match='Unknown quoting style'):
        _validate_quoting('bogus')
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('line', 'expected'),
    [
        pytest.param('# heading', True, id='level-1'),
        pytest.param('## heading', True, id='level-2'),
        pytest.param('### heading', True, id='level-3'),
        pytest.param('# ', True, id='empty-heading'),
        pytest.param('not a heading', False, id='plain-text'),
        pytest.param('#no-space', False, id='hash-no-space'),
        pytest.param('', False, id='empty-line'),
        pytest.param('#', False, id='hash-only')
    ]
)
def test_is_heading_line(
        line: str, expected: bool,
        capsys: CaptureFixture[str]) -> None:
    """Test heading line detection."""
    assert _is_heading_line(line) == expected
    check_capsys(capsys)


def test_get_csv_dialect_applies_overrides(
        capsys: CaptureFixture[str]) -> None:
    """Test that CSV definitions override dialect defaults."""
    defs = CsvDefinitions(
        type=CsvDialect.UNIX, delimiter=';', quoting='all',
        quotechar="'", lineterminator='\r\n', escapechar='\\')
    dialect = _get_csv_dialect(defs)
    assert dialect.delimiter == ';'
    assert dialect.quoting == csv.QUOTE_ALL
    assert dialect.quotechar == "'"
    assert dialect.lineterminator == '\r\n'
    assert dialect.escapechar == '\\'
    check_capsys(capsys)


def test_get_csv_dialect_keeps_defaults_when_none(
        capsys: CaptureFixture[str]) -> None:
    """Test that None values leave dialect defaults unchanged."""
    defs = CsvDefinitions(
        type=CsvDialect.UNIX, delimiter=None, quoting=None,
        quotechar=None, lineterminator=None, escapechar=None)
    dialect = _get_csv_dialect(defs)
    assert dialect.delimiter == ','
    assert dialect.quoting == csv.QUOTE_ALL
    assert dialect.quotechar == '"'
    assert dialect.lineterminator == '\n'
    check_capsys(capsys)


# ── TableIOCsv class-level tests ────────────────────────────────────


def test_csv_file_name_extension(
        capsys: CaptureFixture[str]) -> None:
    """Test that the CSV file name extension is 'csv'."""
    assert TableIOCsv.file_name_extension() == 'csv'
    check_capsys(capsys)


def test_csv_get_description(
        capsys: CaptureFixture[str]) -> None:
    """Test the descriptor returned by get_description."""
    desc = TableIOCsv.get_description()
    assert desc.format_name == 'CSV'
    assert desc.implementation == 'csv'
    assert desc.mandatory_args == []
    assert 'csv_delimiter' in desc.optional_args
    assert 'csv_quoting' in desc.optional_args
    check_capsys(capsys)


def test_csv_get_capabilities(
        capsys: CaptureFixture[str]) -> None:
    """Test the capabilities returned by get_capabilities."""
    caps = TableIOCsv.get_capabilities()
    assert caps.can_write.supported is True
    assert caps.can_read.supported is True
    assert caps.can_fmt_row.supported is False
    assert caps.can_write_box.supported is False
    assert caps.can_read_box.supported is False
    check_capsys(capsys)


def test_csv_init_creates_file_with_csv_extension(
        capsys: CaptureFixture[str]) -> None:
    """Test that init appends .csv to the file name."""
    with TemporaryDirectory() as td:
        obj = TableIOCsv(Path(td) / 'sample', FileAccess.CREATE)
        assert obj.file_name == str(Path(td) / 'sample.csv')
    check_capsys(capsys)


def test_csv_context_manager_opens_and_closes(
        capsys: CaptureFixture[str]) -> None:
    """Test that the context manager opens and closes the file."""
    with TemporaryDirectory() as td:
        obj = TableIOCsv(Path(td) / 'sample', FileAccess.CREATE)
        with obj:
            assert obj.file is not None
        assert obj.file is None
    check_capsys(capsys)


# ── write tests ──────────────────────────────────────────────────────


def test_csv_write_heading(
        capsys: CaptureFixture[str]) -> None:
    """Test writing a heading to a CSV file."""
    with TemporaryDirectory() as td:
        path = Path(td) / 'sample'
        with TableIOCsv(path, FileAccess.CREATE) as w:
            w.write_heading('Report', level=1)
        content = (Path(td) / 'sample.csv').read_text(
            encoding='utf-8')
        assert content.startswith('# Report\n')
    check_capsys(capsys)


def test_csv_write_table_listdata(
        capsys: CaptureFixture[str]) -> None:
    """Test writing list data to a CSV file."""
    with TemporaryDirectory() as td:
        path = Path(td) / 'data'
        data: list[list[Value]] = [
            ['Name', 'Age'],
            ['Alice', '30']
        ]
        with TableIOCsv(path, FileAccess.CREATE) as w:
            w.write_table_listdata(data)
        content = (Path(td) / 'data.csv').read_text(
            encoding='utf-8')
        assert '"Name","Age"\n' in content
        assert '"Alice","30"\n' in content
    check_capsys(capsys)


def test_csv_write_table_listdata_excel_dialect(
        capsys: CaptureFixture[str]) -> None:
    """Test writing list data with the Excel dialect."""
    with TemporaryDirectory() as td:
        path = Path(td) / 'data'
        data: list[list[Value]] = [['a', 'b'], ['c', 'd']]
        with TableIOCsv(path, FileAccess.CREATE,
                        csv_dialect=CsvDialect.EXCEL) as w:
            w.write_table_listdata(data)
        raw = (Path(td) / 'data.csv').read_bytes()
        assert b'a,b\r\n' in raw
        assert b'c,d\r\n' in raw
    check_capsys(capsys)


def test_csv_write_table_fmtlistdata_strips_format(
        capsys: CaptureFixture[str]) -> None:
    """Test that formatted list data has its formatting stripped."""
    with TemporaryDirectory() as td:
        path = Path(td) / 'fmt'
        data = [
            FmtListRow(values=['x', 'y'], fmt=Fmt(bold=True)),
            FmtListRow(values=['1', '2'], fmt=Fmt(italic=True))
        ]
        with TableIOCsv(path, FileAccess.CREATE) as w:
            w.write_table_fmtlistdata(data)
        content = (Path(td) / 'fmt.csv').read_text(
            encoding='utf-8')
        assert '"x","y"\n' in content
        assert '"1","2"\n' in content
    check_capsys(capsys)


def test_csv_write_table_dictdata(
        capsys: CaptureFixture[str]) -> None:
    """Test writing dict data to a CSV file."""
    with TemporaryDirectory() as td:
        path = Path(td) / 'dict'
        data: list[dict[str, Value]] = [
            {'name': 'Alice', 'age': '30'},
            {'name': 'Bob', 'age': '25'}
        ]
        with TableIOCsv(path, FileAccess.CREATE) as w:
            w.write_table_dictdata(data, ['name', 'age'])
        content = (Path(td) / 'dict.csv').read_text(
            encoding='utf-8')
        assert '"name","age"\n' in content
        assert '"Alice","30"\n' in content
        assert '"Bob","25"\n' in content
    check_capsys(capsys)


def test_csv_write_table_fmtdictdata_strips_format(
        capsys: CaptureFixture[str]) -> None:
    """Test that formatted dict data has its formatting stripped."""
    with TemporaryDirectory() as td:
        path = Path(td) / 'fmtd'
        data = [
            FmtDictRow(values={'a': '1', 'b': '2'},
                       fmt=Fmt(bold=True))
        ]
        with TableIOCsv(path, FileAccess.CREATE) as w:
            w.write_table_fmtdictdata(data, ['a', 'b'])
        content = (Path(td) / 'fmtd.csv').read_text(
            encoding='utf-8')
        assert '"a","b"\n' in content
        assert '"1","2"\n' in content
    check_capsys(capsys)


def test_csv_write_none_values(
        capsys: CaptureFixture[str]) -> None:
    """Test that None values are written as empty fields."""
    with TemporaryDirectory() as td:
        path = Path(td) / 'nones'
        data: list[list[Value]] = [['a', None], [None, 'b']]
        with TableIOCsv(path, FileAccess.CREATE) as w:
            w.write_table_listdata(data)
        content = (Path(td) / 'nones.csv').read_text(
            encoding='utf-8')
        assert '"a",""\n' in content
        assert '"","b"\n' in content
    check_capsys(capsys)


def test_csv_write_numeric_values(
        capsys: CaptureFixture[str]) -> None:
    """Test that numeric values are converted to strings."""
    with TemporaryDirectory() as td:
        path = Path(td) / 'nums'
        data: list[list[Value]] = [['val', 'num'], [42, 3.14]]
        with TableIOCsv(path, FileAccess.CREATE) as w:
            w.write_table_listdata(data)
        content = (Path(td) / 'nums.csv').read_text(
            encoding='utf-8')
        assert '"42"' in content
        assert '"3.14"' in content
    check_capsys(capsys)


def test_csv_write_with_custom_delimiter(
        capsys: CaptureFixture[str]) -> None:
    """Test writing with a custom delimiter."""
    with TemporaryDirectory() as td:
        path = Path(td) / 'semi'
        data: list[list[Value]] = [['a', 'b'], ['c', 'd']]
        with TableIOCsv(path, FileAccess.CREATE,
                        csv_dialect=CsvDialect.EXCEL,
                        csv_delimiter=';') as w:
            w.write_table_listdata(data)
        content = (Path(td) / 'semi.csv').read_text(
            encoding='utf-8')
        assert 'a;b' in content
        assert 'c;d' in content
    check_capsys(capsys)


def test_csv_write_table_listdata_rejects_box(
        capsys: CaptureFixture[str]) -> None:
    """Test that writing list data with a box raises an error."""
    with TemporaryDirectory() as td:
        path = Path(td) / 'boxed'
        data: list[list[Value]] = [['a', 'b']]
        with TableIOCsv(path, FileAccess.CREATE) as w:
            with pytest.raises(CapabilityNotSupported):
                w.write_table_listdata(data, box=Box(0, 0, 2, 2))
    check_capsys(capsys)


def test_csv_write_table_dictdata_rejects_box(
        capsys: CaptureFixture[str]) -> None:
    """Test that writing dict data with a box raises an error."""
    with TemporaryDirectory() as td:
        path = Path(td) / 'boxed'
        data: list[dict[str, Value]] = [{'a': '1', 'b': '2'}]
        with TableIOCsv(path, FileAccess.CREATE) as w:
            with pytest.raises(CapabilityNotSupported):
                w.write_table_dictdata(
                    data, ['a', 'b'], box=Box(0, 0, 2, 2))
    check_capsys(capsys)


# ── read tests ───────────────────────────────────────────────────────


def test_csv_read_table_listdata(
        capsys: CaptureFixture[str]) -> None:
    """Test reading list data from a CSV file."""
    with TemporaryDirectory() as td:
        csv_path = Path(td) / 'data.csv'
        csv_path.write_text('"a","b"\n"c","d"\n',
                            encoding='utf-8')
        with TableIOCsv(Path(td) / 'data',
                        FileAccess.READ) as r:
            result = r.read_table_listdata()
        assert result.data == [['a', 'b'], ['c', 'd']]
        assert result.headings == []
    check_capsys(capsys)


def test_csv_read_table_listdata_with_headings(
        capsys: CaptureFixture[str]) -> None:
    """Test reading list data preceded by headings."""
    with TemporaryDirectory() as td:
        csv_path = Path(td) / 'h.csv'
        csv_path.write_text(
            '# Title\n\n"x","y"\n"1","2"\n',
            encoding='utf-8')
        with TableIOCsv(Path(td) / 'h', FileAccess.READ) as r:
            result = r.read_table_listdata()
        assert result.headings == ['Title']
        assert result.data == [['x', 'y'], ['1', '2']]
    check_capsys(capsys)


def test_csv_read_table_listdata_multiple_heading_levels(
        capsys: CaptureFixture[str]) -> None:
    """Test reading headings at different levels."""
    with TemporaryDirectory() as td:
        csv_path = Path(td) / 'm.csv'
        csv_path.write_text(
            '# Main\n## Sub\n\n"a","b"\n',
            encoding='utf-8')
        with TableIOCsv(Path(td) / 'm', FileAccess.READ) as r:
            result = r.read_table_listdata()
        assert result.headings == ['Main', 'Sub']
        assert result.data == [['a', 'b']]
    check_capsys(capsys)


def test_csv_read_table_dictdata(
        capsys: CaptureFixture[str]) -> None:
    """Test reading dict data from a CSV file."""
    with TemporaryDirectory() as td:
        csv_path = Path(td) / 'dd.csv'
        csv_path.write_text(
            '"name","age"\n"Alice","30"\n"Bob","25"\n',
            encoding='utf-8')
        with TableIOCsv(Path(td) / 'dd', FileAccess.READ) as r:
            result = r.read_table_dictdata()
        assert result.data == [
            {'name': 'Alice', 'age': '30'},
            {'name': 'Bob', 'age': '25'}
        ]
        assert result.headings == []
    check_capsys(capsys)


def test_csv_read_table_dictdata_with_headings(
        capsys: CaptureFixture[str]) -> None:
    """Test reading dict data preceded by headings."""
    with TemporaryDirectory() as td:
        csv_path = Path(td) / 'dh.csv'
        csv_path.write_text(
            '## Info\n\n"k","v"\n"a","1"\n',
            encoding='utf-8')
        with TableIOCsv(Path(td) / 'dh', FileAccess.READ) as r:
            result = r.read_table_dictdata()
        assert result.headings == ['Info']
        assert result.data == [{'k': 'a', 'v': '1'}]
    check_capsys(capsys)


def test_csv_read_table_dictdata_header_only(
        capsys: CaptureFixture[str]) -> None:
    """Test reading dict data when only the header row exists."""
    with TemporaryDirectory() as td:
        csv_path = Path(td) / 'ho.csv'
        csv_path.write_text('"col1","col2"\n',
                            encoding='utf-8')
        with TableIOCsv(Path(td) / 'ho', FileAccess.READ) as r:
            result = r.read_table_dictdata()
        assert result.data == []
    check_capsys(capsys)


def test_csv_read_empty_file(
        capsys: CaptureFixture[str]) -> None:
    """Test reading from an empty file returns empty data."""
    with TemporaryDirectory() as td:
        csv_path = Path(td) / 'empty.csv'
        csv_path.write_text('', encoding='utf-8')
        with TableIOCsv(Path(td) / 'empty',
                        FileAccess.READ) as r:
            result = r.read_table_listdata()
        assert result.data == []
        assert result.headings == []
    check_capsys(capsys)


def test_csv_read_table_listdata_rejects_box(
        capsys: CaptureFixture[str]) -> None:
    """Test that reading list data with a box raises an error."""
    with TemporaryDirectory() as td:
        csv_path = Path(td) / 'rb.csv'
        csv_path.write_text('"a","b"\n', encoding='utf-8')
        with TableIOCsv(Path(td) / 'rb', FileAccess.READ) as r:
            with pytest.raises(CapabilityNotSupported):
                r.read_table_listdata(box=Box(0, 0, 1, 1))
    check_capsys(capsys)


def test_csv_read_table_dictdata_rejects_box(
        capsys: CaptureFixture[str]) -> None:
    """Test that reading dict data with a box raises an error."""
    with TemporaryDirectory() as td:
        csv_path = Path(td) / 'rbd.csv'
        csv_path.write_text('"k","v"\n"a","1"\n',
                            encoding='utf-8')
        with TableIOCsv(Path(td) / 'rbd', FileAccess.READ) as r:
            with pytest.raises(CapabilityNotSupported):
                r.read_table_dictdata(box=Box(0, 0, 1, 1))
    check_capsys(capsys)


# ── roundtrip tests ──────────────────────────────────────────────────


def test_csv_write_and_read_listdata_roundtrip(
        capsys: CaptureFixture[str]) -> None:
    """Test writing and then reading back list data."""
    with TemporaryDirectory() as td:
        path = Path(td) / 'rt'
        data: list[list[Value]] = [
            ['Name', 'Score'],
            ['Alice', '100'],
            ['Bob', '85']
        ]
        with TableIOCsv(path, FileAccess.CREATE) as w:
            w.write_table_listdata(data)
        with TableIOCsv(path, FileAccess.READ) as r:
            result = r.read_table_listdata()
        assert result.data == data
        assert result.headings == []
    check_capsys(capsys)


def test_csv_write_and_read_dictdata_roundtrip(
        capsys: CaptureFixture[str]) -> None:
    """Test writing and then reading back dict data."""
    with TemporaryDirectory() as td:
        path = Path(td) / 'rtd'
        data: list[dict[str, Value]] = [
            {'name': 'Alice', 'score': '100'},
            {'name': 'Bob', 'score': '85'}
        ]
        with TableIOCsv(path, FileAccess.CREATE) as w:
            w.write_table_dictdata(data, ['name', 'score'])
        with TableIOCsv(path, FileAccess.READ) as r:
            result = r.read_table_dictdata()
        assert result.data == data
        assert result.headings == []
    check_capsys(capsys)


def test_csv_write_headings_and_multiple_tables_then_read(
        capsys: CaptureFixture[str]) -> None:
    """Test write and readback of headings with several tables."""
    with TemporaryDirectory() as td:
        path = Path(td) / 'multi'
        list_data: list[list[Value]] = [
            ['Name', 'Age'],
            ['Alice', '30'],
            ['Bob', '25']
        ]
        dict_data: list[dict[str, Value]] = [
            {'total': '2', 'avg': '27.5'}
        ]
        with TableIOCsv(path, FileAccess.CREATE) as w:
            w.write_heading('Report')
            w.write_table_listdata(list_data)
            w.write_heading('Summary')
            w.write_table_dictdata(dict_data, ['total', 'avg'])
        with TableIOCsv(path, FileAccess.READ) as r:
            r1 = r.read_table_listdata()
            r2 = r.read_table_listdata()
        assert r1.headings == ['Report']
        assert r1.data == list_data
        assert r2.headings == ['Summary']
        assert r2.data == [
            ['total', 'avg'],
            ['2', '27.5']
        ]
    check_capsys(capsys)


def test_csv_read_multiple_tables_sequentially(
        capsys: CaptureFixture[str]) -> None:
    """Test reading several tables separated by empty lines."""
    with TemporaryDirectory() as td:
        path = Path(td) / 'seq'
        t1: list[list[Value]] = [['a', 'b'], ['1', '2']]
        t2: list[list[Value]] = [['c', 'd'], ['3', '4']]
        with TableIOCsv(path, FileAccess.CREATE) as w:
            w.write_table_listdata(t1)
            w.write_table_listdata(t2)
        with TableIOCsv(path, FileAccess.READ) as r:
            r1 = r.read_table_listdata()
            r2 = r.read_table_listdata()
        assert r1.data == t1
        assert r2.data == t2
    check_capsys(capsys)


def test_csv_heading_levels_roundtrip(
        capsys: CaptureFixture[str]) -> None:
    """Test that heading text is preserved across write and read."""
    with TemporaryDirectory() as td:
        path = Path(td) / 'lvl'
        with TableIOCsv(path, FileAccess.CREATE) as w:
            w.write_heading('Top', level=1)
            w.write_table_listdata([['a', 'b']])
            w.write_heading('Mid', level=2)
            w.write_table_listdata([['c', 'd']])
            w.write_heading('Low', level=3)
            w.write_table_listdata([['e', 'f']])
        with TableIOCsv(path, FileAccess.READ) as r:
            r1 = r.read_table_listdata()
            r2 = r.read_table_listdata()
            r3 = r.read_table_listdata()
        assert r1.headings == ['Top']
        assert r2.headings == ['Mid']
        assert r3.headings == ['Low']
    check_capsys(capsys)


def test_csv_multi_heading_multi_row_roundtrip_with_position(
        capsys: CaptureFixture[str]) -> None:
    """Test roundtrip with multiple headings between tables.

    Writes two tables each preceded by two headings, with more
    than two data rows per table. Verifies that position_row is
    correctly tracked through write and read, including empty
    separator lines.
    Expected file layout (0-based line numbers):
      0: # Main Report
      1: (empty)
      2: ## Data Section
      3: (empty)
      4: "a","b","c"
      5: "1","2","3"
      6: "4","5","6"
      7: (empty)
      8: ## Another Heading
      9: (empty)
     10: ### Details
     11: (empty)
     12: "x","y"
     13: "7","8"
     14: "9","10"
     15: "11","12"
     16: (empty)
    """
    with TemporaryDirectory() as td:
        path = Path(td) / 'pos'
        t1: list[list[Value]] = [
            ['a', 'b', 'c'],
            ['1', '2', '3'],
            ['4', '5', '6']
        ]
        t2: list[list[Value]] = [
            ['x', 'y'],
            ['7', '8'],
            ['9', '10'],
            ['11', '12']
        ]
        with TableIOCsv(path, FileAccess.CREATE) as w:
            p1 = w.write_heading('Main Report', level=1)
            p2 = w.write_heading('Data Section', level=2)
            p3 = w.write_table_listdata(t1)
            p4 = w.write_heading('Another Heading', level=2)
            p5 = w.write_heading('Details', level=3)
            p6 = w.write_table_listdata(t2)
        assert p1.row == 1
        assert p2.row == 3
        assert p3.row == 7
        assert p4.row == 9
        assert p5.row == 11
        assert p6.row == 16
        with TableIOCsv(path, FileAccess.READ) as r:
            r1 = r.read_table_listdata()
            r2 = r.read_table_listdata()
        assert r1.headings == ['Main Report', 'Data Section']
        assert r1.data == t1
        assert r1.last_read_row == 7
        assert r2.headings == ['Another Heading', 'Details']
        assert r2.data == t2
        assert r2.last_read_row == 16
    check_capsys(capsys)


# ── simultaneous objects test ────────────────────────────────────────


def test_csv_two_simultaneous_objects_different_delimiters(
        capsys: CaptureFixture[str]) -> None:
    """Test two concurrent TableIOCsv writers with different delimiters.

    Both use CsvDialect.EXCEL but with different delimiter overrides
    to verify that each object keeps its own dialect state.
    """
    with TemporaryDirectory() as td:
        semi_path = Path(td) / 'semi'
        tab_path = Path(td) / 'tab'
        semi_data: list[list[Value]] = [
            ['alpha', 'beta'],
            ['one', 'two']
        ]
        tab_data: list[list[Value]] = [
            ['gamma', 'delta'],
            ['three', 'four']
        ]
        with TableIOCsv(semi_path, FileAccess.CREATE,
                        csv_dialect=CsvDialect.EXCEL,
                        csv_delimiter=';') as semi_w:
            with TableIOCsv(tab_path, FileAccess.CREATE,
                            csv_dialect=CsvDialect.EXCEL,
                            csv_delimiter='\t') as tab_w:
                semi_w.write_table_listdata(semi_data)
                tab_w.write_table_listdata(tab_data)
        semi_content = (Path(td) / 'semi.csv').read_text(
            encoding='utf-8')
        tab_content = (Path(td) / 'tab.csv').read_text(
            encoding='utf-8')
        assert 'alpha;beta' in semi_content
        assert 'one;two' in semi_content
        assert '\t' not in semi_content
        assert 'gamma\tdelta' in tab_content
        assert 'three\tfour' in tab_content
        assert ';' not in tab_content
        with TableIOCsv(semi_path, FileAccess.READ,
                        csv_dialect=CsvDialect.EXCEL,
                        csv_delimiter=';') as semi_r:
            with TableIOCsv(tab_path, FileAccess.READ,
                            csv_dialect=CsvDialect.EXCEL,
                            csv_delimiter='\t') as tab_r:
                semi_result = semi_r.read_table_listdata()
                tab_result = tab_r.read_table_listdata()
        assert semi_result.data == semi_data
        assert tab_result.data == tab_data
    check_capsys(capsys)


# ── quoting integration test ────────────────────────────────────────


def test_csv_write_and_read_with_quoting_override(
        capsys: CaptureFixture[str]) -> None:
    """Test that a quoting override is applied during write/read."""
    with TemporaryDirectory() as td:
        path = Path(td) / 'q'
        data: list[list[Value]] = [['a', 'b'], ['c', 'd']]
        with TableIOCsv(path, FileAccess.CREATE,
                        csv_dialect=CsvDialect.EXCEL,
                        csv_quoting='all') as w:
            w.write_table_listdata(data)
        content = (Path(td) / 'q.csv').read_text(
            encoding='utf-8')
        assert '"a","b"' in content
        with TableIOCsv(path, FileAccess.READ,
                        csv_dialect=CsvDialect.EXCEL,
                        csv_quoting='all') as r:
            result = r.read_table_listdata()
        assert result.data == data
    check_capsys(capsys)


# ── edge case tests ─────────────────────────────────────────────────


def test_csv_read_skips_leading_empty_lines(
        capsys: CaptureFixture[str]) -> None:
    """Test that leading empty lines before data are skipped."""
    with TemporaryDirectory() as td:
        csv_path = Path(td) / 'lead.csv'
        csv_path.write_text(
            '\n\n\n"a","b"\n"c","d"\n',
            encoding='utf-8')
        with TableIOCsv(Path(td) / 'lead',
                        FileAccess.READ) as r:
            result = r.read_table_listdata()
        assert result.data == [['a', 'b'], ['c', 'd']]
    check_capsys(capsys)


def test_csv_read_after_all_tables_returns_empty(
        capsys: CaptureFixture[str]) -> None:
    """Test that reading past the last table returns empty data."""
    with TemporaryDirectory() as td:
        csv_path = Path(td) / 'one.csv'
        csv_path.write_text('"a","b"\n',
                            encoding='utf-8')
        with TableIOCsv(Path(td) / 'one',
                        FileAccess.READ) as r:
            r1 = r.read_table_listdata()
            r2 = r.read_table_listdata()
        assert r1.data == [['a', 'b']]
        assert r2.data == []
    check_capsys(capsys)


def test_csv_write_heading_rejects_invalid_level(
        capsys: CaptureFixture[str]) -> None:
    """Test that heading levels outside 1-3 are rejected."""
    with TemporaryDirectory() as td:
        with TableIOCsv(Path(td) / 'bad',
                        FileAccess.CREATE) as w:
            with pytest.raises(ValueError, match='range 1 to 3'):
                w.write_heading('Bad', level=0)
            with pytest.raises(ValueError, match='range 1 to 3'):
                w.write_heading('Bad', level=4)
    check_capsys(capsys)


def test_csv_write_heading_rejects_newline_in_text(
        capsys: CaptureFixture[str]) -> None:
    """Test that headings containing newlines are rejected."""
    with TemporaryDirectory() as td:
        with TableIOCsv(Path(td) / 'nl',
                        FileAccess.CREATE) as w:
            with pytest.raises(ValueError, match='newline'):
                w.write_heading('line1\nline2')
    check_capsys(capsys)


def test_csv_init_invalid_quoting_raises_at_construction(
        capsys: CaptureFixture[str]) -> None:
    """Test that an invalid quoting string raises during init."""
    with TemporaryDirectory() as td:
        with pytest.raises(ValueError, match='Unknown quoting'):
            TableIOCsv(Path(td) / 'bad', FileAccess.CREATE,
                       csv_quoting='invalid')
    check_capsys(capsys)
