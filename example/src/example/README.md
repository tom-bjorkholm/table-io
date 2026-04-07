# table-io examples

This directory contains small example programs for programmers who are
new to the `tableio` API. The examples are arranged from the smallest
possible write example to more advanced topics such as value conversion,
box read and write, value search, multi-sheet workbooks and
capability-driven backend selection. The last example also shows a more
advanced extension point: user code can define its own `TableIO`
subclass and register it with the factory. A good way to learn the API
is to read the examples in order and run the ones that match the file
format you are interested in.

All examples use the shared command-line helper in
`cmd_for_examples.py`. That means they follow the same basic style:
you choose an output file with `-o` and a format with `-f`, and many
examples also let you choose an implementation with `-I` or pass
optional backend arguments. The examples that declare capabilities only
offer formats and implementations that can support the feature being
demonstrated, which makes them useful both as runnable demos and as API
documentation.

All examples also use the factory to get a TableIO object of the
correct type to write to different file formats. They demonstrate
the simplest way to use the factory by calling the `create_tableio()`
function.

Most examples now also use the recommended public API directly from the
package root, for example `from tableio import create_tableio,
FileAccess, OptionalArgs`. That keeps the beginner-facing examples easy
to scan. A few advanced topics still import lower-level helpers from
submodules on purpose, such as the value-conversion helpers in `e05`,
the capability-detail types in `e10`, and the backend implementation
helpers in `e20`.

## e00_really_simple_write_table.py

Source:
<https://bitbucket.org/tom-bjorkholm/table-io/src/master/example/src/example/e00_really_simple_write_table.py>

This is the best starting point if you only want to understand the
smallest working write example. It shows how to call
`create_tableio()`, how to use `FileAccess.CREATE`, how to write table
data from a list of rows with `write_table_listdata()`, and how to let
the context manager close the writer correctly when the work is done.

It also reflects the recommended import style for new users: the common
names in the example are imported directly from `tableio` instead of
from several different submodules.

It also shows that `tableio` can write more than plain strings. The
sample data includes numbers, booleans and a `datetime`, so a beginner
can see immediately that the API is designed for typed table values, not
just text output.

## e01_simple_read_write.py

Source:
<https://bitbucket.org/tom-bjorkholm/table-io/src/master/example/src/example/e01_simple_read_write.py>

This example extends `e00` into a complete round-trip: write a file,
reopen it, read the table back and verify that the result matches the
original data. It introduces `FileAccess.READ`, `write_heading()`,
`read_table_listdata()`, and the idea that headings are stored and read
separately from the table body.

For CSV it also demonstrates an important practical detail: backend
arguments can influence how values round-trip. The example sets
`csv_quoting='nonnumeric'` so the read-back behavior is easier to
understand when the file format itself does not preserve rich typing.

## e02_more_write.py

Source:
<https://bitbucket.org/tom-bjorkholm/table-io/src/master/example/src/example/e02_more_write.py>

This example is the main introduction to formatted output. It shows
several different ways to represent formatted data before writing it:
cell-by-cell formatting with `ValueFmt`, row-oriented formatting with
`FmtListRow`, dictionary-based tables, generated header rows with
`first_row_format`, and row formatting for dict-shaped data with
`FmtDictRow`.

It is useful when you already understand the basic write API and want to
see which input shape fits your own data best. It also introduces
`filtered_data_range=True`, which is especially interesting for
spreadsheet-style outputs where the written table range can be marked for
later use.

## e03_rrs_input_format.py

Source:
<https://bitbucket.org/tom-bjorkholm/table-io/src/master/example/src/example/e03_rrs_input_format.py>

This example shows how to prepare a table for a real external consumer.
The data matches the kind of Excel import expected by
`racingrulesofsailing.org`, so the example teaches more than just the
API syntax: it shows how to control column order carefully and how to
write data in a shape that another system expects.

It also uses a list of dictionaries instead of a list of lists. That is
often the most readable choice when the columns have stable names and
you want the code to say `"Email"` or `"Boat Name"` instead of relying on
column positions. The sample data also includes non-English characters,
which makes the example useful for programmers who need international
data.

## e04_rrs_input_format_list.py

Source:
<https://bitbucket.org/tom-bjorkholm/table-io/src/master/example/src/example/e04_rrs_input_format_list.py>

This example is intentionally equivalent to `e03`, but the input is
given as a list of rows instead of a list of dictionaries. The purpose
is comparison: a new programmer can look at `e03` and `e04` side by side
and decide whether named columns or positional rows feel more natural
for their own program.

It is especially useful if your source data already comes from a list of
lists or from code that naturally builds rows in the exact order you
want to write them. Reading both examples together is the fastest way to
understand the tradeoff between the two basic input shapes supported by
the API.

## e05_read_write_valueconversion.py

Source:
<https://bitbucket.org/tom-bjorkholm/table-io/src/master/example/src/example/e05_read_write_valueconversion.py>

This example teaches one of the most important ideas for robust file
interop: the value you read back may carry the same information as the
value you wrote, even if it comes back in a different Python type. The
file format may not preserve enough typing information, so the example
uses helpers such as `value2int()`, `value2float()`, `value2datetime()`,
`value2bool()`, `value2type()` and `value2type_of()` to convert values
back into the type the program expects.

Unlike the everyday `tableio` entry points, those conversion helpers are
still imported from `tableio.valueconversion`. That is intentional: they
are useful, but they are a specialized helper family rather than part of
the small beginner-facing root API.

It reads and writes both list-shaped and dict-shaped tables, and it
shows both the explicit “convert each known cell” approach and the more
general “convert to the type of the expected value” approach. If you are
writing a real application that reads files created by other tools, this
example is worth understanding early.

## e06_box_read_write_update.py

Source:
<https://bitbucket.org/tom-bjorkholm/table-io/src/master/example/src/example/e06_box_read_write_update.py>

This is the first example focused on rectangular box operations in a
spreadsheet-style backend. It writes a larger 10x10 table, closes the
file, reopens it in `FileAccess.UPDATE`, reads a 2x2 box from the larger
table and writes that box somewhere else on the same sheet.

The example teaches several practical spreadsheet concepts at once:
0-based box coordinates, exclusive `bottom` and `right` values, keeping
the `Position` returned by a write, and using `bottom=None` and
`right=None` as a convenient trick when you want the target box size to
come from the data you are writing.

## e07_box_rewrite_with_format.py

Source:
<https://bitbucket.org/tom-bjorkholm/table-io/src/master/example/src/example/e07_box_rewrite_with_format.py>

This example shows another useful box pattern: write a table, keep the
returned `Position`, calculate a box from that position, read the box
back, wrap the values in formatting, and write the same values back into
the same rectangle. In the example, a 2x2 box in the lower-left corner
is rewritten so it becomes bold with a red highlight.

The important beginner lesson here is that coordinates do not have to be
hardcoded. The API returns positions that can be reused in later
operations, which makes programs more robust when the written table size
changes.

## e08_filter_args_tableio.py

Source:
<https://bitbucket.org/tom-bjorkholm/table-io/src/master/example/src/example/e08_filter_args_tableio.py>

This example demonstrates how to build one mixed `OptionalArgsDict`
containing arguments for several formats and then filter it down to the
arguments that make sense for the concrete backend being created. That is
the role of `filter_args_tableio()`, and the example also shows that the
filtering depends on the actual implementation, not just the high-level
format name.

The program resolves the implementation that will be used, writes a
summary of which arguments were kept and removed, and then creates the
final writer with the filtered arguments. It is a good reference if you
want one configuration layer in your application but still need to
support several `tableio` backends cleanly.

## e09_multi_sheet.py

Source:
<https://bitbucket.org/tom-bjorkholm/table-io/src/master/example/src/example/e09_multi_sheet.py>

This example introduces multi-sheet spreadsheet workbooks. It starts on
the default first sheet, writes a table there, creates and selects a
second sheet called `Summary`, writes information about the workbook,
switches back to the first sheet to read data, and then switches again
to continue writing on the summary sheet.

The key API concepts here are `current_sheet_name()`, `select_sheet()`,
`list_sheets()` and the fact that sequential read and write positions are
tracked separately for each sheet. This is the example to read if you
want to understand workbook-style usage rather than single-table files.

## e10_capability_driven_selection.py

Source:
<https://bitbucket.org/tom-bjorkholm/table-io/src/master/example/src/example/e10_capability_driven_selection.py>

This example explains how capability requests influence backend
selection. It compares two capability sets: one where extra features
such as row formatting, highlight and filtered ranges are preferred but
ignorable, and another where the same features are strict requirements.

By listing the matching formats and implementations for both requests,
the example makes the difference between `CAP_NEEDED` and
`CAP_IGNORABLE` concrete. It then creates a writer using the preferred
capability set and writes a small demo table, so the reader can see how
the factory chooses a backend and how optional features may or may not be
honored in practice.

Most of the example now uses the root-level `tableio` API, but it still
imports `SingleCapability` and `Strictness` from
`tableio.capability`. That is a good signal that those two names are
more detailed capability-modeling tools than part of the smallest common
API surface.

## e11_find_value_read_cells_write_cells.py

Source:
<https://bitbucket.org/tom-bjorkholm/table-io/src/master/example/src/example/e11_find_value_read_cells_write_cells.py>

This example demonstrates a very practical spreadsheet workflow: write a
small table, search for a label cell with `find_value()`, use the found
position to build a new box for neighboring cells, read those cells with
`read_cells()`, and then write the same values back with formatting by
calling `write_cells()`.

The example is intentionally easy to inspect in the produced workbook. A
fictive company table is written with economic figures for 2024 and
2025, the row labelled `Revenue` is located, and the two year values on
that same row are rewritten so they become bold with a green highlight.
It is a good reference when you need to find one cell by content and
then update other cells relative to that match.

## e12_find_value_multiple_matches.py

Source:
<https://bitbucket.org/tom-bjorkholm/table-io/src/master/example/src/example/e12_find_value_multiple_matches.py>

This example teaches two more advanced `find_value()` patterns. First,
it searches for more than one cell at a time by looking for the 1x2
value area `[['ABBA', 1974]]`, which is more precise than searching for
just `ABBA` or just `1974`. Second, it shows how to find several
matches: after each match is handled, the example builds a new search
box that starts below the previous match and calls `find_value()` again.

The table contains several 1970s singles where only some rows match the
requested combination of artist and year. For every matching `ABBA`
`1974` row, the example writes text into the `Remark` column on that
same row. Because the visible change is ordinary cell content rather
than formatting, this example is also useful for spreadsheet
implementations that support search and exact cell writes but not rich
formatting.

## e13_table_borders.py

Source:
<https://bitbucket.org/tom-bjorkholm/table-io/src/master/example/src/example/e13_table_borders.py>

This example is the main beginner reference for *where* table borders
are configured in the API. It shows the four table-writing calls that
accept `border_style=...`: `write_table_listdata()`,
`write_table_dictdata()`, `write_table_fmtlistdata()` and
`write_table_fmtdictdata()`.

That makes it a good example to study when you already know how to
write a table, but you are not yet sure where the border style belongs
in the call or how `TableBorderStyle` values are written in code. The
four tables also show that borders work together with the other write
features introduced earlier, such as `ValueFmt`, `FmtListRow`,
`FmtDictRow` and `first_row_format`.

## e14_all_table_borders.py

Source:
<https://bitbucket.org/tom-bjorkholm/table-io/src/master/example/src/example/e14_all_table_borders.py>

This example is the visual companion to `e13`. Instead of focusing on
which API call to use, it writes one sample table for every
`TableBorderStyle` value so a new programmer can open the produced file
and compare the styles side by side.

It is the best example to run when you already know that your program
needs table borders, but you want to choose the style that is closest to
the look you have in mind. It also demonstrates one practical `Box`
pattern: place each demo table under its own heading and shift it one
column to the right so the left outer border is easier to see in
spreadsheet viewers such as Excel.

## e20_register_custom_tableio.py

Source:
<https://bitbucket.org/tom-bjorkholm/table-io/src/master/example/src/example/e20_register_custom_tableio.py>

This example introduces an advanced but very useful extension point:
user code can define its own class derived from `TableIO`, register it
with `register_tableio()`, and then use the ordinary factory API to
create it. The example keeps the custom class in the same script so the
reader can see the full flow in one place: the backend class, the
registration call, the ordinary `create_tableio()` calls, and the
round-trip read-back check.

This is especially useful when a programmer wants to offer both their
own application-specific format and some of the predefined `tableio`
formats to the end user. Once the custom class has been registered, the
same factory can create both the custom format and the built-in formats,
and the caller gets the same `TableIO` API in either case.

The custom format is a simple `LineNumberedCSV` file where every
physical line starts with a five-digit line number and a colon before the
usual CSV content. That is intentionally a format that the built-in
package backends do not already provide, but it is still small enough to
implement using only the Python standard-library `csv` module. The
example class derives from `TableIOTextBased`, which itself derives from
`TableIO`, so the example can focus on the custom hooks instead of basic
text-file open and close handling.

This example is also the deliberate exception to the simplified import
style used by the earlier scripts. It still imports several names from
submodules because implementing a backend needs lower-level extension
hooks that are not part of the beginner-facing root API.

Another important lesson in this example is *when* registration happens.
The call to `register_tableio()` is not done at module import time.
Instead, it happens in the `if __name__ == '__main__':` block, just
before the shared command-line parser is started. That shows a programmer
who dislikes module-load side effects that normal runtime registration is
fully sufficient, as long as it happens before code asks the factory
which formats are available.
