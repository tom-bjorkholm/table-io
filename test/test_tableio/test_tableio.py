#! /usr/local/bin/python3
"""Tests for the tableio module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
# pylint: disable=too-many-lines

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Callable, Optional

import pytest
from pytest import CaptureFixture

from tableio.capability import Capabilities, CapabilityNotSupported, \
    SingleCapability, Strictness
from tableio.tableio import Box, Descriptor, FileAccess, Position, TableIO
from tableio.value_type import CellT, DictDataMap, Fmt, FmtDictData, \
    FmtDictRow, FmtListData, FmtListRow, ListDataSeq, ReadResult, Value, \
    ValueFmt

from .check_capsys import check_capsys
from .impl_meta_test_helper import make_no_border_helper


def make_capability(
        supported: bool = False,
        strictness: Strictness = Strictness.IGNORE) -> SingleCapability:
    """Build a SingleCapability value for tests."""
    return SingleCapability(supported=supported, strictness=strictness)


def make_capabilities(
        filtered_data_range: SingleCapability = SingleCapability(),
        can_write_box: SingleCapability = SingleCapability(),
        can_read_box: SingleCapability = SingleCapability(),
        can_find_value_position: SingleCapability = SingleCapability()) \
        -> Capabilities:
    """Build a Capabilities value for tests."""
    return Capabilities(can_write=make_capability(True, Strictness.STRICT),
                        can_read=make_capability(True, Strictness.STRICT),
                        filtered_data_range=filtered_data_range,
                        can_write_box=can_write_box, can_read_box=can_read_box,
                        can_find_value_position=can_find_value_position)


# pylint: disable-next=too-many-instance-attributes
class RecordingTableIO(TableIO):
    """Concrete TableIO implementation used to observe base-class behavior."""

    capabilities = make_capabilities(
        can_write_box=make_capability(True, Strictness.STRICT),
        can_read_box=make_capability(True, Strictness.STRICT),
        can_find_value_position=make_capability(True, Strictness.STRICT))

    def __init__(self, file_name: str | Path,
                 file_access: FileAccess = FileAccess.CREATE,
                 file_exists_callback:
                 Callable[[str], None] | None = None):
        """Initialize the recording test double."""
        super().__init__(file_name, file_access, file_exists_callback)
        self.events: list[str] = []
        self.close_count: int = 0
        self.last_heading: tuple[str, int] | None = None
        self.last_list_write_data: list[list[Value | ValueFmt]] | None = None
        self.last_list_impl_meta: Optional[TableIO.ImplMetaForWrite] = None
        self.last_list_filtered_data_range: bool | None = None
        self.last_list_write_box: Box | None = None
        self.last_fmtlist_write_data: list[FmtListRow] | None = None
        self.last_fmtlist_impl_meta: Optional[TableIO.ImplMetaForWrite] = \
            None
        self.last_fmtlist_filtered_data_range: bool | None = None
        self.last_fmtlist_write_box: Box | None = None
        self.last_dict_write_data: list[dict[str, Value | ValueFmt]] | None = \
            None
        self.last_dict_impl_meta: Optional[TableIO.ImplMetaForDictWrite] = \
            None
        self.last_column_order: list[str] | None = None
        self.last_dict_first_row_format: Optional[Fmt] = None
        self.last_dict_filtered_data_range: bool | None = None
        self.last_dict_write_box: Box | None = None
        self.last_fmtdict_write_data: list[FmtDictRow] | None = None
        self.last_fmtdict_impl_meta: Optional[TableIO.ImplMetaForDictWrite] = \
            None
        self.last_fmtdict_column_order: list[str] | None = None
        self.last_fmtdict_first_row_format: Optional[Fmt] = None
        self.last_fmtdict_filtered_data_range: bool | None = None
        self.last_fmtdict_write_box: Box | None = None
        self.last_list_read_box: Box | None = None
        self.last_dict_read_box: Box | None = None
        self.last_find_value: Optional[list[list[Value]]] = None
        self.last_find_type_conversion: Optional[bool] = None
        self.last_find_box: Optional[Box] = None
        self.find_result: Optional[Box] = None
        self.last_read_cells_box: Optional[Box] = None
        self.read_cells_result: list[list[Value]] = [['read', 1]]
        self.last_write_cells_data: Optional[list[list[Value | ValueFmt]]] = \
            None
        self.last_write_cells_box: Optional[Box] = None
        self.fail_end_state: bool = False
        self.fail_write_file_suffix: bool = False
        self.fail_close: bool = False
        self.list_read_result: ReadResult[list[list[Value]]] = ReadResult(
            data=[['list', 1]], headings=['before-list'], last_read_row=5)
        self.dict_read_result: ReadResult[list[dict[str, Value]]] = \
            ReadResult(data=[{'alpha': 'dict', 'beta': 2}],
                       headings=['before-dict'], last_read_row=5)

    @classmethod
    def get_description(cls) -> Descriptor:
        """Return the descriptor for the recording implementation."""
        return Descriptor(format_name='recording', implementation='test',
                          capabilities=cls.capabilities,
                          mandatory_args=['file_access'],
                          optional_args=['file_exists_callback'])

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
        """Record the end-state hook and optionally raise."""
        self.events.append('end_state')
        if self.fail_end_state:
            raise RuntimeError('end_state failed')

    def _write_file_suffix(self) -> None:
        """Record the file-suffix hook and optionally raise."""
        self.events.append('write_file_suffix')
        if self.fail_write_file_suffix:
            raise RuntimeError('write_file_suffix failed')

    def _close(self) -> None:
        """Record the close hook and optionally raise."""
        self.events.append('close')
        self.close_count += 1
        if self.fail_close:
            raise RuntimeError('close failed')

    def _write_table_listdata(self, data: ListDataSeq[CellT],
                              impl_meta: TableIO.ImplMetaForWrite) \
            -> Position:
        """Record list-data writes and return a predictable position."""
        self.events.append('write_table_listdata')
        self.last_list_write_data = [list(row) for row in data]
        self.last_list_impl_meta = impl_meta
        self.last_list_filtered_data_range = impl_meta.filtered_data_range
        self.last_list_write_box = impl_meta.box
        return Position(row=len(data) - 1, column=len(data[0]) - 1)

    def _write_heading(self, heading: str, level: int) -> Position:
        """Record heading writes and return a predictable position."""
        self.events.append('write_heading')
        self.last_heading = (heading, level)
        return Position(row=level, column=len(heading))

    def _write_table_fmtlistdata(self, data: FmtListData,
                                 impl_meta: TableIO.ImplMetaForWrite) \
            -> Position:
        """Record formatted list-data writes."""
        self.events.append('write_table_fmtlistdata')
        self.last_fmtlist_write_data = list(data)
        self.last_fmtlist_impl_meta = impl_meta
        self.last_fmtlist_filtered_data_range = impl_meta.filtered_data_range
        self.last_fmtlist_write_box = impl_meta.box
        return Position(row=len(data) - 1, column=len(data[0].values) - 1)

    def _write_table_dictdata(self, data: DictDataMap[CellT],
                              impl_meta: TableIO.ImplMetaForDictWrite) \
            -> Position:
        """Record dict-data writes and return a predictable position."""
        self.events.append('write_table_dictdata')
        self.last_dict_write_data = [dict(row) for row in data]
        self.last_dict_impl_meta = impl_meta
        self.last_column_order = list(impl_meta.column_order)
        self.last_dict_first_row_format = impl_meta.first_row_format
        self.last_dict_filtered_data_range = \
            impl_meta.common_impl.filtered_data_range
        self.last_dict_write_box = impl_meta.common_impl.box
        return Position(row=len(data), column=len(impl_meta.column_order) - 1)

    def _write_table_fmtdictdata(self, data: FmtDictData,
                                 impl_meta: TableIO.ImplMetaForDictWrite) \
            -> Position:
        """Record formatted dict-data writes."""
        self.events.append('write_table_fmtdictdata')
        self.last_fmtdict_write_data = list(data)
        self.last_fmtdict_impl_meta = impl_meta
        self.last_fmtdict_column_order = list(impl_meta.column_order)
        self.last_fmtdict_first_row_format = impl_meta.first_row_format
        self.last_fmtdict_filtered_data_range = \
            impl_meta.common_impl.filtered_data_range
        self.last_fmtdict_write_box = impl_meta.common_impl.box
        return Position(row=len(data), column=len(impl_meta.column_order) - 1)

    def _read_table_listdata(self, box: Box | None = None) -> \
            ReadResult[list[list[Value]]]:
        """Record list-data reads and return the prepared result."""
        self.events.append('read_table_listdata')
        self.last_list_read_box = box
        return self.list_read_result

    def _read_table_dictdata(self, box: Box | None = None) -> \
            ReadResult[list[dict[str, Value]]]:
        """Record dict-data reads and return the prepared result."""
        self.events.append('read_table_dictdata')
        self.last_dict_read_box = box
        return self.dict_read_result

    def _find_value(self, find_value: list[list[Value]],
                    type_conversion: bool = True,
                    box: Optional[Box] = None) -> Optional[Box]:
        """Record find-value calls and return the prepared result."""
        self.events.append('find_value')
        self.last_find_value = [list(row) for row in find_value]
        self.last_find_type_conversion = type_conversion
        self.last_find_box = box
        return self.find_result

    def _read_cells(self, box: Box) -> list[list[Value]]:
        """Record cell reads and return the prepared result."""
        self.events.append('read_cells')
        self.last_read_cells_box = box
        return self.read_cells_result

    def _write_cells(self, data: ListDataSeq[CellT], box: Box) -> None:
        """Record cell writes."""
        self.events.append('write_cells')
        self.last_write_cells_data = [list(row) for row in data]
        self.last_write_cells_box = box

    def check_listdimensions(self, data: ListDataSeq[CellT],
                             box: Box | None = None) -> None:
        """Expose list-dimension validation for tests."""
        self._check_listdimensions(data, box)

    def check_dictdimensions(self, data: DictDataMap[CellT],
                             box: Box | None = None) -> None:
        """Expose dict-dimension validation for tests."""
        self._check_dictdimensions(data, box)


class MinimalTableIO(TableIO):
    """Minimal subclass used to exercise inherited abstract methods."""

    def __init__(self, file_name: str | Path,
                 file_access: FileAccess = FileAccess.CREATE,
                 file_exists_callback:
                 Callable[[str], None] | None = None):
        """Initialize the minimal test double."""
        super().__init__(file_name, file_access, file_exists_callback)

    @classmethod
    def get_description(cls) -> Descriptor:
        """Return a descriptor that allows instantiation in tests."""
        caps = Capabilities()
        return Descriptor(format_name='minimal', implementation='test',
                          capabilities=caps, mandatory_args=['file_access'],
                          optional_args=[])

    @classmethod
    def get_capabilities(cls) -> Capabilities:
        """Return empty capabilities for the minimal implementation."""
        return Capabilities()

    @classmethod
    def file_name_extension(cls) -> str:
        """Return the file name extension used in tests."""
        return 'min'

    def run_end_state(self) -> None:
        """Expose the inherited _end_state method for tests."""
        self._end_state()

    def run_write_file_suffix(self) -> None:
        """Expose the inherited _write_file_suffix method for tests."""
        self._write_file_suffix()

    def run_close_hook(self) -> None:
        """Expose the inherited _close method for tests."""
        self._close()

    def run_write_heading(self, heading: str, level: int) -> Position:
        """Expose the inherited _write_heading method for tests."""
        return self._write_heading(heading, level)

    def run_write_table_listdata(self, data: ListDataSeq[CellT]) -> Position:
        """Expose the inherited _write_table_listdata method for tests."""
        impl_meta = TableIO.ImplMetaForWrite(filtered_data_range=False,
                                             box=None,
                                             borders=make_no_border_helper())
        return self._write_table_listdata(data, impl_meta)

    def run_write_table_fmtlistdata(self, data: FmtListData) -> Position:
        """Expose the inherited _write_table_fmtlistdata method."""
        impl_meta = TableIO.ImplMetaForWrite(filtered_data_range=False,
                                             box=None,
                                             borders=make_no_border_helper())
        return self._write_table_fmtlistdata(data, impl_meta)

    def run_write_table_dictdata(self, data: DictDataMap[CellT],
                                 column_order: list[str]) -> Position:
        """Expose the inherited _write_table_dictdata method for tests."""
        common_impl = TableIO.ImplMetaForWrite(filtered_data_range=False,
                                               box=None,
                                               borders=make_no_border_helper())
        impl_meta = TableIO.ImplMetaForDictWrite(common_impl=common_impl,
                                                 column_order=column_order,
                                                 first_row_format=None)
        return self._write_table_dictdata(data, impl_meta)

    def run_write_table_fmtdictdata(self, data: FmtDictData,
                                    column_order: list[str]) -> Position:
        """Expose the inherited _write_table_fmtdictdata method."""
        common_impl = TableIO.ImplMetaForWrite(filtered_data_range=False,
                                               box=None,
                                               borders=make_no_border_helper())
        impl_meta = TableIO.ImplMetaForDictWrite(common_impl=common_impl,
                                                 column_order=column_order,
                                                 first_row_format=None)
        return self._write_table_fmtdictdata(data, impl_meta)

    def run_read_table_listdata(self) -> ReadResult[list[list[Value]]]:
        """Expose the inherited _read_table_listdata method for tests."""
        return self._read_table_listdata()

    def run_read_table_dictdata(self) -> ReadResult[list[dict[str, Value]]]:
        """Expose the inherited _read_table_dictdata method for tests."""
        return self._read_table_dictdata()

    def run_find_value(self, find_value: list[list[Value]]) -> Optional[Box]:
        """Expose the inherited _find_value method for tests."""
        return self._find_value(find_value)

    def run_read_cells(self, box: Box) -> list[list[Value]]:
        """Expose the inherited _read_cells method for tests."""
        return self._read_cells(box)

    def run_write_cells(self, data: ListDataSeq[CellT], box: Box) -> None:
        """Expose the inherited _write_cells method for tests."""
        self._write_cells(data, box)


class WriteIgnoreBoxTableIO(RecordingTableIO):
    """Recording implementation that ignores write boxes."""

    capabilities = make_capabilities(
        can_write_box=make_capability(False, Strictness.IGNORE),
        can_read_box=make_capability(True, Strictness.STRICT))


class WriteStrictBoxTableIO(RecordingTableIO):
    """Recording implementation that rejects write boxes."""

    capabilities = make_capabilities(
        can_write_box=make_capability(False, Strictness.STRICT),
        can_read_box=make_capability(True, Strictness.STRICT))


class ReadIgnoreBoxTableIO(RecordingTableIO):
    """Recording implementation that ignores read boxes."""

    capabilities = make_capabilities(
        can_write_box=make_capability(True, Strictness.STRICT),
        can_read_box=make_capability(False, Strictness.IGNORE))


class ReadStrictBoxTableIO(RecordingTableIO):
    """Recording implementation that rejects read boxes."""

    capabilities = make_capabilities(
        can_write_box=make_capability(True, Strictness.STRICT),
        can_read_box=make_capability(False, Strictness.STRICT))


class WriteSupportedFilteredDataRangeTableIO(RecordingTableIO):
    """Recording implementation that supports filtered data ranges."""

    capabilities = make_capabilities(
        filtered_data_range=make_capability(True, Strictness.STRICT),
        can_write_box=make_capability(True, Strictness.STRICT),
        can_read_box=make_capability(True, Strictness.STRICT))


class WriteIgnoreFilteredDataRangeTableIO(RecordingTableIO):
    """Recording implementation that ignores filtered data ranges."""

    capabilities = make_capabilities(
        filtered_data_range=make_capability(False, Strictness.IGNORE),
        can_write_box=make_capability(True, Strictness.STRICT),
        can_read_box=make_capability(True, Strictness.STRICT))


class WriteStrictFilteredDataRangeTableIO(RecordingTableIO):
    """Recording implementation that rejects filtered data ranges."""

    capabilities = make_capabilities(
        filtered_data_range=make_capability(False, Strictness.STRICT),
        can_write_box=make_capability(True, Strictness.STRICT),
        can_read_box=make_capability(True, Strictness.STRICT))


def test_tableio_named_tuples_store_values_and_defaults(
        capsys: CaptureFixture[str]) -> None:
    """Test the public NamedTuple values in the tableio module."""
    caps = Capabilities()
    descriptor = Descriptor(format_name='csv', implementation='default',
                            capabilities=caps, mandatory_args=['path'],
                            optional_args=['mode'])
    box = Box(top=1, left=2, bottom=None, right=5)
    position = Position(row=3, column=4)
    impl_meta = TableIO.ImplMetaForWrite(filtered_data_range=True, box=box,
                                         borders=make_no_border_helper())
    dict_impl_meta = TableIO.ImplMetaForDictWrite(
        common_impl=impl_meta, column_order=['alpha', 'beta'],
        first_row_format=Fmt(bold=True))
    assert descriptor.priority == 10
    assert descriptor.format_name == 'csv'
    assert descriptor.implementation == 'default'
    assert descriptor.mandatory_args == ['path']
    assert descriptor.optional_args == ['mode']
    assert box == Box(1, 2, None, 5)
    assert position == Position(3, 4)
    assert impl_meta.filtered_data_range is True
    assert impl_meta.box == box
    assert dict_impl_meta.common_impl == impl_meta
    assert dict_impl_meta.column_order == ['alpha', 'beta']
    assert dict_impl_meta.first_row_format == Fmt(bold=True)
    check_capsys(capsys)


def test_tableio_init_adds_extension_and_stores_callback(
        capsys: CaptureFixture[str]) -> None:
    """Test initialization of a concrete TableIO implementation."""
    def file_exists_callback(file_name: str) -> None:
        """Accept the existing file name without side effects."""
        _ = file_name

    with TemporaryDirectory() as temp_dir:
        table_io = RecordingTableIO(Path(temp_dir) / 'sample',
                                    FileAccess.CREATE, file_exists_callback)
        assert table_io.file_name == str(Path(temp_dir) / 'sample.tio')
        assert table_io.file_access is FileAccess.CREATE
        assert table_io.file_exists_callback is file_exists_callback
        assert table_io.heading_written is False
    check_capsys(capsys)


def test_tableio_init_create_rejects_existing_file_without_callback(
        capsys: CaptureFixture[str]) -> None:
    """Test CREATE mode when the target file already exists."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'sample'
        Path(f'{file_name}.tio').touch()
        with pytest.raises(FileExistsError, match='refusing to overwrite'):
            RecordingTableIO(file_name, FileAccess.CREATE)
    check_capsys(capsys)


def test_tableio_init_create_calls_callback_for_existing_file(
        capsys: CaptureFixture[str]) -> None:
    """Test CREATE mode with a callback that allows overwriting."""
    calls: list[str] = []

    def file_exists_callback(file_name: str) -> None:
        """Record the file name passed to the overwrite callback."""
        calls.append(file_name)

    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'sample'
        expected_name = str(Path(temp_dir) / 'sample.tio')
        Path(expected_name).touch()
        table_io = RecordingTableIO(file_name, FileAccess.CREATE,
                                    file_exists_callback)
        assert table_io.file_name == expected_name
    assert calls == [expected_name]
    check_capsys(capsys)


def test_tableio_init_create_propagates_callback_exception(
        capsys: CaptureFixture[str]) -> None:
    """Test CREATE mode when the overwrite callback rejects the file."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'sample'
        Path(f'{file_name}.tio').touch()

        def file_exists_callback(callback_file_name: str) -> None:
            """Reject the overwrite request with a custom error."""
            raise RuntimeError(f'blocked: {callback_file_name}')
        with pytest.raises(RuntimeError, match='blocked: .*sample.tio'):
            RecordingTableIO(file_name, FileAccess.CREATE,
                             file_exists_callback)
    check_capsys(capsys)


@pytest.mark.parametrize(
    'file_access',
    [pytest.param(FileAccess.READ, id='read'),
     pytest.param(FileAccess.UPDATE, id='update')])
def test_tableio_init_read_and_update_require_existing_file(
        file_access: FileAccess, capsys: CaptureFixture[str]) -> None:
    """Test READ and UPDATE modes when the target file is missing."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'sample'
        with pytest.raises(FileNotFoundError, match='File does not exist'):
            RecordingTableIO(file_name, file_access)
    check_capsys(capsys)


@pytest.mark.parametrize(
    'file_access',
    [pytest.param(FileAccess.READ, id='read'),
     pytest.param(FileAccess.UPDATE, id='update')])
def test_tableio_init_read_and_update_ignore_callback(
        file_access: FileAccess, capsys: CaptureFixture[str]) -> None:
    """Test READ and UPDATE modes with an existing file and a callback."""
    calls: list[str] = []

    def file_exists_callback(file_name: str) -> None:
        """Record if READ or UPDATE ever uses the overwrite callback."""
        calls.append(file_name)

    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'sample'
        expected_name = str(Path(temp_dir) / 'sample.tio')
        Path(expected_name).touch()
        table_io = RecordingTableIO(file_name, file_access,
                                    file_exists_callback)
        assert table_io.file_name == expected_name
        assert table_io.file_access is file_access
    assert not calls
    check_capsys(capsys)


def test_tableio_context_manager_opens_and_closes_once(
        capsys: CaptureFixture[str]) -> None:
    """Test the success path for the context-manager protocol."""
    table_io = RecordingTableIO('sample')
    with table_io as entered_table:
        assert entered_table is table_io
        assert table_io.events == ['open']
    assert table_io.events == [
        'open',
        'end_state',
        'write_file_suffix',
        'close'
    ]
    assert table_io.close_count == 1
    check_capsys(capsys)


def test_tableio_context_manager_preserves_block_exception(
        capsys: CaptureFixture[str]) -> None:
    """Test that close errors are added as notes to block exceptions."""
    table_io = RecordingTableIO('sample')
    table_io.fail_close = True
    with pytest.raises(RuntimeError, match='block failed') as exc_info:
        with table_io:
            raise RuntimeError('block failed')
    assert table_io.events == [
        'open',
        'end_state',
        'write_file_suffix',
        'close'
    ]
    assert table_io.close_count == 1
    assert exc_info.value.__notes__ == [
        'Additionally, close() raised: close failed'
    ]
    check_capsys(capsys)


def test_close_calls_close_once_after_success(
        capsys: CaptureFixture[str]) -> None:
    """Test that close runs its hooks once in order on success."""
    table_io = RecordingTableIO('sample')
    table_io.close()
    assert table_io.events == ['end_state', 'write_file_suffix', 'close']
    assert table_io.close_count == 1
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('fail_attr', 'expected_events', 'expected_error'),
    [
        pytest.param('fail_end_state', ['end_state', 'close'],
                     'end_state failed', id='end-state'),
        pytest.param('fail_write_file_suffix',
                     ['end_state', 'write_file_suffix', 'close'],
                     'write_file_suffix failed', id='write-file-suffix')
    ])
def test_close_calls_close_once_when_finalize_fails(
        fail_attr: str, expected_events: list[str], expected_error: str,
        capsys: CaptureFixture[str]) -> None:
    """Test that close still closes once when finishing the file fails."""
    table_io = RecordingTableIO('sample')
    setattr(table_io, fail_attr, True)
    with pytest.raises(RuntimeError, match=expected_error):
        table_io.close()
    assert table_io.events == expected_events
    assert table_io.close_count == 1
    check_capsys(capsys)


def test_close_keeps_finalize_error_primary_when_close_also_fails(
        capsys: CaptureFixture[str]) -> None:
    """Test that cleanup close errors become notes on the primary error."""
    table_io = RecordingTableIO('sample')
    table_io.fail_end_state = True
    table_io.fail_close = True
    with pytest.raises(RuntimeError, match='end_state failed') as exc_info:
        table_io.close()
    assert table_io.events == ['end_state', 'close']
    assert table_io.close_count == 1
    assert exc_info.value.__notes__ == [
        'Additionally, _close() raised: close failed'
    ]
    check_capsys(capsys)


def test_write_heading_uses_default_levels(
        capsys: CaptureFixture[str]) -> None:
    """Test default heading levels for the first and later headings."""
    table_io = RecordingTableIO('sample')
    first_position = table_io.write_heading('First')
    second_position = table_io.write_heading('Second')
    assert first_position == Position(1, 5)
    assert second_position == Position(2, 6)
    assert table_io.last_heading == ('Second', 2)
    assert table_io.heading_written is True
    assert table_io.events == ['write_heading', 'write_heading']
    check_capsys(capsys)


def test_write_heading_passes_explicit_level(
        capsys: CaptureFixture[str]) -> None:
    """Test that an explicit heading level is passed through unchanged."""
    table_io = RecordingTableIO('sample')
    position = table_io.write_heading('Third', level=3)
    assert position == Position(3, 5)
    assert table_io.last_heading == ('Third', 3)
    assert table_io.heading_written is True
    check_capsys(capsys)


@pytest.mark.parametrize('level', [0, 4])
def test_write_heading_rejects_out_of_range_levels(
        level: int, capsys: CaptureFixture[str]) -> None:
    """Test heading-level validation."""
    table_io = RecordingTableIO('sample')
    with pytest.raises(ValueError, match='range 1 to 3'):
        table_io.write_heading('Bad', level=level)
    assert table_io.heading_written is False
    assert not table_io.events
    check_capsys(capsys)


def test_write_table_listdata_delegates_valid_data_and_box(
        capsys: CaptureFixture[str]) -> None:
    """Test list-data writes through the public base-class method."""
    table_io = RecordingTableIO('sample')
    box = Box(top=3, left=4, bottom=5, right=6)
    position = table_io.write_table_listdata([['alpha', 1], [None, 2.5]],
                                             box=box)
    assert position == Position(1, 1)
    assert table_io.last_list_write_data == [['alpha', 1], [None, 2.5]]
    assert table_io.last_list_filtered_data_range is False
    assert table_io.last_list_write_box == box
    assert table_io.events == ['write_table_listdata']
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('data', 'box', 'expected_error'),
    [
        pytest.param([], None, 'Data is empty', id='empty-data'),
        pytest.param([[]], None, 'First row is empty', id='empty-first-row'),
        pytest.param([['only']], None, 'Data is not at least 2 cells in size',
                     id='one-cell'),
        pytest.param([['left', 1], ['right']], None,
                     'All rows must have the same number of columns',
                     id='ragged'),
        pytest.param([['left', 1], ['right', 2]], Box(0, 0, 1, None),
                     'Wrong number of rows', id='too-many-rows'),
        pytest.param([['left', 1], ['right', 2]], Box(0, 0, None, 1),
                     'Wrong number of columns', id='too-many-columns')
    ])
def test_check_listdimensions_rejects_invalid_shapes(
        data: list[list[Value]], box: Box | None, expected_error: str,
        capsys: CaptureFixture[str]) -> None:
    """Test list-dimension validation."""
    table_io = RecordingTableIO('sample')
    with pytest.raises(ValueError, match=expected_error):
        table_io.check_listdimensions(data, box)
    check_capsys(capsys)


@pytest.mark.parametrize(
    'data',
    [
        pytest.param([['left', 1]], id='single-row-two-columns'),
        pytest.param([['left'], [1]], id='two-rows-single-column')
    ])
def test_check_listdimensions_accepts_minimum_table_size(
        data: list[list[Value]], capsys: CaptureFixture[str]) -> None:
    """Test the minimum valid list-table shapes."""
    table_io = RecordingTableIO('sample')
    table_io.check_listdimensions(data)
    check_capsys(capsys)


def test_write_table_dictdata_normalizes_and_delegates(
        capsys: CaptureFixture[str]) -> None:
    """Test dict-data writes through the public base-class method."""
    table_io = RecordingTableIO('sample')
    box = Box(top=5, left=2, bottom=8, right=4)
    first_row_format = Fmt(bold=True)
    position = table_io.write_table_dictdata(
        [{'alpha': 'left', 'extra': 1}, {'beta': 2.5}], ['alpha', 'beta'],
        first_row_format=first_row_format, missing_ok=True, extra_ok=True,
        filtered_data_range=False, box=box)
    assert position == Position(2, 1)
    assert table_io.last_dict_write_data == [
        {'alpha': 'left', 'beta': None},
        {'alpha': None, 'beta': 2.5}
    ]
    assert table_io.last_column_order == ['alpha', 'beta']
    assert table_io.last_dict_first_row_format == first_row_format
    assert table_io.last_dict_filtered_data_range is False
    assert table_io.last_dict_write_box == box
    assert table_io.events == ['write_table_dictdata']
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('data', 'box', 'expected_error'),
    [
        pytest.param([], None, 'Data is empty', id='empty-data'),
        pytest.param([{}], None, 'First row is empty', id='empty-first-row'),
        pytest.param([{'alpha': 'only'}], None,
                     'Data is not at least 2 cells in size', id='one-cell'),
        pytest.param([{'alpha': 'left', 'beta': 1}], Box(0, 0, 1, None),
                     'Wrong number of rows', id='too-many-rows'),
        pytest.param([{'alpha': 'left', 'beta': 1}], Box(0, 0, None, 1),
                     'Wrong number of columns', id='too-many-columns')
    ])
def test_check_dictdimensions_rejects_invalid_shapes(
        data: list[dict[str, Value]], box: Box | None, expected_error: str,
        capsys: CaptureFixture[str]) -> None:
    """Test dict-dimension validation."""
    table_io = RecordingTableIO('sample')
    with pytest.raises(ValueError, match=expected_error):
        table_io.check_dictdimensions(data, box)
    check_capsys(capsys)


@pytest.mark.parametrize(
    'data',
    [
        pytest.param([{'alpha': 'left', 'beta': 1}], id='single-row'),
        pytest.param([{'alpha': 'left'}, {'alpha': 'right'}],
                     id='two-rows-single-column')
    ])
def test_check_dictdimensions_accepts_minimum_table_size(
        data: list[dict[str, Value]], capsys: CaptureFixture[str]) -> None:
    """Test the minimum valid dict-table shapes."""
    table_io = RecordingTableIO('sample')
    table_io.check_dictdimensions(data)
    check_capsys(capsys)


def test_write_table_listdata_passes_filtered_data_range_when_supported(
        capsys: CaptureFixture[str]) -> None:
    """Test list-data writes with filtered data range enabled."""
    table_io = WriteSupportedFilteredDataRangeTableIO('sample')
    data: list[list[Value]] = [['alpha', 1]]
    position = table_io.write_table_listdata(data, True)
    assert position == Position(0, 1)
    assert table_io.last_list_write_data == data
    assert table_io.last_list_filtered_data_range is True
    assert table_io.last_list_write_box is None
    check_capsys(capsys)


def test_write_table_dictdata_passes_filtered_data_range_when_supported(
        capsys: CaptureFixture[str]) -> None:
    """Test dict-data writes with filtered data range enabled."""
    table_io = WriteSupportedFilteredDataRangeTableIO('sample')
    data: list[dict[str, Value]] = [{'alpha': 'left', 'beta': 1}]
    position = table_io.write_table_dictdata(data, ['alpha', 'beta'],
                                             filtered_data_range=True)
    assert position == Position(1, 1)
    assert table_io.last_dict_write_data == data
    assert table_io.last_dict_filtered_data_range is True
    assert table_io.last_dict_write_box is None
    check_capsys(capsys)


def test_write_table_listdata_ignores_box_when_supported_is_ignore(
        capsys: CaptureFixture[str]) -> None:
    """Test that write-box requests can be ignored by capability policy."""
    table_io = WriteIgnoreBoxTableIO('sample')
    box = Box(1, 1, 2, 3)
    data: list[list[Value]] = [['alpha', 1]]
    position = table_io.write_table_listdata(data, box=box)
    assert position == Position(0, 1)
    assert table_io.last_list_write_box is None
    assert table_io.last_list_write_data == data
    check_capsys(capsys)


def test_write_table_listdata_rejects_box_when_supported_is_strict(
        capsys: CaptureFixture[str]) -> None:
    """Test the write-specific box error message for strict support."""
    table_io = WriteStrictBoxTableIO('sample')
    data: list[list[Value]] = [['alpha', 1]]
    with pytest.raises(CapabilityNotSupported) as exc_info:
        table_io.write_table_listdata(data, box=Box(1, 1, 2, 3))
    assert exc_info.value.action == 'write to a box'
    assert not table_io.events
    check_capsys(capsys)


def test_write_cells_rejects_box_when_supported_is_strict(
        capsys: CaptureFixture[str]) -> None:
    """Test the write-cells box error message for strict support."""
    table_io = WriteStrictBoxTableIO('sample')
    data: list[list[Value]] = [['alpha', 1]]
    with pytest.raises(CapabilityNotSupported) as exc_info:
        table_io.write_cells(data, Box(1, 1, 2, 3))
    assert exc_info.value.action == 'Writing to a box is not supported'
    assert not table_io.events
    check_capsys(capsys)


def test_write_table_listdata_ignores_filtered_data_range_when_allowed(
        capsys: CaptureFixture[str]) -> None:
    """Test that filtered data range requests can be ignored."""
    table_io = WriteIgnoreFilteredDataRangeTableIO('sample')
    data: list[list[Value]] = [['alpha', 1]]
    position = table_io.write_table_listdata(data, True)
    assert position == Position(0, 1)
    assert table_io.last_list_filtered_data_range is False
    assert table_io.last_list_write_data == data
    check_capsys(capsys)


def test_write_table_listdata_rejects_filtered_data_range_when_strict(
        capsys: CaptureFixture[str]) -> None:
    """Test strict rejection when filtered data ranges are unsupported."""
    table_io = WriteStrictFilteredDataRangeTableIO('sample')
    data: list[list[Value]] = [['alpha', 1]]
    with pytest.raises(CapabilityNotSupported) as exc_info:
        table_io.write_table_listdata(data, True)
    assert exc_info.value.action == 'write a filtered data range'
    assert not table_io.events
    check_capsys(capsys)


def test_read_table_listdata_delegates_and_returns_result(
        capsys: CaptureFixture[str]) -> None:
    """Test list-data reads through the public base-class method."""
    table_io = RecordingTableIO('sample')
    box = Box(top=2, left=3, bottom=4, right=5)
    result = table_io.read_table_listdata(box)
    assert result == table_io.list_read_result
    assert table_io.last_list_read_box == box
    assert table_io.events == ['read_table_listdata']
    check_capsys(capsys)


def test_read_table_listdata_ignores_box_when_supported_is_ignore(
        capsys: CaptureFixture[str]) -> None:
    """Test that read-box requests can be ignored by capability policy."""
    table_io = ReadIgnoreBoxTableIO('sample')
    result = table_io.read_table_listdata(Box(1, 1, 3, 3))
    assert result == table_io.list_read_result
    assert table_io.last_list_read_box is None
    check_capsys(capsys)


def test_read_table_dictdata_rejects_box_when_supported_is_strict(
        capsys: CaptureFixture[str]) -> None:
    """Test the read-specific box error message for strict support."""
    table_io = ReadStrictBoxTableIO('sample')
    with pytest.raises(CapabilityNotSupported) as exc_info:
        table_io.read_table_dictdata(Box(1, 1, 3, 3))
    assert exc_info.value.action == 'read from a box'
    assert not table_io.events
    check_capsys(capsys)


def test_read_table_dictdata_delegates_and_returns_result(
        capsys: CaptureFixture[str]) -> None:
    """Test dict-data reads through the public base-class method."""
    table_io = RecordingTableIO('sample')
    box = Box(top=2, left=3, bottom=4, right=5)
    result = table_io.read_table_dictdata(box)
    assert result == table_io.dict_read_result
    assert table_io.last_dict_read_box == box
    assert table_io.events == ['read_table_dictdata']
    check_capsys(capsys)


def test_find_value_normalizes_scalar_and_delegates(
        capsys: CaptureFixture[str]) -> None:
    """Test scalar find requests through the public base-class method."""
    table_io = RecordingTableIO('sample')
    result_box = Box(top=4, left=5, bottom=5, right=6)
    table_io.find_result = result_box
    box = Box(top=2, left=3, bottom=8, right=9)
    result = table_io.find_value('alpha', type_conversion=False, box=box)
    assert result == result_box
    assert table_io.last_find_value == [['alpha']]
    assert table_io.last_find_type_conversion is False
    assert table_io.last_find_box == box
    assert table_io.events == ['find_value']
    check_capsys(capsys)


def test_find_value_normalizes_rectangular_values(
        capsys: CaptureFixture[str]) -> None:
    """Test rectangular find requests through the public base-class method."""
    table_io = RecordingTableIO('sample')
    result_box = Box(top=1, left=1, bottom=3, right=3)
    table_io.find_result = result_box
    result = table_io.find_value([['id', 1], ['name', 'Alice']])
    assert result == result_box
    assert table_io.last_find_value == [['id', 1], ['name', 'Alice']]
    assert table_io.last_find_type_conversion is True
    assert table_io.last_find_box is None
    check_capsys(capsys)


def test_find_value_rejects_invalid_rectangular_shape(
        capsys: CaptureFixture[str]) -> None:
    """Test find-value validation for ragged value grids."""
    table_io = RecordingTableIO('sample')
    with pytest.raises(ValueError, match='All rows must have the same'):
        table_io.find_value([['left', 1], ['right']])
    assert not table_io.events
    check_capsys(capsys)


def test_read_cells_delegates_and_returns_result(
        capsys: CaptureFixture[str]) -> None:
    """Test exact cell reads through the public base-class method."""
    table_io = RecordingTableIO('sample')
    table_io.read_cells_result = [['alpha', 1], ['beta', 2]]
    box = Box(top=2, left=3, bottom=4, right=5)
    result = table_io.read_cells(box)
    assert result == [['alpha', 1], ['beta', 2]]
    assert table_io.last_read_cells_box == box
    assert table_io.events == ['read_cells']
    check_capsys(capsys)


def test_read_cells_rejects_open_ended_box(
        capsys: CaptureFixture[str]) -> None:
    """Test read-cells validation for incomplete boxes."""
    table_io = RecordingTableIO('sample')
    with pytest.raises(ValueError, match='must be not None'):
        table_io.read_cells(Box(top=0, left=0, bottom=None, right=2))
    assert not table_io.events
    check_capsys(capsys)


def test_write_cells_validates_and_delegates(
        capsys: CaptureFixture[str]) -> None:
    """Test exact cell writes through the public base-class method."""
    table_io = RecordingTableIO('sample')
    box = Box(top=2, left=3, bottom=4, right=5)
    data: list[list[Value]] = [['alpha', 1], ['beta', 2]]
    table_io.write_cells(data, box)
    assert table_io.last_write_cells_data == data
    assert table_io.last_write_cells_box == box
    assert table_io.events == ['write_cells']
    check_capsys(capsys)


def test_base_class_not_implemented_class_methods_raise(
        capsys: CaptureFixture[str]) -> None:
    """Test the inherited class-level abstract methods."""
    with pytest.raises(NotImplementedError, match='get_description'):
        TableIO.get_description()
    with pytest.raises(NotImplementedError, match='get_capabilities'):
        TableIO.get_capabilities()
    with pytest.raises(NotImplementedError, match='file_name_extension'):
        TableIO.file_name_extension()
    check_capsys(capsys)


def test_base_class_not_implemented_instance_methods_raise(
        capsys: CaptureFixture[str]) -> None:
    """Test the inherited instance-level abstract methods."""
    table_io = MinimalTableIO('sample')
    list_data: list[list[Value]] = [['alpha', 1]]
    fmt_list_data = [FmtListRow(values=('alpha', 1), fmt=Fmt(bold=True))]
    dict_data: list[dict[str, Value]] = [{'alpha': 'left', 'beta': 1}]
    fmt_dict_data = [
        FmtDictRow(values={'alpha': 'left', 'beta': 1}, fmt=Fmt(italic=True))
    ]
    with pytest.raises(NotImplementedError, match='open method'):
        table_io.open()
    with pytest.raises(NotImplementedError, match='_end_state method'):
        table_io.run_end_state()
    with pytest.raises(NotImplementedError, match='_write_file_suffix method'):
        table_io.run_write_file_suffix()
    with pytest.raises(NotImplementedError, match='_close method'):
        table_io.run_close_hook()
    with pytest.raises(NotImplementedError, match='_write_heading method'):
        table_io.run_write_heading('title', 1)
    with pytest.raises(NotImplementedError,
                       match='_write_table_listdata method'):
        table_io.run_write_table_listdata(list_data)
    with pytest.raises(NotImplementedError,
                       match='_write_table_fmtlistdata method'):
        table_io.run_write_table_fmtlistdata(fmt_list_data)
    with pytest.raises(NotImplementedError,
                       match='_write_table_dictdata method'):
        table_io.run_write_table_dictdata(dict_data, ['alpha', 'beta'])
    with pytest.raises(NotImplementedError,
                       match='_write_table_fmtdictdata method'):
        table_io.run_write_table_fmtdictdata(fmt_dict_data, ['alpha', 'beta'])
    with pytest.raises(NotImplementedError,
                       match='_read_table_listdata method'):
        table_io.run_read_table_listdata()
    with pytest.raises(NotImplementedError,
                       match='_read_table_dictdata method'):
        table_io.run_read_table_dictdata()
    with pytest.raises(NotImplementedError, match='_find_value method'):
        table_io.run_find_value([['alpha']])
    with pytest.raises(NotImplementedError, match='_read_cells method'):
        table_io.run_read_cells(Box(top=0, left=0, bottom=1, right=1))
    with pytest.raises(NotImplementedError, match='_write_cells method'):
        table_io.run_write_cells([['alpha']], Box(0, 0, 1, 1))
    check_capsys(capsys)
