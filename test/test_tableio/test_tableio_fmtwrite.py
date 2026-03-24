#! /usr/local/bin/python3
"""Tests for formatted write methods in the tableio module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest
from pytest import CaptureFixture

from tableio.capability import CapabilityNotSupported
from tableio.tableio import Box, Position
from tableio.value_type import Fmt, FmtDictRow, FmtListRow

from .check_capsys import check_capsys
from .test_tableio import RecordingTableIO, WriteIgnoreBoxTableIO, \
    WriteIgnoreFilteredDataRangeTableIO, WriteStrictBoxTableIO, \
    WriteStrictFilteredDataRangeTableIO, \
    WriteSupportedFilteredDataRangeTableIO


def test_write_table_fmtlistdata_delegates_valid_data_and_box(
        capsys: CaptureFixture[str]) -> None:
    """Test formatted list-data writes through the public method."""
    table_io = RecordingTableIO('sample')
    box = Box(top=3, left=4, bottom=6, right=6)
    data = [
        FmtListRow(values=('alpha', 1), fmt=Fmt(bold=True)),
        FmtListRow(values=[None, 2.5], fmt=Fmt(italic=True))
    ]
    position = table_io.write_table_fmtlistdata(data, box=box)
    assert position == Position(1, 1)
    assert table_io.last_fmtlist_write_data == data
    assert table_io.last_fmtlist_filtered_data_range is False
    assert table_io.last_fmtlist_write_box == box
    assert table_io.events == ['write_table_fmtlistdata']
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('data', 'box', 'expected_error'),
    [
        pytest.param([], None, 'Data is empty', id='empty-data'),
        pytest.param(
            [FmtListRow(values=[], fmt=Fmt())],
            None,
            'First row is empty',
            id='empty-first-row'
        ),
        pytest.param(
            [FmtListRow(values=('only',), fmt=Fmt())],
            None,
            'Data is not at least 2 cells in size',
            id='one-cell'
        ),
        pytest.param(
            [
                FmtListRow(values=('left', 1), fmt=Fmt()),
                FmtListRow(values=('right',), fmt=Fmt())
            ],
            None,
            'All rows must have the same number of columns',
            id='ragged'
        ),
        pytest.param(
            [
                FmtListRow(values=('left', 1), fmt=Fmt()),
                FmtListRow(values=('right', 2), fmt=Fmt())
            ],
            Box(0, 0, 1, None),
            'Too many rows',
            id='too-many-rows'
        ),
        pytest.param(
            [
                FmtListRow(values=('left', 1), fmt=Fmt()),
                FmtListRow(values=('right', 2), fmt=Fmt())
            ],
            Box(0, 0, None, 1),
            'Too many columns',
            id='too-many-columns'
        )
    ]
)
def test_write_table_fmtlistdata_rejects_invalid_shapes(
        data: list[FmtListRow], box: Box | None, expected_error: str,
        capsys: CaptureFixture[str]) -> None:
    """Test formatted list-data validation."""
    table_io = RecordingTableIO('sample')
    with pytest.raises(ValueError, match=expected_error):
        table_io.write_table_fmtlistdata(data, box=box)
    assert not table_io.events
    check_capsys(capsys)


def test_write_table_fmtdictdata_normalizes_and_delegates(
        capsys: CaptureFixture[str]) -> None:
    """Test formatted dict-data writes through the public method."""
    table_io = RecordingTableIO('sample')
    box = Box(top=5, left=2, bottom=9, right=4)
    column_order = ['alpha', 'beta']
    first_row_format = Fmt(italic=True)
    data = [
        FmtDictRow(
            values={'alpha': 'left', 'extra': 1},
            fmt=Fmt(bold=True)
        ),
        FmtDictRow(values={'beta': 2.5}, fmt=Fmt(italic=True))
    ]
    position = table_io.write_table_fmtdictdata(
        data=data,
        column_order=column_order,
        first_row_format=first_row_format,
        missing_ok=True,
        extra_ok=True,
        box=box
    )
    assert position == Position(2, 1)
    assert table_io.last_fmtdict_write_data == [
        FmtDictRow(
            values={'alpha': 'left', 'beta': None},
            fmt=Fmt(bold=True)
        ),
        FmtDictRow(
            values={'alpha': None, 'beta': 2.5},
            fmt=Fmt(italic=True)
        )
    ]
    assert table_io.last_fmtdict_column_order == column_order
    assert table_io.last_fmtdict_first_row_format == first_row_format
    assert table_io.last_fmtdict_filtered_data_range is False
    assert table_io.last_fmtdict_write_box == box
    assert table_io.events == ['write_table_fmtdictdata']
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('data', 'column_order', 'box', 'expected_error'),
    [
        pytest.param([], ['alpha'], None, 'Data is empty', id='empty-data'),
        pytest.param(
            [FmtDictRow(values={}, fmt=Fmt())],
            ['alpha'],
            None,
            'index 0',
            id='empty-first-row'
        ),
        pytest.param(
            [FmtDictRow(values={'alpha': 'only'}, fmt=Fmt())],
            ['alpha'],
            None,
            'Data is not at least 2 cells in size',
            id='one-cell'
        ),
        pytest.param(
            [FmtDictRow(values={'alpha': 'left'}, fmt=Fmt())],
            [],
            None,
            'column_order',
            id='empty-column-order'
        ),
        pytest.param(
            [FmtDictRow(values={'alpha': 'left'}, fmt=Fmt())],
            ['alpha', 'alpha'],
            None,
            'Duplicate column name',
            id='duplicate-column-order'
        ),
        pytest.param(
            [FmtDictRow(values={'alpha': 'left'}, fmt=Fmt())],
            ['alpha', 'beta'],
            None,
            'beta',
            id='missing-column'
        ),
        pytest.param(
            [FmtDictRow(values={'alpha': 'left', 'beta': 1}, fmt=Fmt())],
            ['alpha'],
            None,
            'beta',
            id='extra-column'
        ),
        pytest.param(
            [FmtDictRow(values={'alpha': 'left', 'beta': 1}, fmt=Fmt())],
            ['alpha', 'beta'],
            Box(0, 0, 1, None),
            'Too many rows',
            id='too-many-rows'
        ),
        pytest.param(
            [FmtDictRow(values={'alpha': 'left', 'beta': 1}, fmt=Fmt())],
            ['alpha', 'beta'],
            Box(0, 0, None, 1),
            'Too many columns',
            id='too-many-columns'
        )
    ]
)
def test_write_table_fmtdictdata_rejects_invalid_data(
        data: list[FmtDictRow], column_order: list[str], box: Box | None,
        expected_error: str, capsys: CaptureFixture[str]) -> None:
    """Test formatted dict-data validation."""
    table_io = RecordingTableIO('sample')
    with pytest.raises(ValueError, match=expected_error):
        table_io.write_table_fmtdictdata(data, column_order, box=box)
    assert not table_io.events
    check_capsys(capsys)


def test_write_table_fmtlistdata_passes_filtered_data_range_when_supported(
        capsys: CaptureFixture[str]) -> None:
    """Test formatted list-data writes with filtered data range enabled."""
    table_io = WriteSupportedFilteredDataRangeTableIO('sample')
    data = [FmtListRow(values=('alpha', 1), fmt=Fmt(bold=True))]
    position = table_io.write_table_fmtlistdata(data, True)
    assert position == Position(0, 1)
    assert table_io.last_fmtlist_write_data == data
    assert table_io.last_fmtlist_filtered_data_range is True
    assert table_io.last_fmtlist_write_box is None
    check_capsys(capsys)


def test_write_table_fmtdictdata_passes_filtered_data_range_when_supported(
        capsys: CaptureFixture[str]) -> None:
    """Test formatted dict-data writes with filtered data range enabled."""
    table_io = WriteSupportedFilteredDataRangeTableIO('sample')
    data = [
        FmtDictRow(
            values={'alpha': 'left', 'beta': 1},
            fmt=Fmt(bold=True)
        )
    ]
    position = table_io.write_table_fmtdictdata(
        data,
        ['alpha', 'beta'],
        filtered_data_range=True
    )
    assert position == Position(1, 1)
    assert table_io.last_fmtdict_write_data == data
    assert table_io.last_fmtdict_filtered_data_range is True
    assert table_io.last_fmtdict_write_box is None
    check_capsys(capsys)


def test_write_table_fmtlistdata_ignores_box_when_supported_is_ignore(
        capsys: CaptureFixture[str]) -> None:
    """Test ignoring write-box requests for formatted list-data writes."""
    table_io = WriteIgnoreBoxTableIO('sample')
    data = [FmtListRow(values=('alpha', 1), fmt=Fmt(bold=True))]
    position = table_io.write_table_fmtlistdata(data, box=Box(1, 1, 3, 3))
    assert position == Position(0, 1)
    assert table_io.last_fmtlist_write_box is None
    assert table_io.last_fmtlist_write_data == data
    check_capsys(capsys)


def test_write_table_fmtdictdata_rejects_box_when_supported_is_strict(
        capsys: CaptureFixture[str]) -> None:
    """Test strict box rejection for formatted dict-data writes."""
    table_io = WriteStrictBoxTableIO('sample')
    data = [
        FmtDictRow(
            values={'alpha': 'left', 'beta': 1},
            fmt=Fmt(bold=True)
        )
    ]
    with pytest.raises(CapabilityNotSupported) as exc_info:
        table_io.write_table_fmtdictdata(
            data,
            ['alpha', 'beta'],
            box=Box(1, 1, 3, 3)
        )
    assert exc_info.value.action == 'write to a box'
    assert not table_io.events
    check_capsys(capsys)


def test_write_table_fmtdictdata_ignores_filtered_data_range_when_allowed(
        capsys: CaptureFixture[str]) -> None:
    """Test ignored filtered data ranges for formatted dict-data writes."""
    table_io = WriteIgnoreFilteredDataRangeTableIO('sample')
    data = [
        FmtDictRow(
            values={'alpha': 'left', 'beta': 1},
            fmt=Fmt(italic=True)
        )
    ]
    position = table_io.write_table_fmtdictdata(
        data,
        ['alpha', 'beta'],
        filtered_data_range=True
    )
    assert position == Position(1, 1)
    assert table_io.last_fmtdict_filtered_data_range is False
    assert table_io.last_fmtdict_write_data == data
    check_capsys(capsys)


def test_write_table_fmtlistdata_rejects_filtered_data_range_when_strict(
        capsys: CaptureFixture[str]) -> None:
    """Test strict filtered-range rejection for formatted list-data."""
    table_io = WriteStrictFilteredDataRangeTableIO('sample')
    data = [FmtListRow(values=('alpha', 1), fmt=Fmt(bold=True))]
    with pytest.raises(CapabilityNotSupported) as exc_info:
        table_io.write_table_fmtlistdata(data, True)
    assert exc_info.value.action == 'write a filtered data range'
    assert not table_io.events
    check_capsys(capsys)
