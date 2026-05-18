#! /usr/bin/env python3
"""Command line handling and parsing for the example package."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
import argparse
from enum import IntEnum
from typing import Callable, Optional
from mformat.enum_str_util import from_str, possible_values
from mformat.paper_size import PaperSize
from mformat.document_class import DocumentClass
from tableio import Capabilities, CsvDialect, OptionalArgs, \
    OptionalArgsDict, list_implementations_tableio, \
    list_registered_tableio


type ExampleFunc = Callable[[str, str, Optional[str], OptionalArgs], int]
"""The function type for the example functions.

example_func(format_name: str, output_file_name: str,
             implementation_name: Optional[str],
             optional_args: OptionalArgs) -> int
"""

_CLI_STR_ARGS: list[str] = [
    'character_encoding', 'lang', 'title', 'css_file',
    'latex_preamble', 'csv_delimiter', 'csv_quoting',
    'csv_quotechar', 'csv_lineterminator', 'csv_escapechar']
_CLI_INT_ARGS: list[str] = ['line_length', 'table_max_line_length']
_CLI_ENUM_ARGS: list[tuple[str, type[IntEnum]]] = [
    ('csv_dialect', CsvDialect),
    ('paper_size', PaperSize),
    ('document_class', DocumentClass)]
_ALL_CLI_ARG_NAMES: list[str] = (
    _CLI_STR_ARGS + _CLI_INT_ARGS
    + [name for name, _ in _CLI_ENUM_ARGS])


def _cli_flag(name: str) -> str:
    """Convert an underscore-separated name to a --dashed CLI flag."""
    return '--' + name.replace('_', '-')


def _cli_help(name: str) -> str:
    """Derive a help string from a CLI argument name."""
    return name.replace('_', ' ').capitalize()


def _add_implementation_argument(parser: argparse.ArgumentParser,
                                 caps: Optional[Capabilities] = None) -> None:
    """Add the implementation argument to the parser."""
    impl_choices = list_implementations_tableio(capabilities=caps)
    impl_choices.append('all')
    impl_help = 'The implementation name. '
    impl_help += 'If "all" is specified, all implementations for each '
    impl_help += 'format are tried.'
    impl_help += f' Choices: {", ".join(impl_choices)}'
    impl_help += ' (Default is to use the best matching implementation.)'
    impl_allowed = list_implementations_tableio(lower=True, upper=True,
                                                capabilities=caps)
    impl_allowed.append('all')
    impl_allowed.append('ALL')
    parser.add_argument('-I', '--implementation', help=impl_help, nargs=1,
                        choices=impl_allowed, required=False)


def _add_format_argument(parser: argparse.ArgumentParser,
                         caps: Optional[Capabilities] = None) -> None:
    """Add the format argument to the parser."""
    fmt_choices = list_registered_tableio(capabilities=caps)
    fmt_choices.append('all')
    fmt_help = 'The format name. '
    fmt_help += 'If "all" is specified, all formats are tried.'
    fmt_help += f' Choices: {", ".join(fmt_choices)}'
    fmt_allowed = list_registered_tableio(lower=True, upper=True,
                                          capabilities=caps)
    fmt_allowed.append('all')
    fmt_allowed.append('ALL')
    parser.add_argument('-f', '--format', help=fmt_help, nargs=1,
                        choices=fmt_allowed, required=True)


def _add_optional_args_argument(parser: argparse.ArgumentParser) -> None:
    """Add optional command line arguments for OptionalArgsDict."""
    for name in _CLI_STR_ARGS:
        parser.add_argument(_cli_flag(name), type=str, nargs=1, required=False,
                            help=_cli_help(name))
    for name in _CLI_INT_ARGS:
        parser.add_argument(_cli_flag(name), type=int, nargs=1, required=False,
                            help=_cli_help(name))
    for name, enum_type in _CLI_ENUM_ARGS:
        choices = possible_values(enum_type, include_lower=True,
                                  include_upper=True)
        vals = ', '.join(possible_values(enum_type))
        help_text = f'{_cli_help(name)}. Choices: {vals}'
        parser.add_argument(_cli_flag(name), type=str, nargs=1, required=False,
                            choices=choices, help=help_text)


def _build_optional_args(parsed_args: argparse.Namespace) -> OptionalArgs:
    """Build an OptionalArgsDict from parsed command line arguments."""
    result: OptionalArgsDict = {}
    enum_map: dict[str, type[IntEnum]] = dict(_CLI_ENUM_ARGS)
    for name in _ALL_CLI_ARG_NAMES:
        raw = getattr(parsed_args, name, None)
        if raw is None:
            continue
        value = raw[0] if isinstance(raw, list) else raw
        if name in enum_map:
            value = from_str(enum_map[name], value)
        result[name] = value  # type: ignore[literal-required]
    return result or None


def _output_name_for(base: str, fmt: str, impl: Optional[str],
                     format_is_all: bool, impl_is_all: bool) -> str:
    """Build output file name for one format/impl combination."""
    name = base
    if format_is_all:
        name += f'_{fmt}'
    if impl_is_all and impl is not None:
        name += f'_{impl}'
    return name


def _unpack_and_run_example(example_name: str, func: ExampleFunc,
                            caps: Optional[Capabilities],
                            parsed_args: argparse.Namespace) -> int:
    """Unpack the command line arguments and run the example function.

    Args:
        example_name: The name of the example function.
                      (Used for error messages.)
        func: The example function to run.
        caps: The capabilities requested for the example function.
        parsed_args: The parsed command line arguments, to unpack
                     and pass to the example function.

    Returns:
        The return value of the example function, or the first
        non-zero return value if multiple combinations are tried.
    """
    output_base: str = parsed_args.output[0]
    impl_arg: Optional[str] = (
        parsed_args.implementation[0]
        if parsed_args.implementation else None)
    optional_args = _build_optional_args(parsed_args)
    format_is_all = (
        str(parsed_args.format[0]).upper() == 'ALL')
    impl_is_all = (
        impl_arg is not None
        and impl_arg.upper() == 'ALL')
    formats = (
        list_registered_tableio(capabilities=caps)
        if format_is_all
        else [str(parsed_args.format[0])])
    first_error = 0
    for fmt in formats:
        impls: list[Optional[str]] = []
        if impl_is_all:
            impls.extend(list_implementations_tableio(
                format_name=fmt, capabilities=caps, empty_is_ok=True))
        else:
            impls.append(impl_arg)
        for impl in impls:
            ret = func(
                fmt,
                _output_name_for(output_base, fmt, impl, format_is_all,
                                 impl_is_all),
                impl, optional_args)
            if ret != 0 and first_error == 0:
                first_error = ret
                print(f'{example_name}: error {ret} for '
                      f'format={fmt}, '
                      f'implementation={impl}',
                      file=sys.stderr)
    return first_error


def cmd_parse_and_run_example(example_name: str, func: ExampleFunc,
                              caps: Optional[Capabilities] = None,
                              args: Optional[list[str]] = None) -> None:
    """Parse the command line arguments for the example function."""
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser(description=f'Example: {example_name}')
    parser.add_argument('-o', '--output', help='The output file name',
                        type=str, nargs=1, required=True)
    _add_format_argument(parser, caps)
    _add_implementation_argument(parser, caps)
    _add_optional_args_argument(parser)
    parsed_args = parser.parse_args(args)
    ret = _unpack_and_run_example(example_name, func, caps, parsed_args)
    sys.exit(ret)
