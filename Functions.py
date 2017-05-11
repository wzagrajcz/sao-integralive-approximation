from scipy.integrate import quad
from math import cos, e, pi, sqrt, sin

def calculate_relative_integral_difference(x1, x2, tree_function, f):
    def new_function(x):
        return (f(x) - tree_function(x)) ** 2
    return sqrt(quad(new_function, x1, x2)[0])

def calculate_library_integral_on_range(x1, x2, f):
    return quad(f, x1, x2)[0]
