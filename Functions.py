from scipy.integrate import quad


def f(x):
    return 0.5 * x**4 - 2.34 * x**3 + 0.654 * x**2 - 12*x + 0.75


def calculate_library_integral_on_range(x1, x2):
    return quad(f, x1, x2)[0]
