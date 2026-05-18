#! /usr/local/bin/python3
"""Tests for TableIO sheet helpers and read-only write rejection."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import io
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Callable

import pytest
from pytest import CaptureFixture

from tableio.capability import Capabilities, CapabilityNotSupported, \
    SingleCapability, Strictness
from tableio.tableio import Box, Descriptor, FileAccess, Position, TableIO
from tableio.value_type import CellT, DictDataMap, Fmt, FmtDictData, \
    FmtDictRow, FmtListData, FmtListRow, ListDataSeq, ReadResult, Value

from .check_capsys import check_capsys


_SUPPORTED = SingleCapability(supported=True, strictness=Strictness.STRICT)


class _RecordingTableIO(TableIO):
    """Minimal concrete TableIO used for public API behavior tests."""

    capabilities = Capabilities(can_write=_SUPPORTED, can_read=_SUPPORTED)

    def __init__(self, file_name: str | Path,
                 file_access: FileAccess = FileAccess.CREATE):
        """Initialize the recording test double."""
        super().__init__(file_name=file_name, file_access=file_access)
        self.events: list[str] = []

    @classmethod
    def get_description(cls) -> Descriptor:
        """Return the descriptor for the recording implementation."""
        return Descriptor(format_name='recording', implementation='test',
                          capabilities=cls.capabilities,
                          mandatory_args=['file_access'], optional_args=[])

    @classmethod
    def get_capabilities(cls) -> Capabilities:
        """Return the capabilities for the recording implementation."""
        return cls.capabilities

    @classmethod
    def file_name_extension(cls) -> str:
        """Return the file name extension used in tests."""
        return 'tio'

    def open(self) -> None:
        """Record that the file was opened."""
        self.events.append('open')

    def _end_state(self) -> None:
        """No-op finalization hook."""

    def _write_file_suffix(self) -> None:
        """No-op write hook."""

    def _close(self) -> None:
        """Record that the file was closed."""
        self.events.append('close')

    def _write_heading(self, heading: str, level: int) -> Position:
        """Record heading writes and return a predictable position."""
        _ = heading
        _ = level
        self.events.append('write_heading')
        return Position(0, 0)

    def _write_table_listdata(self, data: ListDataSeq[CellT],
                              impl_meta: TableIO.ImplMetaForWrite) -> \
            Position:
        """Record list-data writes and return a predictable position."""
        _ = data
        _ = impl_meta
        self.events.append('write_table_listdata')
        return Position(0, 0)

    def _write_table_fmtlistdata(self, data: FmtListData,
                                 impl_meta: TableIO.ImplMetaForWrite) -> \
            Position:
        """Record formatted list-data writes."""
        _ = data
        _ = impl_meta
        self.events.append('write_table_fmtlistdata')
        return Position(0, 0)

    def _write_table_dictdata(
            self, data: DictDataMap[CellT],
            impl_meta: TableIO.ImplMetaForDictWrite) -> Position:
        """Record dict-data writes."""
        _ = data
        _ = impl_meta
        self.events.append('write_table_dictdata')
        return Position(0, 0)

    def _write_table_fmtdictdata(
            self, data: FmtDictData,
            impl_meta: TableIO.ImplMetaForDictWrite) -> Position:
        """Record formatted dict-data writes."""
        _ = data
        _ = impl_meta
        self.events.append('write_table_fmtdictdata')
        return Position(0, 0)

    def _read_table_listdata(self, box: Box | None = None) -> \
            ReadResult[list[list[Value]]]:
        """Return a fixed list-data read result."""
        _ = box
        return ReadResult(data=[['alpha', 'beta']], headings=[],
                          last_read_row=0)

    def _read_table_dictdata(self, box: Box | None = None) -> \
            ReadResult[list[dict[str, Value]]]:
        """Return a fixed dict-data read result."""
        _ = box
        return ReadResult(data=[{'alpha': 'beta'}], headings=[],
                          last_read_row=0)


class _MultiSheetRecordingTableIO(_RecordingTableIO):
    """Recording implementation that supports the public sheet API."""

    capabilities = Capabilities(can_write=_SUPPORTED, can_read=_SUPPORTED,
                                multi_sheet=_SUPPORTED)

    def __init__(self, file_name: str | Path,
                 file_access: FileAccess = FileAccess.CREATE):
        """Initialize the multi-sheet recording test double."""
        super().__init__(file_name=file_name, file_access=file_access)
        self.sheet_names: list[str] = ['Sheet1']
        self.selected_sheet_name: str = 'Sheet1'

    def _list_sheets(self) -> list[str]:
        """Return the configured sheet names."""
        self.events.append('list_sheets')
        return list(self.sheet_names)

    def _select_sheet(self, sheet_name: str, create: bool = False) -> None:
        """Select or create a configured sheet."""
        self.events.append('select_sheet')
        for existing_name in self.sheet_names:
            if existing_name.casefold() == sheet_name.casefold():
                self.selected_sheet_name = existing_name
                return
        if not create:
            raise KeyError(sheet_name)
        self.sheet_names.append(sheet_name)
        self.selected_sheet_name = sheet_name

    def _current_sheet_name(self) -> str:
        """Return the configured current sheet name."""
        self.events.append('current_sheet_name')
        return self.selected_sheet_name


class _MinimalSheetTableIO(TableIO):
    """Minimal subclass used to exercise the new abstract sheet hooks."""

    def __init__(self, file_name: str | Path,
                 file_access: FileAccess = FileAccess.CREATE):
        """Initialize the minimal test double."""
        super().__init__(file_name=file_name, file_access=file_access)

    @classmethod
    def get_description(cls) -> Descriptor:
        """Return a descriptor that allows instantiation in tests."""
        return Descriptor(format_name='minimal', implementation='test',
                          capabilities=Capabilities(),
                          mandatory_args=['file_access'], optional_args=[])

    @classmethod
    def get_capabilities(cls) -> Capabilities:
        """Return empty capabilities for the minimal implementation."""
        return Capabilities()

    @classmethod
    def file_name_extension(cls) -> str:
        """Return the file name extension used in tests."""
        return 'min'

    def run_list_sheets(self) -> list[str]:
        """Expose the inherited _list_sheets method for tests."""
        return self._list_sheets()

    def run_select_sheet(self, sheet_name: str, create: bool = False) -> None:
        """Expose the inherited _select_sheet method for tests."""
        self._select_sheet(sheet_name, create)

    def run_current_sheet_name(self) -> str:
        """Expose the inherited _current_sheet_name method for tests."""
        return self._current_sheet_name()


@pytest.mark.parametrize(
    'action',
    [
        pytest.param(lambda table_io: table_io.write_heading('Read only'),
                     id='write-heading'),
        pytest.param(
            lambda table_io: table_io.write_table_listdata([['a', 'b']]),
            id='write-list'),
        pytest.param(
            lambda table_io: table_io.write_table_fmtlistdata([
                FmtListRow(values=('a', 'b'), fmt=Fmt())
            ]),
            id='write-fmtlist'),
        pytest.param(
            lambda table_io: table_io.write_table_dictdata(
                [{'alpha': 'a', 'beta': 'b'}], ['alpha', 'beta']),
            id='write-dict'),
        pytest.param(
            lambda table_io: table_io.write_table_fmtdictdata([
                FmtDictRow(values={'alpha': 'a', 'beta': 'b'}, fmt=Fmt())
            ], ['alpha', 'beta']),
            id='write-fmtdict'),
    ])
def test_write_methods_reject_read_only_access(
        action: Callable[[_RecordingTableIO], object],
        capsys: CaptureFixture[str]) -> None:
    """Public write methods reject FileAccess.READ before delegating."""
    with TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / 'sample.tio'
        file_path.touch()
        table_io = _RecordingTableIO(Path(temp_dir) / 'sample',
                                     file_access=FileAccess.READ)
        with pytest.raises(io.UnsupportedOperation,
                           match='opened for reading'):
            action(table_io)
        assert not table_io.events
    check_capsys(capsys)


def test_sheet_methods_reject_when_multi_sheet_is_unsupported(
        capsys: CaptureFixture[str]) -> None:
    """Public sheet methods raise when the capability is unsupported."""
    table_io = _RecordingTableIO('sample')
    with pytest.raises(CapabilityNotSupported, match='multi sheet'):
        table_io.list_sheets()
    with pytest.raises(CapabilityNotSupported, match='multi sheet'):
        table_io.select_sheet('Other')
    with pytest.raises(CapabilityNotSupported, match='multi sheet'):
        table_io.current_sheet_name()
    check_capsys(capsys)


def test_sheet_methods_delegate_when_multi_sheet_is_supported(
        capsys: CaptureFixture[str]) -> None:
    """Public sheet methods delegate to the implementation hooks."""
    table_io = _MultiSheetRecordingTableIO('sample')
    assert table_io.list_sheets() == ['Sheet1']
    table_io.select_sheet('Summary', create=True)
    assert table_io.current_sheet_name() == 'Summary'
    assert table_io.list_sheets() == ['Sheet1', 'Summary']
    assert table_io.events == [
        'list_sheets',
        'select_sheet',
        'current_sheet_name',
        'list_sheets'
    ]
    check_capsys(capsys)


def test_new_sheet_hooks_raise_not_implemented_by_default(
        capsys: CaptureFixture[str]) -> None:
    """The inherited protected sheet hooks stay abstract by default."""
    table_io = _MinimalSheetTableIO('sample', FileAccess.CREATE)
    with pytest.raises(NotImplementedError, match='_list_sheets method'):
        table_io.run_list_sheets()
    with pytest.raises(NotImplementedError, match='_select_sheet method'):
        table_io.run_select_sheet('Sheet1')
    with pytest.raises(NotImplementedError,
                       match='_current_sheet_name method'):
        table_io.run_current_sheet_name()
    check_capsys(capsys)
