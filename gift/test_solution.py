#!/usr/bin/python3
import unittest
from solution import find_gifts, output

class TestGift(unittest.TestCase):

    def test_basic(self):
        prices = [
            ('Candy Bar', 500), ('Paperback Book', 700), ('Detergent', 1000), ('Headphones', 1400), 
            ('Earmuffs', 2000), ('Bluetooth Stereo', 6000)
        ]
        balance = 2300
        expected = "Paperback Book 700, Headphones 1400"
        actual = output(find_gifts(prices, balance))
        self.assertEqual(actual, expected)

        balance = 10000
        expected = "Earmuffs 2000, Bluetooth Stereo 6000"
        actual = output(find_gifts(prices, balance))
        self.assertEqual(actual, expected)

        balance = 1100
        expected = "Not possible"
        actual = output(find_gifts(prices, balance))
        self.assertEqual(actual, expected)

    def test_multiple(self):
        prices = [('a', 1), ('b', 2), ('c', 9), ('d', 10)]
        balance = 11
        expected = "a 1, d 10"
        actual = output(find_gifts(prices, balance))
        self.assertEqual(actual, expected)

        balance = 12
        expected = "b 2, d 10"
        actual = output(find_gifts(prices, balance))
        self.assertEqual(actual, expected)

    def test_exhaustive(self):
        prices = [('simple', 1), ('abc', 500), ('def', 1000), ('candy', 99999)]
        balance = 99999
        expected = "abc 500, def 1000"
        actual = output(find_gifts(prices, balance))
        self.assertEqual(actual, expected)

        balance = 100000
        expected = "simple 1, candy 99999"
        actual = output(find_gifts(prices, balance))
        self.assertEqual(actual, expected)

    def test_fail(self):
        prices = []
        balance = 0
        expected = "Not possible"
        actual = output(find_gifts(prices, balance))
        self.assertEqual(actual, expected)

        prices = [('a', 1)]
        balance = 1
        expected = "Not possible"
        actual = output(find_gifts(prices, balance))
        self.assertEqual(actual, expected)

        prices = [('a', 100), ('b', 123)]
        balance = 95
        expected = "Not possible"
        actual = output(find_gifts(prices, balance))
        self.assertEqual(actual, expected)
    
    def test_duplicates_equal(self):
        prices = [('a', 1), ('b', 1), ('c', 1), ('d', 1)]
        balance = 2
        expected = "a 1, d 1"
        actual = output(find_gifts(prices, balance))
        self.assertEqual(actual, expected)

    def test_duplicates_unequal(self):
        prices = [('a', 1), ('b', 1), ('c', 1), ('d', 1)]
        balance = 3
        expected = "a 1, d 1"
        actual = output(find_gifts(prices, balance))
        self.assertEqual(actual, expected)

    def test_duplicates_failure(self):
        prices = [('a', 1), ('b', 1), ('c', 1), ('d', 1)]
        balance = 1
        expected = "Not possible"
        actual = output(find_gifts(prices, balance))
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()