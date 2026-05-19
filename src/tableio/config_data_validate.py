#! /usr/local/bin/python3
"""Validation helpers for framework-neutral TableIO configuration."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import codecs
from dataclasses import dataclass
from typing import Optional

from tableio.capability import CAP_NEEDED, Capabilities
from tableio.config_data import ConfigData, CsvConfigData, HtmlConfigData, \
    LatexConfigData
from tableio.config_data_describe import ConfigSpec, tio_config_specs
from tableio.factory import TableIOFactoryNoCapabilityMatch, \
    TableIOFactoryNoSuchError, filter_args_tableio, \
    list_implementations_tableio
from tableio.optional_args import CsvDialect
from tableio.tableio_types import FileAccess


@dataclass
class ConfigIssue:
    """One validation issue for a TableIO configuration.

    The issue name is the dotted user-facing configuration parameter name.
    This lets applications and adapter libraries point diagnostics at the
    same names that appear in configuration files and documentation.
    """

    name: str
    """The dotted configuration parameter name, for example ``csv.quoting``."""

    message: str
    """The human-readable validation message for this parameter."""


class ConfigError(ValueError):
    """Raised when TableIO configuration validation fails.

    The ``issues`` attribute contains all validation issues that could be
    found in one pass. ``str(error)`` is intended to be suitable as a compact
    user-facing summary, while ``issues`` is intended for applications and
    adapter libraries that want to attach messages to individual
    configuration fields.
    """

    issues: tuple[ConfigIssue, ...]
    """The validation issues that caused the exception."""

    def __init__(self, issues: tuple[ConfigIssue, ...],
                 message: Optional[str] = None) -> None:
        """Initialize the configuration validation error.

        Args:
            issues: One or more structured validation issues.
            message: Optional summary message for the whole configuration.
        """
        self.issues = issues
        if message is None:
            message = 'Invalid TableIO configuration'
        if issues:
            issue_text = '; '.join(
                f'{issue.name}: {issue.message}' for issue in issues)
            message = f'{message}: {issue_text}'
        super().__init__(message)


def _add_issue(issues: list[ConfigIssue], name: str, message: str) -> None:
    """Add one validation issue to the list."""
    issues.append(ConfigIssue(name=name, message=message))


def _valid_caps(value: Optional[Capabilities],
                issues: list[ConfigIssue]) -> Optional[Capabilities]:
    """Return valid capabilities or add an issue."""
    if value is None or isinstance(value, Capabilities):
        return value
    _add_issue(issues, 'capabilities', 'must be a Capabilities object.')
    return None


def _valid_file_access(value: Optional[FileAccess],
                       issues: list[ConfigIssue]) -> Optional[FileAccess]:
    """Return valid file access or add an issue."""
    if value is None or isinstance(value, FileAccess):
        return value
    _add_issue(issues, 'file_access', 'must be a FileAccess value.')
    return None


def _choices_text(choices: tuple[str, ...]) -> str:
    """Return a compact allowed choices text."""
    return ', '.join(choices)


def _matches_choice(value: str, choices: tuple[str, ...]) -> bool:
    """Return true if a string matches choices case-insensitively."""
    return value.lower() in (choice.lower() for choice in choices)


def _choice_issue(name: str, value: str, spec: ConfigSpec) -> ConfigIssue:
    """Build an issue for an unknown finite choice."""
    assert spec.choices is not None
    msg = f'must be one of: {_choices_text(spec.choices)}.'
    msg += f' Got {value!r}.'
    return ConfigIssue(name=name, message=msg)


def _valid_choice(value: object, spec: ConfigSpec,
                  issues: list[ConfigIssue]) -> bool:
    """Validate one optional string against spec choices."""
    if value is None:
        return True
    if not isinstance(value, str):
        _add_issue(issues, spec.name, 'must be a string.')
        return False
    assert spec.choices is not None
    if _matches_choice(value, spec.choices):
        return True
    issues.append(_choice_issue(spec.name, value, spec))
    return False


def _validate_str(issues: list[ConfigIssue], name: str, value: object) -> bool:
    """Validate one required string."""
    if isinstance(value, str):
        return True
    _add_issue(issues, name, 'must be a string.')
    return False


def _validate_opt_str(issues: list[ConfigIssue], name: str,
                      value: object) -> bool:
    """Validate one optional string."""
    if value is None or isinstance(value, str):
        return True
    _add_issue(issues, name, 'must be a string or None.')
    return False


def _validate_encoding(issues: list[ConfigIssue], value: object) -> None:
    """Validate one optional encoding name."""
    if not _validate_opt_str(issues, 'character_encoding', value):
        return
    if value is None:
        return
    assert isinstance(value, str)
    try:
        codecs.lookup(value)
    except LookupError:
        _add_issue(issues, 'character_encoding',
                   f'is not a known text encoding: {value!r}.')


def _validate_int_min(issues: list[ConfigIssue], name: str, value: object,
                      minimum: int, inclusive: bool) -> None:
    """Validate one optional integer lower bound."""
    if value is None:
        return
    if type(value) is not int:  # pylint: disable=unidiomatic-typecheck
        _add_issue(issues, name, 'must be an integer or None.')
        return
    if inclusive and value < minimum:
        _add_issue(issues, name, f'must be at least {minimum}.')
    if not inclusive and value <= minimum:
        _add_issue(issues, name, f'must be greater than {minimum}.')


def _validate_one_char(issues: list[ConfigIssue], name: str,
                       value: object) -> None:
    """Validate one optional one-character string."""
    if not _validate_opt_str(issues, name, value):
        return
    if value is not None:
        assert isinstance(value, str)
        if len(value) != 1:
            _add_issue(issues, name, 'must contain exactly one character.')


def _validate_nonempty_str(issues: list[ConfigIssue], name: str,
                           value: object) -> None:
    """Validate one optional non-empty string."""
    if not _validate_opt_str(issues, name, value):
        return
    if value == '':
        _add_issue(issues, name, 'must not be empty.')


def _validate_top_values(config: ConfigData, specs: dict[str, ConfigSpec],
                         issues: list[ConfigIssue]) -> None:
    """Validate top-level configuration values."""
    if _validate_str(issues, 'format_name', config.format_name):
        _valid_choice(config.format_name, specs['format_name'], issues)
    _valid_choice(config.implementation, specs['implementation'], issues)
    _validate_encoding(issues, config.character_encoding)
    _validate_opt_str(issues, 'language', config.language)
    _validate_opt_str(issues, 'title', config.title)
    _valid_choice(config.paper_size, specs['paper_size'], issues)
    _validate_int_min(issues, 'line_length', config.line_length, 10, False)
    _validate_int_min(issues, 'table_max_line_length',
                      config.table_max_line_length, 10, True)
    _valid_choice(config.table_alignment, specs['table_alignment'], issues)


def _validate_csv(config: ConfigData, specs: dict[str, ConfigSpec],
                  issues: list[ConfigIssue]) -> None:
    """Validate CSV-specific configuration values."""
    if config.csv is None:
        return
    if not isinstance(config.csv, CsvConfigData):
        _add_issue(issues, 'csv', 'must be a CsvConfigData object or None.')
        return
    if config.csv.dialect is not None and \
            not isinstance(config.csv.dialect, CsvDialect):
        _add_issue(issues, 'csv.dialect',
                   'must be a CsvDialect value or None.')
    _validate_one_char(issues, 'csv.delimiter', config.csv.delimiter)
    _valid_choice(config.csv.quoting, specs['csv.quoting'], issues)
    _validate_one_char(issues, 'csv.quotechar', config.csv.quotechar)
    _validate_nonempty_str(issues, 'csv.lineterminator',
                           config.csv.lineterminator)
    _validate_one_char(issues, 'csv.escapechar', config.csv.escapechar)


def _validate_html(config: ConfigData, issues: list[ConfigIssue]) -> None:
    """Validate HTML-specific configuration values."""
    if config.html is None:
        return
    if not isinstance(config.html, HtmlConfigData):
        _add_issue(issues, 'html', 'must be a HtmlConfigData object or None.')
        return
    _validate_opt_str(issues, 'html.css_file', config.html.css_file)


def _validate_latex(config: ConfigData, specs: dict[str, ConfigSpec],
                    issues: list[ConfigIssue]) -> None:
    """Validate LaTeX-specific configuration values."""
    if config.latex is None:
        return
    if not isinstance(config.latex, LatexConfigData):
        _add_issue(issues, 'latex',
                   'must be a LatexConfigData object or None.')
        return
    _valid_choice(config.latex.document_class, specs['latex.document_class'],
                  issues)
    _validate_opt_str(issues, 'latex.preamble', config.latex.preamble)


def _caps_for_access(file_access: FileAccess) -> Capabilities:
    """Return the capabilities implied by a file access mode."""
    if file_access == FileAccess.READ:
        return Capabilities(can_read=CAP_NEEDED)
    if file_access == FileAccess.CREATE:
        return Capabilities(can_write=CAP_NEEDED)
    return Capabilities(can_read=CAP_NEEDED, can_write=CAP_NEEDED)


def _check_caps_for_access(capabilities: Capabilities, file_access: FileAccess,
                           issues: list[ConfigIssue]) -> None:
    """Validate that explicit capabilities cover file access."""
    if file_access == FileAccess.READ and not capabilities.can_read.supported:
        _add_issue(issues, 'capabilities.can_read',
                   'FileAccess.READ requires can_read.')
    if file_access == FileAccess.CREATE and \
            not capabilities.can_write.supported:
        _add_issue(issues, 'capabilities.can_write',
                   'FileAccess.CREATE requires can_write.')
    if file_access == FileAccess.UPDATE and \
            not capabilities.can_read.supported:
        _add_issue(issues, 'capabilities.can_read',
                   'FileAccess.UPDATE requires can_read.')
    if file_access == FileAccess.UPDATE and \
            not capabilities.can_write.supported:
        _add_issue(issues, 'capabilities.can_write',
                   'FileAccess.UPDATE requires can_write.')


def _match_caps(capabilities: Optional[Capabilities],
                file_access: Optional[FileAccess],
                issues: list[ConfigIssue]) -> Optional[Capabilities]:
    """Return capabilities to use when matching registered backends."""
    if capabilities is None and file_access is not None:
        return _caps_for_access(file_access)
    if capabilities is not None and file_access is not None:
        _check_caps_for_access(capabilities, file_access, issues)
    return capabilities


def _backend_can_be_checked(config: ConfigData,
                            specs: dict[str, ConfigSpec]) -> bool:
    """Return true if backend names are well enough formed to check."""
    if not isinstance(config.format_name, str):
        return False
    assert specs['format_name'].choices is not None
    if not _matches_choice(config.format_name, specs['format_name'].choices):
        return False
    if config.implementation is None:
        return True
    if not isinstance(config.implementation, str):
        return False
    assert specs['implementation'].choices is not None
    if not _matches_choice(config.implementation,
                           specs['implementation'].choices):
        return False
    return _impl_matches_format(config.format_name, config.implementation)


def _impl_choices(format_name: str) -> tuple[str, ...]:
    """Return implementation choices for one registered format."""
    return tuple(list_implementations_tableio(format_name))


def _impl_matches_format(format_name: str, implementation: str) -> bool:
    """Return true if an implementation belongs to a format."""
    return _matches_choice(implementation, _impl_choices(format_name))


def _validate_impl_for_format(config: ConfigData, specs: dict[str, ConfigSpec],
                              issues: list[ConfigIssue]) -> None:
    """Validate implementation choices that depend on the format name."""
    if config.implementation is None:
        return
    if not isinstance(config.format_name, str):
        return
    if not isinstance(config.implementation, str):
        return
    assert specs['format_name'].choices is not None
    if not _matches_choice(config.format_name, specs['format_name'].choices):
        return
    assert specs['implementation'].choices is not None
    if not _matches_choice(config.implementation,
                           specs['implementation'].choices):
        return
    choices = _impl_choices(config.format_name)
    if _matches_choice(config.implementation, choices):
        return
    msg = f'must be one of the implementations for {config.format_name!r}: '
    msg += f'{_choices_text(choices)}. Got {config.implementation!r}.'
    _add_issue(issues, 'implementation', msg)


def _validate_backend(config: ConfigData, specs: dict[str, ConfigSpec],
                      capabilities: Optional[Capabilities],
                      file_access: Optional[FileAccess],
                      issues: list[ConfigIssue]) -> None:
    """Validate registered backend selection and capability matching."""
    if not _backend_can_be_checked(config, specs):
        return
    match_caps = _match_caps(capabilities, file_access, issues)
    try:
        filter_args_tableio(args=None, format_name=config.format_name,
                            implementation=config.implementation,
                            capabilities=match_caps)
    except TableIOFactoryNoSuchError as err:
        _add_issue(issues, 'implementation', str(err))
    except TableIOFactoryNoCapabilityMatch as err:
        name = 'implementation'
        if config.implementation is None:
            name = 'format_name'
        _add_issue(issues, name, str(err))


def tio_config_validate(config: ConfigData,
                        capabilities: Optional[Capabilities] = None,
                        file_access: Optional[FileAccess] = None) -> None:
    """Validate configuration values and selected combinations.

    All configured values are validated, including values that would be
    ignored by the selected backend. Irrelevant but well-formed parameters
    are valid. For example, CSV values may be present while ``format_name``
    selects an Excel backend, but invalid CSV values are still validation
    errors.

    Args:
        config: Configuration data to validate.
        capabilities: Optional runtime capabilities used for matching.
        file_access: Optional runtime file access used for consistency checks.
    Raises:
        ConfigError: The configuration contains invalid values, unknown
            format or implementation names, or a selected backend that cannot
            fulfill the requested capabilities or file access.
    """
    issues: list[ConfigIssue] = []
    valid_caps = _valid_caps(capabilities, issues)
    valid_access = _valid_file_access(file_access, issues)
    if not isinstance(config, ConfigData):
        issue = ConfigIssue('config', 'must be a ConfigData object.')
        raise ConfigError((issue,))
    specs = tio_config_specs()
    _validate_top_values(config, specs, issues)
    _validate_csv(config, specs, issues)
    _validate_html(config, issues)
    _validate_latex(config, specs, issues)
    _validate_impl_for_format(config, specs, issues)
    _validate_backend(config, specs, valid_caps, valid_access, issues)
    if issues:
        raise ConfigError(tuple(issues))
