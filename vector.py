#!/usr/bin/env python3

from typing import Type, Sequence, Iterable, Optional, Union
import typing

import math
from decimal import Decimal


Numeric = Union[float, int, Decimal]


def radToDeg(r):
    return r * 180/math.pi

def degToRad(d):
    return d * math.pi/180

class Vector(object):
    def __init__(self, coords):
        self.coords = tuple(coords)
        self.dims = len(coords)

    def __getitem__(self, item):
        return self.coords[item]

    def __str__(self):
        return 'Vector: {}'.format(self.coords)

    def __eq__(self, other: 'Vector'):
        return self.coords == other.coords

    def __add__(self, other: 'Vector'):
        # assume dims are the same
        return Vector([x + y for x,y in zip(self.coords, other.coords)])

    def __sub__(self, other: 'Vector'):
        # assume dims are the same
        return Vector([x - y for x, y in zip(self.coords, other.coords)])

    def __mul__(self, other):
        if isinstance(other, type(self)):
            # return Vector([x * y for x, y in zip(self.coords, other.coords)])
            raise NotImplemented()
        elif isinstance(other, typing.get_args(Numeric)):
            return Vector([x * other for x in self.coords])
        else:
            raise NotImplemented()
    __rmul__ = __mul__

    def __truediv__(self, scalar: Decimal):
        return Vector([x / scalar for x in self.coords])

    def __matmul__(self, other: 'Vector'):
        """dot product"""
        return sum(x * y for x, y in zip(self.coords, other.coords))

    def magnitude(self) -> Numeric:
        return sum(x ** Decimal('2') for x in self.coords) ** Decimal('.5')

    def normalize(self) -> 'Vector':
        # AKA direction, or unit vector
        mag = self.magnitude()
        if mag == 0:
            return self * 0
        return self * (1 / mag)

    def angle(self, other: 'Vector', tolerance=1e-10) -> Optional[Numeric]:
        if self.is_zero() or other.is_zero():
            return None

        dot = self.normalize() @ other.normalize()
        if 1 < abs(dot) < 1 + tolerance:
            # set as 1 or -1
            dot = math.copysign(1, dot)

        return math.acos(dot)

    def is_orthogonal_to(self, other: 'Vector', tolerance=1e-10):
        return abs(self @ other) < tolerance

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    def is_parallel_to(self, other: 'Vector', tolerance=1e-10):
        if self.is_zero() or other.is_zero():
            return True

        angle = abs(self.angle(other))
        return angle < tolerance or abs(angle - math.pi) < tolerance

    def component_parallel_to(self, other: 'Vector') -> 'Vector':
        """Returns self, projected onto the basis vector"""
        norm = other.normalize()
        return (self @ norm) * norm

    def component_orthogonal_to(self, other: 'Vector'):
        """Returns the component vector of self, orthogonal to the other"""
        return self - self.component_parallel_to(other)

    def cross(self, other: 'Vector'):
        a,b = self,other
        return Vector([
            a[1]*b[2] - b[1]*a[2],
          -(a[0]*b[2] - b[0]*a[2]),
            a[0]*b[1] - b[0]*a[1]
        ])

    def area_of_parallelogram(self, other: 'Vector'):
        return self.cross(other).magnitude()

    def area_of_triangle(self, other: 'Vector'):
        return self.area_of_parallelogram(other) / 2


if __name__ == '__main__':

    assert(Vector([1,2,3]) == Vector([1,2,3]))

    assert(Vector([1,2,3]) + Vector([1,2,3]) == Vector([2,4,6]))
    assert(Vector([1,2,3]) - Vector([1,2,3]) == Vector([0,0,0]))

    assert(Vector([1, 2, 3]) * 2 == Vector([2, 4, 6]))
    assert(Vector([1, 2, 3]) / 2 == Vector([0.5, 1, 1.5]))

    assert(Vector([1, 2, 3]).normalize().magnitude() == 1)

    # dot product
    assert(Vector([1,2,-1]) @ Vector([3,1,0]) == 5)

    a = Vector([1,1])
    assert(a @ a == round(a.magnitude() ** 2, 10))

    b = Vector([-1, -1])
    assert(a @ b == round(a.magnitude() * b.magnitude() * math.cos(math.pi), 10))

    # angle
    assert(round(a.angle(a),5) == 0)
    assert(round(a.angle(b), 5) == round(math.pi, 5))


    # parallel, orthogonal

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

    for v,w,(parallel, orthogonal) in zip(vs, ws, answers):
        assert v.is_parallel_to(w) == parallel
        assert v.is_orthogonal_to(w) == orthogonal

    print("pass")


    # projection, component
    # v = Vector([3.039, 1.879])
    # b = Vector([0.825, 2.036])
    # print(v.component_parallel_to(b))
    #
    # v = Vector([-9.88, -3.264, -8.159])
    # b = Vector([-2.155, -9.353, -9.473])
    # print(v.component_orthogonal_to(b))
    #
    #
    # v = Vector([3.009, -6.172, 3.692, -2.51])
    # b = Vector([6.404, -9.144, 2.759, 8.718])
    # print(v.component_parallel_to(b), v.component_orthogonal_to(b))


    # cross product, parallelogram, and triangle
    v = Vector([8.462, 7.893, -8.187])
    w = Vector([6.984, -5.975, 4.778])
    print(v.cross(w))

    v = Vector([-8.987, -9.838, 5.031])
    w = Vector([-4.268, -1.861, -8.866])
    print(v.area_of_parallelogram(w))

    v = Vector([1.5, 9.547, 3.691])
    w = Vector([-6.007, 0.124, 5.772])
    print(v.area_of_triangle(w))
