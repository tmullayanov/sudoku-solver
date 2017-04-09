'''
analyzer.py - module which actually solves sudoku puzzle.

exported functions:
    - solve
    - suggest_move
    - make_move
'''
import copy
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


def search_ensured(field):
    '''
    This subroutine tries to find cells which have only one value as
    an option.
    Returns list of such cells if they exist.
    Empty list otherwise.

    Field MUST be consistent.
    '''
    ensured_predicate = lambda cell: not cell.value and len(cell.options) == 1
    return list(filter(ensured_predicate, field.cells))


def suggest_move(field, modify_state=False):
    '''
    Returns PAIR(tuple) of CELL that may be set surely and VALUE to be set.
    Returns None if no such cell exists.

    If MODIFY_STATE is set, the internals of the argument would be modified.
    '''
    field = field if modify_state else copy.deepcopy(field)
    force_consistency(field)
    try:
        cell = search_ensured(field)[0]
        value = cell.options.get_sole_option()
        assert value, "Ensured cell doesn't have only one option!"
        return cell, value
    except IndexError as e:  # FIXME: call to heuristic should happen here.
        return

def make_move(field):
    '''
    Calls suggest_move() and returns new instance of
    datatypes.Field with at max one new cell set.
    '''
    n_field = copy.deepcopy(field)
    r = suggest_move(n_field, modify_state=True)
    if r:
        cell, val = r
        cell.set(val)
        eliminate(val, n_field.list_all_peers(cell))
    return n_field


def solve(field):
    '''
    Tries to solve the board. Returns new instance of field with all cells set.
    If failure, raises Exception with new instance of field with current state.
    '''
    n_field = copy.deepcopy(field)
    empty_cells = lambda: len(list(filter(lambda cell: not cell.value,
                                          n_field.cells)))
    force_consistency(n_field)
    blank_iters, blank_limit = 0, 3

    while empty_cells() > 0:
        soles = search_ensured(n_field)
        if not soles:
            blank_iters += 1
            if blank_iters >= blank_limit:
                raise ValueError("Cannot solve!", n_field)
            continue

        blank_iters = 0
        for s in soles:
            val = s.options.get_sole_option()
            s.set(val)
            eliminate(val, n_field.list_all_peers(s))
    return n_field
