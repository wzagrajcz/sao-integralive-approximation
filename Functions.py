from scipy.integrate import quad
from math import cos, e, pi, sqrt, sin


def f(x):
    a = 100
    sigma = 10
    mi = 0
    # return a / (sigma * sqrt(2 * pi)) * e ** ((-1 * x**2)/(2 * sigma**2)) * cos(x/3)
    # return 0.5 * x**4 - 2.34 * x**3 + 0.654 * x**2 - 12*x + 0.75
    return max(2*sin(x/2.0), 1.5)


def calculate_library_integral_on_range(x1, x2):
    return quad(f, x1, x2)[0]
