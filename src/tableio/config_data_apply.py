#! /usr/local/bin/python3
"""Apply framework-neutral configuration data to TableIO backends."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Callable, Optional, TypeVar, cast

from mformat.mformat import PathLike
from tableio.access_capability import add_access_capabilities
from tableio.capability import Capabilities, capability_match
from tableio.config_data import ConfigData, CsvConfigData, HtmlConfigData, \
    LatexConfigData
from tableio.config_data_error import ConfigError, ConfigIssue
from tableio.config_data_validate import tio_config_validate
from tableio.factory import create_tableio, filter_args_tableio, \
    list_implementations_tableio, list_registered_tableio, usage_tableio
from tableio.optional_args import CsvDialect, OptionalArgs, OptionalArgsDict
from tableio.tableio import TableIO
from tableio.tableio_types import FileAccess


_FORMAT_PRIORITY = ('excel', 'ods', 'csv')
_ValueT = TypeVar('_ValueT')


def _config_error(name: str, message: str) -> None:
    """Raise one structured configuration error."""
    raise ConfigError((ConfigIssue(name, message),))


def _check_default_input(capabilities: Capabilities, file_access: FileAccess,
                         format_name: Optional[str],
                         implementation: Optional[str],
                         include_all_options: bool) -> None:
    """Validate runtime values used for default selection."""
    if not isinstance(capabilities, Capabilities):
        _config_error('capabilities', 'must be a Capabilities object.')
    if not isinstance(file_access, FileAccess):
        _config_error('file_access', 'must be a FileAccess value.')
    if format_name is not None and not isinstance(format_name, str):
        _config_error('format_name', 'must be a string or None.')
    if implementation is not None and not isinstance(implementation, str):
        _config_error('implementation', 'must be a string or None.')
    if not isinstance(include_all_options, bool):
        _config_error('include_all_options', 'must be a bool.')


def _registered_formats_by_lower() -> dict[str, str]:
    """Return registered format names keyed by lowercase name."""
    return {name.lower(): name for name in list_registered_tableio()}


def _candidate_formats(format_name: Optional[str]) -> list[str]:
    """Return default-selection format candidates."""
    formats = _registered_formats_by_lower()
    if format_name is not None:
        if format_name.lower() not in formats:
            _config_error('format_name',
                          f'is not registered: {format_name!r}.')
        return [formats[format_name.lower()]]
    return [
        formats[name] for name in _FORMAT_PRIORITY if name in formats
    ]


def _candidate_impls(format_name: str,
                     implementation: Optional[str]) -> list[str]:
    """Return default-selection implementation candidates."""
    impls = list_implementations_tableio(format_name, alphabetical=False)
    if implementation is None:
        return impls
    for impl in impls:
        if impl.lower() == implementation.lower():
            return [impl]
    return []


def _match_group(format_name: str, implementation: str,
                 capabilities: Capabilities) -> Optional[int]:
    """Return strictness group for a candidate implementation."""
    offered = usage_tableio(format_name, implementation).capabilities
    if capability_match(offered, capabilities, ignore_allowed=False):
        return 0
    if capability_match(offered, capabilities, ignore_allowed=True):
        return 1
    return None


def _best_default_names(capabilities: Capabilities, format_name: Optional[str],
                        implementation: Optional[str]) -> tuple[str, str]:
    """Return canonical default format and implementation names."""
    matches: list[tuple[int, int, int, str, str]] = []
    for format_index, fmt in enumerate(_candidate_formats(format_name)):
        for impl in _candidate_impls(fmt, implementation):
            group = _match_group(fmt, impl, capabilities)
            if group is None:
                continue
            priority = usage_tableio(fmt, impl).priority
            matches.append((group, format_index, -priority, fmt, impl))
    if matches:
        _, _, _, selected_format, selected_impl = sorted(matches)[0]
        return selected_format, selected_impl
    name = 'implementation' if implementation is not None else 'format_name'
    _config_error(name, 'does not match registered TableIO backends.')
    raise AssertionError('Unreachable default selection failure.')


def _base_arg_items(config: ConfigData) -> list[tuple[str, str, object]]:
    """Return configured top-level optional argument values."""
    return [
        ('character_encoding', 'character_encoding',
         config.character_encoding),
        ('language', 'lang', config.language),
        ('title', 'title', config.title),
        ('paper_size', 'paper_size', config.paper_size),
        ('line_length', 'line_length', config.line_length),
        ('table_max_line_length', 'table_max_line_length',
         config.table_max_line_length),
        ('table_alignment', 'table_alignment', config.table_alignment)
    ]


def _csv_arg_items(config: ConfigData) -> list[tuple[str, str, object]]:
    """Return configured CSV optional argument values."""
    if config.csv is None:
        return []
    return [
        ('csv.dialect', 'csv_dialect', config.csv.dialect),
        ('csv.delimiter', 'csv_delimiter', config.csv.delimiter),
        ('csv.quoting', 'csv_quoting', config.csv.quoting),
        ('csv.quotechar', 'csv_quotechar', config.csv.quotechar),
        ('csv.lineterminator', 'csv_lineterminator',
         config.csv.lineterminator),
        ('csv.escapechar', 'csv_escapechar', config.csv.escapechar)
    ]


def _html_arg_items(config: ConfigData) -> list[tuple[str, str, object]]:
    """Return configured HTML optional argument values."""
    if config.html is None:
        return []
    return [('html.css_file', 'css_file', config.html.css_file)]


def _latex_arg_items(config: ConfigData) -> list[tuple[str, str, object]]:
    """Return configured LaTeX optional argument values."""
    if config.latex is None:
        return []
    return [
        ('latex.document_class', 'document_class',
         config.latex.document_class),
        ('latex.preamble', 'latex_preamble', config.latex.preamble)
    ]


def _arg_items(config: ConfigData) -> list[tuple[str, str, object]]:
    """Return all configured optional argument values."""
    return _base_arg_items(config) + _csv_arg_items(config) + \
        _html_arg_items(config) + _latex_arg_items(config)


def _arg_dict(config: ConfigData) -> OptionalArgsDict:
    """Return unfiltered optional arguments from non-None config values."""
    args: dict[str, object] = {}
    for _, arg_name, value in _arg_items(config):
        if value is not None:
            args[arg_name] = value
    return cast(OptionalArgsDict, args)


def _filtered_args(config: ConfigData, capabilities: Optional[Capabilities],
                   extra_args: Optional[OptionalArgsDict] = None) -> \
        OptionalArgs:
    """Return filtered optional arguments, or None when empty."""
    args: OptionalArgsDict = _arg_dict(config)
    if extra_args is not None:
        args.update(extra_args)
    filtered = filter_args_tableio(args, config.format_name,
                                   config.implementation,
                                   capabilities=capabilities)
    if not filtered:
        return None
    return filtered


def _all_option_config(format_name: str, implementation: str) -> ConfigData:
    """Return a configuration object with all options visible."""
    csv = CsvConfigData(dialect=CsvDialect.UNIX, delimiter=',', quoting='all',
                        quotechar='"', lineterminator='\n', escapechar='\\')
    html = HtmlConfigData(css_file='style.css')
    latex = LatexConfigData(document_class='Report', preamble='')
    return ConfigData(format_name=format_name, implementation=implementation,
                      character_encoding='utf-8', language='en',
                      title='HTML file', paper_size='A4', line_length=79,
                      table_max_line_length=140,
                      table_alignment='CENTER_BUT_DIGITS_RIGHT', csv=csv,
                      html=html, latex=latex)


def tio_config_default(capabilities: Capabilities, file_access: FileAccess,
                       format_name: Optional[str] = None,
                       implementation: Optional[str] = None,
                       include_all_options: bool = False) -> ConfigData:
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
        include_all_options: Include visible non-None values for all
            configuration options, for teaching and configuration templates.
    Returns:
        A configuration object containing durable user choices only.
    """
    _check_default_input(capabilities, file_access, format_name,
                         implementation, include_all_options)
    match_caps = add_access_capabilities(file_access, capabilities)
    selected_format, selected_impl = _best_default_names(match_caps,
                                                         format_name,
                                                         implementation)
    if format_name is not None:
        selected_format = format_name
    if implementation is not None:
        selected_impl = implementation
    if include_all_options:
        config = _all_option_config(selected_format, selected_impl)
    else:
        config = ConfigData(format_name=selected_format,
                            implementation=selected_impl)
    tio_config_validate(config, capabilities=match_caps)
    return config


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
    tio_config_validate(config, capabilities=capabilities)
    return _filtered_args(config, capabilities)


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
    tio_config_validate(config, capabilities=capabilities,
                        file_access=file_access)
    extra_args = None
    if file_exists_callback is not None:
        extra_args = cast(OptionalArgsDict, {
            'file_exists_callback': file_exists_callback
        })
    args = _filtered_args(config, capabilities, extra_args)
    return create_tableio(format_name=config.format_name, file_name=file_name,
                          file_access=file_access, args=args,
                          implementation=config.implementation,
                          capabilities=capabilities)


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
    tio_config_validate(config, capabilities=capabilities)
    filtered = _filtered_args(config, capabilities)
    filtered_names = set(filtered or {})
    return [
        name for name, arg_name, value in _arg_items(config)
        if value is not None and arg_name not in filtered_names
    ]


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
    tio_config_validate(config, capabilities=capabilities)
    filtered = _filtered_args(config, capabilities)
    filtered_names = set(filtered or {})
    csv = _trim_csv(config, filtered_names)
    html = _trim_html(config, filtered_names)
    latex = _trim_latex(config, filtered_names)
    return ConfigData(format_name=config.format_name,
                      implementation=config.implementation,
                      character_encoding=_kept(config.character_encoding,
                                               'character_encoding',
                                               filtered_names),
                      language=_kept(config.language, 'lang', filtered_names),
                      title=_kept(config.title, 'title', filtered_names),
                      paper_size=_kept(config.paper_size, 'paper_size',
                                       filtered_names),
                      line_length=_kept(config.line_length, 'line_length',
                                        filtered_names),
                      table_max_line_length=_kept(
                          config.table_max_line_length,
                          'table_max_line_length', filtered_names),
                      table_alignment=_kept(config.table_alignment,
                                            'table_alignment', filtered_names),
                      csv=csv, html=html, latex=latex)


def _kept(value: Optional[_ValueT], arg_name: str,
          filtered_names: set[str]) -> Optional[_ValueT]:
    """Return value when its optional argument was kept."""
    if arg_name in filtered_names:
        return value
    return None


def _trim_csv(config: ConfigData,
              filtered_names: set[str]) -> Optional[CsvConfigData]:
    """Return trimmed CSV configuration data."""
    if config.csv is None:
        return None
    csv = CsvConfigData(
        dialect=config.csv.dialect
        if 'csv_dialect' in filtered_names else None,
        delimiter=config.csv.delimiter
        if 'csv_delimiter' in filtered_names else None,
        quoting=config.csv.quoting
        if 'csv_quoting' in filtered_names else None,
        quotechar=config.csv.quotechar
        if 'csv_quotechar' in filtered_names else None,
        lineterminator=config.csv.lineterminator
        if 'csv_lineterminator' in filtered_names else None,
        escapechar=config.csv.escapechar
        if 'csv_escapechar' in filtered_names else None)
    if csv == CsvConfigData():
        return None
    return csv


def _trim_html(config: ConfigData,
               filtered_names: set[str]) -> Optional[HtmlConfigData]:
    """Return trimmed HTML configuration data."""
    if config.html is None or 'css_file' not in filtered_names:
        return None
    return HtmlConfigData(css_file=config.html.css_file)


def _trim_latex(config: ConfigData,
                filtered_names: set[str]) -> Optional[LatexConfigData]:
    """Return trimmed LaTeX configuration data."""
    if config.latex is None:
        return None
    latex = LatexConfigData(
        document_class=config.latex.document_class
        if 'document_class' in filtered_names else None,
        preamble=config.latex.preamble
        if 'latex_preamble' in filtered_names else None)
    if latex == LatexConfigData():
        return None
    return latex
