'''
analyzer.py - module which actually solves sudoku puzzle.

exported functions:
    - solve
    - suggest_move
    - make_move
'''
from .datatypes import Field, Cell  #FIXME: check for import redundancy

__all__ = ['solve', 'suggest_move', 'make_move']

def eliminate(v, cells):
    '''
    Removes value V from all cells specified.
    Supplementary method, not exported.
    '''
    for c in cells:
        c.options.remove(v)


def yield_all_set(field):
    return filter(lambda x: x.value, field.cells)

def force_consistency(field):
    '''
    This subroutine removes all set values from all peers' options
    which makes the field internals consistent.
    '''
    for alive in yield_all_set(field):
        eliminate(alive.value, field.list_all_peers(alive))
