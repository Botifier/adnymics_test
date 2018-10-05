#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from fibonacci import Fibonacci


class FibonacciTest(unittest.TestCase):

    def setUp(self):
        self._fib = Fibonacci()
    
    def test_limit(self):
        self.assertEqual(self._fib.sequence(0, 0), [0])
        self.assertEqual(self._fib.sequence(1, 1), [1])

    def test_normal(self):
        self.assertEqual(self._fib.sequence(3, 5), [2, 3, 5])

    def test_large(self):
        x = self._fib.sequence(0, 100)
        self.assertEqual(len(x), 101)
        self.assertEqual(x[97], 83621143489848422977)
        self.assertEqual(x[98], 135301852344706746049)
        self.assertEqual(x[99], 218922995834555169026)

    def test_xlarge(self):
        """Result is too long so just verify the first and last 32 digits of
        the last number
        """
        x = self._fib.sequence(0, 100000)
        self.assertEqual(len(x), 100001)
        s = str(x[99999])
        self.assertEqual(len(s), 20899)
        self.assertEqual(s[:32], '16052857682729819697035016991663')
        self.assertEqual(s[-32:], '35545120747688390605016278790626')

    def test_reset_cache(self):
        self._fib.sequence(0, 5)
        self._fib.reset_cache()
        self.assertEqual(self._fib.get_cache(), [0, 1])

if __name__ == '__main__':
    unittest.main()