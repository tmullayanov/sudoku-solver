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
import sys
import itertools

__all__ = ['Field', 'Cell', 'UnknownSymbolError', 'IncorrectInputError']

def grouper(iterable, by=3, fillvalue=None):
    ''' grouper('ABCDEFG', by=3, fillvalue='x') -> ABC DEF Gxx '''
    args = [iter(iterable)] * by
    return itertools.zip_longest(*args, fillvalue=fillvalue)

#TODO: rename SilentSet -> Options
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

    def get_sole_option(self):
        '''
        Returns the only option. If there's 0 or more than 1 option, returns None
        '''
        if len(self) == 1:
            return list(self)[0]

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

    def pprint(self, out=sys.stdout):
        '''
        Pretty-print all the cells to OUT
        '''
        lines = (self.horizontal_line(line=i) for i in range(self.ROWS_MAX))
        c = self.COLS_MAX
        border = '%s\n' % ('=' * (c + c//3 - 1))
        out.write(border)
        for (n, line) in enumerate(lines):
            if not (n % 3) and n:  # avoid n == 0
                out.write('+'.join(['---']*3))
                out.write('\n')

            groups = list(grouper(line, by=3))
            out.write('|'.join(('%s' * len(g)) % g for g in groups))
            out.write('\n')
        out.write(border)

    def _get_subset(self, rule):
        '''
        Tricky. This method returns list of cells matching
        2-argument predicate RULE.
        Arguments of RULE: row and column where cells is located at.

        This method is supplementary for specific methods which select
        horizontal/vertical line and subsquares.
        '''
        f = lambda cell: rule(cell.row, cell.col)
        return list(filter(f, self.cells))

    def horizontal_line(self, cell=None, line=0):
        if cell:
            line = cell.row
        assert 0 <= line < self.ROWS_MAX, "line out of bound"
        rule = lambda x, _: x == line
        return self._get_subset(rule)

    def vertical_line(self, cell=None, column=0):
        if cell:
            column = cell.col
        assert 0 <= column < self.COLS_MAX, "column out of bound"
        rule = lambda _, y: y == column
        return self._get_subset(rule)

    def subsquare_for(self, cell=None, row=0, col=0):
        '''
        Returns list of cells located in the same subsquare that is specified
        either by CELL or by ROW and COL explicilty.
        CELL specification has higher priority
        '''
        if cell:
            row, col = cell.row, cell.col
        # calculating subsquare borders:
        # row_left, row_right, column_bottom, column_top

        row_l, col_t = row // 3 * 3, col // 3 * 3
        row_r, col_b = row_l + 3, col_t + 3
        # use those borders to construct rule
        rule = lambda x, y: row_l <= x < row_r and col_t <= y < col_b
        return self._get_subset(rule)

    def subsquare_by_num(self, num):
        '''
        The following enumeration is implied:
        0|1|2
        -+-+-
        3|4|5
        -+-+-
        6|7|8
        '''
        row_l, col_t = 3 * (num // 3), 3 * (num % 3)
        row_r, col_b = row_l + 3, col_t + 3
        rule = lambda x, y: row_l <= x < row_r and col_t <= y < col_b
        return self._get_subset(rule)

    def get_all_subsets(self):
        '''
        Returns generator that yields all subsets in the following order:
          - horizontal lines
          - vertical lines
          - subsquares
        '''
        for i in range(0, self.ROWS_MAX):
            yield self.horizontal_line(line=i)
        for i in range(0, self.COLS_MAX):
            yield self.vertical_line(column=i)
        for i in range(0, self.COLS_MAX):
            yield self.subsquare_by_num(num=i)

    def list_all_peers(self, cell):
        _all = self.horizontal_line(cell=cell) + \
                self.vertical_line(cell=cell) + \
                self.subsquare_for(cell=cell)
        return [x for x in _all if x is not cell]

    def __eq__(self, other):
        return self.rows == other.rows and self.cells == other.cells


class Cell(object):
    '''
    This type is responsible for modeling cell from sudoku game field.
    Cell contains info about current state and possible options
    '''

    DEFAULT_OPTIONS = SilentSet(range(1, 10))
    EVEN = SilentSet(range(2, 10, 2))
    ODD = SilentSet(range(1, 10, 2))

    def __init__(self, val, row, col):

        if val.isnumeric() and 0 < int(val) < 10:
            self.value = int(val)
            self.options = SilentSet()
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
        return str(self.value) if self.value else '.'

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
