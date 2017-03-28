import unittest
import os

# setUp
from .context import ssolver
loader = ssolver.loader

class BadInput(unittest.TestCase):
    
    def testShortLine(self):
        with self.assertRaises(ssolver.IncorrectInputError) as cm:
            loader.load_field('input/incorrect1.sudoku')


class OKInput(unittest.TestCase):

    def testLoadSimple(self):
        f = loader.load_field('input/simple.sudoku')
        self.assertEqual(f.rows, ssolver.datatypes.Field.ROWS_MAX)
        self.assertEqual(f.value_at(0, 1), 3)

    def testLoadSpaces(self):
        f = loader.load_field('input/spaces.sudoku')
        self.assertEqual(f.rows, ssolver.datatypes.Field.ROWS_MAX)
        self.assertEqual(f.value_at(0, 0), 8)
