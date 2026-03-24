#! /usr/local/bin/python3
"""Tests for the tableio_excel_openpyxl module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from pytest import CaptureFixture

from tableio.color import Color
from tableio.tableio import Box, FileAccess
from tableio.tableio_excel_openpyxl import TableIOExcelOpenPyXL
from tableio.value_type import Fmt, FmtDictRow, Value, ValueFmt

from .check_capsys import check_capsys


_XML_NS = {
    'sheet': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
}


def _create_formula_workbook(file_path: Path,
                             cached_value: Optional[int] = None) -> None:
    """Create a workbook with one formula cell and an optional cached value."""
    workbook = Workbook()
    worksheet = workbook.active
    assert isinstance(worksheet, Worksheet)
    worksheet['A1'] = '=1+2'
    worksheet['B1'] = 'x'
    workbook.save(file_path)
    workbook.close()
    if cached_value is None:
        return
    temp_path = file_path.with_name(f'{file_path.stem}_tmp.xlsx')
    with ZipFile(file_path) as zip_file, \
            ZipFile(temp_path, 'w') as temp_zip:
        for item in zip_file.infolist():
            data = zip_file.read(item.filename)
            if item.filename == 'xl/worksheets/sheet1.xml':
                root = ET.fromstring(data)
                cell = root.find('.//sheet:c[@r="A1"]', _XML_NS)
                assert cell is not None
                value = cell.find('sheet:v', _XML_NS)
                assert value is not None
                value.text = str(cached_value)
                data = ET.tostring(root, encoding='utf-8',
                                   xml_declaration=False)
            temp_zip.writestr(item, data)
    temp_path.replace(file_path)


def test_excel_round_trip_sequential_list_reads(
        capsys: CaptureFixture[str]) -> None:
    """Two list sections can be written and then read back sequentially."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'sample'
        first_data: list[list[Value]] = [
            ['Flag', 'When'],
            [True, datetime(2026, 3, 23, 10, 0, 0)]
        ]
        second_data: list[list[Value]] = [['One', 'Two'], ['Three', 'Four']]
        with TableIOExcelOpenPyXL(file_name, FileAccess.CREATE) as table_io:
            table_io.write_heading('Report')
            table_io.write_heading('Flags')
            table_io.write_table_listdata(first_data)
            table_io.write_table_listdata(second_data)
        with TableIOExcelOpenPyXL(file_name, FileAccess.READ) as table_io:
            first_result = table_io.read_table_listdata()
            second_result = table_io.read_table_listdata()
        assert first_result.headings == ['Report', 'Flags']
        assert first_result.data == first_data
        assert second_result.headings == []
        assert second_result.data == second_data
    check_capsys(capsys)


def test_excel_round_trip_dictdata_in_box(
        capsys: CaptureFixture[str]) -> None:
    """Dict data can be written into and read back from a box."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'boxed'
        data: list[dict[str, Value]] = [
            {'name': 'Alice', 'active': True},
            {'name': 'Bob', 'active': None}
        ]
        box = Box(top=1, left=1, bottom=4, right=3)
        with TableIOExcelOpenPyXL(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_dictdata(data=data, column_order=[
                'name', 'active'
            ], box=box)
        with TableIOExcelOpenPyXL(file_name, FileAccess.READ) as table_io:
            result = table_io.read_table_dictdata(box=box)
        assert result.headings == []
        assert result.data == data
    check_capsys(capsys)


def test_excel_update_default_write_starts_after_last_used_row(
        capsys: CaptureFixture[str]) -> None:
    """UPDATE mode appends after the used area with a blank row separator."""
    with TemporaryDirectory() as temp_dir:
        saved_path = Path(temp_dir) / 'update.xlsx'
        workbook = Workbook()
        worksheet = workbook.active
        assert isinstance(worksheet, Worksheet)
        worksheet['A1'] = 'old'
        worksheet['B1'] = 'row'
        workbook.save(saved_path)
        workbook.close()
        with TableIOExcelOpenPyXL(
                Path(temp_dir) / 'update', FileAccess.UPDATE) as table_io:
            table_io.write_table_listdata([['new', 'row']])
        workbook = load_workbook(saved_path, data_only=True)
        worksheet = workbook.active
        assert isinstance(worksheet, Worksheet)
        assert worksheet['A1'].value == 'old'
        assert worksheet['B1'].value == 'row'
        assert worksheet['A2'].value is None
        assert worksheet['B2'].value is None
        assert worksheet['A3'].value == 'new'
        assert worksheet['B3'].value == 'row'
        workbook.close()
    check_capsys(capsys)


def test_excel_write_formatted_listdata_applies_formatting_and_filter(
        capsys: CaptureFixture[str]) -> None:
    """Per-cell formatting and one filtered table are written."""
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
        with TableIOExcelOpenPyXL(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_listdata(data, filtered_data_range=True)
        workbook = load_workbook(Path(temp_dir) / 'formatted.xlsx')
        worksheet = workbook.active
        assert isinstance(worksheet, Worksheet)
        assert [table.ref for table in worksheet.tables.values()] == [
            'A1:B2'
        ]
        assert worksheet['A1'].font.bold is True
        assert worksheet['A2'].font.italic is True
        assert worksheet['A2'].fill.fill_type == 'solid'
        assert worksheet['A2'].fill.fgColor.rgb == 'FFFFFF00'
        workbook.close()
    check_capsys(capsys)


def test_excel_table_width_uses_table_content_not_heading(
        capsys: CaptureFixture[str]) -> None:
    """Table column widths ignore headings written outside table cells."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'table_width_heading'
        with TableIOExcelOpenPyXL(file_name, FileAccess.CREATE) as table_io:
            table_io.write_heading('Heading text that is much wider than '
                                   'column A needs')
            table_io.write_table_listdata([
                ['id', 'report date'],
                ['A', datetime(2026, 3, 24, 14, 30, 0)]
            ])
        workbook = load_workbook(Path(temp_dir) / 'table_width_heading.xlsx')
        worksheet = workbook.active
        assert isinstance(worksheet, Worksheet)
        assert worksheet.column_dimensions['A'].width == 13.0
        assert worksheet.column_dimensions['B'].width == 21.0
        workbook.close()
    check_capsys(capsys)


def test_excel_write_multiple_filtered_ranges_keeps_all_tables(
        capsys: CaptureFixture[str]) -> None:
    """Sequential filtered writes are kept as separate worksheet tables."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'multiple_filters'
        first_data: list[list[Value]] = [['Name', 'Active'], ['Alice', True]]
        second_data: list[list[Value]] = [
            ['Issue', 'State'],
            ['TIO-123', 'Done']
        ]
        with TableIOExcelOpenPyXL(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_listdata(first_data, filtered_data_range=True)
            table_io.write_table_listdata(second_data,
                                          filtered_data_range=True)
        workbook = load_workbook(Path(temp_dir) / 'multiple_filters.xlsx')
        worksheet = workbook.active
        assert isinstance(worksheet, Worksheet)
        assert sorted(table.ref for table in worksheet.tables.values()) == [
            'A1:B2',
            'A4:B5'
        ]
        workbook.close()
    check_capsys(capsys)


def test_excel_table_width_is_widen_only_with_cap(
        capsys: CaptureFixture[str]) -> None:
    """Box rewrites keep an already widened column width."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'table_width_cap'
        box = Box(top=0, left=0, bottom=2, right=1)
        with TableIOExcelOpenPyXL(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_listdata([
                ['text'],
                ['x' * 80]
            ], box=box)
            table_io.write_table_listdata([
                ['text'],
                ['y']
            ], box=box)
        workbook = load_workbook(Path(temp_dir) / 'table_width_cap.xlsx')
        worksheet = workbook.active
        assert isinstance(worksheet, Worksheet)
        assert worksheet['A2'].value == 'y'
        assert worksheet.column_dimensions['A'].width == 50.0
        workbook.close()
    check_capsys(capsys)


def test_excel_box_write_removes_overlapping_filtered_table(
        capsys: CaptureFixture[str]) -> None:
    """Rewriting a boxed area removes any stale overlapping table metadata."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'rewrite_box'
        box = Box(top=0, left=0, bottom=3, right=2)
        with TableIOExcelOpenPyXL(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_listdata(
                [['Name', 'Active'], ['Alice', True]],
                filtered_data_range=True,
                box=box)
            table_io.write_table_listdata([['updated', 'value']], box=box)
        workbook = load_workbook(Path(temp_dir) / 'rewrite_box.xlsx')
        worksheet = workbook.active
        assert isinstance(worksheet, Worksheet)
        assert not worksheet.tables
        workbook.close()
    check_capsys(capsys)


def test_excel_write_row_formatted_dictdata_applies_formatting(
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
        with TableIOExcelOpenPyXL(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_fmtdictdata(
                data=data,
                column_order=['name', 'active'],
                filtered_data_range=True)
        workbook = load_workbook(Path(temp_dir) / 'row_formatted.xlsx')
        worksheet = workbook.active
        assert isinstance(worksheet, Worksheet)
        assert [table.ref for table in worksheet.tables.values()] == [
            'A1:B3'
        ]
        assert worksheet['A2'].font.bold is True
        assert worksheet['B2'].font.bold is True
        assert worksheet['A2'].fill.fgColor.rgb == 'FFC6EFCE'
        assert worksheet['A3'].font.italic is True
        assert worksheet['B3'].font.italic is True
        assert worksheet['A3'].fill.fgColor.rgb == 'FFFFC7CE'
        workbook.close()
    check_capsys(capsys)


def test_excel_write_dictdata_applies_first_row_format(
        capsys: CaptureFixture[str]) -> None:
    """Dict header cells can be formatted with first_row_format."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'dict_header_fmt'
        data: list[dict[str, Value]] = [
            {'name': 'Alice', 'active': True}
        ]
        with TableIOExcelOpenPyXL(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_dictdata(
                data=data,
                column_order=['name', 'active'],
                first_row_format=Fmt(bold=True, highlight=Color.YELLOW))
        workbook = load_workbook(Path(temp_dir) / 'dict_header_fmt.xlsx')
        worksheet = workbook.active
        assert isinstance(worksheet, Worksheet)
        assert worksheet['A1'].value == 'name'
        assert worksheet['B1'].value == 'active'
        assert worksheet['A1'].font.bold is True
        assert worksheet['B1'].font.bold is True
        assert worksheet['A1'].fill.fgColor.rgb == 'FFFFFF00'
        assert worksheet['B1'].fill.fgColor.rgb == 'FFFFFF00'
        assert worksheet['A2'].font.bold is False
        assert worksheet['B2'].font.bold is False
        workbook.close()
    check_capsys(capsys)


def test_excel_write_fmtdictdata_applies_first_row_format(
        capsys: CaptureFixture[str]) -> None:
    """Formatted dict writes keep header and data-row formatting separate."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'fmtdict_header_fmt'
        data = [
            FmtDictRow(values={'name': 'Alice', 'active': True},
                       fmt=Fmt(italic=True, highlight=Color.GREEN))
        ]
        with TableIOExcelOpenPyXL(file_name, FileAccess.CREATE) as table_io:
            table_io.write_table_fmtdictdata(
                data=data,
                column_order=['name', 'active'],
                first_row_format=Fmt(bold=True))
        workbook = load_workbook(Path(temp_dir) / 'fmtdict_header_fmt.xlsx')
        worksheet = workbook.active
        assert isinstance(worksheet, Worksheet)
        assert worksheet['A1'].font.bold is True
        assert worksheet['B1'].font.bold is True
        assert worksheet['A2'].font.italic is True
        assert worksheet['B2'].font.italic is True
        assert worksheet['A2'].fill.fgColor.rgb == 'FFC6EFCE'
        assert worksheet['B2'].fill.fgColor.rgb == 'FFC6EFCE'
        workbook.close()
    check_capsys(capsys)


def test_excel_read_formula_uses_cached_value(
        capsys: CaptureFixture[str]) -> None:
    """A formula cell is read as its cached value."""
    with TemporaryDirectory() as temp_dir:
        saved_path = Path(temp_dir) / 'formula.xlsx'
        _create_formula_workbook(saved_path, cached_value=3)
        with TableIOExcelOpenPyXL(
                Path(temp_dir) / 'formula', FileAccess.READ) as table_io:
            result = table_io.read_table_listdata()
        assert result.data == [[3, 'x']]
    check_capsys(capsys)


def test_excel_read_formula_without_cached_value_returns_none(
        capsys: CaptureFixture[str]) -> None:
    """A formula without a cached result is read as None."""
    with TemporaryDirectory() as temp_dir:
        saved_path = Path(temp_dir) / 'formula.xlsx'
        _create_formula_workbook(saved_path)
        with TableIOExcelOpenPyXL(
                Path(temp_dir) / 'formula', FileAccess.READ) as table_io:
            result = table_io.read_table_listdata()
        assert result.data == [[None, 'x']]
    check_capsys(capsys)
