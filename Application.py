from TreeManager import *
import matplotlib.pyplot as plt
import numpy as np
import os

poligon_degree = 3
mn = -2
mx = 3

print calculate_library_integral_on_range(mn, mx)

new_tree = TreeManager().initialize_tree(mn, mx, poligon_degree)
print new_tree.calculate_integrate()

for i in range(4):
    new_tree = TreeManager().add_node_for_worst_fitting_range(new_tree, poligon_degree)
    print new_tree.calculate_integrate()


def get_plot():
    global domain, values
    domain = np.arange(mn, mx, 0.01)
    values = []
    for i in domain:
        values.append(new_tree.calculate_value(i))
    plt.plot(domain, f(domain))
    plt.plot(domain, values)
    plt.savefig('./plots/final.png')


if not os.path.exists("./plots/"):
    os.makedirs("./plots/")
get_plot()










