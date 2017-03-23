from ManagePoligons import *

tree = Tree(Tree(Node(), Node()), Tree(Node(), Node()))

poligon_degree = 2
points = [3, 4, 5, 6, 7]

poligons = ManagePoligons(points, poligon_degree, f).resolve_poligons_list()
tree.map_poligons_over_tree(poligons)
print tree.calculate_integrate()
