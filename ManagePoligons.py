import numpy as np
from Utils import *
from NodeAndPoligon import *


class ManagePoligons:
    def __init__(self, points, poligon_degree, f):
        self.points = points
        self.poligon_degree = poligon_degree
        self.f = f
        self.number_of_points = len(points) - 2
        self.number_of_ranges = len(points) - 1
        self.matrix_size = (poligon_degree + 1) * self.number_of_ranges

    def get_value_at_point(self, point, coefficient, degree):
        return (point ** degree) * coefficient

    def get_equation_for_value_at_point(self, point, index_of_poligon):
        offset = index_of_poligon * (self.poligon_degree + 1)

        equation = [0] * self.matrix_size

        for degree in range(self.poligon_degree + 1):
            equation[offset + self.poligon_degree - degree] += self.get_value_at_point(point, 1, degree)

        return equation, self.f(point)

    def get_equation_for_nth_derivative_equality_at_point(self, point, index_of_point, n):
        offset = (index_of_point - 1) * (self.poligon_degree + 1)

        equation = [0] * self.matrix_size

        for degree in range(self.poligon_degree + 1):
            equation[offset + degree] += get_nth_diff_at_point(point, 1, self.poligon_degree - degree, n)
            equation[offset + degree + self.poligon_degree + 1] += get_nth_diff_at_point(point, -1,
                                                                                        self.poligon_degree - degree, n)

        return equation, 0

    # wyleco
    def get_equation_for_nth_derivative_equality(self, left_edge_point, right_edge_point,
                                                 poligon_degree, right_point_index, n):
        matrix_size = right_point_index * (poligon_degree + 1)
        offset = matrix_size - (poligon_degree + 1) - 1

        equation = [0] * matrix_size

        for degree in range(poligon_degree + 1):
            equation[poligon_degree - degree] += get_nth_diff_at_point(left_edge_point, 1, poligon_degree - degree, n)
            equation[poligon_degree - degree + offset + 1] += get_nth_diff_at_point(right_edge_point, -1, poligon_degree - degree, n)

        return equation, 0

    def build_system_of_equations(self):
        coefficients_matrix = []
        result_matrix = []

        for poligon_idx in range(self.number_of_ranges):
            equation, value = self.get_equation_for_value_at_point(self.points[poligon_idx], poligon_idx)
            coefficients_matrix.append(equation)
            result_matrix.append(value)
            equation, value = self.get_equation_for_value_at_point(self.points[poligon_idx + 1], poligon_idx)
            coefficients_matrix.append(equation)
            result_matrix.append(value)

        for point_idx in range(1, len(self.points) - 1):
            for derivative_degree in range(1, self.poligon_degree):
                equation, value = self.get_equation_for_nth_derivative_equality_at_point(self.points[point_idx],
                                                                                         point_idx, derivative_degree)

                coefficients_matrix.append(equation)
                result_matrix.append(value)

        if len(self.points) == 2:
            for degree in range(1, self.poligon_degree):
                equation = self.get_equation_for_nth_derivative_value(self.points[0], self.poligon_degree, degree)
                coefficients_matrix.append(equation)
                result_matrix.append(0)
        else:
            for degree in range(1, self.poligon_degree):
                equation, value = self.get_equation_for_nth_derivative_equality(
                    self.points[0], self.points[-1], self.poligon_degree, len(self.points) - 1, degree)

                coefficients_matrix.append(equation)
                result_matrix.append(value)

        return coefficients_matrix, result_matrix

    def resolve_poligons_list(self):
        coefficients_matrix, result_matrix = self.build_system_of_equations()
        coefficients_array = np.array(coefficients_matrix)
        result_array = np.array(result_matrix)

        list_of_factors = np.linalg.solve(coefficients_array, result_array).tolist()
        list_of_poligons = []

        for poligon_idx in range(len(list_of_factors)/(self.poligon_degree + 1)):
            poligon_factors = list_of_factors[poligon_idx * (self.poligon_degree + 1):(poligon_idx + 1) * (self.poligon_degree + 1)]

            monomials = []
            for factor_idx in range(len(poligon_factors)):
                monomials.append(Monomial(poligon_factors[factor_idx], len(poligon_factors) - factor_idx - 1))

            list_of_poligons.append(Poligon(monomials, self.points[poligon_idx], self.points[poligon_idx + 1]))

        return list_of_poligons

    def get_equation_for_nth_derivative_value(self, point, poligon_degree, n):

        equation = [0] * self.matrix_size
        for degree in range(poligon_degree + 1):
            params = self.get_derivative_n_params_at_point(1, degree, n)
            equation[poligon_degree - degree] = (point ** params[1]) * params[0]

        return equation

    def get_derivative_n_params_at_point(self, coefficient, degree, n):
        if n == 0:
            return coefficient, degree
        return self.get_derivative_n_params_at_point(coefficient * degree, degree - 1, n - 1)