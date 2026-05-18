#! /usr/bin/env python3
"""Tests for ZIP archive rewrite helpers."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional
from zipfile import ZipFile, ZipInfo

import pytest

from tableio._archive_rewrite import rewrite_zip_archive, \
    temporary_output_path


def _write_zip_file(file_path: Path, files: dict[str, bytes]) -> None:
    """Write one ZIP file containing the provided test files."""
    with ZipFile(file_path, 'w') as archive:
        for entry_name, entry_data in files.items():
            archive.writestr(entry_name, entry_data)


def test_temporary_output_path_returns_missing_sibling_path() -> None:
    """Test that the temporary path is missing and in the same folder."""
    with TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / 'example.xlsx'
        file_path.write_bytes(b'content')
        temp_path = temporary_output_path(file_path, '.xlsx')
        assert temp_path.parent == file_path.parent
        assert temp_path.suffix == '.xlsx'
        assert temp_path != file_path
        assert not temp_path.exists()


def test_rewrite_zip_archive_rewrites_and_removes_entries() -> None:
    """Test that ZIP entries can be rewritten and removed."""
    with TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / 'example.zip'
        _write_zip_file(
            file_path,
            {'keep.txt': b'keep', 'change.txt': b'lower',
             'remove.txt': b'remove'})

        def rewrite_entry(item: ZipInfo, data: bytes) -> Optional[bytes]:
            """Rewrite one test entry when needed."""
            if item.filename == 'change.txt':
                return data.upper()
            if item.filename == 'remove.txt':
                return None
            return data

        rewrite_zip_archive(file_path, rewrite_entry)
        with ZipFile(file_path, 'r') as archive:
            assert set(archive.namelist()) == {'keep.txt', 'change.txt'}
            assert archive.read('keep.txt') == b'keep'
            assert archive.read('change.txt') == b'LOWER'


def test_rewrite_zip_archive_adds_extra_entries() -> None:
    """Test that missing extra entries are appended to the archive."""
    with TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / 'example.zip'
        _write_zip_file(file_path, {'keep.txt': b'keep'})

        def rewrite_entry(_item: ZipInfo, data: bytes) -> Optional[bytes]:
            """Keep every existing entry unchanged."""
            return data

        rewrite_zip_archive(file_path, rewrite_entry,
                            {'keep.txt': b'new-value', 'extra.txt': b'extra'})
        with ZipFile(file_path, 'r') as archive:
            assert set(archive.namelist()) == {'keep.txt', 'extra.txt'}
            assert archive.read('keep.txt') == b'keep'
            assert archive.read('extra.txt') == b'extra'


def test_rewrite_zip_archive_removes_temp_file_after_failure() -> None:
    """Test that failed rewrites remove the temporary sibling archive."""
    with TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / 'example.zip'
        _write_zip_file(file_path, {'keep.txt': b'keep'})

        def rewrite_entry(_item: ZipInfo, _data: bytes) -> Optional[bytes]:
            """Fail after the temporary target archive has been created."""
            raise RuntimeError('rewrite failure')

        with pytest.raises(RuntimeError, match='rewrite failure'):
            rewrite_zip_archive(file_path, rewrite_entry)
        assert [path.name for path in Path(temp_dir).iterdir()] == [
            'example.zip'
        ]
        with ZipFile(file_path, 'r') as archive:
            assert archive.read('keep.txt') == b'keep'
