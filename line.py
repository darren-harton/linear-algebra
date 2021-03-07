from decimal import getcontext, Decimal as _Decimal
getcontext().prec = 30

from vector import Vector


class Decimal(_Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

class Line:
    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        # Only 2D is supported for now
        self.dims = 2

        if normal_vector is None:
            zeros = [Decimal('0') for _ in range(self.dims)]
            normal_vector = Vector(zeros)
        if not isinstance(normal_vector, Vector):
            normal_vector = Vector([Decimal(x) for x in normal_vector])
        self.normal_vector = normal_vector

        if constant_term is None:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.basepoint = None
        self.set_basepoint()


    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = [Decimal('0') for _ in range(self.dims)]

            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = c / initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e


    def is_parallel_to(self, other: 'Line', tolerance=1e-10):
        return self.normal_vector.is_parallel_to(other.normal_vector, tolerance=tolerance)


    def __eq__(self, other: 'Line'):
        # Equal or equivalent

        if self.normal_vector.is_zero():
            if not other.normal_vector.is_zero():
                return False
            diff = self.constant_term - other.constant_term
            return diff.is_near_zero()

        if other.normal_vector.is_zero():
            return False

        if not self.is_parallel_to(other):
            return False

        # If the vector connecting the basepoints is orthogonal to the line's normal vector,
        #  they must be the same line
        base_vect = Vector([a-b for a,b in zip(self.basepoint, other.basepoint)])
        return self.normal_vector.is_orthogonal_to(base_vect)


    def intersection_with(self, other: 'Line'):
        if self == other:
            # All points intersect
            return self

        if self.is_parallel_to(other):
            return None

        (A,B),k1 = self.normal_vector.coords, self.constant_term
        (C,D),k2 = other.normal_vector.coords, other.constant_term

        denom = A*D - B*C
        x = ( D*k1 - B*k2)/denom
        y = (-C*k1 + A*k2)/denom
        return x,y


    def __repr__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dims) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output


    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not Decimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)
