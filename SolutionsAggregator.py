from Functions import *
import matplotlib.pyplot as plt
import numpy as np
import operator


class SolutionsAggregator:
    def __init__(self, mn, mx, epsilon, beta, f):
        self.min = mn
        self.max = mx
        self.epsilon = epsilon
        self.beta = beta
        self.solutions = {}
        self.ordered_solutions = []
        self.solutions_epsilon = {}
        self.f = f

    def add_solution_to_pool(self, solution, degree):
        self.solutions[solution] = degree

    def solution_greatness(self, degree, number_of_points, difference_to_solution):
        return self.beta * 0.01 * (1.0 / 8.0 - 1.0 / (((degree + 1) * (number_of_points - 1)) ** 3)) + (1.0 - self.beta) * difference_to_solution

    def order_solutions(self):
        solutions_fit = {}
        exact_value = calculate_library_integral_on_range(self.min, self.max, self.f)

        for solution, degree in self.solutions.iteritems():
            number_of_points = len(solution.get_list_of_points())
            solution_fit = abs(calculate_relative_integral_difference(self.min, self.max, solution.calculate_value, self.f)) / abs(exact_value)

            if solution_fit <= self.epsilon:
                self.solutions_epsilon[solution] = solution_fit
                solutions_fit[solution] = self.solution_greatness(degree, number_of_points, solution_fit)

        self.ordered_solutions = sorted(solutions_fit.items(), key=operator.itemgetter(1))

    def get_color_plot(self, tree, file_path):
        plt.cla()
        plt.clf()
        plt.close()
        global_domain = np.arange(self.min, self.max, 0.01)
        original_values = []

        for i in global_domain:
            original_values.append(self.f(i))
        plt.plot(global_domain, original_values, label='original')

        list_of_points = tree.get_list_of_points()

        for point_idx in range(len(list_of_points) - 1):
            domain = np.arange(list_of_points[point_idx], list_of_points[point_idx + 1], 0.01)
            values = []

            for i in domain:
                values.append(tree.calculate_value(i))
            plt.plot(domain, values, label=tree.get_poligon_str_repr(domain[0]))
        # plt.legend(loc='upper center')
        plt.savefig(file_path)

    def save_best_n_solutions_to_file(self, n, path, extention='png'):
        number_of_solutions_to_save = min(n, len(self.ordered_solutions))
        for i in range(number_of_solutions_to_save):
            self.get_color_plot(self.ordered_solutions[i][0], path + str(i) + '.' + extention)
        print "Saved " + str(number_of_solutions_to_save) + " solutions"

    # deprecated
    def serialize_solutions_to_file(self, file_path):
        f = open(file_path, 'w+')
        for solution_idx in range(len(self.ordered_solutions)):
            string_buffer = str(solution_idx) + ': ' + '\n'
            string_buffer = string_buffer + '\t' + 'cost_function_value: ' + str(
                self.ordered_solutions[solution_idx][1]) + '\n'

            solution = self.ordered_solutions[solution_idx][0]

            string_buffer = string_buffer + '\t' + 'epsilon: ' + str(self.solutions_epsilon[solution]) + '\n'
            string_buffer = string_buffer + '\t' + 'degree: ' + str(self.solutions[solution]) + '\n'
            string_buffer = string_buffer + '\t' + 'num_of_midpoints: ' + str(
                len(solution.get_list_of_points()) - 2) + '\n'

            f.write(string_buffer)

        f.close()

    def get_best_fitness(self):
        return self.ordered_solutions[0][1]

    def serialize_solutions_as_json(self, file_path):
        f = open(file_path, "w+")
        f.write("[\n")

        for solution_idx in range(len(self.ordered_solutions)):
            solution_buffor = "\t{\n"
            solution_buffor += '\t\t' + "\"solution index\" : " + str(solution_idx+1) + ",\n"
            solution_buffor += '\t\t' + "\"solution greatness\" : " + str(
                self.ordered_solutions[solution_idx][1]) + ",\n"

            solution = self.ordered_solutions[solution_idx][0]

            solution_buffor += '\t\t' + "\"epsilon\" : " + str(self.solutions_epsilon[solution]) + ",\n"
            solution_buffor += '\t\t' + "\"degree\" : " + str(self.solutions[solution]) + ",\n"
            solution_buffor += '\t\t' + "\"number of midpoints\" : " + str(
                len(solution.get_list_of_points()) - 2) + ",\n"

            solution_buffor += '\t\t' + "\"tree\" : " + solution.serialize_as_json(3) + "\n"

            solution_buffor += "\t}"

            if solution_idx != len(self.ordered_solutions) - 1:
                solution_buffor += ","

            solution_buffor += "\n"

            f.write(solution_buffor)

        f.write("]\n")
        f.close()

    def order_solutions_with_external_comparator(self, comparator):
        solutions_fit = {}
        exact_value = calculate_library_integral_on_range(self.min, self.max, self.f)

        for solution, degree in self.solutions.iteritems():
            number_of_points = len(solution.get_list_of_points())
            solution_fit = abs(
                calculate_relative_integral_difference(self.min, self.max, solution.solution.calculate_value, self.f)) / abs(
                exact_value)

            if solution_fit <= self.epsilon:
                self.solutions_epsilon[solution] = solution_fit
                solutions_fit[solution] = comparator(degree, number_of_points, solution_fit)

        self.ordered_solutions = sorted(solutions_fit.items(), key=operator.itemgetter(1))
