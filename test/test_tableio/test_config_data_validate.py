#! /usr/bin/env python3
"""Tests for TableIO configuration validation."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional, cast

import pytest

import tableio.config_data_validate as validate_module
from tableio import CAP_NEEDED, Capabilities, ConfigData, ConfigError, \
    ConfigIssue, CsvConfigData, CsvDialect, FileAccess, HtmlConfigData, \
    LatexConfigData, tio_config_validate
from tableio.factory import TableIOFactoryNoSuchError
from tableio.optional_args import OptionalArgs
from .file_access_test_helper import unsupported_file_access


def _issue_names(error: ConfigError) -> set[str]:
    """Return issue names from a ConfigError."""
    return {issue.name for issue in error.issues}


def _validate_error(config: ConfigData) -> ConfigError:
    """Validate a config and return the raised validation error."""
    with pytest.raises(ConfigError) as exc_info:
        tio_config_validate(config)
    return exc_info.value


def test_error_summary() -> None:
    """The ConfigError keeps issues and has a compact summary."""
    issues = (
        ConfigIssue('format_name', 'must be known.'),
        ConfigIssue('csv.quoting', 'must be known.'))
    error = ConfigError(issues)
    assert error.issues == issues
    assert str(error) == (
        'Invalid TableIO configuration: format_name: must be known.; '
        'csv.quoting: must be known.')


def test_accepts_default() -> None:
    """The default configuration is valid with the registered backends."""
    tio_config_validate(ConfigData())


def test_accepts_access_default() -> None:
    """Default Excel selection can create files."""
    tio_config_validate(ConfigData(), file_access=FileAccess.CREATE)


def test_accepts_backend_case() -> None:
    """Format and implementation names are case-insensitive."""
    config = ConfigData(format_name='excel', implementation='openpyxl')
    tio_config_validate(config, file_access=FileAccess.READ)


def test_accepts_ignored_valid() -> None:
    """Ignored values are allowed when they are well-formed."""
    config = ConfigData(
        format_name='Excel',
        csv=CsvConfigData(dialect=CsvDialect.EXCEL, delimiter=';'))
    tio_config_validate(config)


def test_checks_ignored() -> None:
    """Ignored values are still validated."""
    error = _validate_error(ConfigData(format_name='Excel',
                                       csv=CsvConfigData(quoting='American')))
    assert _issue_names(error) == {'csv.quoting'}


@pytest.mark.parametrize(
    'config',
    [
        ConfigData(paper_size='letter'),
        ConfigData(table_alignment='center'),
        ConfigData(csv=CsvConfigData(quoting='ALL')),
        ConfigData(latex=LatexConfigData(document_class='article'))
    ])
def test_accepts_choice_case(config: ConfigData) \
        -> None:
    """Finite string choices are checked case-insensitively."""
    tio_config_validate(config)


@pytest.mark.parametrize(
    ('config', 'name'),
    [
        (ConfigData(paper_size='Tabloid'), 'paper_size'),
        (ConfigData(table_alignment='middle'), 'table_alignment'),
        (ConfigData(csv=CsvConfigData(quoting='American')), 'csv.quoting'),
        (ConfigData(latex=LatexConfigData(document_class='Memo')),
         'latex.document_class')
    ])
def test_rejects_unknown_choices(config: ConfigData, name: str) -> None:
    """Finite string choices reject unknown values."""
    assert _issue_names(_validate_error(config)) == {name}


@pytest.mark.parametrize(
    ('config', 'name'),
    [
        (ConfigData(line_length=10), 'line_length'),
        (ConfigData(table_max_line_length=9), 'table_max_line_length')
    ])
def test_rejects_line_bounds(config: ConfigData, name: str) -> None:
    """Text line lengths follow mformat lower bounds."""
    assert _issue_names(_validate_error(config)) == {name}


def test_accepts_line_bounds() -> None:
    """Text line length lower bounds accept the first valid values."""
    tio_config_validate(ConfigData(line_length=11, table_max_line_length=10))


@pytest.mark.parametrize(
    ('config', 'name'),
    [
        (ConfigData(character_encoding='not-an-encoding'),
         'character_encoding'),
        (ConfigData(csv=CsvConfigData(delimiter=';;')), 'csv.delimiter'),
        (ConfigData(csv=CsvConfigData(quotechar='')), 'csv.quotechar'),
        (ConfigData(csv=CsvConfigData(escapechar='xx')), 'csv.escapechar'),
        (ConfigData(csv=CsvConfigData(lineterminator='')),
         'csv.lineterminator')
    ])
def test_rejects_scalar_values(config: ConfigData, name: str) -> None:
    """Scalar validation catches malformed values."""
    assert _issue_names(_validate_error(config)) == {name}


def test_accepts_encoding() -> None:
    """Known text encodings are accepted."""
    tio_config_validate(ConfigData(character_encoding='utf-8'))


@pytest.mark.parametrize(
    ('config', 'name'),
    [
        (ConfigData(character_encoding=cast(Optional[str], 123)),
         'character_encoding'),
        (ConfigData(language=cast(Optional[str], 123)), 'language'),
        (ConfigData(title=cast(Optional[str], 123)), 'title'),
        (ConfigData(format_name=cast(str, 123)), 'format_name'),
        (ConfigData(implementation=cast(Optional[str], 123)),
         'implementation'),
        (ConfigData(line_length=cast(Optional[int], 'wide')),
         'line_length'),
        (ConfigData(csv=cast(Optional[CsvConfigData], object())), 'csv'),
        (ConfigData(csv=CsvConfigData(
            dialect=cast(Optional[CsvDialect], 'excel'))), 'csv.dialect'),
        (ConfigData(csv=CsvConfigData(delimiter=cast(Optional[str], 1))),
         'csv.delimiter'),
        (ConfigData(csv=CsvConfigData(lineterminator=cast(Optional[str], 1))),
         'csv.lineterminator'),
        (ConfigData(html=cast(Optional[HtmlConfigData], object())), 'html'),
        (ConfigData(html=HtmlConfigData(css_file=cast(Optional[str], 1))),
         'html.css_file'),
        (ConfigData(latex=cast(Optional[LatexConfigData], object())),
         'latex'),
        (ConfigData(latex=LatexConfigData(
            preamble=cast(Optional[str], 1))), 'latex.preamble')
    ])
def test_rejects_wrong_types(config: ConfigData, name: str) -> None:
    """Runtime validation catches wrong value types."""
    assert _issue_names(_validate_error(config)) == {name}


def test_rejects_non_config() -> None:
    """Validation rejects non-ConfigData objects."""
    with pytest.raises(ConfigError) as exc_info:
        tio_config_validate(cast(ConfigData, object()))
    assert _issue_names(exc_info.value) == {'config'}


def test_collects_issues() -> None:
    """Validation reports all independent issues found in one pass."""
    config = ConfigData(format_name='Unknown', line_length=0,
                        csv=CsvConfigData(delimiter=';;', quoting='bad'))
    error = _validate_error(config)
    assert _issue_names(error) == {
        'format_name', 'line_length', 'csv.delimiter', 'csv.quoting'
    }


def test_rejects_unknown_format() -> None:
    """Validation requires the format to be registered."""
    error = _validate_error(ConfigData(format_name='Unknown'))
    assert _issue_names(error) == {'format_name'}


def test_unknown_format_skips_impl() -> None:
    """Implementation format checks wait until the format name is known."""
    error = _validate_error(ConfigData(format_name='Unknown',
                                       implementation='csv'))
    assert _issue_names(error) == {'format_name'}


def test_bad_format_type_skips_impl() -> None:
    """Implementation format checks wait for a string format name."""
    config = ConfigData(format_name=cast(str, 123), implementation='csv')
    assert _issue_names(_validate_error(config)) == {'format_name'}


def test_rejects_unknown_impl() -> None:
    """Validation requires the implementation to be registered."""
    error = _validate_error(ConfigData(implementation='Unknown'))
    assert _issue_names(error) == {'implementation'}


def test_rejects_wrong_format_impl() -> None:
    """Validation requires the implementation to belong to the format."""
    error = _validate_error(ConfigData(format_name='Excel',
                                       implementation='csv'))
    assert _issue_names(error) == {'implementation'}
    assert 'implementations for' in error.issues[0].message


def test_rejects_cap_mismatch() -> None:
    """Validation checks selected backend capability matches."""
    config = ConfigData(format_name='CSV', implementation='csv')
    with pytest.raises(ConfigError) as exc_info:
        tio_config_validate(
            config, capabilities=Capabilities(can_write_box=CAP_NEEDED))
    assert _issue_names(exc_info.value) == {'implementation'}


def test_checks_access_match() -> None:
    """Validation checks file access even without explicit capabilities."""
    with pytest.raises(ConfigError) as exc_info:
        tio_config_validate(ConfigData(format_name='md'),
                            file_access=FileAccess.READ)
    assert _issue_names(exc_info.value) == {'format_name'}


def test_rejects_impl_access() -> None:
    """Pinned implementations must support requested file access."""
    config = ConfigData(format_name='Excel', implementation='XlsxWriter')
    with pytest.raises(ConfigError) as exc_info:
        tio_config_validate(config, file_access=FileAccess.READ)
    assert _issue_names(exc_info.value) == {'implementation'}


def test_rejects_caps_access() -> None:
    """Explicit capabilities must include file access requirements."""
    with pytest.raises(ConfigError) as exc_info:
        tio_config_validate(ConfigData(),
                            capabilities=Capabilities(can_write=CAP_NEEDED),
                            file_access=FileAccess.READ)
    assert _issue_names(exc_info.value) == {'capabilities.can_read'}


def test_rejects_runtime_types() -> None:
    """Runtime argument type errors are reported as validation issues."""
    with pytest.raises(ConfigError) as exc_info:
        tio_config_validate(ConfigData(),
                            capabilities=cast(Optional[Capabilities],
                                              object()),
                            file_access=cast(Optional[FileAccess], object()))
    assert _issue_names(exc_info.value) == {'capabilities', 'file_access'}


@pytest.mark.parametrize(
    'capabilities',
    [pytest.param(None, id='access-only'),
     pytest.param(Capabilities(), id='with-capabilities')])
def test_unsupported_file_access(capabilities: Optional[Capabilities]) -> None:
    """Unsupported future FileAccess values are validation issues."""
    with pytest.raises(ConfigError) as exc_info:
        tio_config_validate(ConfigData(), capabilities=capabilities,
                            file_access=unsupported_file_access())
    assert _issue_names(exc_info.value) == {'file_access'}


def test_backend_no_such_reported(monkeypatch: pytest.MonkeyPatch) -> None:
    """Backend lookup disappearance is reported as an implementation issue."""
    def raise_no_such(
            args: OptionalArgs, format_name: str,
            implementation: Optional[str],
            capabilities: Optional[Capabilities] = None) -> OptionalArgs:
        """Raise a no-such error from a fake backend lookup."""
        del args, format_name, implementation, capabilities
        raise TableIOFactoryNoSuchError('missing backend')

    monkeypatch.setattr(validate_module, 'filter_args_tableio', raise_no_such)
    error = _validate_error(ConfigData(format_name='CSV',
                                       implementation='csv'))
    assert _issue_names(error) == {'implementation'}
