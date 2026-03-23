# tableio

The tableio package contains a number of classes providing a uniform way for
a python program to write table data (rows of columns) to and read table data
from a number of different common file formats.

The primary intended use is for text output from a python program, where the
programmer would like the user to be able to select the input and output file
formats.

The support for spreadsheets is for reading and writing data. There is no
intention to support reading or writing formulas. There is no support for
running calculations in the spreadsheets (although nothing will stop a
receiver of a spreadsheet created by tableio package to manually add
formulas in the received spreadsheet).

## Early design phase

This project is in an early design phase. This means that major changes to the APIs are still expected.

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
| HTML        | mformat        | yes       | -        |
| LaTeX       | mformat        | yes       | -        |
| docx        | mformat        | yes       | -        |
| md          | mformat        | yes       | -        |
| odt         | mformat        | yes       | -        |
| pdf         | mformat        | yes       | -        |
| rst         | mformat        | yes       | -        |
| rtf         | mformat        | yes       | -        |
| txt         | mformat        | yes       | -        |

## Example programs

Some example programs are available at: [https://bitbucket.org/tom-bjorkholm/table-io/src/master/example/src/example/](https://bitbucket.org/tom-bjorkholm/table-io/src/master/example/src/example/).

## API documentation

Be aware that this is still in early development. The APIs may change between versions.

You can find the public API documentation at [https://bitbucket.org/tom-bjorkholm/table-io/src/master/doc/api.md](https://bitbucket.org/tom-bjorkholm/table-io/src/master/doc/api.md)

You can find the protected API documentation at [https://bitbucket.org/tom-bjorkholm/table-io/src/master/doc/protected_api.md](https://bitbucket.org/tom-bjorkholm/table-io/src/master/doc/protected_api.md)
The protected API documentation is only for developers that want to
extend the framework with by adding their own classes as registered
readers/writers to the factory.

Even though the API documentation exists, most users and programmers probably get
a better start by reading the examples.

## Version history

| Version | Date        | Python version | Comment                |
|---------|-------------|----------------|------------------------|
| 0.1     | 2026 Mar 23 | 3.12 or newer  | First released version |

## Test summary

- Test result: 634 passed in 15s
- No Flake8 warnings.
- No mypy errors found.
- Built version(s): 0.1.1
- Build and test using Python 3.14.3
