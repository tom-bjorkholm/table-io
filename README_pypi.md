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
- writing a table as a filtered data range
- writing a table to a specific location in a spreadsheet (specified by a box)
- reading table data from a specific location in a spreadsheet (specified by a box)
- using multiple sheets in spreadsheets
- finding location where some data is present in spreadsheet and doing modifications
  at that position or at positions relative to that position.
- several border styles for tables

## Example programs

The best way to learn to use this package is to use the provided
example programs:
[https://bitbucket.org/tom-bjorkholm/table-io/src/master/example/src/example/README.md](https://bitbucket.org/tom-bjorkholm/table-io/src/master/example/src/example/README.md).

## API documentation

You can find the public API documentation at [https://bitbucket.org/tom-bjorkholm/table-io/src/master/doc/api.md](https://bitbucket.org/tom-bjorkholm/table-io/src/master/doc/api.md)

You can find the protected API documentation at [https://bitbucket.org/tom-bjorkholm/table-io/src/master/doc/protected_api.md](https://bitbucket.org/tom-bjorkholm/table-io/src/master/doc/protected_api.md)
The protected API documentation is only for developers that want to
extend the framework by adding their own classes as registered
readers/writers to the factory.

Even though the API documentation exists, most users and programmers probably get
a better start by reading the examples.

## Test summary

- Test result: 1186 passed in 18s
- No flake8 warnings.
- No mypy errors found.
- Built version(s): 0.7.1
- Build and test using Python 3.14.4
