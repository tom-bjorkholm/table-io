#! /usr/bin/env python3
"""Show how to write and read timedelta (duration) values."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import timedelta
from typing import Optional
from tableio import CAP_NEEDED, CAP_NOT_USED, Capabilities, DictData, \
    FileAccess, ListData, OptionalArgs, TimeDeltaFallback, Value, \
    create_tableio, format_timedelta, parse_timedelta
from tableio.valueconversion import value2timedelta
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
# pylint: enable=duplicate-code


def read_durations(values: list[Value]) -> list[timedelta]:
    """Convert values read from a file back to timedelta values.

    Spreadsheet formats (Excel, ODS) store timedelta values natively, so
    what we read back already is a timedelta. Formats without native
    timedelta support (like CSV) store a fallback representation, so what
    we read back is a string (or a number of seconds).

    Args:
        values: The values read from the file.
    Returns:
        The values converted to timedelta.
    """
    durations: list[timedelta] = []
    for value in values:
        #
        # parse_timedelta() returns a timedelta value unchanged (native
        # timedelta support), and converts all fallback representations.
        # So we do not need to know if the file format had native support,
        # or which fallback was used when the file was written.
        # It accepts str, int, float and timedelta (and raises TypeError for
        # bool), so we first check that we got one of the accepted types.
        #
        assert isinstance(value, (str, int, float, timedelta))
        durations.append(parse_timedelta(value))
    return durations


def e15_timedelta(format_name: str, output_file_name: str,
                  implementation_name: Optional[str],
                  optional_args: OptionalArgs) -> int:
    """Write timedelta values, read them back and convert them."""
    #
    # A timedelta is a duration, like 'three hours and five minutes'.
    # Here are some tasks with an estimated and an actual duration.
    # Notice that durations may be longer than a day, have fractions of
    # a second, and may even be negative (like a difference).
    # Notice: Microsoft Excel has no duration type. It stores a duration as
    # a number of days with a time number format. The cell shows for
    # instance '72:00:00', but by design the formula bar shows the value as
    # a date and time (like '1/3/1900 12:00:00 AM'). Excel does the same
    # for durations typed in by hand. LibreOffice shows '72:00:00' in both.
    #
    data: ListData[Value] = [
        ['task', 'estimate', 'actual'],
        ['design', timedelta(hours=6), timedelta(hours=7, minutes=30)],
        ['build', timedelta(days=2, hours=3), timedelta(days=3)],
        ['test', timedelta(minutes=45), timedelta(minutes=41, seconds=2.5)]
    ]
    #
    # The same kind of data can of course also be written as dict data.
    # Here we write how much each task was late (a negative value
    # means the task was done early).
    # Notice: Microsoft Excel cannot display negative durations (it shows
    # '####' in the cell), but the value is stored and read back correctly.
    # LibreOffice displays the negative duration.
    #
    datad: DictData[Value] = [
        {'task': 'design', 'late': timedelta(hours=1, minutes=30)},
        {'task': 'build', 'late': timedelta(days=1, hours=5)},
        {'task': 'test', 'late': timedelta(minutes=-3, seconds=-57.5)}
    ]
    #
    # format_timedelta() formats a timedelta in any of the fallback
    # formats. It is used internally by the formats that lack native
    # timedelta support, but it is also useful for text you create
    # yourself. Here we use it in a heading.
    #
    total = sum((row['late'] for row in datad
                 if isinstance(row['late'], timedelta)), timedelta(0))
    heading = 'Total late: ' + \
        str(format_timedelta(total, TimeDeltaFallback.DHMS_STRING_LONG))
    #
    # Formats without native timedelta support (CSV and the write-only
    # document formats) write timedelta values using a fallback format.
    # The fallback is chosen with the optional argument
    # 'timedelta_fallback' (on the command line of this example:
    # --timedelta-fallback). The default is TimeDeltaFallback.HMS_STRING,
    # that writes for instance two days and three hours as '51:00:00'.
    # Formats with native timedelta support silently ignore the fallback.
    #
    with create_tableio(format_name=format_name, file_name=output_file_name,
                        file_access=FileAccess.CREATE,
                        implementation=implementation_name, capabilities=CAPS,
                        args=optional_args) as tableio:
        tableio.write_table_listdata(data=data)
        tableio.write_heading(heading)
        tableio.write_table_dictdata(data=datad, column_order=['task', 'late'])
    #
    # Now we pretend to be another program that reads the file.
    #
    with create_tableio(format_name=format_name, file_name=output_file_name,
                        file_access=FileAccess.READ,
                        implementation=implementation_name, capabilities=CAPS,
                        args=optional_args) as tableio:
        result = tableio.read_table_listdata()
        resultd = tableio.read_table_dictdata()
    #
    # We convert the read values with our helper function read_durations()
    # and check that they are the same as the values we wrote.
    #
    for written_row, read_row in zip(data[1:], result.data[1:], strict=True):
        assert read_durations(read_row[1:]) == written_row[1:]
    assert resultd.headings == [heading]
    #
    # Instead of our own helper we can also use value2timedelta() from the
    # value conversion helpers (see example e05). It accepts the same
    # values as parse_timedelta(), and raises the value conversion
    # exceptions for values that cannot be converted.
    #
    for written_dict, read_dict in zip(datad, resultd.data, strict=True):
        assert value2timedelta(read_dict['late']) == written_dict['late']
    return 0


if __name__ == '__main__':
    cmd_parse_and_run_example(example_name='e15_timedelta', func=e15_timedelta,
                              caps=CAPS)
