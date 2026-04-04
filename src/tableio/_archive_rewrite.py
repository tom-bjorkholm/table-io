#! /usr/bin/env python3
"""Helpers for rewriting spreadsheet ZIP archives safely.

Spreadsheet writers first save library output to a temporary archive.
These helpers then build a rewritten copy in a second temporary archive
and replace the first archive only after both ZIP files are closed.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable, Optional
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


def temporary_output_path(source_path: Path, suffix: str) -> Path:
    """Return one missing temporary path next to ``source_path``.

    The temporary file is created in the same directory as
    ``source_path`` so a later ``Path.replace()`` stays on the same
    filesystem. The file name uses ``suffix`` and the returned path does
    not exist when this function returns.
    """
    with NamedTemporaryFile(delete=False, dir=source_path.parent,
                            suffix=suffix) as temp_file:
        temp_path = Path(temp_file.name)
    temp_path.unlink()
    return temp_path


def rewrite_zip_archive(
        archive_path: Path,
        rewrite_entry: Callable[[ZipInfo, bytes], Optional[bytes]],
        extra_entries: Optional[dict[str, bytes]] = None) -> None:
    """Rewrite one ZIP archive by copying it into a new archive.

    The original archive at ``archive_path`` is read entry by entry and
    a rewritten archive is written to a sibling temporary file. The
    callback receives each original ``ZipInfo`` together with its bytes.
    Returning ``None`` drops the entry. Any mapping passed in
    ``extra_entries`` is appended after copied entries, except for names
    that were already written.

    The original archive is replaced only after both ZIP files have been
    closed. This avoids replacing an archive while it is still open,
    which is a safer pattern on Windows as well as on Unix-like systems.

    Args:
        archive_path: Path to the archive to rewrite in place.
        rewrite_entry: Callback invoked once for each original ZIP entry.
            The callback receives the original ``ZipInfo`` together with
            the entry bytes. It returns replacement bytes for the output
            archive, or ``None`` to drop the entry completely.
        extra_entries: Optional mapping of extra archive members to add
            after copying rewritten entries. Names that were already
            written are left unchanged.
    """
    temp_path = temporary_output_path(archive_path, archive_path.suffix)
    try:
        with ZipFile(archive_path, 'r') as source_zip, \
                ZipFile(temp_path, 'w',
                        compression=ZIP_DEFLATED) as target_zip:
            written_names: set[str] = set()
            for item in source_zip.infolist():
                data = rewrite_entry(item, source_zip.read(item.filename))
                if data is None:
                    continue
                target_zip.writestr(item, data)
                written_names.add(item.filename)
            if extra_entries is not None:
                for entry_name, entry_data in extra_entries.items():
                    if entry_name in written_names:
                        continue
                    target_zip.writestr(entry_name, entry_data)
        temp_path.replace(archive_path)
    finally:
        if temp_path.exists():
            temp_path.unlink()
