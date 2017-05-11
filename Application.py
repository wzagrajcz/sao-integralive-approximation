from TreeManager import *
from StartupManager import *
from SolutionsAggregator import *
import os

def f(x):
    return max(2*sin(x/2.0), 1.5)

# def f_polynomial(x, degree, *params):
#     f = 0
#     for x in reversed(range(degree)):
#         f += pow()


#def f(x):
    #a = 100
    #sigma = 10
    #mi = 0
    # return a / (sigma * sqrt(2 * pi)) * e ** ((-1 * x**2)/(2 * sigma**2)) * cos(x/3)
    # return 0.5 * x**4 - 2.34 * x**3 + 0.654 * x**2 - 12*x + 0.75
    #return max(2*sin(x/2.0), 1.5)
    # a = -10
    # sigma = 10
    # b = 0.3
    # c = 0.2
    # d = 0.1
    # e = 2
    # return a/(sigma * sqrt(b*pi)) * e ** ( (-c * x**2) / (d * sigma**2) ) * cos(x/e)

mn = -10
mx = 10
epsilon = 0.1

posible_degrees = range(1, 6)
trees = {}
startup_manager = StartupManager(posible_degrees)
solutions_aggregator = SolutionsAggregator(mn, mx, epsilon, 0.5, f)


for i in range(125):
    degree = startup_manager.get_most_optimal_solution()

    if degree not in trees:
        tree = TreeManager(f).initialize_tree(mn, mx, degree)
        startup_manager.register_new_solution(degree, startup_manager.how_many_new_points(2) + 2)
        trees[degree] = tree
        solutions_aggregator.add_solution_to_pool(tree, degree)

    else:
        previous_tree = trees[degree]
        previous_number_of_points = len(previous_tree.get_list_of_points())
        points_to_insert = startup_manager.how_many_new_points(previous_number_of_points)
        tree = TreeManager(f).add_node_for_some_ranges(previous_tree, degree, points_to_insert)
        startup_manager.register_new_solution(degree, previous_number_of_points + points_to_insert +
                            startup_manager.how_many_new_points(previous_number_of_points + points_to_insert))
        trees[degree] = tree
        solutions_aggregator.add_solution_to_pool(tree, degree)

solutions_aggregator.order_solutions()
directory = './plots/' + f.__name__ + '/'
if not os.path.exists(directory):
    os.makedirs(directory)
solutions_aggregator.save_best_n_solutions_to_file(1, directory)
solutions_aggregator.serialize_solutions_as_json("./solutions.json")
