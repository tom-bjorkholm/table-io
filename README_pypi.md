# tableio

The tableio package contains a number of classes providing a uniform way for
a python program to write table data (rows of columns) to and read table data
from a number of different common file formats.

An increasing number of users want output from programs to be in a format
like a spreadsheet, and not the old fashoned raw text files. Similarly,
many users want the data they feed into programs to be in a particular format
(like a spreadsheet). The tableio package tries to make it easier for the
programmer to fullfil requests like that.

The primary intended use is for data table output from a python program
and data table input to a python program, where the programmer would like
the user to be able to select the input and output file formats.

The support for spreadsheets is for reading and writing data. There is no
intention to support reading or writing formulas. There is no support for
running calculations in the spreadsheets (although nothing will stop a
receiver of a spreadsheet created by tableio package to manually add
formulas in the received spreadsheet).

## Installing tableio

### Installing tableio on mac and Linux

````sh
pip3 install --upgrade tableio
````

### Installing tableio on Microsoft Windows

````sh
pip install --upgrade tableio
````

## Supported formats

The currently supported formats are:

| File format | Implementation | Can write | Can read |
|-------------|----------------|-----------|----------|
| CSV         | csv            | yes       | yes      |
| Excel       | OpenPyXL       | yes       | yes      |
| Excel       | XlsxWriter     | yes       | -        |
| Excel       | pylightxl      | yes       | yes      |
| ODS         | odfdo          | yes       | yes      |
| HTML        | mformat        | yes       | -        |
| LaTeX       | mformat        | yes       | -        |
| docx        | mformat        | yes       | -        |
| md          | mformat        | yes       | -        |
| odt         | mformat        | yes       | -        |
| pdf         | mformat        | yes       | -        |
| reST        | mformat        | yes       | -        |
| rtf         | mformat        | yes       | -        |
| txt         | mformat        | yes       | -        |

## Features

All features are not available for all file formats. Often the file
format restricts what features are reasonable in that format. Using
a selection mechanism called Capabilities it is possible to select
file format at runtime based on what features are essential. It is
also possible to ignore some features when using a file format that
cannot support that feature (like ignoring bold fomatting in CSV).

The main features are:

- File open modes: Create, Read or Update
- Writing tables from list of lists or list of dicts
- Writing headings before and between tables
- Reading tables to list of lists or list of dicts, including the headings
  before the table.
- formatting per cell or per row:
  - bold format
  - italics format
  - highlight colour
- reading and writing cells with data types:
  - str
  - bool
  - int
  - float
  - datetime
  - timedelta (see below)
- writing a table as a filtered data range
- writing a table to a specific location in a spreadsheet (specified by a box)
- reading table data from a specific location in a spreadsheet (specified by a box)
- using multiple sheets in spreadsheets
- finding location where some data is present in spreadsheet and doing modifications
  at that position or at positions relative to that position.
- several border styles for tables

## Timedelta (duration) values

Excel (OpenPyXL, XlsxWriter, pylightxl) and ODS (odfdo) store `timedelta`
values natively, as duration cells, and read them back as `timedelta`.
(OpenPyXL reads durations with millisecond precision.)
The cells are displayed as `[hh]:mm:ss` (hours do not wrap at 24, seconds
are displayed rounded to whole seconds, the stored value is exact).
Microsoft Excel has no duration type, it stores a duration as a number of
days with a time number format. So by design Excel shows the cell as for
instance `72:00:00`, but shows the value as a date and time (like
`1/3/1900 12:00:00 AM`) in the formula bar when the cell is selected. Excel
does the same for durations typed in by hand, and LibreOffice shows
`72:00:00` in both places for the same file.
Notice also that Microsoft Excel cannot display negative durations (it
shows `####`). The stored value is still correct, it is read back
correctly and LibreOffice displays it as for instance `-00:03:58`. If
negative durations must be readable in Microsoft Excel, consider storing
the magnitude and the sign in separate columns.

Formats without native duration support (CSV and all write-only document
formats) write a fallback representation, selected with the optional
argument `timedelta_fallback` (a `TimeDeltaFallback` value):

| TimeDeltaFallback     | Two days, three hours and 1.5 seconds |
|-----------------------|---------------------------------------|
| `HMS_STRING` (default)| `51:00:01.5`                          |
| `DHMS_STRING`         | `2 d 03:00:01.5`                      |
| `DHMS_STRING_LONG`    | `2 days 03:00:01.5`                   |
| `WDHMS_STRING`        | `2 d 03:00:01.5` (with `W w` if a week or more) |
| `WDHMS_STRING_LONG`   | `2 days 03:00:01.5` (with `W weeks` if a week or more) |
| `FLOATSECONDS`        | `183601.5`                            |

Negative durations get a leading `-`. When reading such a file the values
are strings (CSV). Convert them with `parse_timedelta()`, that accepts all
fallback formats (and `timedelta` values, so it works for all formats).
`format_timedelta()` formats a `timedelta` in any of the fallback formats.

## Example programs

The best way to learn to use this package is to use the provided
example programs:
[https://github.com/tom-bjorkholm/table-io/blob/master/example/src/example/README.md](https://github.com/tom-bjorkholm/table-io/blob/master/example/src/example/README.md).

## API documentation

You can find the public API documentation at [https://github.com/tom-bjorkholm/table-io/blob/master/doc/api.md](https://github.com/tom-bjorkholm/table-io/blob/master/doc/api.md)

You can find the protected API documentation at [https://github.com/tom-bjorkholm/table-io/blob/master/doc/protected_api.md](https://github.com/tom-bjorkholm/table-io/blob/master/doc/protected_api.md)
The protected API documentation is only for developers that want to
extend the framework by adding their own classes as registered
readers/writers to the factory.

Even though the API documentation exists, most users and programmers probably get
a better start by reading the examples.

## Test summary

- Test result: 1567 passed in 14s
- No flake8 warnings.
- No mypy errors found.
- No pylint warnings.
- No python layout warnings.
- Built version(s): 1.2
- Build and test using Python 3.13.15
