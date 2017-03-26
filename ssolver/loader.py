'''
loader.py - module implementing loading sudoku from input stream.
Format of the sudoku is described in README.md

Exported functions:
    load_field(fname)
    parse_field(lines)

Note that "load_field" is used as wrapper for parse_field.
'''
from ssolver.datatypes import Field, IncorrectInputError, UnknownSymbolError

def _enough(iterable, n=9):
    return len(iterable) == n


def parse_field(lines):
    field = Field.make_empty()
    for line in lines:
        clean_line = wipe_separators(line)
        
        if clean_line:
            field.add_row(clean_line)
        else:
            continue

        if field.ready():
            break

    if field.ready():
        return field
    else:
        raise ValueError('Field is not ready!')


def wipe_separators(line):
    replacement_table = str.maketrans('', '', '# \n\r\t')
    return line.translate(replacement_table)


def load_field(fname):
    with open(fname, 'r') as inp:
        lines = list(filter(None, inp.readlines()))
        return parse_field(lines)
