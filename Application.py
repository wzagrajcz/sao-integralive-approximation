from TreeManager import *
from StartupManager import *
from SolutionsAggregator import *

mn = -10
mx = 10
epsilon = 0.1

posible_degrees = range(1, 6)
trees = {}
startup_manager = StartupManager(posible_degrees)
solutions_aggregator = SolutionsAggregator(mn, mx, epsilon, 0.5)


for i in range(125):
    degree = startup_manager.get_most_optimal_solution()

    if degree not in trees:
        tree = TreeManager().initialize_tree(mn, mx, degree)
        startup_manager.register_new_solution(degree, startup_manager.how_many_new_points(2) + 2)
        trees[degree] = tree
        solutions_aggregator.add_solution_to_pool(tree, degree)

    else:
        previous_tree = trees[degree]
        previous_number_of_points = len(previous_tree.get_list_of_points())
        points_to_insert = startup_manager.how_many_new_points(previous_number_of_points)
        tree = TreeManager().add_node_for_some_ranges(previous_tree, degree, points_to_insert)
        startup_manager.register_new_solution(degree, previous_number_of_points + points_to_insert +
                            startup_manager.how_many_new_points(previous_number_of_points + points_to_insert))
        trees[degree] = tree
        solutions_aggregator.add_solution_to_pool(tree, degree)


solutions_aggregator.order_solutions()
solutions_aggregator.save_best_n_solutions_to_file(25, './plots/')
solutions_aggregator.serialize_solutions_as_json("./solutions.json")
