#! /usr/bin/env python3
"""Tests for TableIO configuration data helpers."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import inspect
from pathlib import Path
from typing import Callable

import pytest

from tableio import CAP_IGNORABLE, CAP_NEEDED, Capabilities, ConfigData, \
    ConfigError, CsvConfigData, CsvDialect, FileAccess, HtmlConfigData, \
    LatexConfigData, tio_config_create, tio_config_default, \
    tio_config_ignored_names, tio_config_optional_args, tio_config_trim
from tableio.tableio_csv import TableIOCsv


def _issue_names(error: ConfigError) -> set[str]:
    """Return issue names from a ConfigError."""
    return {issue.name for issue in error.issues}


def test_default_excel_writer() -> None:
    """Default output configuration lets runtime choose implementation."""
    config = tio_config_default(Capabilities(), FileAccess.CREATE)
    expected = ConfigData(format_name='Excel')
    assert config == expected


def test_default_excel_reader() -> None:
    """Default input configuration lets runtime choose implementation."""
    config = tio_config_default(Capabilities(), FileAccess.READ)
    expected = ConfigData(format_name='Excel')
    assert config == expected


def test_default_impl_included() -> None:
    """Default configuration can include selected implementation."""
    config = tio_config_default(Capabilities(), FileAccess.CREATE,
                                impl_in_cfg=True)
    expected = ConfigData(format_name='Excel', implementation='XlsxWriter')
    assert config == expected


def test_default_all_options() -> None:
    """Expanded default configuration includes every configurable leaf."""
    config = tio_config_default(Capabilities(), FileAccess.CREATE,
                                include_all_options=True)
    csv = CsvConfigData(dialect=CsvDialect.UNIX, delimiter=',', quoting='all',
                        quotechar='"', lineterminator='\n', escapechar='\\')
    expected = ConfigData(
        format_name='Excel', implementation='XlsxWriter',
        character_encoding='utf-8', language='en', title='HTML file',
        paper_size='A4', line_length=79, table_max_line_length=140,
        table_alignment='CENTER_BUT_DIGITS_RIGHT', csv=csv,
        html=HtmlConfigData(css_file='style.css'),
        latex=LatexConfigData(document_class='Report', preamble=''))
    assert config == expected


def test_default_all_keeps_name_case() -> None:
    """Expanded defaults preserve explicit user-supplied name casing."""
    config = tio_config_default(
        Capabilities(), FileAccess.READ, format_name='excel',
        implementation='openpyxl', include_all_options=True)
    assert config.format_name == 'excel'
    assert config.implementation == 'openpyxl'
    assert config.csv is not None
    assert config.html is not None
    assert config.latex is not None


def test_default_all_options_filters() -> None:
    """Expanded defaults are valid when filtered for one backend."""
    config = tio_config_default(Capabilities(), FileAccess.CREATE,
                                format_name='CSV', include_all_options=True)
    assert config.implementation == 'csv'
    assert tio_config_optional_args(config) == {
        'character_encoding': 'utf-8',
        'csv_dialect': CsvDialect.UNIX,
        'csv_delimiter': ',',
        'csv_quoting': 'all',
        'csv_quotechar': '"',
        'csv_lineterminator': '\n',
        'csv_escapechar': '\\'
    }


def test_default_keeps_name_case() -> None:
    """Explicit format and implementation names keep caller spelling."""
    caps = Capabilities()
    config = tio_config_default(caps, FileAccess.READ, format_name='excel',
                                implementation='openpyxl')
    expected = ConfigData(format_name='excel', implementation='openpyxl')
    assert config == expected


def test_default_from_impl() -> None:
    """An explicit implementation can drive default format selection."""
    config = tio_config_default(Capabilities(), FileAccess.CREATE,
                                implementation='odfdo')
    assert config == ConfigData(format_name='ODS', implementation='odfdo')


def test_default_impl_excluded() -> None:
    """Explicit implementation pins can be excluded from configuration."""
    config = tio_config_default(Capabilities(), FileAccess.CREATE,
                                implementation='odfdo', impl_in_cfg=False)
    assert config == ConfigData(format_name='ODS')


def test_default_all_no_impl() -> None:
    """Expanded defaults can still omit the selected implementation."""
    config = tio_config_default(Capabilities(), FileAccess.CREATE,
                                include_all_options=True, impl_in_cfg=False)
    assert config.format_name == 'Excel'
    assert config.implementation is None
    assert config.csv is not None
    assert config.html is not None
    assert config.latex is not None


def test_default_prefers_cap_support() -> None:
    """Ignorable used capabilities affect implementation selection."""
    caps = Capabilities(can_find_value_position=CAP_IGNORABLE)
    config = tio_config_default(caps, FileAccess.CREATE, impl_in_cfg=True)
    expected = ConfigData(format_name='Excel', implementation='OpenPyXL')
    assert config == expected


def test_default_rejects_no_match() -> None:
    """Default selection reports when pinned choices cannot match."""
    caps = Capabilities(can_read_box=CAP_NEEDED)
    with pytest.raises(ConfigError) as exc_info:
        tio_config_default(caps, FileAccess.CREATE, format_name='CSV')
    assert _issue_names(exc_info.value) == {'format_name'}


def test_default_rejects_bad_impl() -> None:
    """Default selection reports unknown implementation pins."""
    with pytest.raises(ConfigError) as exc_info:
        tio_config_default(Capabilities(), FileAccess.CREATE,
                           implementation='missing')
    assert _issue_names(exc_info.value) == {'implementation'}


def test_default_bad_include_all() -> None:
    """Default selection validates the include_all_options flag."""
    with pytest.raises(ConfigError) as exc_info:
        tio_config_default(Capabilities(), FileAccess.CREATE,
                           include_all_options=1)  # type: ignore[arg-type]
    assert _issue_names(exc_info.value) == {'include_all_options'}


def test_default_bad_impl_in_cfg() -> None:
    """Default selection validates the implementation include flag."""
    with pytest.raises(ConfigError) as exc_info:
        tio_config_default(Capabilities(), FileAccess.CREATE,
                           impl_in_cfg=1)  # type: ignore[arg-type]
    assert _issue_names(exc_info.value) == {'impl_in_cfg'}


def test_format_keyword_only() -> None:
    """Format name must be passed by keyword."""
    param = inspect.signature(tio_config_default).parameters['format_name']
    assert param.kind == inspect.Parameter.KEYWORD_ONLY


def test_optional_args_empty() -> None:
    """Optional args return None when all configured values are ignored."""
    config = ConfigData(format_name='Excel', title='Ignored',
                        csv=CsvConfigData(delimiter=';'))
    assert tio_config_optional_args(config) is None


def test_optional_args_csv() -> None:
    """Optional args include non-None values relevant to CSV."""
    config = ConfigData(
        format_name='CSV', character_encoding='latin-1',
        csv=CsvConfigData(dialect=CsvDialect.EXCEL, delimiter=';',
                          quoting='all', quotechar='"'),
        html=HtmlConfigData(css_file='table.css'))
    args = tio_config_optional_args(config)
    assert args == {
        'character_encoding': 'latin-1',
        'csv_dialect': CsvDialect.EXCEL,
        'csv_delimiter': ';',
        'csv_quoting': 'all',
        'csv_quotechar': '"'
    }


def test_optional_args_text() -> None:
    """Optional args include text backend values."""
    config = ConfigData(format_name='txt', line_length=72,
                        table_max_line_length=60, table_alignment='CENTER')
    assert tio_config_optional_args(config) == {
        'line_length': 72,
        'table_max_line_length': 60,
        'table_alignment': 'CENTER'
    }


def test_create_config_values(tmp_path: Path) -> None:
    """Create builds the selected TableIO object with config arguments."""
    config = ConfigData(format_name='CSV', csv=CsvConfigData(delimiter=';'))
    table = tio_config_create(config, tmp_path / 'created', FileAccess.CREATE)
    assert isinstance(table, TableIOCsv)
    assert table.csv_definitions.delimiter == ';'


def test_create_runtime_callback(tmp_path: Path) -> None:
    """Create passes the runtime file-exists callback separately."""
    file_name = tmp_path / 'existing.csv'
    file_name.write_text('old', encoding='utf-8')
    called: list[str] = []

    def callback(name: str) -> None:
        """Record one overwrite callback invocation."""
        called.append(name)

    config = ConfigData(format_name='CSV')
    tio_config_create(config, file_name, FileAccess.CREATE,
                      file_exists_callback=callback)
    assert called == [str(file_name)]


def test_ignored_non_none() -> None:
    """Ignored names lists configured leaves irrelevant to the backend."""
    config = ConfigData(format_name='CSV', character_encoding='utf-8',
                        title='Ignored',
                        csv=CsvConfigData(delimiter=';', quotechar='"'),
                        html=HtmlConfigData(css_file='table.css'))
    assert tio_config_ignored_names(config) == ['title', 'html.css_file']


def test_ignored_skips_none() -> None:
    """Ignored names ignores nested sections without configured leaves."""
    config = ConfigData(format_name='CSV', csv=CsvConfigData())
    assert tio_config_ignored_names(config) == []


def test_trim_keeps_relevant() -> None:
    """Trim returns a compact copy without mutating the original."""
    config = ConfigData(format_name='CSV', character_encoding='utf-8',
                        title='Ignored',
                        csv=CsvConfigData(delimiter=';', quotechar='"'),
                        html=HtmlConfigData(css_file='table.css'))
    trimmed = tio_config_trim(config)
    assert trimmed == ConfigData(
        format_name='CSV', character_encoding='utf-8',
        csv=CsvConfigData(delimiter=';', quotechar='"'))
    assert config.title == 'Ignored'
    assert config.html == HtmlConfigData(css_file='table.css')


def test_trim_removes_empty() -> None:
    """Trim removes nested config sections that have no kept values."""
    config = ConfigData(format_name='CSV', csv=CsvConfigData(),
                        html=HtmlConfigData())
    assert tio_config_trim(config) == ConfigData(format_name='CSV')


@pytest.mark.parametrize(
    'helper',
    [tio_config_optional_args, tio_config_ignored_names, tio_config_trim])
def test_helpers_validate_ignored(
        helper: Callable[[ConfigData], object]) -> None:
    """Helpers validate configured values even when they are ignored."""
    config = ConfigData(format_name='Excel', csv=CsvConfigData(quoting='bad'))
    with pytest.raises(ConfigError) as exc_info:
        helper(config)
    assert _issue_names(exc_info.value) == {'csv.quoting'}
