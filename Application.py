from TreeManager import *
from StartupManager import *
from SolutionsAggregator import *
import os
import math

def non_differentiable_function(x, a, b):
    return max(a*math.sin(x/b), 1.0)

def gaussian_distribution_periodic_function(x, sigma, a):
    return ((1.0/(sigma * math.sqrt(2.0*math.pi))) * math.exp(-math.pow(x,2)/(2.0*math.pow(sigma,2)))) * math.cos(x/a)

def gaussian_distribution_function(x, sigma, ni):
    return (1.0/(sigma * math.sqrt(2.0*math.pi))) * math.exp(-math.pow(x-ni,2)/(2.0*math.pow(sigma,2)))

def polynomial_function(x, degree, params)
    f = 0
    for i in reversed(range(degree)):
        f += pow(x,i)*params[i]
    return f

# def f(fun, x, *args):
#     return fun(x, args)

def run(f, case_number):
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
    directory = './plots/' + f.__name__ + '/' + str(case_number) + '/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    solutions_aggregator.save_best_n_solutions_to_file(1, directory)
    solutions_aggregator.serialize_solutions_as_json(directory + 'solutions.json')

#run(f(), 0)