import unittest
import os

# setUp
from .context import ssolver
parser = ssolver.parser

class BadInput(unittest.TestCase):
    
    def testShortLine(self):
        with self.assertRaises(ssolver.IncorrectInputError) as cm:
            parser.parse('input/incorrect1.sudoku')
