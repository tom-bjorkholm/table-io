#! /usr/bin/env python3
"""Spreadsheet validation helpers for example tests."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import NamedTuple, Optional, cast
import pandas as pd  # type: ignore[import-untyped]
from odfdo import Document, Table
from odfdo.style import Style
from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from openxml_audit import (  # type: ignore[import-untyped]
    OdfValidator,
    OpenXmlValidator,
    ValidationResult
)
from tableio.color import Color
from tableio.value_type import get_checked_type


class ExpectedCellStyle(NamedTuple):
    """Expected style values for one spreadsheet cell.

    A value of ``None`` means that the corresponding style aspect is not
    checked.
    """

    bold: Optional[bool] = None
    italic: Optional[bool] = None
    background_color: Optional[Color] = None


class RelativeStyleExpectation(NamedTuple):
    """Expected style for one cell relative to an anchor cell.

    The anchor cell is at offset ``(0, 0)``.
    """

    row_offset: int
    col_offset: int
    expected_style: ExpectedCellStyle


class AnchoredStyleExpectation(NamedTuple):
    """Style checks anchored on the first matching row fragment.

    The row fragment is matched on the specified sheet as a left-to-right
    ordered subsequence within one row. For example ``['hello', 'world']``
    matches the row ``['hello', 'wonderful', 'world']``. The anchor cell is
    the first cell of the first match, selected by the lowest row number and
    then the lowest column number.
    """

    sheet_name: str
    anchor_row_fragment: list[str]
    relative_expectations: list[RelativeStyleExpectation]


class SheetContentExpectation(NamedTuple):
    """Ordered row-fragment expectations for one sheet.

    Each row fragment is matched as a left-to-right ordered subsequence
    within one row. For example ``['hello', 'world']`` matches the row
    ``['hello', 'wonderful', 'world']``.
    """

    sheet_name: str
    row_fragments: list[list[str]]


def _spreadsheet_output_path(output_base: Path | str, suffix: str) -> Path:
    """Return the actual file path after tableio appends its suffix."""
    normalized_suffix = suffix if suffix.startswith('.') else f'.{suffix}'
    return Path(f'{output_base}{normalized_suffix}')


def _normalize_file_path(file_name: Path | str) -> Path:
    """Return one normalized file path."""
    return Path(file_name)


def _spreadsheet_suffix(file_path: Path) -> str:
    """Return the supported spreadsheet suffix in lowercase."""
    suffix = file_path.suffix.lower()
    if suffix not in ['.xlsx', '.ods']:
        raise ValueError(f'Unsupported spreadsheet suffix: {file_path}')
    return suffix


def _check_file_exists(file_path: Path) -> None:
    """Check that one target file exists."""
    if not file_path.is_file():
        raise AssertionError(f'Spreadsheet file does not exist: {file_path}')


def _syntax_validation_result(file_path: Path) -> ValidationResult:
    """Return the syntax-validation result for one spreadsheet file."""
    suffix = _spreadsheet_suffix(file_path)
    if suffix == '.xlsx':
        return OpenXmlValidator().validate(file_path)
    return OdfValidator().validate(file_path)


def _raise_syntax_error(file_path: Path,
                        validation_result: ValidationResult) -> None:
    """Raise one assertion with collected syntax-validation errors."""
    formatted_errors = '\n'.join(
        str(error) for error in validation_result.errors[:20]
    )
    raise AssertionError(
        f'Syntax validation failed for {file_path}:\n{formatted_errors}'
    )


def _read_spreadsheet_content(file_path: Path) -> dict[str, pd.DataFrame]:
    """Read one spreadsheet into a mapping of sheet names to data frames."""
    workbook_data = pd.read_excel(
        file_path,
        sheet_name=None,
        header=None,
        dtype=object
    )
    return cast(dict[str, pd.DataFrame], workbook_data)


def _normalize_cell_value(value: object) -> str:
    """Return one cell value normalized to text for fragment matching."""
    if bool(pd.isna(value)):
        return ''
    return str(value)


def _sheet_rows(sheet_data: pd.DataFrame) -> list[list[str]]:
    """Return one sheet as normalized rows of text."""
    return [
        [_normalize_cell_value(value) for value in row]
        for row in sheet_data.itertuples(index=False, name=None)
    ]


def _match_row_fragment(row_values: list[str],
                        row_fragment: list[str]) -> Optional[int]:
    """Return the first matching column for one row fragment."""
    if not row_fragment:
        raise AssertionError('Row fragments must not be empty.')
    for start_column, cell_value in enumerate(row_values):
        if cell_value != row_fragment[0]:
            continue
        next_fragment_index = 1
        for row_value in row_values[start_column + 1:]:
            if next_fragment_index == len(row_fragment):
                break
            if row_value == row_fragment[next_fragment_index]:
                next_fragment_index += 1
        if next_fragment_index == len(row_fragment):
            return start_column
    return None


def _find_matching_row(rows: list[list[str]],
                       row_fragment: list[str],
                       start_row: int = 0) -> Optional[tuple[int, int]]:
    """Return the first row and column matching one row fragment."""
    for row_index in range(start_row, len(rows)):
        start_column = _match_row_fragment(rows[row_index], row_fragment)
        if start_column is not None:
            return row_index, start_column
    return None


def _check_sheet_names(actual_sheet_names: list[str],
                       expected_fragments:
                       list[SheetContentExpectation]) -> None:
    """Check that actual sheet names match the expected sheet order."""
    expected_sheet_names = [
        fragment.sheet_name for fragment in expected_fragments
    ]
    if actual_sheet_names != expected_sheet_names:
        raise AssertionError(
            'Unexpected sheet names. '
            f'Expected {expected_sheet_names}, got {actual_sheet_names}.'
        )


def _ods_table(document: Document, sheet_name: str) -> Table:
    """Return one ODS table by sheet name."""
    table = document.body.get_table(name=sheet_name)
    if table is None:
        raise AssertionError(f'Missing sheet {sheet_name!r} in ODS document.')
    return get_checked_type(table, Table)


def _color_from_rgb_text(rgb_text: Optional[str]) -> Color:
    """Return one tableio color from a workbook RGB string."""
    if rgb_text is None:
        return Color.NONE
    normalized = rgb_text.upper()
    if normalized.startswith('#'):
        normalized = normalized[1:]
    normalized = normalized[-6:]
    color_map = {
        'FFC7CE': Color.RED,
        'C6EFCE': Color.GREEN,
        'FFFF00': Color.YELLOW
    }
    return color_map.get(normalized, Color.NONE)


def _excel_fill_color(worksheet: Worksheet,
                      row_index: int,
                      col_index: int) -> Color:
    """Return one Excel cell background color."""
    cell = worksheet.cell(row=row_index + 1, column=col_index + 1)
    if cell.fill.fill_type != 'solid':
        return Color.NONE
    rgb_value = cell.fill.fgColor.rgb
    if rgb_value is None:
        rgb_value = cell.fill.start_color.rgb
    return _color_from_rgb_text(rgb_value)


def _excel_actual_style(worksheet: Worksheet,
                        row_index: int,
                        col_index: int) -> ExpectedCellStyle:
    """Return actual style values for one Excel cell."""
    cell = worksheet.cell(row=row_index + 1, column=col_index + 1)
    return ExpectedCellStyle(
        bold=bool(cell.font.bold),
        italic=bool(cell.font.italic),
        background_color=_excel_fill_color(worksheet, row_index, col_index)
    )


def _ods_actual_style(document: Document,
                      table: Table,
                      row_index: int,
                      col_index: int) -> ExpectedCellStyle:
    """Return actual style values for one ODS cell."""
    cell = table.get_cell((col_index, row_index), clone=False)
    if cell.style is None:
        return ExpectedCellStyle(
            bold=False,
            italic=False,
            background_color=Color.NONE
        )
    style = document.get_style('table-cell', cell.style)
    if style is None:
        return ExpectedCellStyle(
            bold=False,
            italic=False,
            background_color=Color.NONE
        )
    checked_style = get_checked_type(style, Style)
    table_props = cast(
        dict[str, str], checked_style.get_properties('table-cell') or {}
    )
    text_props = cast(
        dict[str, str], checked_style.get_properties('text') or {}
    )
    return ExpectedCellStyle(
        bold=text_props.get('fo:font-weight') == 'bold',
        italic=text_props.get('fo:font-style') == 'italic',
        background_color=_color_from_rgb_text(
            table_props.get('fo:background-color')
        )
    )


def _cell_position_text(row_index: int, col_index: int) -> str:
    """Return a readable cell position string."""
    return f'row {row_index + 1}, column {col_index + 1}'


def _cell_location_text(file_path: Path,
                        sheet_name: str,
                        row_index: int,
                        col_index: int) -> str:
    """Return a readable file, sheet and cell location string."""
    return (
        f'{_cell_position_text(row_index, col_index)} '
        f'in sheet {sheet_name!r} of {file_path}'
    )


def _check_style_match(location_text: str,
                       expected_style: ExpectedCellStyle,
                       actual_style: ExpectedCellStyle) -> None:
    """Check one actual style against one expected style."""
    if (expected_style.bold is not None and
            actual_style.bold != expected_style.bold):
        raise AssertionError(
            f'Unexpected bold value at {location_text}. '
            f'Expected {expected_style.bold}, got {actual_style.bold}.'
        )
    if (expected_style.italic is not None and
            actual_style.italic != expected_style.italic):
        raise AssertionError(
            f'Unexpected italic value at {location_text}. '
            f'Expected {expected_style.italic}, got {actual_style.italic}.'
        )
    if (expected_style.background_color is not None and
            actual_style.background_color != expected_style.background_color):
        raise AssertionError(
            f'Unexpected background color at {location_text}. '
            f'Expected {expected_style.background_color}, '
            f'got {actual_style.background_color}.'
        )


def _anchor_match(rows: list[list[str]],
                  row_fragment: list[str],
                  sheet_name: str,
                  file_path: Path) -> tuple[int, int]:
    """Return one anchor match or raise a clear assertion."""
    anchor_match = _find_matching_row(rows, row_fragment)
    if anchor_match is None:
        raise AssertionError(
            f'Could not find style anchor {row_fragment!r} '
            f'in sheet {sheet_name!r} of {file_path}.'
        )
    return anchor_match


def _check_excel_styles(file_path: Path,
                        workbook_data: dict[str, pd.DataFrame],
                        style_expectations:
                        list[AnchoredStyleExpectation]) -> None:
    """Check style expectations in one Excel workbook."""
    workbook = load_workbook(file_path)
    try:
        for style_expectation in style_expectations:
            rows = _sheet_rows(workbook_data[style_expectation.sheet_name])
            anchor_row_index, anchor_col_index = _anchor_match(
                rows,
                style_expectation.anchor_row_fragment,
                style_expectation.sheet_name,
                file_path
            )
            worksheet = get_checked_type(
                workbook[style_expectation.sheet_name], Worksheet
            )
            for relative_expectation in (
                    style_expectation.relative_expectations):
                target_row_index = (
                    anchor_row_index + relative_expectation.row_offset
                )
                target_col_index = (
                    anchor_col_index + relative_expectation.col_offset
                )
                actual_style = _excel_actual_style(
                    worksheet,
                    target_row_index,
                    target_col_index
                )
                _check_style_match(
                    _cell_location_text(
                        file_path,
                        style_expectation.sheet_name,
                        target_row_index,
                        target_col_index
                    ),
                    relative_expectation.expected_style,
                    actual_style
                )
    finally:
        workbook.close()


def _check_ods_styles(file_path: Path,
                      workbook_data: dict[str, pd.DataFrame],
                      style_expectations:
                      list[AnchoredStyleExpectation]) -> None:
    """Check style expectations in one ODS document."""
    document = Document(file_path)
    for style_expectation in style_expectations:
        rows = _sheet_rows(workbook_data[style_expectation.sheet_name])
        anchor_row_index, anchor_col_index = _anchor_match(
            rows,
            style_expectation.anchor_row_fragment,
            style_expectation.sheet_name,
            file_path
        )
        table = _ods_table(document, style_expectation.sheet_name)
        for relative_expectation in style_expectation.relative_expectations:
            target_row_index = (
                anchor_row_index + relative_expectation.row_offset
            )
            target_col_index = (
                anchor_col_index + relative_expectation.col_offset
            )
            actual_style = _ods_actual_style(
                document,
                table,
                target_row_index,
                target_col_index
            )
            _check_style_match(
                _cell_location_text(
                    file_path,
                    style_expectation.sheet_name,
                    target_row_index,
                    target_col_index
                ),
                relative_expectation.expected_style,
                actual_style
            )


def check_spreadsheet_syntax(file_name: Path | str) -> None:
    """Check that one spreadsheet file passes syntax validation."""
    file_path = _normalize_file_path(file_name)
    _check_file_exists(file_path)
    validation_result = _syntax_validation_result(file_path)
    if not validation_result.is_valid:
        _raise_syntax_error(file_path, validation_result)


def check_spreadsheet_content(
        file_name: Path | str,
        expected_fragments: list[SheetContentExpectation]) -> None:
    """Check spreadsheet content against sheet-aware row fragments.

    The actual workbook sheet order must match the order of the
    ``SheetContentExpectation`` items.
    """
    file_path = _normalize_file_path(file_name)
    _check_file_exists(file_path)
    _spreadsheet_suffix(file_path)
    workbook_data = _read_spreadsheet_content(file_path)
    _check_sheet_names(list(workbook_data.keys()), expected_fragments)
    for sheet_expectation in expected_fragments:
        rows = _sheet_rows(workbook_data[sheet_expectation.sheet_name])
        next_row_index = 0
        for row_fragment in sheet_expectation.row_fragments:
            match = _find_matching_row(rows, row_fragment, next_row_index)
            if match is None:
                raise AssertionError(
                    f'Could not find row fragment {row_fragment!r} '
                    f'in sheet {sheet_expectation.sheet_name!r} '
                    f'of {file_path}.'
                )
            next_row_index = match[0] + 1


def check_spreadsheet_styles(
        file_name: Path | str,
        style_expectations: list[AnchoredStyleExpectation]) -> None:
    """Check spreadsheet styles against anchored style expectations."""
    file_path = _normalize_file_path(file_name)
    _check_file_exists(file_path)
    suffix = _spreadsheet_suffix(file_path)
    if not style_expectations:
        return
    workbook_data = _read_spreadsheet_content(file_path)
    if suffix == '.xlsx':
        _check_excel_styles(file_path, workbook_data, style_expectations)
        return
    _check_ods_styles(file_path, workbook_data, style_expectations)


def check_spreadsheet_file(
        file_name: Path | str,
        expected_fragments: list[SheetContentExpectation],
        style_expectations:
        Optional[list[AnchoredStyleExpectation]] = None) -> None:
    """Check spreadsheet syntax, content and optional style expectations."""
    check_spreadsheet_syntax(file_name)
    check_spreadsheet_content(file_name, expected_fragments)
    if style_expectations is not None:
        check_spreadsheet_styles(file_name, style_expectations)
