#! /usr/local/bin/python3
"""ODF validation with openxml_audit, using family-aware style checks.

openxml_audit 0.8.0 rules ODFSEMCHAIN006 (parent style family mismatch) and
ODFSEMCHAIN008 (duplicate style name) compare style names without the
style family. ODF 1.3 only requires a style name to be unique within its
style family, and odfdo (like LibreOffice) writes for instance 'Default'
both as a graphic style and as a table-cell style. The results of these two
rules are replaced by the family-aware checks in this module.

openxml_audit 0.8.0 rule ODFSEMCHAIN002 (unused automatic style) does not
count references by style:data-style-name, so a data style (like the
duration data style) used by a cell style is reported as unused. Such
false positive warnings are removed.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import re
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile
from openxml_audit import OdfValidator  # type: ignore[import-untyped]
from openxml_audit.errors import (  # type: ignore[import-untyped]
    ValidationError, ValidationErrorType, ValidationResult,
    ValidationSeverity)

_FAMILY_BLIND_RULES = frozenset({'ODFSEMCHAIN006', 'ODFSEMCHAIN008'})
_OFFICE_NS = 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'
_STYLE_NS = 'urn:oasis:names:tc:opendocument:xmlns:style:1.0'
_NAME = f'{{{_STYLE_NS}}}name'
_FAMILY = f'{{{_STYLE_NS}}}family'
_PARENT = f'{{{_STYLE_NS}}}parent-style-name'
_DATA_STYLE = f'{{{_STYLE_NS}}}data-style-name'
_UNUSED_STYLE_RULE = 'ODFSEMCHAIN002'
_UNUSED_STYLE_RE = re.compile(
    r"Automatic style '(?P<name>.*)' is declared but never referenced")


def _style_containers(file_path: Path) -> list[tuple[str, list[ET.Element]]]:
    """Return (part/container, named style elements) for each container."""
    ret: list[tuple[str, list[ET.Element]]] = []
    with ZipFile(file_path) as zip_file:
        for part in ('content.xml', 'styles.xml'):
            root = ET.fromstring(zip_file.read(part))
            for container_name in ('automatic-styles', 'styles'):
                container = root.find(f'{{{_OFFICE_NS}}}{container_name}')
                if container is not None:
                    ret.append((f'{part}/{container_name}',
                                [element for element in container
                                 if element.get(_NAME)]))
    return ret


def _style_key(element: ET.Element) -> tuple[str, str, str]:
    """Return the (element, family, name) key identifying one style."""
    return element.tag, element.get(_FAMILY, ''), element.get(_NAME, '')


def _semantic_error(description: str) -> ValidationError:
    """Return one semantic validation error."""
    return ValidationError(error_type=ValidationErrorType.SEMANTIC,
                           description=description)


def _duplicate_errors(containers: list[tuple[str, list[ET.Element]]]) -> \
        list[ValidationError]:
    """Return errors for styles defined twice in the same family."""
    return [_semantic_error(f'Duplicate style {key[2]!r} (family '
                            f'{key[1]!r}) in {scope}')
            for scope, styles in containers
            for key, count in Counter(map(_style_key, styles)).items()
            if count > 1]


def _family_errors(containers: list[tuple[str, list[ET.Element]]]) -> \
        list[ValidationError]:
    """Return errors for parent styles only existing in other families."""
    styles = [style for _, scope_styles in containers
              for style in scope_styles]
    families: dict[str, set[str]] = {}
    for style in styles:
        families.setdefault(style.get(_NAME, ''), set()).add(
            style.get(_FAMILY, ''))
    return [_semantic_error(f'Style {style.get(_NAME)!r} inherits from '
                            f'{style.get(_PARENT)!r} of another family')
            for style in styles
            if style.get(_PARENT) in families and
            style.get(_FAMILY, '') not in families[style.get(_PARENT, '')]]


def _is_false_positive(error: ValidationError,
                       data_style_refs: set[str]) -> bool:
    """Return True for the known false positives of openxml_audit."""
    if error.id in _FAMILY_BLIND_RULES:
        return True
    match = _UNUSED_STYLE_RE.fullmatch(error.description)
    return error.id == _UNUSED_STYLE_RULE and match is not None and \
        match['name'] in data_style_refs


def odf_validation_result(file_path: Path) -> ValidationResult:
    """Validate one ODF file, using corrected style checks."""
    result = OdfValidator().validate(file_path)
    containers = _style_containers(file_path)
    data_style_refs = {style.get(_DATA_STYLE, '')
                       for _, styles in containers for style in styles}
    errors = [error for error in result.errors
              if not _is_false_positive(error, data_style_refs)] + \
        _duplicate_errors(containers) + _family_errors(containers)
    is_valid = not any(error.severity == ValidationSeverity.ERROR
                       for error in errors)
    return ValidationResult(is_valid=is_valid, errors=errors,
                            file_path=result.file_path,
                            file_format=result.file_format)
