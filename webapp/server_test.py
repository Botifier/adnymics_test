#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from server import Server


class ServerTest(unittest.TestCase):

    def setUp(self):
        self._app = Server()._test_client()

    def test_index(self):
        rv = self._app.get('/')
        self.assertTrue(rv.status.startswith('200 '))
        self.assertEqual(rv.headers['content-type'],
                         'text/plain; charset=utf-8')
        self.assertTrue(rv.data.startswith(b'Currently'))

    def test_fib_not_a_number(self):
        rv = self._app.get('/fib/x/2')
        self.assertTrue(rv.status.startswith('400 '))

    def test_fib_float_numbers(self):
        rv = self._app.get('/fib/1.0/2')
        self.assertTrue(rv.status.startswith('400 '))

    def test_fib_negative_numers(self):
        rv = self._app.get('/fib/-1/2')
        self.assertTrue(rv.status.startswith('400 '))

    def test_fib_overflowed_numbers(self):
        rv = self._app.get('/fib/2/99999999999999')
        self.assertTrue(rv.status.startswith('413 '))

    def test_fib_wrong_order_numbers(self):
        rv = self._app.get('/fib/4/2')
        self.assertTrue(rv.status.startswith('400 '))

    def test_fib_zero(self):
        rv = self._app.get('/fib/0/0')
        self.assertTrue(rv.status.startswith('200 '))
        self.assertEqual(rv.data, b'[0]')

    def test_fib_normal(self):
        rv = self._app.get('/fib/3/5')
        self.assertTrue(rv.status.startswith('200 '))
        self.assertEqual(rv.headers['content-type'], 'application/json')
        self.assertEqual(rv.data, b'[2, 3, 5]')


if __name__ == '__main__':
    unittest.main()