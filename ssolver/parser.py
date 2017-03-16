'''
parser.py - module implementing parsing sudoku from input stream.

Exported functions:
    parse
    parse_field
'''
from ssolver.datatypes import Field, IncorrectInputError, UnknownSymbolError

def _enough(iterable, n=9):
    return len(iterable) == n

def parse_field(lines):
    field = Field.make_empty() 
    for line in lines:
        clean_line = wipe_separators(line)
        field.add_row(clean_line)
        
        if field.ready():
            break
    
    if field.ready():
        return field
    else:
        raise ValueError('Field is not ready!')


def wipe_separators(line):
    replacement_table = str.maketrans('','', '# \n\r\t')
    return line.translate(replacement_table)

def parse(fname):
    with open(fname, 'r') as inp:
        lines = list(filter(None, inp.readlines()))
        return parse_field(lines) 


