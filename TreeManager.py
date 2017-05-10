from ManagePoligons import *
from ProbablityDistribution import *
import random
import sys


class TreeManager:
    def __init__(self, f):
        self.iterations = 10
        self.levels = 4
        self.f = f

    def initialize_tree(self, left_limit, right_limit, poligon_degree):
        return ManagePoligons([left_limit, right_limit], poligon_degree, self.f).resolve_poligons_list()[0]

    def clone_tree_structure(self, source):
        if source.left.is_tree():
            left = self.clone_tree_structure(source.left)
        else:
            left = source.left.mock_poligon()

        if source.right.is_tree():
            right = self.clone_tree_structure(source.right)
        else:
            right = source.right.mock_poligon()

        return Tree(left, right, source.midpoint)

    def add_node_for_some_ranges(self, root, poligon_degree, number_of_nodes):
        if root.is_tree():
            all_poligons = root.get_list_of_poligons()
            midpoint_map = {}

            for poligon in all_poligons:
                midpoint_map[poligon] = self.find_random_point_between(poligon.high_limit, poligon.low_limit)

            thicker_tree = self.clone_tree_structure(root)

            for poligon, midpoint in midpoint_map.iteritems():
                thicker_tree.insert_new_point(midpoint)

            list_of_points = [all_poligons[0].low_limit]
            for poligon in all_poligons:
                list_of_points.append(midpoint_map[poligon])
                list_of_points.append(poligon.high_limit)

            new_poligons = ManagePoligons(list_of_points, poligon_degree, self.f).resolve_poligons_list()
            midpoint_to_improvement = {}

            for i in range(len(all_poligons)):
                source_poligon = all_poligons[i]
                left_poligon = new_poligons[2 * i]
                right_poligon = new_poligons[2 * i + 1]

                exact_value = calculate_library_integral_on_range(source_poligon.low_limit, source_poligon.high_limit, self.f)

                def joined_calculate_poligon_value(x):
                    return left_poligon.alternative_calculate_value(x) + right_poligon.alternative_calculate_value(x)

                before_split_error = abs(calculate_relative_integral_difference(source_poligon.low_limit, source_poligon.high_limit, source_poligon.calculate_value, self.f)) / abs(exact_value)
                after_split_error = abs(calculate_relative_integral_difference(source_poligon.low_limit, source_poligon.high_limit, joined_calculate_poligon_value, self.f)) / abs(exact_value)


                midpoint_to_improvement[midpoint_map[source_poligon]] = before_split_error - after_split_error

            distribution = ProbabilityDistribution(midpoint_to_improvement)

            destination_tree = self.clone_tree_structure(root)

            for i in range(int(number_of_nodes)):
                destination_tree.insert_new_point(distribution.get_random_element())

            points = destination_tree.get_list_of_points()
            destination_tree.map_poligons_over_tree(ManagePoligons(points, poligon_degree, self.f).resolve_poligons_list())

            return destination_tree

        else:
            low_limit = root.low_limit
            high_limit = root.high_limit

            midpoint = self.find_random_point_between(high_limit, low_limit)
            poligons_list = ManagePoligons([low_limit, midpoint, high_limit], poligon_degree,
                                           self.f).resolve_poligons_list()

            return Tree(poligons_list[0], poligons_list[1], midpoint)

    def find_random_point_between(self, high_limit, low_limit):
        draw = 0
        while draw == 0:
            draw = random.random()

        return low_limit + (high_limit - low_limit) * draw
