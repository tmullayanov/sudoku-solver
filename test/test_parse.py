import unittest
import os

# setUp
from .context import ssolver
loader = ssolver.loader

class BadInput(unittest.TestCase):
    
    def testShortLine(self):
        with self.assertRaises(ssolver.IncorrectInputError) as cm:
            loader.load_field('input/incorrect1.sudoku')
