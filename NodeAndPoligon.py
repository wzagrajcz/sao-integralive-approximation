
class Node:

    def __init__(self):
        pass

    def calculate_integrate(self):
        return None


class Tree (Node):
    def __init__(self, left, right):
        Node.__init__(self)
        self.left = left
        self.right = right

    def calculate_integrate(self):
        return self.left.calculateIntegrate() + self.right.calculateIntegrate()


class Poligon (Node):
    def __init__(self, monomials, low_limit, high_limit):
        Node.__init__(self)
        self.monomials = monomials
        self.low_limit = low_limit
        self.high_limit = high_limit

    def __repr__(self):
        b = ""
        for monomial_idx in range(len(self.monomials)):
            b += str(self.monomials[monomial_idx].coefficient)
            if monomial_idx != len(self.monomials) - 1:
                b += "x^" + str(self.monomials[monomial_idx].degree) + " + "

        return b

    def calculate_integrate(self):
        aggregator = 0
        for monomial in self.monomials:
            aggregator = aggregator +  \
                         monomial.getIntegralPartAt(self.high_limit) - monomial.getIntegralPartAt(self.low_limit)

        return aggregator


class Monomial:

    def __init__(self, coefficient, degree):
        self.coefficient = coefficient
        self.degree = degree

    def get_integral_part_at(self, border):
        return ((border + 0.0) ** (self.degree + 1.0)) * (self.coefficient + 0.0) / (self.degree + 1.0)
