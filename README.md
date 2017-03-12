# Sudoku-solver

This module provides functionality needed for solving simple sudoku 9x9 with 3x3 subsquares.

Currently there is no support for sudoku with any other field size (since there is no way to represent custom subfields)

# Input format

This section describes sudoku input format as follows:

First lines should describe the initial state of the field. There is no limitation to using spaces or blank lines.

The meaning of the symbols:

    * 1-9 - is used for numbers that are given
    * \* literally - is used for empty cell which may contain any number from [1,9].
    * "e" - is used for empty cell to specify that only **e**ven numbers may be contained in this cell
    * "o" - same as above, except for **o**dd numbers
    * \Space, \Newline, \# - any of those are treated as separators and parser doesn't care about them.

## Incorrect input

Parser would raise Exception when it processes the line with too few/many cells specified. The exception also should be raised when there is not enough lines covered.
Though, if there is too many lines, parser may ignore them instead of raising Exception
