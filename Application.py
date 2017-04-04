from TreeManager import *
import matplotlib.pyplot as plt
import numpy as np
import os

poligon_degree = 2
mn = -10
mx = 10

# print calculate_library_integral_on_range(mn, mx)
#
# new_tree = TreeManager().initialize_tree(mn, mx, poligon_degree)
# print new_tree.calculate_integrate()
#
# for i in range(7):
#     new_tree = TreeManager().add_node_for_worst_fitting_range(new_tree, poligon_degree)
#     print new_tree.calculate_integrate()

tree_2 = TreeManager().initialize_tree(mn, mx, poligon_degree)
tree_2 = TreeManager().add_node_for_some_ranges(tree_2, poligon_degree, 1)
tree_2 = TreeManager().add_node_for_some_ranges(tree_2, poligon_degree, 2)
tree_2 = TreeManager().add_node_for_some_ranges(tree_2, poligon_degree, 4)

def get_plot():
    global domain, values
    domain = np.arange(mn, mx, 0.01)
    values = []
    original = []
    for i in domain:
        values.append(tree_2.calculate_value(i))
        original.append(f(i))
    plt.plot(domain, original)
    plt.plot(domain, values)
    plt.savefig('./plots/final.png')


def get_color_plot(tree):
    global_domain = np.arange(mn, mx, 0.01)
    original_values = []

    for i in global_domain:
        original_values.append(f(i))
    plt.plot(global_domain, original_values, label='original')

    list_of_points = tree.get_list_of_points()

    for point_idx in range(len(list_of_points) - 1):
        domain = np.arange(list_of_points[point_idx], list_of_points[point_idx + 1], 0.01)
        values = []

        for i in domain:
            values.append(tree.calculate_value(i))
        plt.plot(domain, values, label=tree.get_poligon_str_repr(domain[0]))
    # plt.legend(loc='upper center')
    plt.savefig('./plots/color.png')

if not os.path.exists("./plots/"):
    os.makedirs("./plots/")
get_color_plot(tree_2)
