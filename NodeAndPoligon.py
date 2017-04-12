from Functions import *


class Node:

    def __init__(self):
        pass

    def calculate_integrate(self):
        return None

    def is_tree(self):
        return False


class Tree (Node):
    def __init__(self, left, right, midpoint):
        Node.__init__(self)
        self.left = left
        self.right = right
        self.midpoint = midpoint

    def calculate_integrate(self):
        return self.left.calculate_integrate() + self.right.calculate_integrate()

    def is_tree(self):
        return True

    def calculate_value(self, point):
        if self.midpoint < point:
            return self.right.calculate_value(point)
        return self.left.calculate_value(point)

    def get_poligon_str_repr(self, point):
        if self.midpoint < point:
            return self.right.get_poligon_str_repr(point)
        return self.left.get_poligon_str_repr(point)

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

    def insert_new_point(self, midpoint):
        if self.left.is_tree():
            self.left.insert_new_point(midpoint)
        else:
            if self.left.is_in_range(midpoint):
                left_poligon = Poligon([], self.left.low_limit, midpoint)
                right_poligon = Poligon([], midpoint, self.left.high_limit)
                self.left = Tree(left_poligon, right_poligon, midpoint)

        if self.right.is_tree():
            self.right.insert_new_point(midpoint)
        else:
            if self.right.is_in_range(midpoint):
                left_poligon = Poligon([], self.right.low_limit, midpoint)
                right_poligon = Poligon([], midpoint, self.right.high_limit)
                self.right = Tree(left_poligon, right_poligon, midpoint)

    def get_list_of_points(self):
        list_of_points = self.get_list_of_points_helper()
        list_of_points.append(self.get_highest_point())
        return list_of_points

    def get_highest_point(self):
        if self.right.is_tree():
            return self.right.get_highest_point()
        return self.right.high_limit

    def get_list_of_points_helper(self):
        list_of_points = []
        if self.left.is_tree():
            list_of_points += self.left.get_list_of_points_helper()
        else:
            list_of_points.append(self.left.low_limit)

        if self.right.is_tree():
            list_of_points += self.right.get_list_of_points_helper()
        else:
            list_of_points.append(self.right.low_limit)

        return list_of_points

    def get_list_of_ranges(self):
        return self.left.get_list_of_ranges() + self.right.get_list_of_ranges()

    def get_list_of_poligons(self):
        l = []
        if not self.left.is_tree():
            l.append(self.left)
        else:
            l = l + self.left.get_list_of_poligons()
        if not self.right.is_tree():
            l.append(self.right)
        else:
            l = l + self.right.get_list_of_poligons()
        return l

    def serialize_as_json(self, level):
        string_buffer = "{\n"
        string_buffer += "\t"*level + "\"midpoint\" : " + str(self.midpoint) + ",\n"
        string_buffer += "\t"*level + "\"left\" : " + self.left.serialize_as_json(level+1) + ",\n"
        string_buffer += "\t"*level + "\"right\" : " + self.right.serialize_as_json(level+1) + "\n"
        string_buffer += "\t"*(level-1) + "}"

        return string_buffer


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

    def serialize_as_json(self, level):
        string_buffer = "{\n"
        string_buffer += "\t"*level + "\"low limit\" : " + str(self.low_limit) + ",\n"
        string_buffer += "\t"*level + "\"high limit\" : " + str(self.high_limit) + ",\n"
        string_buffer += "\t"*level + "\"coefficients\" : " + "[\n"
        for monomial_idx in range(len(self.monomials)):
            string_buffer += self.monomials[monomial_idx].serialize_as_json(level+1)
            if monomial_idx != len(self.monomials) - 1:
                string_buffer += ","
            string_buffer += "\n"
        string_buffer += "\t"*level + "]\n"
        string_buffer += "\t"*(level-1) + "}"
        return string_buffer

    def get_poligon_str_repr(self, point):
        return self.__repr__()

    def calculate_integrate(self):
        aggregator = 0
        for monomial in self.monomials:
            aggregator = aggregator + \
                         monomial.get_integral_part_at(self.high_limit) - monomial.get_integral_part_at(self.low_limit)

        return aggregator

    def get_list_of_points(self):
        return [self.low_limit, self.high_limit]

    def is_tree(self):
        return False

    def calculate_value(self, point):
        if self.is_in_range(point):
            return self.calculate_value_at_point(point)

    def calculate_integrality_error(self):
        original = calculate_library_integral_on_range(self.low_limit, self.high_limit)
        calculated = self.calculate_integrate()
        return abs(original - calculated)/ abs(original), self.low_limit, self.high_limit#

    def mock_poligon(self):
        return Poligon([], self.low_limit, self.high_limit)

    def is_in_range(self, point):
        return self.low_limit <= point <= self.high_limit

    def calculate_value_at_point(self, point):
        aggregator = 0
        for monomial in self.monomials:
            aggregator += monomial.get_value_at_point(point)

        return aggregator

    def get_list_of_ranges(self):
        return self.low_limit, self.high_limit


class Monomial:
    def __init__(self, coefficient, degree):
        self.coefficient = coefficient
        self.degree = degree

    def get_integral_part_at(self, border):
        return ((border + 0.0) ** (self.degree + 1.0)) * (self.coefficient + 0.0) / (self.degree + 1.0)

    def get_value_at_point(self, point):
        return (point ** self.degree) * self.coefficient

    def serialize_as_json(self, level):
        if self.degree == 0:
            monomial_suffix = ""
        else:
            monomial_suffix = " * x^" + str(self.degree)

        return "\t"*level + "\"" + str(self.coefficient) + monomial_suffix + "\""
