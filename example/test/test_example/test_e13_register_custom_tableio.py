#! /usr/bin/env python3
"""Tests for registering a custom TableIO example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
from example.e13_register_custom_tableio import \
    CUSTOM_FORMAT_NAME, CUSTOM_IMPLEMENTATION_NAME, LineNumberedCsvTableIO, \
    e13_register_custom_tableio
from tableio.factory import TableIOFactoryConflictError, register_tableio


EXPECTED_LINES: list[str] = [
    '00001:# A user-defined TableIO class was registered with the factory.',
    '00002:',
    '00003:## Each physical line in this format starts with 00001: style.',
    '00004:',
    '00005:"Step","What happens"',
    '00006:"1","User code defines a TableIO-derived class"',
    '00007:"2","User code registers that class with register_tableio()"',
    '00008:"3","The factory can now create the custom backend"',
    '00009:',
    '00010:## Writer information:',
    '00011:',
    '00012:"Attribute","Value","Requested value"',
    '00013:"Type name","LineNumberedCSV","LineNumberedCSV"',
    ('00014:"Implementation","user_line_numbered_csv",'
     '"user_line_numbered_csv"'),
    '00015:"Priority","10",""',
    '00016:"Mandatory arguments","(none)",""',
    '00017:"Optional argument","file_exists_callback",""',
    '00018:"Optional argument","character_encoding",""',
    '00019:"Optional argument","csv_type",""',
    '00020:"Optional argument","csv_delimiter",""',
    '00021:"Optional argument","csv_quoting",""',
    '00022:"Optional argument","csv_quotechar",""',
    '00023:"Optional argument","csv_lineterminator",""',
    '00024:"Optional argument","csv_escapechar",""',
    '00025:"Capability can_write","supported (strict)",""',
    '00026:"Capability can_read","supported (strict)",""',
    '00027:"Capability can_fmt_row","not supported (ignore)",""',
    '00028:"Capability can_fmt_value","not supported (ignore)",""',
    '00029:"Capability filtered_data_range","not supported (ignore)",""',
    '00030:"Capability can_write_box","not supported (strict)",""',
    '00031:"Capability can_read_box","not supported (strict)",""',
    '00032:"Capability can_write_highlight","not supported (ignore)",""',
    '00033:"Capability multi_sheet","not supported (strict)",""',
    ('00034:"Capability can_find_value_position",'
     '"not supported (strict)",""'),
    '00035:'
]


def ensure_custom_backend_registered() -> None:
    """Register the custom backend once for this test process."""
    try:
        register_tableio(LineNumberedCsvTableIO)
    except TableIOFactoryConflictError:
        pass


def test_e13_register_custom_tableio_text(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test e13 using the custom line-numbered CSV backend."""
    ensure_custom_backend_registered()
    with TemporaryDirectory() as tmp_dir:
        output_path = Path(tmp_dir) / 'output'
        result = e13_register_custom_tableio(
            format_name=CUSTOM_FORMAT_NAME,
            output_file_name=str(output_path),
            implementation_name=CUSTOM_IMPLEMENTATION_NAME,
            optional_args=None)
        text = Path(f'{output_path}.lncsv').read_text(encoding='utf-8')
        assert text == '\n'.join(EXPECTED_LINES) + '\n'
        assert result == 0
    out, err = capsys.readouterr()
    assert out == ''
    assert err == ''
