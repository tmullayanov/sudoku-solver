'''
datatypes.py - module defining field representation

exported class:
    Field
    Cell
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

    def __init__(self):
        self.cells = []

    @classmethod
    def make_empty(cls):
        return cls()

    def add_row(self, row):
        self.cells.extend(Cell(c) for c in row)


class Cell(object):
    '''
    This type is responsible for modeling cell from sudoku game field.
    Cell contains info about current state and possible options
    '''

    DEFAULT_OPTIONS = SilentSet(range(1, 10))
    EVEN = SilentSet(range(2, 10, 2))
    ODD = SilentSet(range(1, 10, 2))

    def __init__(self, val):

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

        
###################
# EXCEPTIONS
###################

class UnknownSymbolError(ValueError): pass 
class IncorrectInputError(ValueError): pass
