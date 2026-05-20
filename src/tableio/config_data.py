#! /usr/local/bin/python3
"""Configuration data for the tableio package."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from dataclasses import dataclass
from typing import Optional
from tableio.optional_args import CsvDialect


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
