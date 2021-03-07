import unittest
from decimal import Decimal

from line import Line


class TestLine(unittest.TestCase):
    def test_basic(self):

        A = Line(['4.046', '2.836'], '1.21')
        B = Line(['10.115', '7.09'], '3.025')
        assert A == B

        C, D = Line(['7.204','3.182'], '8.68'), Line(['8.172', '4.114'], '9.883')
        x,y = C.intersection_with(D)
        assert (round(x,3), round(y,3)) == (Decimal('1.173'), Decimal('0.073'))

        E, F = Line(['1.182','5.562'], '6.744'), Line(['1.773', '8.343'], '9.525')
        assert E.intersection_with(F) is None

if __name__ == '__main__':
    unittest.main()