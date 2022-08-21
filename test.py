import unittest
import main

class TestFailure(unittest.TestCase):
    def testFail(self):
        assert(main.add(2,3) == 5)

if __name__ == '__main__':
    unittest.main()