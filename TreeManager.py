from ManagePoligons import *
import random


class TreeManager:
    def __init__(self):
        pass

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

        return Tree(left, right)

    def add_node_for_worst_fitting_range(self, root, poligon_degree):
        if root.is_tree():
            range = root.find_worst_fitting_range()
            midpoint = self.find_random_point_between(range[1], range[2])
            new_tree = self.clone_tree_structure(root)
            new_tree.insert_new_point(midpoint)
            points = new_tree.get_list_of_points()
            new_tree.map_poligons_over_tree(ManagePoligons(points, poligon_degree, f).resolve_poligons_list())
            return new_tree
        else:
            low_limit = root.low_limit
            high_limit = root.high_limit

            midpoint = self.find_random_point_between(high_limit, low_limit)
            poligons_list = ManagePoligons([low_limit, midpoint, high_limit], poligon_degree, f).resolve_poligons_list()
            return Tree(poligons_list[0], poligons_list[1])

    def find_random_point_between(self, high_limit, low_limit):
        draw = 0
        while draw == 0:
            draw = random.random()

        return low_limit + (high_limit - low_limit) * draw



