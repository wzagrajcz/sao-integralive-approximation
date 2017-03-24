from TreeManager import *

poligon_degree = 2
mn = 2
mx = 5
tree = TreeManager().initialize_tree(mn, mx, poligon_degree)
print calculate_library_integral_on_range(mn, mx)
print tree.calculate_integrate()
new_tree = TreeManager().add_node_for_worst_fitting_range(tree, poligon_degree)
print new_tree.calculate_integrate()
for i in range(10):
    new_tree = TreeManager().add_node_for_worst_fitting_range(new_tree, poligon_degree)
    print new_tree.calculate_integrate()