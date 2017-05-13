import math


# polynomials
# degree params (starting from x_0,x_1...,x_degree-1)

class PolynomialFunctionProvider:
    def __init__(self, test_case):
        self.degree = test_case[0]
        self.params = test_case[1]

    def function(self, x):
        f = 0
        for i in reversed(range(self.degree)):
            f += pow(x, i) * self.params[i]
        return f

    def provide(self):
        return self.function


class GaussianDistributionPeriodicFunctionProvider:
    def __init__(self, test_case):
        self.sigma = test_case[0]
        self.a = test_case[1]

    def function(self, x):
        return ((1.0 / (self.sigma * math.sqrt(2.0 * math.pi))) * math.exp(
            -math.pow(x, 2) / (2.0 * math.pow(self.sigma, 2)))) * math.cos(x / self.a)

    def provide(self):
        return self.function


class GaussianDistributionFunctionProvider:
    def __init__(self, test_case):
        self.sigma = test_case[0]
        self.ni = test_case[1]

    def function(self, x):
        return (1.0/(self.sigma * math.sqrt(2.0*math.pi))) * math.exp(-math.pow(x-self.ni,2)/(2.0*math.pow(self.sigma,2)))

    def provide(self):
        return self.function


class NonDifferentiableFunctionProvider:
    def __init__(self, test_case):
        self.a = test_case[0]
        self.b = test_case[1]

    def function(self, x):
        return max(self.a*math.sin(x/self.b), 1.0)

    def provide(self):
        return self.function


polynomial_function_params = \
    [
        # f(x) = 3
        [1, [3, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        # f(x) = 1.2x + 9
        [2, [1.2, 9, 0, 0, 0, 0, 0, 0, 0, 0]],
        # f(x) = 3.2x^2 - 1.69x - 8.14
        [3, [3.2, -1.69, -8.14, 0, 0, 0, 0, 0, 0, 0]],
        # f(x) = -7.2x^3 + 1.09x^2 + 12.49x - 6.1
        [4, [-7.2, 1.09, 12.49, -6.1, 0, 0, 0, 0, 0, 0]],
        # f(x) = 2.1x^4 + 8.1x^3 - 12.3x^2 + 8.1x - 1.1
        [5, [2.1, 8.1, -12.3, 8.1, -1.1, 0, 0, 0, 0, 0]],
        # f(x) = 8.3x^5 + 9x^4 + 2.4x^3 - 6.1x^2 - 3.1x - 9.2
        [6, [8.3, 9, 2.4, -6.1, -3.1, -9.2, 0, 0, 0, 0]],
        # f(x) = 23x^6 + 2.3x^5 + 4x^4 + 6.1x^3 - 5.1x^2 - 1.4x - 12.2
        [7, [23, 2.3, 4, 6.1, -5.1, 1.4, 12.2, 0, 0, 0]],
        # f(x) = 5.9x^7 + 2.3x^6 - 4x^5 - 5.1x^3 + 1.4x^2 + 12.2x - 4.1
        [8, [5.9, 2.3, -4, 0, -5.1, 1.4, 12.2, -4.1, 0, 0]],
        # f(x) = -3.5x^8 + 2.3x^7 + 4x^6 + 6.1x^5 - 5.1x^4 + 1.4x^3 + 12.2x^2 + 4.1x - 12.2
        [9, [-3.5, 2.3, 4, 6.1, -5.1, 1.4, 12.2, 4.1, -12.2, 0]],
        # f(x) = -1.3x^9 - 2.3x^8 + 4x^7 + x^6 - 0.23x^5 + 2.1x^2 - x + 1
        [10, [-1.3, 2.3, 4, 1, -0.23, 0, 0, 2.1, -1, 1]]
    ]

# Gaussian distribution
# sigma ni
# f(x) = (1.0/(sigma * math.sqrt(2.0*math.pi))) * math.exp(-math.pow(x-ni,2)/(2.0*math.pow(sigma,2)))
gaussian_distribution_function_params = \
    [
        [2.0, 0.0],
        [1.0, 0.0],
        [0.5, 0.0],
        [1.0, 3.0]
    ]

# Gaussian distribution and periodic functions
# sigma ni a
# f(x) = ((1.0/(sigma * math.sqrt(2.0*math.pi))) * math.exp(-math.pow(x-ni,2)/(2.0*math.pow(sigma,2)))) * cos(x/a)
gaussian_distribution_periodic_function_params = \
    [
        [1.0, 2.0],
        [1.0, 1.0],
        [1.5, 0.5]
    ]

# max(a*sin(x/b), 1.0)
# a b c
non_differentiable_function_params = \
    [
        [2.0, 2.0],
        [10.0, 2.0],
        [2.0, 5.0],
        [2.0, 0.5]
    ]
