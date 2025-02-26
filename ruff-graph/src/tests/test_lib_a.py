import unittest
from src import lib_a

class TestLibA(unittest.TestCase):
    def test_one(self):
        lib_a.foo()

if __name__ == '__main__':
    unittest.main()