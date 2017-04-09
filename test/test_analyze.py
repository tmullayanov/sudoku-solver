import unittest
import os

# setUp
from .context import ssolver
types = ssolver.datatypes
an = ssolver.analyzer

class Consistency(unittest.TestCase):

    def testBasicElimination(self):
        dummies = [types.Cell('*', 0, 0), types.Cell('*', 0, 1)]
        spare = 4

        self.assertTrue(all(spare in d.options for d in dummies))
        an.eliminate(spare, dummies)
        self.assertFalse(any(spare in d.options for d in dummies))

    def testSimpleField(self):
        f = ssolver.loader.load_field('input/simple.sudoku')

        living = an.yield_all_set(f)
        an.force_consistency(f)
        self.assertFalse(any(l.value in c.options for l in living for c in
                             f.list_all_peers(l)))


class SoluteTrivia(unittest.TestCase):

    def setUp(self):
        self.field = ssolver.loader.load_field('input/.simple.trivia')
        an.force_consistency(self.field)

    def testEnsured(self):
        ensured = an.search_ensured(self.field)
        self.assertEqual(1, len(ensured))
        ensured = ensured[0]
        self.assertEqual(0, ensured.row)
        self.assertEqual(0, ensured.col)

    def testTriviaSuggestion(self):
        r = an.suggest_move(self.field)
        self.assertIsNotNone(r, msg="Incorrect suggestion!")
        cell, val = r
        self.assertEqual((0, 0), (cell.row, cell.col))
        self.assertEqual(6, val)

    def testTriviaSolve(self):
        golden = ssolver.loader.load_field('input/simple.solution')
        solved = an.solve(self.field)

        self.assertEqual(golden, solved)
