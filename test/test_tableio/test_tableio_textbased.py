#! /usr/local/bin/python3
"""Tests for the tableio_textbased module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import io
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Callable

import pytest
from pytest import CaptureFixture

from tableio.capability import Capabilities
from tableio.tableio import Descriptor, FileAccess
from tableio.tableio_textbased import TableIOTextBased

from .check_capsys import check_capsys


class RecordingTextBasedTableIO(TableIOTextBased):
    """Concrete TableIOTextBased implementation used in tests."""

    def __init__(self, file_name: str | Path,
                 file_access: FileAccess = FileAccess.CREATE,
                 file_exists_callback:
                 Callable[[str], None] | None = None,
                 character_encoding: str = 'utf-8'):
        """Initialize the recording text-based test double."""
        super().__init__(file_name=file_name, file_access=file_access,
                         file_exists_callback=file_exists_callback,
                         character_encoding=character_encoding)
        self.events: list[str] = []

    @classmethod
    def get_desciption(cls) -> Descriptor:
        """Return the descriptor for the recording implementation."""
        return Descriptor(
            format_name='textbased',
            implementation='test',
            capabilities=Capabilities(),
            mandatory_args=['file_access'],
            optional_args=['file_exists_callback', 'character_encoding']
        )

    @classmethod
    def get_capabilities(cls) -> Capabilities:
        """Return empty capabilities for the recording implementation."""
        return Capabilities()

    @classmethod
    def file_name_extension(cls) -> str:
        """Return the file name extension used in tests."""
        return 'txtb'

    def _end_state(self) -> None:
        """Record the end-state hook."""
        self.events.append('end_state')

    def _write_file_suffix(self) -> None:
        """Record the file-suffix hook."""
        self.events.append('write_file_suffix')

    def write_text(self, text: str) -> int:
        """Write text through the inherited file object."""
        assert self.file is not None
        return self.file.write(text)

    def read_from_start(self) -> str:
        """Read the whole file from the beginning."""
        assert self.file is not None
        self.file.seek(0, io.SEEK_SET)
        return self.file.read()

    def seek_to_end(self) -> None:
        """Seek to the end of the file."""
        assert self.file is not None
        self.file.seek(0, io.SEEK_END)

    def tell(self) -> int:
        """Return the current file position."""
        assert self.file is not None
        return self.file.tell()

    def get_last_chars_written(self, num_chars: int) -> str:
        """Expose the inherited tail-reading helper for tests."""
        return self._get_last_chars_written(num_chars)

    def ensure_empty_line_before(self) -> None:
        """Expose the inherited empty-line helper for tests."""
        self._ensure_empty_line_before()


def test_textbased_init_stores_default_callback_and_encoding(
        capsys: CaptureFixture[str]) -> None:
    """Test initialization defaults specific to TableIOTextBased."""
    with TemporaryDirectory() as temp_dir:
        table_io = RecordingTextBasedTableIO(Path(temp_dir) / 'sample')
        assert table_io.file_name == str(Path(temp_dir) / 'sample.txtb')
        assert table_io.file_exists_callback is None
        assert table_io.character_encoding == 'utf-8'
        assert table_io.file is None
    check_capsys(capsys)


def test_textbased_open_read_mode_is_read_only(
        capsys: CaptureFixture[str]) -> None:
    """Test that READ mode opens a read-only text file."""
    with TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / 'sample.txtb'
        file_path.write_text('alpha', encoding='utf-8')
        table_io = RecordingTextBasedTableIO(
            Path(temp_dir) / 'sample',
            FileAccess.READ)
        with table_io:
            assert table_io.file is not None
            assert table_io.file.readable() is True
            assert table_io.file.writable() is False
            assert table_io.read_from_start() == 'alpha'
            with pytest.raises(io.UnsupportedOperation):
                table_io.write_text('beta')
        assert table_io.file is None
    check_capsys(capsys)


def test_textbased_open_create_mode_supports_read_after_write(
        capsys: CaptureFixture[str]) -> None:
    """Test that CREATE mode allows reading data after writing it."""
    with TemporaryDirectory() as temp_dir:
        file_name = Path(temp_dir) / 'sample'
        table_io = RecordingTextBasedTableIO(file_name, FileAccess.CREATE)
        with table_io:
            assert table_io.file is not None
            assert table_io.file.readable() is True
            assert table_io.file.writable() is True
            table_io.write_text('alpha')
            assert table_io.read_from_start() == 'alpha'
        assert (Path(temp_dir) / 'sample.txtb').read_text(
            encoding='utf-8') == 'alpha'
    check_capsys(capsys)


def test_textbased_open_update_mode_supports_read_and_write(
        capsys: CaptureFixture[str]) -> None:
    """Test that UPDATE mode allows reading and then appending text."""
    with TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / 'sample.txtb'
        file_path.write_text('alpha', encoding='utf-8')
        table_io = RecordingTextBasedTableIO(
            Path(temp_dir) / 'sample',
            FileAccess.UPDATE)
        with table_io:
            assert table_io.read_from_start() == 'alpha'
            table_io.seek_to_end()
            table_io.write_text('\nbeta')
        assert file_path.read_text(encoding='utf-8') == 'alpha\nbeta'
    check_capsys(capsys)


def test_textbased_open_rejects_second_open(
        capsys: CaptureFixture[str]) -> None:
    """Test that opening the same instance twice raises an error."""
    with TemporaryDirectory() as temp_dir:
        table_io = RecordingTextBasedTableIO(Path(temp_dir) / 'sample')
        table_io.open()
        with pytest.raises(RuntimeError, match='already open'):
            table_io.open()
        table_io.close()
        assert table_io.file is None
    check_capsys(capsys)


def test_textbased_get_last_chars_written_preserves_position(
        capsys: CaptureFixture[str]) -> None:
    """Test tail reading for ASCII text while keeping the write position."""
    with TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / 'sample.txtb'
        table_io = RecordingTextBasedTableIO(
            Path(temp_dir) / 'sample',
            FileAccess.CREATE)
        with table_io:
            table_io.write_text('abcdef')
            current_pos = table_io.tell()
            assert table_io.get_last_chars_written(3) == 'def'
            assert table_io.tell() == current_pos
            table_io.write_text('g')
        assert file_path.read_text(encoding='utf-8') == 'abcdefg'
    check_capsys(capsys)


def test_textbased_get_last_chars_written_handles_utf8_multibyte_text(
        capsys: CaptureFixture[str]) -> None:
    """Test tail reading for multibyte UTF-8 text."""
    with TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / 'sample.txtb'
        table_io = RecordingTextBasedTableIO(
            Path(temp_dir) / 'sample',
            FileAccess.CREATE)
        with table_io:
            table_io.write_text('A😀åäö')
            current_pos = table_io.tell()
            assert table_io.get_last_chars_written(4) == '😀åäö'
            assert table_io.tell() == current_pos
            table_io.write_text('!')
        assert file_path.read_text(encoding='utf-8') == 'A😀åäö!'
    check_capsys(capsys)


def test_textbased_get_last_chars_written_returns_whole_short_file(
        capsys: CaptureFixture[str]) -> None:
    """Test tail reading when fewer characters exist than requested."""
    with TemporaryDirectory() as temp_dir:
        table_io = RecordingTextBasedTableIO(
            Path(temp_dir) / 'sample',
            FileAccess.CREATE)
        with table_io:
            table_io.write_text('hi')
            assert table_io.get_last_chars_written(5) == 'hi'
    check_capsys(capsys)


@pytest.mark.parametrize(
    ('initial_text', 'expected_text'),
    [
        pytest.param('', 'beta', id='empty-file'),
        pytest.param('alpha', 'alpha\n\nbeta', id='no-trailing-newline'),
        pytest.param('alpha\n', 'alpha\n\nbeta', id='single-newline'),
        pytest.param('alpha\n\n', 'alpha\n\nbeta', id='already-empty-line'),
        pytest.param('åäö', 'åäö\n\nbeta', id='multibyte-text')
    ]
)
def test_textbased_ensure_empty_line_before(
        initial_text: str, expected_text: str,
        capsys: CaptureFixture[str]) -> None:
    """Test inserting exactly one empty line before appended text."""
    with TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / 'sample.txtb'
        table_io = RecordingTextBasedTableIO(
            Path(temp_dir) / 'sample',
            FileAccess.CREATE)
        with table_io:
            table_io.write_text(initial_text)
            table_io.ensure_empty_line_before()
            table_io.write_text('beta')
        assert file_path.read_text(encoding='utf-8') == expected_text
    check_capsys(capsys)
