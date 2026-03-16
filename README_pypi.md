# tableio


The tableio package contains a number of classes providing a uniform way for
a python program to write table data (rows of columns) to and read table data
from a number of different common file formats.

The primary intended use is for text output from a python program, where the
programmer would like the user to be able to select the input and output file
formats.

## Early design phase

This project is in an early design phase. This means that major changes to the APIs are still expected.

## Later availability / Installing tableio

### Installing base mformat on mac and Linux

````sh
pip3 install --upgrade mformat
````

### Installing base mformat on Microsoft Windows

````sh
pip install --upgrade mformat
````

## Installing mformat-ext (extended package)

The extended package contains support also for output formats that require some
additional dependencies. Use this if you want the full selection of output
formats.

If you want to use it, install it using pip from
[https://pypi.org/project/mformat-ext](https://pypi.org/project/mformat-ext) .
There is no need to download anything from Bitbucket to write Python programs
that use the library.

### Installing extended mformat on mac and Linux

````sh
pip3 install --upgrade mformat-ext
````

### Installing extended mformat on Microsoft Windows

````sh
pip install --upgrade mformat-ext
````

## What it does

The main features supported in a uniform way for all supported output file
formats are:

- Factory function that takes file format and output file name as arguments

- It opens and closes a file in the selected format, with protection against
  accidentically overwriting an existing file

- The recommended way to use it is as a context manager in a with-clause,
  opening and closing the file

- Headings (several levels)

- Paragraphs

- Nested bullet point lists

- Nested numbered point lists

- Mixed nested numbered point and bullet point lists

- Tables

- URLs in paragraphs, headings, numbered point list items and in bullet point
  list items

## Design of program that uses mformat

It is recommended that the ouput function(s) of the a Python program using
mformat should have a with-clause getting the formatting object from the factory
(easiest with `with create_mf(file_format=fmt, file_name=output_file_name) as`
).

In the context of the with-clause the programmer just calls a minimum of member
functions:

- `new_paragraph` to start a new paragraph with some provided text content.

- `new_heading` to start a new heading with some provided text content.

- `new_bullet_item` to start a new bullet point list item with some provided
  text content, and if needed to start the bullet point list with the bullet
  point item.

- `new_numbered_point_item` to start a new numbered point list item with some
  provided text content, and if needed to start the numbered point list with the
  number point list item.

- `new_block_quote` to start a new block quote with some provided text content.

- `add_text` to add more text to an already started paragraph, heading, block
  quote, numbered point list item, bullet point list item or numbered point list
  item.

- `add_url` to add a URL (link) to an already started paragraph, heading, block
  quote, numbered point list item, bullet point list item or numbered point list
  item.

- `add_code_in_text` to add some short text (function name, variable name, etc.)
  as code to an already started paragraph, heading, block quote, bullet point
  list item or numbered point list item.

- `new_table` to start a new table with the provided first row.

- `add_table_row` to add another row to an already started table.

- `write_complete_table` to write a table all at once.

- `write_code_block` to write some preformatted text as a code block

There are no member functions to end or close any document item. Each document
item is automatically closed as another docuemnt item is started (or when
closing the file at the end of the context manager scope). new_bullet_item and
new_numbered_point_item take an optional level argument, that is used to change
to another nesting level.

## Example programs

A number of minimal but complete example programs are provided to help the
programmer new to mformat. See
[list of examples](https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/README.md)
.

## API documentation

API documentation automatically extracted from the Python code and docstrings
are available
[here for the public API](https://bitbucket.org/tom-bjorkholm/mformat/src/master/doc/api.md)
for programmers using the API and
[here for the protected API](https://bitbucket.org/tom-bjorkholm/mformat/src/master/doc/protected_api.md)
for programmers that want to extend the API by adding their own derived class
that provide some other output format.

Even though some may like reading API documentation, the
[example programs](https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/README.md)
probably provide a better introduction.

## Version history

| Version | Date        | Python version | Description                     |
|---------|-------------|----------------|---------------------------------|
| 0.6     | 14 Mar 2026 | 3.12 or newer  | Added PDF and LaTeX formats     |
| 0.5     | 07 Mar 2026 | 3.12 or newer  | Added RTF, TXT and reST formats |
| 0.4     | 21 Feb 2026 | 3.12 or newer  | Added block quote support       |
| 0.3     | 18 Feb 2026 | 3.12 or newer  | Improved API and fixes          |
| 0.2.2   | 31 Jan 2026 | 3.12 or newer  | Dependency corrected            |
| 0.2.1   | 30 Jan 2026 | 3.12 or newer  | Minor documentation fix         |
| 0.2     | 30 Jan 2026 | 3.12 or newer  | First released version          |

## Output file formats

The following table provides information about in which version support for a
format was introduced.

| Format | Full name of format      | Which package | Starting at version |
|--------|--------------------------|---------------|---------------------|
| docx   | Microsoft Word           | mformat-ext   | 0.2                 |
| html   | HTML Web page            | mformat       | 0.2                 |
| LaTeX  | LaTeX typesetting        | mformat       | 0.6                 |
| md     | Markdown                 | mformat       | 0.2                 |
| odt    | Open Document Text       | mformat-ext   | 0.2                 |
| pdf    | Portable Document Format | mformat-ext   | 0.6                 |
| reST   | reStructured Text        | mformat       | 0.5                 |
| rtf    | Rich Text Format         | mformat-ext   | 0.5                 |
| txt    | Plain text               | mformat       | 0.5                 |

## Test summary

- Test result: 2 failed, 139 passed in 5s
- Flake8 errors/warnings.
- No mypy errors found.
- Built version(s): 0.0.1
- Build and test using Python 3.14.3
