#! /usr/local/bin/python3
"""Configuration data and helper signatures for the tableio package."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from dataclasses import dataclass
from typing import Callable, Optional

from mformat.mformat import PathLike
from tableio.capability import Capabilities
from tableio.optional_args import CsvDialect, OptionalArgs
from tableio.tableio import TableIO
from tableio.tableio_types import FileAccess


@dataclass
class CsvConfigData:
    """CSV-specific configuration values.

    This class holds durable user choices that only have meaning for CSV
    output. The values are allowed to be present even when another format is
    selected; helper functions decide whether they are relevant for the
    current TableIO backend. The class has no configuration-framework base
    class, so adapter libraries may combine it with their own base classes.
    """

    dialect: Optional[CsvDialect] = None
    """The CSV dialect template to use, or ``None`` for backend default."""

    delimiter: Optional[str] = None
    """The CSV delimiter to use, or ``None`` for backend default."""

    quoting: Optional[str] = None
    """The CSV quoting style to use, or ``None`` for backend default."""

    quotechar: Optional[str] = None
    """The CSV quote character to use, or ``None`` for backend default."""

    lineterminator: Optional[str] = None
    """The CSV line terminator to use, or ``None`` for backend default."""

    escapechar: Optional[str] = None
    """The CSV escape character to use, or ``None`` for backend default."""


@dataclass
class HtmlConfigData:
    """HTML-specific configuration values.

    The class has no configuration-framework base class, so adapter
    libraries may combine it with their own base classes.
    """

    css_file: Optional[str] = None
    """The CSS file path or URL to reference, or ``None`` for no CSS file."""


@dataclass
class LatexConfigData:
    """LaTeX-specific configuration values.

    The class has no configuration-framework base class, so adapter
    libraries may combine it with their own base classes.
    """

    document_class: Optional[str] = None
    """The LaTeX document class to use, or ``None`` for backend default."""

    preamble: Optional[str] = None
    """Extra LaTeX preamble text, or ``None`` for backend default."""


@dataclass
class ConfigData:  # pylint: disable=too-many-instance-attributes
    """Durable, framework-neutral TableIO configuration choices.

    This class intentionally excludes runtime intent. File names, file access,
    capabilities and callbacks are supplied to helper functions instead of
    being stored as configuration values. The default format is Excel, and
    format-specific nested sections default to ``None`` until a user or
    application deliberately configures them.

    The class has no configuration-framework base class, so adapter libraries
    may combine it with their own base classes.
    """

    format_name: str = 'excel'
    """The TableIO format name. Matching is case-insensitive."""

    implementation: Optional[str] = None
    """The optional implementation pin, or ``None`` to choose best match."""

    character_encoding: Optional[str] = None
    """The text encoding to use, or ``None`` for backend default."""

    language: Optional[str] = None
    """The document language value mapped to backend ``lang`` arguments."""

    title: Optional[str] = None
    """The document title, or ``None`` for backend default."""

    paper_size: Optional[str] = None
    """The document paper size, or ``None`` for backend default."""

    line_length: Optional[int] = None
    """The preferred text line length, or ``None`` for backend default."""

    table_max_line_length: Optional[int] = None
    """The preferred text table line length, or ``None`` for default."""

    table_alignment: Optional[str] = None
    """The preferred text table alignment, or ``None`` for default."""

    csv: Optional[CsvConfigData] = None
    """CSV-specific configuration values, or ``None`` when unset."""

    html: Optional[HtmlConfigData] = None
    """HTML-specific configuration values, or ``None`` when unset."""

    latex: Optional[LatexConfigData] = None
    """LaTeX-specific configuration values, or ``None`` when unset."""


def tio_config_default(capabilities: Capabilities, file_access: FileAccess,
                       format_name: Optional[str] = None,
                       implementation: Optional[str] = None) -> ConfigData:
    """Return recommended default configuration data.

    Default format and implementation selection first prefers implementations
    that strictly support the requested capabilities, then implementations
    that can tolerate capabilities marked as ignorable. If several formats
    match equally well, the preferred format order is Excel, ODS, then CSV.
    If several implementations of the selected format match equally well,
    their TableIO implementation priority is used.

    Args:
        capabilities: Runtime capabilities the application intends to use.
        file_access: Runtime file access requested by the application.
        format_name: Optional preferred format name.
        implementation: Optional preferred implementation name.
    Returns:
        A configuration object containing durable user choices only.
    """
    raise NotImplementedError


def tio_config_optional_args(config: ConfigData,
                             capabilities: Optional[Capabilities] = None) -> \
        OptionalArgs:
    """Build TableIO optional arguments from configuration data.

    The returned arguments contain only values relevant to the selected
    format and implementation. ``None`` values and irrelevant parameters are
    omitted. Runtime-only callbacks are not included.

    Args:
        config: Configuration data to convert.
        capabilities: Optional runtime capabilities used for matching.
    Returns:
        Optional arguments suitable for ``create_tableio``.
    """
    raise NotImplementedError


def tio_config_create(
        config: ConfigData, file_name: PathLike, file_access: FileAccess,
        capabilities: Optional[Capabilities] = None,
        file_exists_callback: Optional[Callable[[str], None]] = None) -> \
        TableIO:
    """Create a TableIO object from configuration and runtime values.

    Args:
        config: Durable configuration data.
        file_name: Runtime file name to open.
        file_access: Runtime file access to request.
        capabilities: Optional runtime capabilities used for matching.
        file_exists_callback: Optional runtime overwrite callback.
    Returns:
        A TableIO object intended for use as a context manager.
    """
    raise NotImplementedError


def tio_config_ignored_names(config: ConfigData,
                             capabilities: Optional[Capabilities] = None) -> \
        list[str]:
    """Return configured parameters ignored by the selected backend.

    Args:
        config: Configuration data to inspect.
        capabilities: Optional runtime capabilities used for matching.
    Returns:
        Dotted parameter names whose values are well-formed but irrelevant.
    """
    raise NotImplementedError


def tio_config_trim(config: ConfigData,
                    capabilities: Optional[Capabilities] = None) -> ConfigData:
    """Return a copy without parameters irrelevant to the selected backend.

    The original configuration object is not mutated. This helper is intended
    for applications that want to write a compact, backend-specific snapshot
    while still allowing the normal configuration file to keep portable
    preferences for several formats.

    Args:
        config: Configuration data to copy and trim.
        capabilities: Optional runtime capabilities used for matching.
    Returns:
        A copy of ``config`` containing only relevant configured values.
    """
    raise NotImplementedError
