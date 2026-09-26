#! /usr/local/bin/python3
"""Tests for the family-aware ODF validation test helper."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import timedelta
from pathlib import Path
from zipfile import ZipInfo
import pytest
from tableio._archive_rewrite import rewrite_zip_archive
from tableio.tableio_ods_odfdo import TableIOOdsOdfdo
from tableio.tableio_types import FileAccess
from tableio.value_type import Value
from .odf_validation_helper import odf_validation_result

_STYLE_NS = 'urn:oasis:names:tc:opendocument:xmlns:style:1.0'


def _ods_with_extra_style(tmp_path: Path, extra_style: str,
                          part: str = 'styles.xml',
                          container: str = 'office:styles') -> Path:
    """Write one ODS file (with a duration) and add extra_style."""
    file_path = tmp_path / 'styles.ods'
    with TableIOOdsOdfdo(file_path, FileAccess.CREATE) as table_io:
        row: list[Value] = ['a', timedelta(hours=30)]
        table_io.write_table_listdata([row])

    def add_style(item: ZipInfo, data: bytes) -> bytes:
        """Insert extra_style first in container of part."""
        if item.filename != part or not extra_style:
            return data
        text = data.decode('utf-8')
        start = text.index('>', text.index(f'<{container}')) + 1
        return (text[:start] + extra_style + text[start:]).encode('utf-8')
    rewrite_zip_archive(file_path, add_style)
    return file_path


def test_same_name_other_family(tmp_path: Path) -> None:
    """Reused names across families and used data styles are valid."""
    result = odf_validation_result(_ods_with_extra_style(tmp_path, ''))
    assert result.is_valid, [str(error) for error in result.errors]
    assert not result.errors, [str(error) for error in result.errors]


def test_detects_unused_style(tmp_path: Path) -> None:
    """Automatic styles that really are unused are still reported."""
    extra_style = f'<style:style xmlns:style="{_STYLE_NS}" ' \
        'style:name="Unused" style:family="table-cell"/>'
    result = odf_validation_result(_ods_with_extra_style(
        tmp_path, extra_style, 'content.xml', 'office:automatic-styles'))
    assert any("'Unused' is declared but never referenced" in
               error.description for error in result.errors)


@pytest.mark.parametrize(
    ('extra_style', 'message'),
    [(f'<style:style xmlns:style="{_STYLE_NS}" style:name="Default" '
      'style:family="table-cell"/>', "Duplicate style 'Default'"),
     (f'<style:style xmlns:style="{_STYLE_NS}" style:name="Odd" '
      'style:family="paragraph" style:parent-style-name="Heading"/>',
      "Style 'Odd' inherits from 'Heading' of another family")])
def test_detects_real_issues(tmp_path: Path, extra_style: str,
                             message: str) -> None:
    """Duplicates within one family and family mismatches are errors."""
    result = odf_validation_result(_ods_with_extra_style(tmp_path,
                                                         extra_style))
    assert not result.is_valid
    assert any(message in error.description for error in result.errors)
