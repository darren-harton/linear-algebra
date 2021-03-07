import unittest
from decimal import Decimal

from plane import Plane


class TestLine(unittest.TestCase):
    def test_basic(self):

        A = Plane(['-0.412', '3.806', '0.728'], '-3.46')
        B = Plane(['1.03', '-9.515', '-1.82'], '8.65')
        assert A == B

        C, D = Plane(['2.611','5.528', '0.283'], '4.6'), \
               Plane(['7.714', '8.306', '5.342'], '3.76')
        assert C != D
        assert not C.is_parallel_to(D)

        E, F = Plane(['-7.926','8.625', '-7.212'], '-7.952'), \
               Plane(['-2.642', '2.875', '-2.404'], '-2.443')
        assert E != F
        assert E.is_parallel_to(F)

if __name__ == '__main__':
    unittest.main()