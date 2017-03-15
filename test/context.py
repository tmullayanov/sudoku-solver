'''
context.py - module serving testing needs.

This module resolves package properly with simple and EXPLICIT path modification.

Using of this module in every test suite allows the developer avoid installing package into the system or interact with "setup.py develop".

The method is taken from Hitchhiker's Guide to Python:
    https://docs.python-guide.org/en/latest/writing/structure
'''
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import ssolver
