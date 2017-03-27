'''
datatypes.py - module defining field representation

exported classes:
    Field
    Cell

exported exceptions:
    UnknownSymbolError
    IncorrectInputError
'''
import copy as cp


class SilentSet(set):
    '''
    The purpose of this type is to provide a way of silent removal of elements.
    This is accomplished with overriding set.remove method
    '''

    def remove(self, value):
        '''
        remove an element if it exists. Stays quiet otherwise
        '''
        if value in self:
            super().remove(value)


class Field(object):
    '''
    This is the type for modeling sudoku game field.
    The field is represented as 1D array of cells
    '''
    ROWS_MAX = 9
    COLS_MAX = 9

    def __init__(self, cells):
        self.cells = cells
        self.rows = 0

    @classmethod
    def make_empty(cls):
        return cls(cells=[])

    def _check(self, row):
        if len(row) != self.COLS_MAX:
            raise IncorrectInputError(
                'Expected %s columns; found %s' % (self.COLS_MAX, len(row)))

    @classmethod
    def copy(cls, field):
        assert cls is type(field), "Type mismatch: %s expected; %s found" % (
            cls, type(field))
        return cp.deepcopy(field)

    def add_row(self, row):
        '''Fills next row, checks if enough symbols are provided'''
        self._check(row)

        self.cells.extend(Cell(c, self.rows, j) for (j, c) in enumerate(row))
        self.rows += 1

    def ready(self):
        '''True if ROWS_MAX rows were loaded'''
        return self.rows == self.ROWS_MAX

    def cell_at(self, row, col):
        '''Returns cell at specified position'''
        assert 0 <= row < self.ROWS_MAX, "row out of bound"
        assert 0 <= col < self.COLS_MAX, "col out of bound"
        return self.cells[row * self.ROWS_MAX + col]

    def value_at(self, row, col):
        cell = self.cell_at(row, col)
        return cell.value


class Cell(object):
    '''
    This type is responsible for modeling cell from sudoku game field.
    Cell contains info about current state and possible options
    '''

    DEFAULT_OPTIONS = SilentSet(range(1, 10))
    EVEN = SilentSet(range(2, 10, 2))
    ODD = SilentSet(range(1, 10, 2))

    def __init__(self, val, row, col):

        if val.isnumeric():
            self.value = int(val)
            self.options = cp.copy(self.DEFAULT_OPTIONS)
            self.options.remove(self.value)
        elif val == 'e':  # 'e' for even
            self.value = 0
            self.options = cp.copy(self.EVEN)
        elif val == 'o':  # 'o' for odd
            self.value = 0
            self.options = cp.copy(self.ODD)
        elif val == '*':
            self.value = 0
            self.options = cp.copy(self.DEFAULT_OPTIONS)
        else:
            raise UnknownSymbolError('Unexpected symbol: %s' % val)
        
        self.row = row
        self.col = col

    def __repr__(self):
        return 'Cell(%s, row=%s, col=%s)' % (self.value, self.row, self.col)

    def __str__(self):
        return repr(self)

    def __innerEq__(self, cell):
        '''
        Supplementary method used in __eq__.
        Compares value and options.
        '''
        return self.value == cell.value and self.options == cell.options

    def __eq__(self, cell):
        type_eq = type(self) is type(cell)
        return type_eq and self.__innerEq__(cell)

    def set(self, val):
        assert val in self.options, "Value is not an option!"
        self.value = val
        self.options = SilentSet()

    def remove(self, *values):
        '''Removes one or more elements from possible options'''
        for val in values:
            self.options.remove(val)


###################
# EXCEPTIONS/ERRORS
###################

class UnknownSymbolError(ValueError):
    pass


class IncorrectInputError(ValueError):
    pass
