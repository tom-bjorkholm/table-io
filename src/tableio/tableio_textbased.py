#! /usr/bin/env python3
"""Reader/writer base class for a text-based file format."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import io
from typing import Optional, Callable
from mformat.mformat import PathLike
from tableio.tableio import TableIO, FileAccess


_OPEN_MODES: dict[FileAccess, str] = {
    FileAccess.READ: 'rt',
    FileAccess.CREATE: 'wt+',
    FileAccess.UPDATE: 'rt+'
}


class TableIOTextBased(TableIO):
    """Reader/writer base class for a text-based file format.

    This intermediate base class for text-based formats exists
    so that common functionality for text-based formats can be implemented
    in a single place.
    """

    def __init__(self, file_name: PathLike,
                 file_access: FileAccess,
                 file_exists_callback: Optional[Callable[[str], None]] = None,
                 character_encoding: str = 'utf-8'):
        """Initialize the TableIOTextBased reader/writer class."""
        super().__init__(file_name=file_name, file_access=file_access,
                         file_exists_callback=file_exists_callback)
        self.file: Optional[io.TextIOWrapper] = None
        self.character_encoding: str = character_encoding

    def open(self) -> None:
        """Open the file.

        Avoid using this method directly.
        Use derived class as a context manager instead, using a with statement.
        """
        if self.file is not None:
            raise RuntimeError(f'File {self.file_name} already open')
        file = open(file=self.file_name,  # pylint: disable=consider-using-with
                    mode=_OPEN_MODES[self.file_access],
                    encoding=self.character_encoding)
        assert isinstance(file, io.TextIOWrapper)
        self.file = file

    def _close(self) -> None:
        """Close the file.

        Avoid using this method directly.
        Use derived class as a context manager instead, using a with statement.
        """
        if self.file is not None:
            self.file.close()
            self.file = None

    def _get_last_chars_written_impl(self, num_chars: int, end_pos: int,
                                     rec_count: int) -> str:
        """Get the last characters written to the file.

        This is an implementation detail of the _get_last_chars_written method.
        Keep the file pointer at the same position, i.e. (normally) at the
        end of the file, so that we can continue writing after the last
        characters.
        Returns the last characters written to the file.
        As utf-8 encode characters may be 1-6 bytes long, we need to read
        more than num_chars characters to get the last characters.
        (On Microsoft Windows the newline character is 2 bytes long CR/LF.)
        If we start reading bytes that are in the middle of a character,
        the utf-8 decoder will raise and exception. If we read 6 bytes for
        every character we are guaranteed to get the last characters.
        If the reading happens to be in the middle of a character it will
        be a character before the characters we are looking for. If
        decoding fails we will try again with a larger number of bytes,
        to try to find a place in the file where some preceeding character
        starts.
        Args:
            num_chars: The number of characters to get.
            end_pos: The position at end of file to start reading from.
            rec_count: The number of recursive calls.
        Returns:
            The last characters written to the file.
        """
        assert self.file is not None
        assert num_chars > 0
        if rec_count > 8:  # pragma: no cover
            # Limit 8 is bigger than longest utf-8 encoded character (6 bytes)
            return ''
        number_of_bytes = min(num_chars * 6 + rec_count, end_pos)
        self.file.seek(end_pos - number_of_bytes, io.SEEK_SET)
        try:
            last_chars = self.file.read(number_of_bytes)
        except UnicodeDecodeError:
            return self._get_last_chars_written_impl(num_chars, end_pos,
                                                     rec_count + 1)
        self.file.seek(end_pos, io.SEEK_SET)
        return last_chars[-num_chars:]

    def _get_last_chars_written(self, num_chars: int) -> str:
        """Get the last characters written to the file.

        Keep the file pointer at the same position, i.e. at the end of the
        file, so that we can continue writing after the last characters.
        Returns the last characters written to the file.
        """
        assert self.file is not None
        assert num_chars > 0
        cur_pos = self.file.tell()
        last_chars = self._get_last_chars_written_impl(num_chars, cur_pos, 0)
        self.file.seek(cur_pos, io.SEEK_SET)
        return last_chars

    def _ensure_empty_line_before(self) -> int:
        """Ensure an empty line before the write position.

        If we are at the beginning of the file do nothing.
        If we have an empty line before the current position do nothing.
        Otherwise insert an empty line before the current position.
        Returns the number of new lines inserted.
        """
        assert self.file is not None
        last_chars = self._get_last_chars_written(2)
        if last_chars in ('\n\n', '\r\n\r\n', '\n', '\r\n', ''):
            # no previous line or previous line is an empty line
            return 0
        if last_chars[-1] == '\n':
            # previous line ends with a newline
            self.file.write('\n')
            return 1
        # previous line does not end with a newline
        self.file.write('\n\n')
        return 2
