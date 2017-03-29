from ManagePoligons import *
import random
import sys

class TreeManager:
    def __init__(self):
        self.iterations = 10
        self.levels = 4

    def initialize_tree(self, left_limit, right_limit, poligon_degree):
        return ManagePoligons([left_limit, right_limit], poligon_degree, f).resolve_poligons_list()[0]

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

    def add_node_for_worst_fitting_range(self, root, poligon_degree):
        candidate_trees = {}
        error_to_point = {}

        if root.is_tree():
            searching_range = root.find_worst_fitting_range()

            points = root.get_list_of_points()
            reference_integral = calculate_library_integral_on_range(points[0], points[-1])

            min_point = searching_range[1]
            max_point = searching_range[2]

            for j in range(self.levels):

                for i in range(self.iterations):
                    midpoint = self.find_random_point_between(min_point, max_point)
                    new_tree = self.clone_tree_structure(root)
                    new_tree.insert_new_point(midpoint)
                    points = new_tree.get_list_of_points()
                    new_tree.map_poligons_over_tree(ManagePoligons(points, poligon_degree, f).resolve_poligons_list())
                    error = abs(new_tree.calculate_integrate() - reference_integral)
                    candidate_trees[error] = new_tree
                    error_to_point[error] = midpoint

                best_midpoint = None
                lowest_error = sys.float_info.max

                for error, midpoint in error_to_point.iteritems():
                    if error < lowest_error:
                        lowest_error = error
                        best_midpoint = midpoint

                highest_smaller = sys.float_info.min
                lowest_higher = sys.float_info.max

                for error, midpoint in error_to_point.iteritems():
                    if best_midpoint > midpoint > highest_smaller:
                        highest_smaller = midpoint
                    if best_midpoint < midpoint < lowest_higher:
                        lowest_higher = midpoint

                min_point = highest_smaller
                max_point = lowest_higher

        else:
            low_limit = root.low_limit
            high_limit = root.high_limit

            reference_integral = calculate_library_integral_on_range(low_limit, high_limit)

            for i in range(self.iterations):
                midpoint = self.find_random_point_between(high_limit, low_limit)
                poligons_list = ManagePoligons([low_limit, midpoint, high_limit], poligon_degree, f).resolve_poligons_list()

                new_tree = Tree(poligons_list[0], poligons_list[1], midpoint)
                candidate_trees[abs(new_tree.calculate_integrate() - reference_integral)] = new_tree

        fitting_error = sys.float_info.max
        best_tree = None

        for error, tree in candidate_trees.iteritems():
            if error < fitting_error:
                fitting_error = error
                best_tree = tree

        return best_tree

    def find_random_point_between(self, high_limit, low_limit):
        draw = 0
        while draw == 0:
            draw = random.random()

        return low_limit + (high_limit - low_limit) * draw



