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

    

if __name__ == '__main__':
    unittest.main()