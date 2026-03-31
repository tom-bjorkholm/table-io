#! /usr/local/bin/python3
"""Tests for the excel cross usage of different implementations."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from tempfile import TemporaryDirectory
from datetime import datetime, timedelta
import pytest
from pytest import CaptureFixture
from tableio.color import Color
from tableio.tableio import TableIO
from tableio.tableio_types import FileAccess
from tableio.value_type import ListData, DictData, Value, \
    ListDataSeq, DictDataMap, Fmt, FmtListRow, FmtDictRow, ValueFmt
from tableio.valueconversion import value2type_of
from tableio.tableio_excel_openpyxl import TableIOExcelOpenPyXL
from tableio.tableio_excel_pylightxl import TableIOExcelPylightxl
from tableio.tableio_excel_xlsxwriter import TableIOExcelXlsxWriter
from .check_capsys import check_capsys

_WRITERS = [TableIOExcelOpenPyXL, TableIOExcelPylightxl,
            TableIOExcelXlsxWriter]
_READERS = [TableIOExcelOpenPyXL, TableIOExcelPylightxl]


def _all_formats() -> list[Fmt]:
    """Return all bold/italic/highlight format combinations."""
    ret: list[Fmt] = []
    for bold in [False, True]:
        for italic in [False, True]:
            for highlight in [Color.NONE, Color.RED, Color.GREEN,
                              Color.YELLOW]:
                ret.append(Fmt(bold=bold, italic=italic,
                               highlight=highlight))
    return ret


_ALL_FORMATS = _all_formats()


def _format_case_value(index: int) -> Value:
    """Return one deterministic test value for a formatting case."""
    case_index = index % 6
    if case_index == 0:
        return f'value {index}'
    if case_index == 1:
        return index
    if case_index == 2:
        return index + 0.5
    if case_index == 3:
        return index % 2 == 0
    if case_index == 4:
        return datetime(2026, 3, 31, 9, 0, 0) + timedelta(days=index)
    return None


def _formatted_list_tables() -> tuple[ListData[Value], ListData[ValueFmt]]:
    """Return one plain and one cell-formatted list table."""
    plain_data: ListData[Value] = [
        ['Col A', 'Col B', 'Col C', 'Col D'],
        [_format_case_value(0), _format_case_value(1),
         _format_case_value(2), _format_case_value(3)],
        [_format_case_value(4), _format_case_value(5),
         _format_case_value(6), _format_case_value(7)],
        [_format_case_value(8), _format_case_value(9),
         _format_case_value(10), _format_case_value(11)]
    ]
    formatted_data: ListData[ValueFmt] = []
    format_index = 0
    for row in plain_data:
        formatted_row: list[ValueFmt] = []
        for cell in row:
            formatted_row.append(
                ValueFmt(value=cell, fmt=_ALL_FORMATS[format_index]))
            format_index += 1
        formatted_data.append(formatted_row)
    return plain_data, formatted_data


def _row_formatted_list_tables() -> tuple[ListData[Value], list[FmtListRow]]:
    """Return one plain and one row-formatted list table."""
    plain_data: ListData[Value] = [['Label', 'Value']]
    for index in range(1, len(_ALL_FORMATS)):
        plain_data.append([f'row {index}', _format_case_value(index - 1)])
    formatted_data = [
        FmtListRow(values=row, fmt=fmt)
        for row, fmt in zip(plain_data, _ALL_FORMATS, strict=True)
    ]
    return plain_data, formatted_data


def _formatted_dict_tables() -> tuple[DictData[Value], DictData[ValueFmt],
                                      list[str]]:
    """Return one plain and one cell-formatted dict table."""
    column_order = ['alpha', 'beta', 'gamma', 'delta']
    plain_data: DictData[Value] = []
    formatted_data: DictData[ValueFmt] = []
    format_index = 0
    for _row_index in range(4):
        plain_row: dict[str, Value] = {}
        formatted_row: dict[str, ValueFmt] = {}
        for column_name in column_order:
            value = _format_case_value(format_index)
            plain_row[column_name] = value
            formatted_row[column_name] = ValueFmt(
                value=value, fmt=_ALL_FORMATS[format_index])
            format_index += 1
        plain_data.append(plain_row)
        formatted_data.append(formatted_row)
    return plain_data, formatted_data, column_order


def _row_formatted_dict_tables() -> tuple[DictData[Value],
                                          list[FmtDictRow], list[str]]:
    """Return one plain and one row-formatted dict table."""
    column_order = ['label', 'value']
    plain_data: DictData[Value] = []
    formatted_data: list[FmtDictRow] = []
    for index, fmt in enumerate(_ALL_FORMATS):
        row = {'label': f'row {index}', 'value': _format_case_value(index)}
        plain_data.append(row)
        formatted_data.append(FmtDictRow(values=row, fmt=fmt))
    return plain_data, formatted_data, column_order


def compare_lists(original: ListData[Value],
                  readback: ListDataSeq[Value]) -> bool:
    """Compare two lists of lists of objects."""
    if len(original) != len(readback):
        print(f'Original list has {len(original)} rows, '
              f'readback has {len(readback)} rows')
        return False
    for rownum, (orow, rrow) in enumerate(zip(original, readback)):
        if len(orow) != len(rrow):
            print(f'Row {rownum} has {len(orow)} columns, '
                  f'readback has {len(rrow)} columns')
            return False
        for colnum, (ocell, rcell) in enumerate(zip(orow, rrow)):
            if ocell != value2type_of(rcell, ocell):
                print(f'Cell {colnum} in row {rownum} is '
                      f'{ocell}, readback is {rcell}')
                return False
    return True


def compare_dicts(original: DictData[Value],
                  readback: DictDataMap[Value]) -> bool:
    """Compare two dicts of dicts of objects."""
    if len(original) != len(readback):
        print(f'Original list of dicts has {len(original)} rows, '
              f'readback has {len(readback)} rows')
        return False
    for rownum, (orow, rrow) in enumerate(zip(original, readback)):
        if len(orow) != len(rrow):
            print(f'Row {rownum} has {len(orow)} columns, '
                  f'readback has {len(rrow)} columns')
            return False
        for key in orow.keys():
            if key not in rrow:
                print(f'Key {key} is in original but not in readback')
                return False
            if orow[key] != value2type_of(rrow[key], orow[key]):
                print(f'Value for key {key} in row {rownum} is '
                      f'{orow[key]}, readback is {rrow[key]}')
                return False
    return True


@pytest.mark.parametrize('filtered', [False, True])
@pytest.mark.parametrize('writer', _WRITERS)
@pytest.mark.parametrize('reader', _READERS)
def test_unformatted(capsys: CaptureFixture[str], writer: type[TableIO],
                     reader: type[TableIO], filtered: bool) -> None:
    """Test the unformatted excel cross usage of different implementations."""
    head1 = 'Testing unformatted excel cross usage'
    head2 = 'This is a test of the unformatted excel cross usage'
    data1: ListData[Value] = [['Hello', 'World', '!'],
                              ['Hallo', 2, False],
                              ['Several words in cell', None,
                               datetime.now().replace(microsecond=0)]]
    data2: DictData[Value] = [
        {'Name': 'Ronald', 'Age': 25,
         'Pass date': datetime(year=2026, month=3, day=31),
         'Score': 100.0, 'Valid': True},
        {'Name': 'George', 'Age': 22,
         'Pass date': datetime(year=2025, month=2, day=5),
         'Score': 95.5, 'Valid': True},
        {'Name': 'Mia', 'Age': 23,
         'Pass date': datetime(year=2020, month=12, day=25),
         'Score': 98.0, 'Valid': False}]
    column_order = ['Name', 'Age', 'Pass date', 'Score', 'Valid']
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / 'test.xlsx'
        with writer(temp_path, FileAccess.CREATE) as w_tableio:
            w_tableio.write_heading(head1)
            w_tableio.write_heading(head2)
            w_tableio.write_table_listdata(data=data1,
                                           filtered_data_range=filtered)
            w_tableio.write_table_dictdata(data=data2,
                                           column_order=column_order,
                                           filtered_data_range=filtered)
        with reader(temp_path, FileAccess.READ) as r_tableio:
            readback1 = r_tableio.read_table_listdata()
            readback2 = r_tableio.read_table_dictdata()
            assert compare_lists(data1, readback1.data)
            assert compare_dicts(data2, readback2.data)
    check_capsys(capsys)


@pytest.mark.parametrize('filtered', [False, True])
@pytest.mark.parametrize('writer', _WRITERS)
@pytest.mark.parametrize('reader', _READERS)
def test_formatted_listdata(capsys: CaptureFixture[str], writer: type[TableIO],
                            reader: type[TableIO], filtered: bool) -> None:
    """Test formatted list-data writes across Excel implementations."""
    data, formatted_data = _formatted_list_tables()
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / 'formatted_list.xlsx'
        with writer(temp_path, FileAccess.CREATE) as w_tableio:
            w_tableio.write_table_listdata(data=formatted_data,
                                           filtered_data_range=filtered)
        with reader(temp_path, FileAccess.READ) as r_tableio:
            readback = r_tableio.read_table_listdata()
            assert compare_lists(data, readback.data)
    check_capsys(capsys)


@pytest.mark.parametrize('filtered', [False, True])
@pytest.mark.parametrize('writer', _WRITERS)
@pytest.mark.parametrize('reader', _READERS)
def test_row_formatted_listdata(capsys: CaptureFixture[str],
                                writer: type[TableIO],
                                reader: type[TableIO],
                                filtered: bool) -> None:
    """Test row-formatted list-data writes across Excel implementations."""
    data, formatted_data = _row_formatted_list_tables()
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / 'row_formatted_list.xlsx'
        with writer(temp_path, FileAccess.CREATE) as w_tableio:
            w_tableio.write_table_fmtlistdata(data=formatted_data,
                                              filtered_data_range=filtered)
        with reader(temp_path, FileAccess.READ) as r_tableio:
            readback = r_tableio.read_table_listdata()
            assert compare_lists(data, readback.data)
    check_capsys(capsys)


@pytest.mark.parametrize('filtered', [False, True])
@pytest.mark.parametrize('writer', _WRITERS)
@pytest.mark.parametrize('reader', _READERS)
def test_formatted_dictdata(capsys: CaptureFixture[str], writer: type[TableIO],
                            reader: type[TableIO], filtered: bool) -> None:
    """Test formatted dict-data writes across Excel implementations."""
    data, formatted_data, column_order = _formatted_dict_tables()
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / 'formatted_dict.xlsx'
        with writer(temp_path, FileAccess.CREATE) as w_tableio:
            for first_row_format in _ALL_FORMATS:
                w_tableio.write_table_dictdata(
                    data=formatted_data,
                    column_order=column_order,
                    first_row_format=first_row_format,
                    filtered_data_range=filtered)
        with reader(temp_path, FileAccess.READ) as r_tableio:
            for _first_row_format in _ALL_FORMATS:
                readback = r_tableio.read_table_dictdata()
                assert compare_dicts(data, readback.data)
    check_capsys(capsys)


@pytest.mark.parametrize('filtered', [False, True])
@pytest.mark.parametrize('writer', _WRITERS)
@pytest.mark.parametrize('reader', _READERS)
def test_row_formatted_dictdata(capsys: CaptureFixture[str],
                                writer: type[TableIO],
                                reader: type[TableIO],
                                filtered: bool) -> None:
    """Test row-formatted dict-data writes across Excel implementations."""
    data, formatted_data, column_order = _row_formatted_dict_tables()
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / 'row_formatted_dict.xlsx'
        with writer(temp_path, FileAccess.CREATE) as w_tableio:
            for first_row_format in _ALL_FORMATS:
                w_tableio.write_table_fmtdictdata(
                    data=formatted_data,
                    column_order=column_order,
                    first_row_format=first_row_format,
                    filtered_data_range=filtered)
        with reader(temp_path, FileAccess.READ) as r_tableio:
            for _first_row_format in _ALL_FORMATS:
                readback = r_tableio.read_table_dictdata()
                assert compare_dicts(data, readback.data)
    check_capsys(capsys)
