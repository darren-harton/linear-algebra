import unittest
import math

from vector import Vector
# from line import Line


class TestVector(unittest.TestCase):
    def test_basic(self):
        assert (Vector([1, 2, 3]) == Vector([1, 2, 3]))

        assert (Vector([1, 2, 3]) + Vector([1, 2, 3]) == Vector([2, 4, 6]))
        assert (Vector([1, 2, 3]) - Vector([1, 2, 3]) == Vector([0, 0, 0]))

        assert (Vector([1, 2, 3]) * 2 == Vector([2, 4, 6]))
        assert (Vector([1, 2, 3]) / 2 == Vector([0.5, 1, 1.5]))

        assert (Vector([1, 2, 3]).normalize().magnitude() == 1)

        # dot product
        assert(Vector([1,2,-1]) @ Vector([3,1,0]) == 5)

        a = Vector([1,1])
        assert(a @ a == round(a.magnitude() ** 2, 10))

        b = Vector([-1, -1])
        assert(a @ b == round(a.magnitude() * b.magnitude() * math.cos(math.pi), 10))

        # angle
        assert(round(a.angle(a),5) == 0)
        assert(round(a.angle(b), 5) == round(math.pi, 5))

    def test_parallel_orthogonal(self):
        vs = [
            Vector([-7.579, -7.88]),
            Vector([-2.029, 9.97, 4.172]),
            Vector([-2.328, -7.284, -1.214]),
            Vector([2.118, 4.827])
        ]

        ws = [
            Vector([22.737, 23.64]),
            Vector([-9.231, -6.639, -7.245]),
            Vector([-1.821, 1.072, -2.94]),
            Vector([0, 0])
        ]

        answers = [
            (True, False),
            (False, False),
            (False, True),
            (True, True),
        ]

        for v, w, (parallel, orthogonal) in zip(vs, ws, answers):
            assert v.is_parallel_to(w) == parallel
            assert v.is_orthogonal_to(w) == orthogonal

    def test_projection_orthogonal(self):
        # TODO: get answers
        v = Vector([3.039, 1.879])
        b = Vector([0.825, 2.036])
        print(v.component_parallel_to(b))

        v = Vector([-9.88, -3.264, -8.159])
        b = Vector([-2.155, -9.353, -9.473])
        print(v.component_orthogonal_to(b))


        v = Vector([3.009, -6.172, 3.692, -2.51])
        b = Vector([6.404, -9.144, 2.759, 8.718])
        print(v.component_parallel_to(b), v.component_orthogonal_to(b))


    def test_cross_product_parallelogram_and_triangle(self):
        # TODO: get answers
        v = Vector([8.462, 7.893, -8.187])
        w = Vector([6.984, -5.975, 4.778])
        print(v.cross(w))

        v = Vector([-8.987, -9.838, 5.031])
        w = Vector([-4.268, -1.861, -8.866])
        print(v.area_of_parallelogram(w))

        v = Vector([1.5, 9.547, 3.691])
        w = Vector([-6.007, 0.124, 5.772])
        print(v.area_of_triangle(w))

if __name__ == '__main__':
    unittest.main()