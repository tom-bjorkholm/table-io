#! /usr/local/bin/python3
"""Tests for the tableio_ods_odfdo module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Optional

from odfdo import Cell, Document, Table
from odfdo.body import Spreadsheet
from odfdo.named_range import NamedRange
from odfdo.style import Style
from pytest import CaptureFixture

from tableio.color import Color
from tableio.tableio import Box, FileAccess
from tableio.tableio_ods_odfdo import TableIOOdsOdfdo
from tableio.value_type import Fmt, FmtDictRow, Value, ValueFmt, \
    get_checked_type

from .check_capsys import check_capsys


def _load_document(file_path: Path) -> tuple[Document, Table]:
    """Load one ODS document and return its first table."""
    document = Document(file_path)
    table = document.body.get_table(position=0)
    assert isinstance(table, Table)
    return document, table


def _cell_style_properties(
        document: Document,
        table: Table,
        row: int,
        column: int) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return table-cell and text properties for one styled cell."""
    cell = table.get_cell((column, row), clone=False)
    assert cell.style is not None
    style = document.get_style('table-cell', cell.style)
    assert style is not None
    table_props = get_checked_type(style, Style).get_properties(
        'table-cell') or {}
    text_props = get_checked_type(style, Style).get_properties('text') or {}
    return table_props, text_props


def _filtered_named_ranges(document: Document,
                           table_name: str) -> list[NamedRange]:
    """Return filter named ranges for one table."""
    spreadsheet = get_checked_type(document.body, Spreadsheet)
    return [named_range for named_range in spreadsheet.get_named_ranges()
            if named_range.usage == 'filter' and
            named_range.table_name == table_name]


def _column_width_cm(document: Document, table: Table,
                     column: int) -> Optional[float]:
    """Return one column width in centimetres from the saved style."""
    odf_column = table.get_column(column)
    if odf_column.style is None:
        return None
    style = document.get_style('table-column', odf_column.style)
    assert style is not None
    properties = get_checked_type(style, Style).get_properties(
        'table-column') or {}
    width_text = properties.get('style:column-width')
    if width_text is None:
        return None
    assert isinstance(width_text, str)
    assert width_text.endswith('cm')
    return float(width_text[:-2])


def _create_formula_document(file_path: Path,
                             cached_value: Optional[int] = None) -> None:
    """Create one ODS file with a formula cell and optional cached value."""
    document = Document('spreadsheet')
    document.body.clear()
    table = Table('Sheet1')
    document.body.append(table)
    table.set_cell((0, 0), Cell(cached_value, formula='of:=1+2'),
                   clone=False)
    table.set_value((1, 0), 'x')
    document.save(file_path)


# pylint: disable=duplicate-code
def test_ods_round_trip_sequential_list_reads(
        capsys: CaptureFixture[str]) -> None:
    """Two list sections can be written and then read back sequentially."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'sample'
        first_data: list[list[Value]] = [
            ['Flag', 'When'],
            [True, datetime(2026, 3, 23, 10, 0, 0)]
        ]
        second_data: list[list[Value]] = [['One', 'Two'], ['Three', 'Four']]
        with TableIOOdsOdfdo(file_name, FileAccess.CREATE) as table_io:
            table_io.write_heading('Report')
            table_io.write_heading('Flags')
            table_io.write_table_listdata(first_data)
            table_io.write_table_listdata(second_data)
        with TableIOOdsOdfdo(file_name, FileAccess.READ) as table_io:
            first_result = table_io.read_table_listdata()
            second_result = table_io.read_table_listdata()
        assert first_result.headings == ['Report', 'Flags']
        assert first_result.data == first_data
        assert second_result.headings == []
        assert second_result.data == second_data
    check_capsys(capsys)


def test_ods_round_trip_dictdata_in_box(
        capsys: CaptureFixture[str]) -> None:
    """Dict data can be written into and read back from a box."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'boxed'
        data: list[dict[str, Value]] = [
            {'name': 'Alice', 'active': True},
            {'name': 'Bob', 'active': None}
        ]
        box = Box(top=1, left=1, bottom=4, right=3)
        with TableIOOdsOdfdo(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_dictdata(data=data, column_order=[
                'name', 'active'
            ], box=box)
        with TableIOOdsOdfdo(file_name, FileAccess.READ) as table_io:
            result = table_io.read_table_dictdata(box=box)
        assert result.headings == []
        assert result.data == data
    check_capsys(capsys)


def test_ods_update_default_write_starts_after_last_used_row(
        capsys: CaptureFixture[str]) -> None:
    """UPDATE mode appends after the used area with a blank row separator."""
    with TemporaryDirectory() as temp_dir:
        saved_path = Path(temp_dir) / 'update.ods'
        document = Document('spreadsheet')
        document.body.clear()
        table = Table('Sheet1')
        document.body.append(table)
        table.set_value((0, 0), 'old')
        table.set_value((1, 0), 'row')
        document.save(saved_path)
        with TableIOOdsOdfdo(
                Path(temp_dir) / 'update', FileAccess.UPDATE) as table_io:
            table_io.write_table_listdata([['new', 'row']])
        document, table = _load_document(saved_path)
        assert table.get_value((0, 0)) == 'old'
        assert table.get_value((1, 0)) == 'row'
        assert table.get_value((0, 1)) is None
        assert table.get_value((1, 1)) is None
        assert table.get_value((0, 2)) == 'new'
        assert table.get_value((1, 2)) == 'row'
        _ = document
    check_capsys(capsys)


def test_ods_write_formatted_listdata_applies_formatting_and_filter(
        capsys: CaptureFixture[str]) -> None:
    """Per-cell formatting and one filtered range are written."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'formatted'
        data = [
            [ValueFmt(value='Name', fmt=Fmt(bold=True)),
             ValueFmt(value='Active', fmt=Fmt(bold=True))],
            [ValueFmt(value='Alice', fmt=Fmt(italic=True,
                                             highlight=Color.YELLOW)),
             ValueFmt(value=True, fmt=Fmt(italic=True,
                                          highlight=Color.YELLOW))]
        ]
        with TableIOOdsOdfdo(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_listdata(data, filtered_data_range=True)
        document, table = _load_document(Path(temp_dir) / 'formatted.ods')
        named_ranges = _filtered_named_ranges(document, str(table.name))
        assert len(named_ranges) == 1
        assert named_ranges[0].crange == (0, 0, 1, 1)
        _, text_props = _cell_style_properties(document, table, 0, 0)
        table_props, text_props_row = _cell_style_properties(
            document, table, 1, 0)
        assert text_props['fo:font-weight'] == 'bold'
        assert text_props_row['fo:font-style'] == 'italic'
        assert table_props['fo:background-color'] == '#ffff00'
    check_capsys(capsys)


def test_ods_write_multiple_filtered_ranges_keeps_all_ranges(
        capsys: CaptureFixture[str]) -> None:
    """Sequential filtered writes are kept as separate named ranges."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'multiple_filters'
        first_data: list[list[Value]] = [['Name', 'Active'], ['Alice', True]]
        second_data: list[list[Value]] = [
            ['Issue', 'State'],
            ['TIO-123', 'Done']
        ]
        with TableIOOdsOdfdo(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_listdata(first_data, filtered_data_range=True)
            table_io.write_table_listdata(second_data,
                                          filtered_data_range=True)
        document, table = _load_document(
            Path(temp_dir) / 'multiple_filters.ods')
        named_ranges = _filtered_named_ranges(document, str(table.name))
        assert sorted(named_range.crange for named_range in named_ranges) == [
            (0, 0, 1, 1),
            (0, 3, 1, 4)
        ]
    check_capsys(capsys)


def test_ods_table_width_is_widen_only_with_cap(
        capsys: CaptureFixture[str]) -> None:
    """Box rewrites keep an already widened column width."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'table_width_cap'
        box = Box(top=0, left=0, bottom=2, right=1)
        with TableIOOdsOdfdo(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_listdata([
                ['text'],
                ['x' * 80]
            ], box=box)
            table_io.write_table_listdata([
                ['text'],
                ['y']
            ], box=box)
        document, table = _load_document(
            Path(temp_dir) / 'table_width_cap.ods')
        assert table.get_value((0, 1)) == 'y'
        assert _column_width_cm(document, table, 0) == 12.50
    check_capsys(capsys)


def test_ods_box_write_removes_overlapping_filtered_range(
        capsys: CaptureFixture[str]) -> None:
    """Rewriting a boxed area removes stale overlapping filter metadata."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'rewrite_box'
        box = Box(top=0, left=0, bottom=3, right=2)
        with TableIOOdsOdfdo(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_listdata(
                [['Name', 'Active'], ['Alice', True]],
                filtered_data_range=True,
                box=box)
            table_io.write_table_listdata([['updated', 'value']], box=box)
        document, table = _load_document(Path(temp_dir) / 'rewrite_box.ods')
        assert _filtered_named_ranges(document, str(table.name)) == []
    check_capsys(capsys)


def test_ods_write_row_formatted_dictdata_applies_formatting(
        capsys: CaptureFixture[str]) -> None:
    """Row formatting for dict rows is copied to each written cell."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'row_formatted'
        data = [
            FmtDictRow(values={'name': 'Alice', 'active': True},
                       fmt=Fmt(bold=True, highlight=Color.GREEN)),
            FmtDictRow(values={'name': 'Bob', 'active': False},
                       fmt=Fmt(italic=True, highlight=Color.RED))
        ]
        with TableIOOdsOdfdo(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_fmtdictdata(
                data=data,
                column_order=['name', 'active'],
                filtered_data_range=True)
        document, table = _load_document(Path(temp_dir) / 'row_formatted.ods')
        named_ranges = _filtered_named_ranges(document, str(table.name))
        assert len(named_ranges) == 1
        assert named_ranges[0].crange == (0, 0, 1, 2)
        row2_table_props, row2_text_props = _cell_style_properties(
            document, table, 1, 0)
        row3_table_props, row3_text_props = _cell_style_properties(
            document, table, 2, 0)
        assert row2_text_props['fo:font-weight'] == 'bold'
        assert row2_table_props['fo:background-color'] == '#c6efce'
        assert row3_text_props['fo:font-style'] == 'italic'
        assert row3_table_props['fo:background-color'] == '#ffc7ce'
    check_capsys(capsys)


def test_ods_write_dictdata_applies_first_row_format(
        capsys: CaptureFixture[str]) -> None:
    """Dict header cells can be formatted with first_row_format."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'dict_header_fmt'
        data: list[dict[str, Value]] = [
            {'name': 'Alice', 'active': True}
        ]
        with TableIOOdsOdfdo(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_dictdata(
                data=data,
                column_order=['name', 'active'],
                first_row_format=Fmt(bold=True, highlight=Color.YELLOW))
        document, table = _load_document(
            Path(temp_dir) / 'dict_header_fmt.ods')
        assert table.get_value((0, 0)) == 'name'
        assert table.get_value((1, 0)) == 'active'
        header_table_props, header_text_props = _cell_style_properties(
            document, table, 0, 0)
        assert header_text_props['fo:font-weight'] == 'bold'
        assert header_table_props['fo:background-color'] == '#ffff00'
        assert table.get_cell((0, 1), clone=False).style is None
    check_capsys(capsys)


def test_ods_write_fmtdictdata_applies_first_row_format(
        capsys: CaptureFixture[str]) -> None:
    """Formatted dict writes keep header and row formatting separate."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'fmtdict_header_fmt'
        data = [
            FmtDictRow(values={'name': 'Alice', 'active': True},
                       fmt=Fmt(italic=True, highlight=Color.GREEN))
        ]
        with TableIOOdsOdfdo(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_fmtdictdata(
                data=data,
                column_order=['name', 'active'],
                first_row_format=Fmt(bold=True))
        document, table = _load_document(
            Path(temp_dir) / 'fmtdict_header_fmt.ods')
        _, header_text_props = _cell_style_properties(document, table, 0, 0)
        data_table_props, data_text_props = _cell_style_properties(
            document, table, 1, 0)
        assert header_text_props['fo:font-weight'] == 'bold'
        assert data_text_props['fo:font-style'] == 'italic'
        assert data_table_props['fo:background-color'] == '#c6efce'
    check_capsys(capsys)


def test_ods_read_formula_uses_cached_value(
        capsys: CaptureFixture[str]) -> None:
    """A formula cell is read as its cached value."""
    with TemporaryDirectory() as temp_dir:
        saved_path = Path(temp_dir) / 'formula.ods'
        _create_formula_document(saved_path, cached_value=3)
        with TableIOOdsOdfdo(
                Path(temp_dir) / 'formula', FileAccess.READ) as table_io:
            result = table_io.read_table_listdata()
        assert result.data == [[3, 'x']]
    check_capsys(capsys)


def test_ods_read_formula_without_cached_value_returns_none(
        capsys: CaptureFixture[str]) -> None:
    """A formula without a cached result is read as None."""
    with TemporaryDirectory() as temp_dir:
        saved_path = Path(temp_dir) / 'formula.ods'
        _create_formula_document(saved_path)
        with TableIOOdsOdfdo(
                Path(temp_dir) / 'formula', FileAccess.READ) as table_io:
            result = table_io.read_table_listdata()
        assert result.data == [[None, 'x']]
    check_capsys(capsys)
# pylint: enable=duplicate-code
