import operator
import math


class StartupManager:
    def __init__(self, possible_degrees):
        self.priority_queue = []

        self.temporary_cost_dictionary = {}
        for degree in possible_degrees:
            self.temporary_cost_dictionary[degree] = self.cost_function(degree, 2)

        self.priority_queue = sorted(self.temporary_cost_dictionary.items(), key=operator.itemgetter(1))

    def cost_function(self, degree, number_of_points):
        return ((degree + 1)*(number_of_points - 1))**3

    def get_most_optimal_solution(self):
        return self.priority_queue.pop(0)[0]

    def register_new_solution(self, degree, number_of_points):
        self.temporary_cost_dictionary[degree] = self.cost_function(degree, number_of_points)
        self.priority_queue = sorted(self.temporary_cost_dictionary.items(), key=operator.itemgetter(1))

    def how_many_new_points(self, previous_number_of_points):
        if previous_number_of_points <= 9:
            return previous_number_of_points - 1
        return math.ceil(math.sqrt(previous_number_of_points)/3)


