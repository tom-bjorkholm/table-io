#! /usr/local/bin/python3
"""Checkers for the example package."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
import os
from typing import NamedTuple, Callable, Optional
from pathlib import Path
from tempfile import TemporaryDirectory
from pytest import CaptureFixture
from tableio import OptionalArgs
from .spreadsheet_checkers import check_spreadsheet_file, \
    SheetContentExpectation, AnchoredStyleExpectation


class Example(NamedTuple):
    """Example function with arguments."""

    example_function: Callable[[str, str, Optional[str], OptionalArgs], int]
    format_name: str
    implementation_name: Optional[str] = None
    optional_args: OptionalArgs = None


type SheetContentExpectations = list[SheetContentExpectation]
type AnchoredStyleExpectations = Optional[list[AnchoredStyleExpectation]]


def _print_text(text: str) -> None:
    """Print the text."""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    for line in lines[:500]:
        print(f'{line[:800]}', file=sys.stderr)


def _print_line_col_of_pos(text: str, pos: int) -> None:
    """Print the line number and column number of the position in the text."""
    lines = text[:pos].split('\n')
    print(f'Position: {pos} is line: {len(lines)}, column: {len(lines[-1])}',
          file=sys.stderr)


def check_text_in_order(text: str, expected_txts: list[str]) -> None:
    """Check that the text contains expected text in the expected order."""
    for expected_txt in expected_txts:
        if expected_txt not in text:
            print(f'Expected text: "{expected_txt}" not found in text.',
                  file=sys.stderr)
            print('Text:', file=sys.stderr)
            _print_text(text)
        assert expected_txt in text
    start = 0
    for num, expected_txt in enumerate(expected_txts):
        pos = text.find(expected_txt, start)
        if pos == -1:
            print(f'Expected text with index {num - 1} ended at '
                  f'position {start} in text.', file=sys.stderr)
            print(f'Expected text index {num - 1}: {expected_txts[num - 1]}',
                  file=sys.stderr)
            print(f'Expected text with index {num} not found in text '
                  f'starting at position {start}.', file=sys.stderr)
            _print_line_col_of_pos(text, start)
            print(f'Failing expected text: {expected_txt}', file=sys.stderr)
            print(f'Text from position {start}:', file=sys.stderr)
            _print_text(text[start:])
            print('\n\n----Complete text beginning:-------------\n',
                  file=sys.stderr)
            _print_text(text)
        assert pos != -1
        start = pos + len(expected_txt)


def check_example_spreadsheet(example: Example, capture: CaptureFixture[str],
                              expected_fragments: SheetContentExpectations,
                              style_expectations: AnchoredStyleExpectations
                              = None) -> None:
    """Check the example spreadsheet.

    Args:
        example: The example function and arguments.
        capture: The capture fixture.
        expected_fragments: The expected fragments.
        style_expectations: The style expectations.
    """
    with TemporaryDirectory() as tmp_dir:
        output_path = Path(tmp_dir) / 'output'
        assert example.format_name.lower() in ['ods', 'excel']
        if example.format_name.lower() == 'ods':
            output_path = output_path.with_suffix('.ods')
        elif example.format_name.lower() == 'excel':
            output_path = output_path.with_suffix('.xlsx')
        else:
            raise ValueError(f'Unsupported format: {example.format_name}')
        result = example.example_function(example.format_name,
                                          str(output_path),
                                          example.implementation_name,
                                          example.optional_args)
        os.system(f'ls -l {tmp_dir}')
        check_spreadsheet_file(output_path, expected_fragments,
                               style_expectations)
        assert result == 0
    out, err = capture.readouterr()
    assert out == ''
    assert err == ''


def check_example_md_csv(example: Example, capture: CaptureFixture[str],
                         expected_fragments: list[str]) -> None:
    """Check the example generating a markdown or CSV file.

    Args:
        example: The example function and arguments.
        capture: The capture fixture.
        expected_fragments: The expected fragments.
    """
    with TemporaryDirectory() as tmp_dir:
        output_path = Path(tmp_dir) / 'output'
        assert example.format_name.lower() in ['md', 'csv']
        if example.format_name.lower() == 'md':
            output_path = output_path.with_suffix('.md')
        elif example.format_name.lower() == 'csv':
            output_path = output_path.with_suffix('.csv')
        else:
            raise ValueError(f'Unsupported format: {example.format_name}')
        result = example.example_function(example.format_name,
                                          str(output_path),
                                          example.implementation_name,
                                          example.optional_args)
        os.system(f'ls -l {tmp_dir}')
        with open(output_path, 'r', encoding='utf-8') as file:
            text = file.read()
        check_text_in_order(text, expected_fragments)
        assert result == 0
    out, err = capture.readouterr()
    assert out == ''
    assert err == ''
