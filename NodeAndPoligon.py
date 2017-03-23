from Functions import *


class Node:

    def __init__(self):
        pass

    def calculate_integrate(self):
        return None

    def is_tree(self):
        return False


class Tree (Node):
    def __init__(self, left, right):
        Node.__init__(self)
        self.left = left
        self.right = right

    def calculate_integrate(self):
        return self.left.calculate_integrate() + self.right.calculate_integrate()

    def is_tree(self):
        return True

    def map_poligons_over_tree(self, poligon_list):
        if self.left.is_tree():
            self.left.map_poligons_over_tree(poligon_list)
        else:
            self.left = poligon_list.pop(0)

        if self.right.is_tree():
            self.right.map_poligons_over_tree(poligon_list)
        else:
            self.right = poligon_list.pop(0)

    def find_worst_fitting_range(self):
        if self.left.is_tree():
            left_error = self.left.find_worst_fitting_range()
        else:
            left_error = self.left.calculate_integrality_error()

        if self.right.is_tree():
            right_error = self.right.find_worst_fitting_range()
        else:
            right_error = self.right.calculate_integrality_error()

        if left_error[0] > right_error[0]:
            return left_error
        return right_error


class Poligon(Node):
    def __init__(self, monomials, low_limit, high_limit):
        Node.__init__(self)
        self.monomials = monomials
        self.low_limit = low_limit
        self.high_limit = high_limit

    def __repr__(self):
        b = ""
        for monomial_idx in range(len(self.monomials)):
            b += str(self.monomials[monomial_idx].coefficient)
            if monomial_idx != len(self.monomials) - 1:
                b += "x^" + str(self.monomials[monomial_idx].degree) + " + "

        return b

    def calculate_integrate(self):
        aggregator = 0
        for monomial in self.monomials:
            aggregator = aggregator + \
                         monomial.get_integral_part_at(self.high_limit) - monomial.get_integral_part_at(self.low_limit)

        return aggregator

    def is_tree(self):
        return False

    def calculate_integrality_error(self):
        original = calculate_library_integral_on_range(self.low_limit, self.high_limit)
        calculated = self.calculate_integrate()

        return abs((original - calculated) / original), self.low_limit, self.high_limit


class Monomial:
    def __init__(self, coefficient, degree):
        self.coefficient = coefficient
        self.degree = degree

    def get_integral_part_at(self, border):
        return ((border + 0.0) ** (self.degree + 1.0)) * (self.coefficient + 0.0) / (self.degree + 1.0)
