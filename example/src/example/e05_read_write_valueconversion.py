#! /usr/bin/env python3
"""How to use the tableio package to read data with value conversion."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
from datetime import datetime
from tableio.factory import create_tableio
from tableio.optional_args import OptionalArgs
from tableio.tableio import FileAccess
from tableio.value_type import Value, ListData
from tableio.valueconversion import value2int, value2float, value2datetime, \
    value2bool, value2type
from tableio.capability import Capabilities, CAP_NEEDED, CAP_NOT_USED
from .cmd_for_examples import cmd_parse_and_run_example

#
# As usual we define the capabilities we need.
# Here we only need to read and write.
#
CAPS = Capabilities(
    can_write=CAP_NEEDED,
    can_read=CAP_NEEDED,
    can_fmt_row=CAP_NOT_USED,
    can_fmt_value=CAP_NOT_USED,
    filtered_data_range=CAP_NOT_USED,
    can_write_box=CAP_NOT_USED,
    can_read_box=CAP_NOT_USED,
    can_write_highlight=CAP_NOT_USED)


def e05_read_write_valueconversion(format_name: str, output_file_name: str,
                                   implementation_name: Optional[str],
                                   optional_args: OptionalArgs) -> int:
    """Read data with value conversion."""
    #
    # In e01_simple_read_write.py we did set the csv parameters to
    # get the data to be read back as the same type that it was written.
    # That is not always possible. Many times the file format will not
    # convert a value to a type the file format can support.
    #
    # A more general way to get a value of the type we know it actually was
    # is to use value conversion. When using value conversion, the actual
    # value we read is what the file format could store it as. Then we can
    # convert it to the type we know is correct for the information it
    # carries.
    #
    # Here is some example data that we will read and write:
    #
    start_time: datetime = datetime.now().replace(microsecond=0)
    end_time: datetime = datetime(year=2036, month=3, day=26,
                                  hour=12, minute=5, second=49)
    data1: ListData[Value] = [
        ['name', 'value', 'rounded', 'valid', 'when'],
        ['real', 3.14159, 3, True, start_time],
        ['fake', 2.71828, 3, False, end_time],
    ]
    #
    # We create the tableio object using the factory and use it as
    # a context manager to ensure it is closed properly. The file is
    # created if it does not exist. If it exists, an exception is raised.
    # With this tableio object we only write the data to the file.
    #
    with create_tableio(format_name=format_name,
                        file_name=output_file_name,
                        file_access=FileAccess.CREATE,
                        implementation=implementation_name,
                        capabilities=CAPS,
                        args=optional_args) as tableio:
        #
        # We write the data to the file.
        #
        tableio.write_table_listdata(data1)
    #
    # Now we pretend to be another program that reads the data from the file.
    # As usual we do this by creating a new tableio object using the factory
    # and use it as a context manager to ensure it is closed properly.
    #
    with create_tableio(format_name=format_name,
                        file_name=output_file_name,
                        file_access=FileAccess.READ,
                        implementation=implementation_name,
                        capabilities=CAPS,
                        args=optional_args) as tableio:
        #
        # We read the data back from the file.
        #
        result = tableio.read_table_listdata()
        #
        # Now we move on to verify that the data read back is
        # the same as the data we wrote.
        #
        # First we do it the hard way by comparing specific cell values.
        #
        data2 = result.data
        # assert not result.header  # no headers. len(result.header) == 0
        assert len(data1) == len(data2)
        assert len(data1[0]) == len(data2[0])
        assert data1[0] == data2[0]  # We assume rows with only str stays only str.
        assert data1[1][1] == value2float(data2[1][1])
        assert data1[1][2] == value2int(data2[1][2])
        assert data1[1][3] == value2bool(data2[1][3])
        print(format_name, data1[1][4], value2datetime(data2[1][4]))
        assert data1[1][4] == value2datetime(data2[1][4])
        assert data1[2][1] == value2float(data2[2][1])
        assert data1[2][2] == value2int(data2[2][2])
        assert data1[2][3] == value2bool(data2[2][3])
        assert data1[2][4] == value2datetime(data2[2][4])
        #
        # We also do it the easy way by comparing more automatic type detection.
        #
        for row1, row2 in zip(data1, data2):
            for value1, value2 in zip(row1, row2):
                assert value1 == value2type(value2, type(value1))
    return 0


if __name__ == '__main__':
    cmd_parse_and_run_example(example_name='e05_read_write_valueconversion',
                              func=e05_read_write_valueconversion,
                              caps=CAPS)
