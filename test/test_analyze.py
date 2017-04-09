import unittest
import os
import itertools

# setUp
from .context import ssolver
types = ssolver.datatypes
an = ssolver.analyzer

class Consistency(unittest.TestCase):

    def test_basic_elimination(self):
        dummies = [types.Cell('*', 0, 0), types.Cell('*', 0, 1)]
        spare = 4

        self.assertTrue(all(spare in d.options for d in dummies))
        an.eliminate(spare, dummies)
        self.assertFalse(any(spare in d.options for d in dummies))

    def test_simple_field(self):
        f = ssolver.loader.load_field('input/simple.sudoku')

        living = an.yield_all_set(f)
        an.force_consistency(f)
        self.assertFalse(any(l.value in c.options for l in living for c in
                             f.list_all_peers(l)))
