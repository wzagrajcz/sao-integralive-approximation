from scipy.integrate import quad


def f(x):
    return x ** 2 + 2 * x + 1


def calculate_library_integral_on_range(x1, x2):
    return quad(f, x1, x2)[0]
