import unittest
from src import lib_b

class TestLibB(unittest.TestCase):
    def test_lib_b(self):
        lib_b.foo()

if __name__ == '__main__':
    unittest.main()