from TreeManager import *
from StartupManager import *
from SolutionsAggregator import *
from Tests import *
import os

def run(f, case_number, try_no, alpha):
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
    directory = 'plots/' + f.__name__ + '/try_no_' + str(try_no) + '/alpha_' + str(alpha) + '/case_number_' + str(case_number) + '/'
    if not os.path.exists(directory):
       os.makedirs(directory)
    solutions_aggregator.save_best_n_solutions_to_file(1, directory)
    solutions_aggregator.serialize_solutions_as_json(directory + 'solutions.json')

    print str(solutions_aggregator.get_best_fitness()) + ',',

def test():

    print 'PolynomialFunction'
    for i in range(len(polynomial_function_params)):
        for alpha in [0.0, 1.0, 3.0, 6.0, 10.0, 20.0, 100.0, 1000.0]:
            print str(alpha) + ',' + str(i) + ',',
            for try_no in range(0,5):
                f = PolynomialFunctionProvider(polynomial_function_params[i]).provide()
                try:
                    run(f, i, try_no, alpha)
                except:
                    print 'na,',
            print " "

    print 'GaussianDistributionPeriodicFunction'
    for i in range(len(gaussian_distribution_periodic_function_params)):
        for alpha in [0.0, 1.0, 3.0, 6.0, 10.0, 20.0, 100.0, 1000.0]:
            print str(alpha) + ',' + str(i) + ',',
            for try_no in range(0,5):
                f = GaussianDistributionPeriodicFunctionProvider(gaussian_distribution_periodic_function_params[i]).provide()
                try:
                    run(f, i, try_no, alpha)
                except:
                    print 'na,',
            print " "

    print 'GaussianDistributionFunction'
    for i in range(len(gaussian_distribution_function_params)):
        for alpha in [0.0, 1.0, 3.0, 6.0, 10.0, 20.0, 100.0, 1000.0]:
            print str(alpha) + ',' + str(i) + ',',
            for try_no in range(0,5):
                f = GaussianDistributionPeriodicFunctionProvider(gaussian_distribution_function_params[i]).provide()
                try:
                    run(f, i, try_no, alpha)
                except:
                    print 'na,',
            print " "

    print 'NonDifferentiableFunction'
    for i in range(len(non_differentiable_function_params)):
        for alpha in [0.0, 1.0, 3.0, 6.0, 10.0, 20.0, 100.0, 1000.0]:
            print str(alpha) + ',' + str(i) + ',',
            for try_no in range(0,5):
                f = GaussianDistributionPeriodicFunctionProvider(non_differentiable_function_params[i]).provide()
                try:
                    run(f, i, try_no, alpha)
                except:
                    print 'na,',
            print " "

test()
