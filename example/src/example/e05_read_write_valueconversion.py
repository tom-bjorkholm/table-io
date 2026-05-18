#! /usr/bin/env python3
"""Show how to read data back with value conversion helpers."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
from datetime import datetime, timedelta
from tableio import CAP_NEEDED, CAP_NOT_USED, Capabilities, DictData, \
    FileAccess, ListData, OptionalArgs, ReadResult, Value, create_tableio
from tableio.valueconversion import value2int, value2float, value2datetime, \
    value2bool, value2type, value2type_of
from .cmd_for_examples import cmd_parse_and_run_example

#
# As usual we define the capabilities we need.
# Here we only need to read and write.
#
# pylint: disable=duplicate-code
CAPS = Capabilities(can_write=CAP_NEEDED, can_read=CAP_NEEDED,
                    can_fmt_row=CAP_NOT_USED, can_fmt_value=CAP_NOT_USED,
                    filtered_data_range=CAP_NOT_USED,
                    can_write_box=CAP_NOT_USED, can_read_box=CAP_NOT_USED,
                    can_write_highlight=CAP_NOT_USED)


def compare_written_to_read1(written: ListData[Value],
                             result: ReadResult[ListData[Value]]) -> None:
    """Compare the written data to the read data.

    The written and read data should carry the same information, but the
    limitations of the file type may have changed the types of the values.
    We will convert the values to the expected type and compare them.
    Here we do it the hard way by comparing specific cell values,
    converted to the expected type for that cell.

    Args:
        written: The written data.
        result: The read data.
    """
    assert not result.headings  # no headings. len(result.headings) == 0
    assert len(written) == len(result.data)
    assert len(written[0]) == len(result.data[0])
    # We assume rows with only str stays only str.
    assert written[0] == result.data[0]
    # We convert the values to the expected type for each cell.
    assert written[1][1] == value2float(result.data[1][1])
    assert written[1][2] == value2int(result.data[1][2])
    assert written[1][3] == value2bool(result.data[1][3])
    assert written[1][4] == value2datetime(result.data[1][4])
    assert written[2][1] == value2float(result.data[2][1])
    assert written[2][2] == value2int(result.data[2][2])
    assert written[2][3] == value2bool(result.data[2][3])
    assert written[2][4] == value2datetime(result.data[2][4])


def compare_written_to_read2(written: ListData[Value],
                             result: ReadResult[ListData[Value]]) -> None:
    """Compare the written data to the read data.

    The written and read data should carry the same information, but the
    limitations of the file type may have changed the types of the values.
    We will convert the values to the expected type and compare them.
    Here we do it the easy way by using value2type() to convert each
    read value to the type of the written value we compare it with.

    Args:
        written: The written data.
        result: The read data.
    """
    assert not result.headings  # no headings. len(result.headings) == 0
    assert len(written) == len(result.data)
    assert len(written[0]) == len(result.data[0])
    # We convert the values to the expected type for each cell.
    for row1, row2 in zip(written, result.data):
        for value1, value2 in zip(row1, row2):
            assert value1 == value2type(value2, type(value1))


def compare_written_to_read3(written: DictData[Value],
                             result: ReadResult[DictData[Value]]) -> None:
    """Compare the written data to the read data.

    The written and read data should carry the same information, but the
    limitations of the file type may have changed the types of the values.
    We will convert the values to the expected type and compare them.
    Here we do it the easy way by using value2type_of() with the written
    value as the type example we want to convert to.

    Args:
        written: The written data.
        result: The read data.
    """
    assert not result.headings  # no headings. len(result.headings) == 0
    assert len(written) == len(result.data)
    assert len(written[0]) == len(result.data[0])
    # We convert the values to the expected type for each cell.
    for row1, row2 in zip(written, result.data):
        for key1, value1 in row1.items():
            assert value1 == value2type_of(row2[key1], value1)


def e05_read_write_valueconversion(format_name: str, output_file_name: str,
                                   implementation_name: Optional[str],
                                   optional_args: OptionalArgs) -> int:
    """Read data back and convert values to the expected Python types."""
    #
    # In e01_simple_read_write.py we set CSV parameters so values were
    # often read back as the same type they were written. That is not
    # always possible. Many file formats cannot preserve every Python type.
    #
    # A more general solution is to use value conversion. The value we read
    # back is whatever representation the file format could store, and we
    # then convert that value to the Python type we actually want.
    #
    # We will read and write both list and dict data.
    # Here is some example data that we will read and write:
    #
    start_time: datetime = datetime.now().replace(microsecond=0)
    end_time: datetime = datetime(year=2036, month=3, day=26, hour=12,
                                  minute=5, second=49)
    data1: ListData[Value] = [
        ['name', 'value', 'rounded', 'valid', 'when'],
        ['real', 3.14159, 3, True, start_time],
        ['fake', 2.71828, 3, False, end_time],
    ]
    datad1: DictData[Value] = [
        {'name': 'magic', 'answer': 42, 'part': 0.5, 'valid': True,
         'when': start_time - timedelta(seconds=1)},
        {'name': 'show', 'answer': 100, 'part': 0.25, 'valid': False,
         'when': datetime(year=2026, month=12, day=25, hour=8, minute=5,
                          second=49)},
    ]
    column_order: list[str] = ['name', 'answer', 'part', 'valid', 'when']
    #
    # We create the tableio object using the factory and use it as
    # a context manager to ensure it is closed properly. The file is
    # created if it does not exist. If it exists, an exception is raised.
    # In this first context manager we only write the data to the file.
    #
    with create_tableio(format_name=format_name, file_name=output_file_name,
                        file_access=FileAccess.CREATE,
                        implementation=implementation_name, capabilities=CAPS,
                        args=optional_args) as tableio:
        #
        # We write the data to the file.
        #
        tableio.write_table_listdata(data=data1)
        tableio.write_table_dictdata(data=datad1, column_order=column_order)
    #
    # Now we pretend to be another program that reads the data from the
    # file. As usual we do this by creating a new tableio object with the
    # factory and using it as a context manager.
    #
    with create_tableio(format_name=format_name, file_name=output_file_name,
                        file_access=FileAccess.READ,
                        implementation=implementation_name, capabilities=CAPS,
                        args=optional_args) as tableio:
        #
        # We read the data back from the file.
        #
        result = tableio.read_table_listdata()
        resultd = tableio.read_table_dictdata()
        #
        # Now we move on to verify that the data read back is
        # the same as the data we wrote.
        compare_written_to_read1(data1, result)
        compare_written_to_read2(data1, result)
        compare_written_to_read3(datad1, resultd)
    return 0


if __name__ == '__main__':
    cmd_parse_and_run_example(example_name='e05_read_write_valueconversion',
                              func=e05_read_write_valueconversion, caps=CAPS)
