#! /usr/local/bin/python3
"""Description metadata for framework-neutral TableIO configuration."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from dataclasses import dataclass
from typing import Optional

from mformat.document_class import DocumentClass
from mformat.paper_size import PaperSize
from mformat.plain_text_table import TableAlignment

from tableio.factory import list_implementations_tableio, \
    list_registered_tableio, usage_tableio
from tableio.optional_args import CsvDialect


@dataclass
class ConfigSpec:  # pylint: disable=too-many-instance-attributes
    """Documentation metadata for one configuration parameter.

    Applications and configuration adapters can use these specifications to
    build user-facing documentation without duplicating TableIO knowledge.
    """

    name: str
    """The dotted configuration parameter name."""

    description: str
    """The user-facing description of the configuration parameter."""

    value_type: str
    """The user-facing value type description."""

    default_text: Optional[str] = None
    """The user-facing default value description, if there is one."""

    choices: Optional[tuple[str, ...]] = None
    """Allowed values, if the value has a finite advertised choice set."""

    relevant_formats: Optional[tuple[str, ...]] = None
    """Formats where this parameter can affect the created backend."""

    relevant_impls: Optional[tuple[str, ...]] = None
    """Implementations where this parameter can affect the backend."""

    optional_arg: Optional[str] = None
    """The TableIO optional argument name this parameter maps to."""


_CSV_QUOTING_VALUES = (
    'all', 'minimal', 'nonnumeric', 'none', 'strings', 'notnull')


def _csv_dialect_choices() -> tuple[str, ...]:
    """Return advertised CSV dialect choices."""
    return tuple(member.name for member in CsvDialect)


def _table_alignment_choices() -> tuple[str, ...]:
    """Return advertised plain text table alignment choices."""
    return tuple(member.name for member in TableAlignment)


def _formats_for_arg(optional_arg: str) -> tuple[str, ...]:
    """Return registered formats that accept an optional argument."""
    formats = []
    for format_name in list_registered_tableio():
        for implementation in list_implementations_tableio(format_name):
            usage = usage_tableio(format_name, implementation)
            if optional_arg in usage.optional_args:
                formats.append(format_name)
                break
    return tuple(formats)


def _impls_for_arg(optional_arg: str) -> tuple[str, ...]:
    """Return registered implementations that accept an optional argument."""
    impls = []
    for format_name in list_registered_tableio():
        for implementation in list_implementations_tableio(format_name):
            usage = usage_tableio(format_name, implementation)
            if optional_arg in usage.optional_args and implementation not in \
                    impls:
                impls.append(implementation)
    return tuple(impls)


def _arg_spec(spec: ConfigSpec) -> ConfigSpec:
    """Build a config spec mapped to one TableIO optional argument."""
    assert spec.optional_arg is not None
    spec.relevant_formats = _formats_for_arg(spec.optional_arg)
    spec.relevant_impls = _impls_for_arg(spec.optional_arg)
    return spec


def tio_config_specs() -> dict[str, ConfigSpec]:
    """Return documentation metadata for configuration parameters.

    Returns:
        A mapping from dotted parameter names to structured specifications.
    """
    specs = [
        ConfigSpec(name='format_name',
                   description='The TableIO format name to use.',
                   value_type='str', default_text='excel',
                   choices=tuple(list_registered_tableio())),
        ConfigSpec(name='implementation',
                   description='The TableIO implementation name to use.',
                   value_type='Optional[str]',
                   default_text='None means choose best match.',
                   choices=tuple(list_implementations_tableio())),
        _arg_spec(ConfigSpec(name='character_encoding',
                             description='The text encoding.',
                             value_type='Optional[str]',
                             default_text='None means backend default.',
                             optional_arg='character_encoding')),
        _arg_spec(ConfigSpec(name='language',
                             description='The document language value.',
                             value_type='Optional[str]',
                             default_text='None means backend default.',
                             optional_arg='lang')),
        _arg_spec(ConfigSpec(name='title', description='The document title.',
                             value_type='Optional[str]',
                             default_text='None means backend default.',
                             optional_arg='title')),
        _arg_spec(ConfigSpec(name='paper_size',
                             description='The document paper size.',
                             value_type='Optional[str]',
                             default_text='None means backend default.',
                             choices=tuple(PaperSize.allowed_values()),
                             optional_arg='paper_size')),
        _arg_spec(ConfigSpec(name='line_length',
                             description='The maximum text line length.',
                             value_type='Optional[int]',
                             default_text='None means backend default.',
                             optional_arg='line_length')),
        _arg_spec(ConfigSpec(name='table_max_line_length',
                             description='The maximum table line length.',
                             value_type='Optional[int]',
                             default_text='None means backend default.',
                             optional_arg='table_max_line_length')),
        _arg_spec(ConfigSpec(name='table_alignment',
                             description='The text table alignment.',
                             value_type='Optional[str]',
                             default_text='None means backend default.',
                             choices=_table_alignment_choices(),
                             optional_arg='table_alignment')),
        _arg_spec(ConfigSpec(name='csv.dialect',
                             description='The CSV dialect template.',
                             value_type='Optional[CsvDialect]',
                             default_text='None means backend default.',
                             choices=_csv_dialect_choices(),
                             optional_arg='csv_dialect')),
        _arg_spec(ConfigSpec(name='csv.delimiter',
                             description='The one-character CSV delimiter.',
                             value_type='Optional[str]',
                             default_text='None means backend default.',
                             optional_arg='csv_delimiter')),
        _arg_spec(ConfigSpec(name='csv.quoting',
                             description='The CSV quoting style.',
                             value_type='Optional[str]',
                             default_text='None means backend default.',
                             choices=_CSV_QUOTING_VALUES,
                             optional_arg='csv_quoting')),
        _arg_spec(ConfigSpec(name='csv.quotechar',
                             description='The CSV quote character.',
                             value_type='Optional[str]',
                             default_text='None means backend default.',
                             optional_arg='csv_quotechar')),
        _arg_spec(ConfigSpec(name='csv.lineterminator',
                             description='The CSV line terminator.',
                             value_type='Optional[str]',
                             default_text='None means backend default.',
                             optional_arg='csv_lineterminator')),
        _arg_spec(ConfigSpec(name='csv.escapechar',
                             description='The CSV escape character.',
                             value_type='Optional[str]',
                             default_text='None means backend default.',
                             optional_arg='csv_escapechar')),
        _arg_spec(ConfigSpec(name='html.css_file',
                             description='The CSS file path or URL.',
                             value_type='Optional[str]',
                             default_text='None means no CSS file.',
                             optional_arg='css_file')),
        _arg_spec(ConfigSpec(name='latex.document_class',
                             description='The LaTeX document class.',
                             value_type='Optional[str]',
                             default_text='None means backend default.',
                             choices=tuple(DocumentClass.allowed_values()),
                             optional_arg='document_class')),
        _arg_spec(ConfigSpec(name='latex.preamble',
                             description='Extra LaTeX preamble text.',
                             value_type='Optional[str]',
                             default_text='None means backend default.',
                             optional_arg='latex_preamble'))
    ]
    return {spec.name: spec for spec in specs}


def tio_config_descriptions() -> dict[str, str]:
    """Return descriptions for configuration parameters.

    Returns:
        A mapping from dotted parameter names to description strings.
    """
    return {
        name: spec.description
        for name, spec in tio_config_specs().items()
    }


def tio_config_describe(name: str) -> str:
    """Return the description for one configuration parameter.

    Args:
        name: Dotted configuration parameter name.
    Returns:
        The user-facing description string.
    Raises:
        KeyError: The configuration parameter name is unknown.
    """
    return tio_config_specs()[name].description
