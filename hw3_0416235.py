""" Find other works at https://github.com/AilurusUmbra/GA2 """
import unittest
from SimplePoint1 import Point


class testPoint(unittest.TestCase):
    xMax =  100
    xMin = -100
    yMax =  200
    yMin = -200

    def test_limit(self):
        p1 = Point(10, 20)
        self.assertLessEqual(p1.x, self.xMax)
        self.assertGreaterEqual(p1.x, self.xMin)
        self.assertLessEqual(p1.y, self.yMax)
        self.assertGreaterEqual(p1.y, self.yMin)


if __name__ == '__main__':
    unittest.main()
