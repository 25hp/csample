import unittest

import csample


class TestCase(unittest.TestCase):
    def test_0(self):
        self.assertEqual(4060533391, csample.sample('Hello'))


if __name__ == '__main__':
    unittest.main()
