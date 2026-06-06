#! /usr/bin/env python3
"""Measure TableIO table read and write speed from the command line."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
from pathlib import Path
import sys
from time import perf_counter
from typing import Callable, NamedTuple, Optional

from tableio import FileAccess, OptionalArgsDict, TableIO, Value, \
    access_capabilities, create_tableio

_READ_CAPS = access_capabilities(FileAccess.READ)
_WRITE_CAPS = access_capabilities(FileAccess.CREATE)


class _SpeedConfig(NamedTuple):
    """Validated speed-test command-line configuration."""

    format_name: str
    implementation: Optional[str]
    loops: int
    dict_data: bool
    input_file: Optional[Path]
    output_file: Optional[Path]
    rows: Optional[int]
    columns: Optional[int]


class _TableShape(NamedTuple):
    """Physical row and column count for one measured table."""

    rows: int
    columns: int


class _TargetInfo(NamedTuple):
    """Resolved target file and selected TableIO implementation."""

    file_name: Path
    format_name: str
    implementation: str


class _TimingResult(NamedTuple):
    """Timing samples and the table shape observed in the last loop."""

    times: list[float]
    shape: _TableShape


class _RunResult(NamedTuple):
    """The operation, target and timing result from one speed test."""

    operation: str
    target: _TargetInfo
    result: _TimingResult


def _allow_existing(file_name: str) -> None:
    """Allow creating a TableIO object only to inspect its resolved file."""
    _ = file_name


def _path_arg(value: object) -> Optional[Path]:
    """Return an optional argparse Path value with a checked type."""
    if value is None:
        return None
    if not isinstance(value, Path):
        raise TypeError('Expected Path argument from argparse.')
    return value


def _str_arg(value: object, name: str) -> str:
    """Return an argparse string value with a checked type."""
    if not isinstance(value, str):
        raise TypeError(f'Expected string argument for {name}.')
    return value


def _optional_str_arg(value: object, name: str) -> Optional[str]:
    """Return an optional argparse string value with a checked type."""
    if value is None:
        return None
    return _str_arg(value, name)


def _optional_int_arg(value: object, name: str) -> Optional[int]:
    """Return an optional argparse int value with a checked type."""
    if value is None:
        return None
    if not isinstance(value, int):
        raise TypeError(f'Expected integer argument for {name}.')
    return value


def _bool_arg(value: object, name: str) -> bool:
    """Return an argparse bool value with a checked type."""
    if not isinstance(value, bool):
        raise TypeError(f'Expected bool argument for {name}.')
    return value


def _check_positive(parser: argparse.ArgumentParser, value: int,
                    name: str) -> None:
    """Reject non-positive integer command-line values."""
    if value < 1:
        parser.error(f'{name} must be at least 1.')


def _check_output_size(parser: argparse.ArgumentParser, rows: int,
                       columns: int, dict_data: bool) -> None:
    """Reject output sizes that TableIO cannot write as tables."""
    _check_positive(parser, rows, 'rows')
    _check_positive(parser, columns, 'columns')
    if rows == 1 and columns == 1:
        parser.error('Output table must contain at least two cells.')
    if dict_data and rows < 2:
        parser.error('Dict output needs at least two physical rows.')
    if dict_data and rows == 2 and columns == 1:
        parser.error('Dict output needs at least two data cells.')


def _config_from_args(parser: argparse.ArgumentParser,
                      parsed: argparse.Namespace) -> _SpeedConfig:
    """Build validated configuration from parsed argparse values."""
    format_name = _str_arg(parsed.format_name, 'format')
    implementation = _optional_str_arg(parsed.implementation, 'implementation')
    loops = _optional_int_arg(parsed.loops, 'loops')
    assert loops is not None
    _check_positive(parser, loops, 'loops')
    rows = _optional_int_arg(parsed.rows, 'rows')
    columns = _optional_int_arg(parsed.columns, 'columns')
    input_file = _path_arg(parsed.input_file)
    output_file = _path_arg(parsed.output_file)
    dict_data = _bool_arg(parsed.dict_data, 'dict_data')
    if output_file is None:
        if rows is not None or columns is not None:
            parser.error('Rows and columns are only valid with output.')
    else:
        if rows is None or columns is None:
            parser.error('Output mode requires rows and columns.')
        _check_output_size(parser, rows, columns, dict_data)
    return _SpeedConfig(format_name=format_name, implementation=implementation,
                        loops=loops, dict_data=dict_data,
                        input_file=input_file, output_file=output_file,
                        rows=rows, columns=columns)


def _parse_args(args: Optional[list[str]]) -> _SpeedConfig:
    """Parse command-line arguments for the speed test program."""
    parser = argparse.ArgumentParser(
        description='Measure TableIO table read and write speed.')
    parser.add_argument('-f', '--format', dest='format_name', required=True,
                        help='TableIO format name.')
    parser.add_argument('--implementation', required=False,
                        help='Optional TableIO implementation name.')
    parser.add_argument('-l', '--loops', type=int, default=1,
                        help='Number of read or write loops.')
    parser.add_argument('-d', '--dict-data', action='store_true',
                        help='Use dict data instead of list data.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--input', dest='input_file', type=Path,
                       help='Input file name to read.')
    group.add_argument('-o', '--output', dest='output_file', type=Path,
                       help='Output file name to write.')
    parser.add_argument('-r', '--rows', type=int,
                        help='Physical row count for output.')
    parser.add_argument('-c', '--columns', type=int,
                        help='Column count for output.')
    return _config_from_args(parser, parser.parse_args(args))


def _existing_args() -> OptionalArgsDict:
    """Return optional args that allow resolving an existing target file."""
    return OptionalArgsDict(file_exists_callback=_allow_existing)


def _probe_tableio(config: _SpeedConfig, file_name: Path,
                   access: FileAccess) -> TableIO:
    """Create a TableIO object to inspect the selected implementation."""
    args = _existing_args() if access == FileAccess.CREATE else None
    capabilities = _WRITE_CAPS if access == FileAccess.CREATE else _READ_CAPS
    return create_tableio(format_name=config.format_name, file_name=file_name,
                          file_access=access, args=args,
                          implementation=config.implementation,
                          capabilities=capabilities)


def _target_info(config: _SpeedConfig) -> _TargetInfo:
    """Return the resolved target path and selected implementation."""
    file_name = config.output_file
    access = FileAccess.CREATE
    if file_name is None:
        file_name = config.input_file
        access = FileAccess.READ
    assert file_name is not None
    table_io = _probe_tableio(config, file_name, access)
    desc = table_io.get_description()
    return _TargetInfo(file_name=Path(table_io.file_name),
                       format_name=desc.format_name,
                       implementation=desc.implementation)


def _cell_value(row: int, column: int, columns: int) -> Value:
    """Return one unique cell value for the generated speed-test table."""
    cell_index = row * columns + column
    if cell_index % 2 == 0:
        return f's{cell_index}'
    return cell_index


def _list_data(rows: int, columns: int) -> list[list[Value]]:
    """Create generated list data for one write speed test."""
    return [
        [_cell_value(row, column, columns) for column in range(columns)]
        for row in range(rows)]


def _column_names(columns: int) -> list[str]:
    """Create unique dict column names for one write speed test."""
    return [f'c{column}' for column in range(columns)]


def _dict_data(rows: int, columns: int,
               column_names: list[str]) -> list[dict[str, Value]]:
    """Create generated dict data for one write speed test."""
    return [
        {
            name: _cell_value(row, column, columns)
            for column, name in enumerate(column_names)
        }
        for row in range(1, rows)]


def _list_shape(data: list[list[Value]]) -> _TableShape:
    """Return the physical shape of list table data."""
    if not data:
        return _TableShape(rows=0, columns=0)
    return _TableShape(rows=len(data), columns=len(data[0]))


def _dict_shape(data: list[dict[str, Value]]) -> _TableShape:
    """Return the physical shape of dict table data."""
    if not data:
        return _TableShape(rows=0, columns=0)
    return _TableShape(rows=len(data) + 1, columns=len(data[0]))


def _measure(loops: int, action: Callable[[], _TableShape],
             setup: Optional[Callable[[], None]] = None) -> _TimingResult:
    """Measure repeated action calls and return all timing samples."""
    times: list[float] = []
    shape = _TableShape(rows=0, columns=0)
    for _ in range(loops):
        if setup is not None:
            setup()
        start_time = perf_counter()
        shape = action()
        times.append(perf_counter() - start_time)
    return _TimingResult(times=times, shape=shape)


def _write_list(config: _SpeedConfig, target: _TargetInfo) -> _TimingResult:
    """Measure writing generated list data."""
    rows = config.rows
    columns = config.columns
    assert rows is not None
    assert columns is not None
    data = _list_data(rows, columns)

    def write_once() -> _TableShape:
        """Write the generated list data once."""
        with create_tableio(format_name=config.format_name,
                            file_name=target.file_name,
                            file_access=FileAccess.CREATE,
                            implementation=config.implementation,
                            capabilities=_WRITE_CAPS) as table_io:
            table_io.write_table_listdata(data)
        return _TableShape(rows=rows, columns=columns)

    return _measure(config.loops, write_once,
                    setup=lambda: target.file_name.unlink(missing_ok=True))


def _write_dict(config: _SpeedConfig, target: _TargetInfo) -> _TimingResult:
    """Measure writing generated dict data."""
    rows = config.rows
    columns = config.columns
    assert rows is not None
    assert columns is not None
    column_names = _column_names(columns)
    data = _dict_data(rows, columns, column_names)

    def write_once() -> _TableShape:
        """Write the generated dict data once."""
        with create_tableio(format_name=config.format_name,
                            file_name=target.file_name,
                            file_access=FileAccess.CREATE,
                            implementation=config.implementation,
                            capabilities=_WRITE_CAPS) as table_io:
            table_io.write_table_dictdata(data, column_order=column_names)
        return _TableShape(rows=rows, columns=columns)

    return _measure(config.loops, write_once,
                    setup=lambda: target.file_name.unlink(missing_ok=True))


def _read_list(config: _SpeedConfig, target: _TargetInfo) -> _TimingResult:
    """Measure reading list data from the configured input file."""

    def read_once() -> _TableShape:
        """Read list data once."""
        with create_tableio(format_name=config.format_name,
                            file_name=target.file_name,
                            file_access=FileAccess.READ,
                            implementation=config.implementation,
                            capabilities=_READ_CAPS) as table_io:
            result = table_io.read_table_listdata()
        return _list_shape(result.data)

    return _measure(config.loops, read_once)


def _read_dict(config: _SpeedConfig, target: _TargetInfo) -> _TimingResult:
    """Measure reading dict data from the configured input file."""

    def read_once() -> _TableShape:
        """Read dict data once."""
        with create_tableio(format_name=config.format_name,
                            file_name=target.file_name,
                            file_access=FileAccess.READ,
                            implementation=config.implementation,
                            capabilities=_READ_CAPS) as table_io:
            result = table_io.read_table_dictdata()
        return _dict_shape(result.data)

    return _measure(config.loops, read_once)


def _run_speed_test(config: _SpeedConfig) -> _RunResult:
    """Run the requested speed test and return operation metadata."""
    target = _target_info(config)
    if config.output_file is not None:
        if config.dict_data:
            return _RunResult('write', target, _write_dict(config, target))
        return _RunResult('write', target, _write_list(config, target))
    if config.dict_data:
        return _RunResult('read', target, _read_dict(config, target))
    return _RunResult('read', target, _read_list(config, target))


def _average(values: list[float]) -> float:
    """Return the arithmetic mean of a non-empty float list."""
    return sum(values) / len(values)


def _print_result(config: _SpeedConfig, operation: str, target: _TargetInfo,
                  result: _TimingResult) -> None:
    """Print one speed-test result summary."""
    print(f'operation: {operation}')
    print(f'data: {"dict" if config.dict_data else "list"}')
    print(f'format: {target.format_name}')
    print(f'implementation: {target.implementation}')
    print(f'rows: {result.shape.rows}')
    print(f'columns: {result.shape.columns}')
    print(f'loops: {len(result.times)}')
    print(f'min_seconds: {min(result.times):.6f}')
    print(f'max_seconds: {max(result.times):.6f}')
    print(f'average_seconds: {_average(result.times):.6f}')


def main(args: Optional[list[str]] = None) -> int:
    """Run the speed test program."""
    config = _parse_args(args)
    run_result = _run_speed_test(config)
    _print_result(config, run_result.operation, run_result.target,
                  run_result.result)
    return 0


if __name__ == '__main__':
    sys.exit(main())
