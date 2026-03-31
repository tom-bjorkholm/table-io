#! /usr/local/bin/python3
"""Tests for the excel cross usage of different implementations."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from tempfile import TemporaryDirectory
from datetime import datetime
import pytest
from pytest import CaptureFixture
from tableio.tableio import TableIO
from tableio.tableio_types import FileAccess
from tableio.value_type import ListData, DictData, Value, \
    ListDataSeq, DictDataMap
from tableio.valueconversion import value2type_of
from tableio.tableio_excel_openpyxl import TableIOExcelOpenPyXL
from tableio.tableio_excel_pylightxl import TableIOExcelPylightxl
from tableio.tableio_excel_xlsxwriter import TableIOExcelXlsxWriter
from .check_capsys import check_capsys


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
@pytest.mark.parametrize('writer',
                         [TableIOExcelOpenPyXL, TableIOExcelPylightxl,
                          TableIOExcelXlsxWriter])
@pytest.mark.parametrize('reader',
                         [TableIOExcelOpenPyXL, TableIOExcelPylightxl])
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
