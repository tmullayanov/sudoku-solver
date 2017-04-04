import unittest
import os

# setUp
from .context import ssolver
Cell = ssolver.datatypes.Cell

class CellCase(unittest.TestCase):

    def setUp(self):
        self.cell = Cell('0', row=0, col=0)

    def testOptions(self):
        values = range(1, 10)
        for v in values:
            self.assertTrue(v in self.cell.options)

    def testRemove(self):
        values = range(2, 10)
        self.cell.remove(1)
        
        self.assertTrue(1 not in self.cell.options)
        self.assertTrue(any(x in self.cell.options for x in values))

    
    def testSetClean(self):
        values = range(1, 10)
        solution = 1

        self.cell.set(solution)
        
        self.assertTrue(any(x not in self.cell.options for x in values))
        self.assertEqual(self.cell.value, solution)

    def testSetRemoved(self):
        toRemove = 1
        self.cell.remove(toRemove)
        self.assertTrue(toRemove not in self.cell.options)

        with self.assertRaises(AssertionError) as err:
            self.cell.set(toRemove)

    def testEq(self):
        other = Cell('0', row=5, col=5)
        self.assertEqual(self.cell, other)
