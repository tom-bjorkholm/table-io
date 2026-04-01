#! /usr/bin/env python3
"""Show multi-cell searches and repeated find_value() searches."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
from tableio.factory import create_tableio
from tableio.optional_args import OptionalArgs
from tableio.tableio import FileAccess, Box
from tableio.value_type import Value, ListData
from tableio.capability import Capabilities, CAP_NEEDED, CAP_NOT_USED
from .cmd_for_examples import cmd_parse_and_run_example


# pylint: disable=duplicate-code
CAPS = Capabilities(
    can_write=CAP_NEEDED,
    can_read=CAP_NEEDED,
    can_fmt_row=CAP_NOT_USED,
    can_fmt_value=CAP_NOT_USED,
    filtered_data_range=CAP_NOT_USED,
    can_write_box=CAP_NEEDED,
    can_read_box=CAP_NEEDED,
    can_write_highlight=CAP_NOT_USED,
    multi_sheet=CAP_NOT_USED,
    can_find_value_position=CAP_NEEDED
)
# pylint: enable=duplicate-code


def build_singles_table() -> ListData[Value]:
    """Build a larger table of 1970s singles."""
    return [
        ['Group/artist', 'Year', 'Remark', 'Single'],
        ['David Bowie', 1974, '', 'Rebel Rebel'],
        ['ABBA', 1974, '', 'Waterloo'],
        ['Queen', 1974, '', 'Killer Queen'],
        ['ABBA', 1975, '', 'Mamma Mia'],
        ['The Rubettes', 1974, '', 'Sugar Baby Love'],
        ['ABBA', 1974, '', 'Honey, Honey'],
        ['Mud', 1974, '', 'Tiger Feet'],
        ['ABBA', 1976, '', 'Fernando'],
        ['Sweet', 1974, '', 'Fox on the Run'],
        ['ABBA', 1974, '', 'So Long'],
        ['Bee Gees', 1977, '', 'Stayin Alive'],
        ['ABBA', 1977, '', 'Knowing Me, Knowing You']]


def remark_box_for_match(match_box: Box) -> Box:
    """Return the remark-cell box on the same row as one match."""
    assert match_box.bottom is not None
    return Box(top=match_box.top, left=2, bottom=match_box.bottom, right=3)


def next_search_box(match_box: Box) -> Box:
    """Return a box that searches only later rows in artist/year columns."""
    assert match_box.bottom is not None
    return Box(top=match_box.bottom, left=0, bottom=None, right=None)


# pylint: disable=duplicate-code
def e12_find_value_multiple_matches(
        format_name: str,
        output_file_name: str,
        implementation_name: Optional[str],
        optional_args: OptionalArgs) -> int:
    """Find each ABBA 1974 row and mark it in the remark column."""
    #
    # This example uses a larger table than e11 on purpose.
    #
    # We want several rows that look similar but are not matches:
    # - ABBA in years other than 1974
    # - other artists in 1974
    # - several real ABBA 1974 matches
    #
    # That makes it easier to see why searching for one cell is sometimes
    # too broad, and why a rectangular search with more than one value can
    # be much more precise.
    #
    singles_table = build_singles_table()
    with create_tableio(format_name=format_name,
                        file_name=output_file_name,
                        file_access=FileAccess.CREATE,
                        implementation=implementation_name,
                        capabilities=CAPS,
                        args=optional_args) as tableio:
        #
        # First write the full table with an empty Remark column.
        #
        # The later writes will only update the Remark cells for rows that
        # match our search condition.
        #
        tableio.write_table_listdata(singles_table)
        #
        # find_value() can search for a whole rectangular area of cells.
        #
        # Here the search area is one row high and two columns wide:
        # - left column must contain 'ABBA'
        # - right column must contain 1974
        #
        # That is more specific than searching for just 'ABBA' or just
        # 1974, because both of those values also appear in rows we do not
        # want to edit.
        #
        search_value: ListData[Value] = [['ABBA', 1974]]
        #
        # We skip the header row by starting at top=1.
        #
        search_box: Optional[Box] = Box(top=1, left=0, bottom=None, right=None)
        match_number = 0
        while True:
            #
            # find_value() returns the first match inside the current
            # search box, scanning top-to-bottom and left-to-right.
            #
            match_box = tableio.find_value(search_value, box=search_box)
            if match_box is None:
                break
            assert match_box.bottom is not None
            #
            # The returned box fits tightly around the found search area.
            #
            # Because our search area is one row by two columns, the match
            # box covers exactly the artist cell and the year cell on the
            # matching row.
            #
            match_number += 1
            #
            # The visible change in this example is plain text in the
            # Remark column instead of formatting.
            #
            # That keeps the example useful even for spreadsheet
            # implementations that support searching and exact cell writes
            # but do not support bold text or highlights.
            #
            remark_text = f'found and edited {match_number}'
            tableio.write_cells([[remark_text]],
                                box=remark_box_for_match(match_box))
            #
            # To search for the next match, we build a new search box that
            # starts on the row immediately below the current match.
            #
            # That way the next call cannot find the same row again, but it
            # can still find every later ABBA 1974 row in the sheet.
            #
            search_box = next_search_box(match_box)
        #
        # This assert is a small self-check for the example program.
        #
        # It confirms that the loop found all three ABBA singles from 1974
        # that we intentionally placed in the sample data.
        #
        assert match_number == 3
    return 0
# pylint: enable=duplicate-code


if __name__ == '__main__':
    cmd_parse_and_run_example(
        example_name='e12_find_value_multiple_matches',
        func=e12_find_value_multiple_matches, caps=CAPS)
