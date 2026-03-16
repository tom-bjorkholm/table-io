#! /usr/bin/env python3
"""Reader/writer base class for a file format."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from types import TracebackType
from typing import TypedDict, Callable, Optional
from mformat.mformat import PathLike
from tableio.capability import Capabilities


class Descriptor(TypedDict):
    """Descriptors of the reader/writer class for a file format."""

    name: str
    capabilities: Capabilities
    mandatory_args: list[str]
    optional_args: list[str]


class TableIO:
    """Reader/writer base class for a file format."""

    def __init__(self, file_name: PathLike,
                 file_exists_callback: Optional[Callable[[str], None]]
                 = None):
        """Initialize the TableIO reader/writer class.

        Args:
            file_name: The name of the file to write to.
            file_exists_callback: A callback function to call if the file
                                  already exists. Return to allow the file to
                                  be overwritten. Raise an exception to
                                  prevent the file from being overwritten.
                                  (May for instance save existing file as
                                  backup.)
                                  (Default is to raise an exception.)
        """
        self.file_exists_callback: Optional[Callable[[str], None]] = \
            file_exists_callback
        self.file_name: str = \
            self.file_name_with_extension(file_name,
                                          self.file_name_extension())

    @classmethod
    def get_desciption(cls) -> Descriptor:
        """Get the description of the reader/writer class.

        Must be overridden by subclasses.
        """
        err = 'Subclass must implement get_desciption method'
        raise NotImplementedError(err)
        # pylint: disable=unreachable
        return Descriptor(name='', mandatory_args=[],
                          capabilities=Capabilities(),
                          optional_args=['file_exists_callback'])

    @staticmethod
    def file_name_with_extension(file_name: PathLike,
                                 extension: str) -> str:
        """Return the file name with the extension."""
        return f"{str(file_name)}.{extension}"

    @classmethod
    def file_name_extension(cls) -> str:
        """Return the extension of the file name."""
        msg = 'Subclass must implement file_name_extension method'
        raise NotImplementedError(msg)
        # pylint: disable=unreachable
        return ''

    def __enter__(self) -> 'TableIO':
        """Enter the context manager."""
        self.open()
        return self

    def __exit__(self, exc_type: type[BaseException] | None,
                 exc_value: BaseException | None,
                 traceback: TracebackType | None) -> bool:
        """Exit the context manager.

        Closes the file. If the with block raised an exception,
        close errors are noted on it to preserve it as primary.

        Args:
            exc_type: The type of the exception.
            exc_value: The value of the exception.
            traceback: The traceback of the exception.
        Returns:
            False if an exception should propagate, True otherwise.
        """
        if exc_type is None:
            self.close()
            return True
        try:
            self.close()
        # pylint: disable-next=broad-exception-caught
        except Exception as close_exc:
            assert exc_value is not None
            exc_value.add_note(
                f'Additionally, close() raised: {close_exc}')
        return False

    def open(self) -> None:
        """Open the file.

        Avoid using this method directly.
        Use MultiFormat as a context manager instead, using a with statement.
        """
        err = 'Subclass must implement open method'
        raise NotImplementedError(err)

    def close(self) -> None:
        """Close the file.

        Avoid using this method directly.
        Use MultiFormat as a context manager instead, using a with statement.
        """
        try:  # we need to close the file even if an exception is raised
            self._end_state()
            self._write_file_suffix()
            self._close()
        finally:
            self._close()
        # The _close method should internally guard against multiple closes.

    def _end_state(self) -> None:
        """End the state of the file."""
        err = 'Subclass must implement _end_state method'
        raise NotImplementedError(err)

    def _write_file_suffix(self) -> None:
        """Write the file suffix."""
        err = 'Subclass must implement _write_file_suffix method'
        raise NotImplementedError(err)

    def _close(self) -> None:
        """Close the file."""
        err = 'Subclass must implement _close method'
        raise NotImplementedError(err)
