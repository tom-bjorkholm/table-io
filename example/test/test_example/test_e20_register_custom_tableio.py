#! /usr/bin/env python3
"""Tests for registering a custom TableIO example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
from example.e20_register_custom_tableio import \
    CUSTOM_FORMAT_NAME, CUSTOM_IMPLEMENTATION_NAME, LineNumberedCsvTableIO, \
    e20_register_custom_tableio
from tableio.capability import capability_to_str
from tableio.factory import TableIOFactoryConflictError, register_tableio


def expected_lines() -> list[str]:
    """Return the expected numbered output lines for the custom backend."""
    payloads = [
        '# A user-defined TableIO class was registered with the factory.',
        '',
        '## Each physical line in this format starts with 00001: style.',
        '',
        '"Step","What happens"',
        '"1","User code defines a TableIO-derived class"',
        '"2","User code registers that class with register_tableio()"',
        '"3","The factory can now create the custom backend"',
        '',
        '## Writer information:',
        '',
        '"Attribute","Value","Requested value"',
        '"Type name","LineNumberedCSV","LineNumberedCSV"',
        ('"Implementation","user_line_numbered_csv",'
         '"user_line_numbered_csv"'),
        '"Priority","10",""',
        '"Mandatory arguments","(none)",""',
        '"Optional argument","file_exists_callback",""',
        '"Optional argument","character_encoding",""',
        '"Optional argument","csv_dialect",""',
        '"Optional argument","csv_delimiter",""',
        '"Optional argument","csv_quoting",""',
        '"Optional argument","csv_quotechar",""',
        '"Optional argument","csv_lineterminator",""',
        '"Optional argument","csv_escapechar",""'
    ]
    capabilities = LineNumberedCsvTableIO.get_description().capabilities
    for key, value in zip(capabilities._fields, capabilities):
        payloads.append(f'"Capability {key}","{capability_to_str(value)}",""')
    payloads.append('')
    return [
        f'{line_number:05d}:{payload}'
        for line_number, payload in enumerate(payloads, start=1)
    ]


def ensure_custom_backend_registered() -> None:
    """Register the custom backend once for this test process."""
    try:
        register_tableio(LineNumberedCsvTableIO)
    except TableIOFactoryConflictError:
        pass


def test_e20_register_custom_tableio_text(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test e20 using the custom line-numbered CSV backend."""
    ensure_custom_backend_registered()
    with TemporaryDirectory() as tmp_dir:
        output_path = Path(tmp_dir) / 'output'
        result = e20_register_custom_tableio(
            format_name=CUSTOM_FORMAT_NAME, output_file_name=str(output_path),
            implementation_name=CUSTOM_IMPLEMENTATION_NAME, optional_args=None)
        text = Path(f'{output_path}.lncsv').read_text(encoding='utf-8')
        assert text == '\n'.join(expected_lines()) + '\n'
        assert result == 0
    out, err = capsys.readouterr()
    assert out == ''
    assert err == ''
