#! /usr/bin/env python3
"""Tests for TableIO configuration description metadata."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tableio
import tableio.config_data as config_data_module
from tableio import ConfigSpec, tio_config_describe, \
    tio_config_descriptions, tio_config_specs


_EXPECTED_NAMES = {
    'format_name',
    'implementation',
    'character_encoding',
    'language',
    'title',
    'paper_size',
    'line_length',
    'table_max_line_length',
    'table_alignment',
    'csv.dialect',
    'csv.delimiter',
    'csv.quoting',
    'csv.quotechar',
    'csv.lineterminator',
    'csv.escapechar',
    'html.css_file',
    'latex.document_class',
    'latex.preamble'
}


def _choices(specs: dict[str, ConfigSpec], name: str) -> tuple[str, ...]:
    """Return non-empty choices from a spec."""
    choices = specs[name].choices
    assert choices is not None
    assert choices
    return choices


def _formats(specs: dict[str, ConfigSpec], name: str) -> tuple[str, ...]:
    """Return non-empty relevant formats from a spec."""
    formats = specs[name].relevant_formats
    assert formats is not None
    assert formats
    return formats


def test_root_exports() -> None:
    """Configuration helper names are exported from tableio."""
    assert tableio.ConfigSpec is ConfigSpec
    assert hasattr(tableio, 'ConfigError')
    assert hasattr(tableio, 'ConfigIssue')
    assert hasattr(tableio, 'tio_config_validate')


def test_no_config_data_reexport() -> None:
    """Split metadata and validation names are not on config_data."""
    assert not hasattr(config_data_module, 'ConfigSpec')
    assert not hasattr(config_data_module, 'ConfigError')
    assert not hasattr(config_data_module, 'ConfigIssue')
    assert not hasattr(config_data_module, 'tio_config_specs')
    assert not hasattr(config_data_module, 'tio_config_validate')


def test_spec_names() -> None:
    """tio_config_specs describes every current configuration parameter."""
    specs = tio_config_specs()
    assert set(specs) == _EXPECTED_NAMES
    assert all(name == spec.name for name, spec in specs.items())
    assert all(spec.description for spec in specs.values())
    assert all(spec.value_type for spec in specs.values())


def test_spec_choices() -> None:
    """Finite choices are available from ConfigSpec."""
    specs = tio_config_specs()
    assert {'Excel', 'ODS', 'CSV'} <= set(_choices(specs, 'format_name'))
    assert {'all', 'minimal', 'nonnumeric', 'none'} <= \
        set(_choices(specs, 'csv.quoting'))
    assert set(_choices(specs, 'csv.dialect')) == {'EXCEL', 'UNIX'}
    assert 'CENTER_BUT_DIGITS_RIGHT' in _choices(specs, 'table_alignment')
    assert {'A3', 'A4', 'A5', 'Legal', 'Letter'} == \
        set(_choices(specs, 'paper_size'))
    assert {'Article', 'Report', 'Book', 'Letter'} == \
        set(_choices(specs, 'latex.document_class'))


def test_spec_relevance() -> None:
    """Optional argument specs describe backend relevance."""
    specs = tio_config_specs()
    assert 'CSV' in _formats(specs, 'csv.delimiter')
    assert specs['csv.delimiter'].optional_arg == 'csv_delimiter'
    assert 'HTML' in _formats(specs, 'html.css_file')
    assert specs['html.css_file'].optional_arg == 'css_file'
    assert 'ODS' in _formats(specs, 'language')
    assert specs['language'].optional_arg == 'lang'


def test_descriptions_from_specs() -> None:
    """Description helpers expose the same text as ConfigSpec."""
    specs = tio_config_specs()
    descriptions = tio_config_descriptions()
    assert descriptions == {
        name: spec.description for name, spec in specs.items()
    }
    assert tio_config_describe('csv.quoting') == \
        specs['csv.quoting'].description


def test_describe_unknown() -> None:
    """tio_config_describe raises KeyError for unknown parameters."""
    try:
        tio_config_describe('not.a.parameter')
    except KeyError as err:
        assert err.args == ('not.a.parameter',)
    else:
        raise AssertionError('Expected KeyError')
