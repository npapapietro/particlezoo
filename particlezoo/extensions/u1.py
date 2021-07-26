from liesym import Group
from sympy import Symbol, exp, I, simplify
from functools import reduce

class U1(Group):
    """U1 Group. Technically continuous, but represented
    in this module as discrete"""

    def __new__(cls):
        return super().__new__(cls,"U", 1)

    def generators(self) -> list:
        """Infinite circle group generators
        """
        theta = Symbol(r"\theta")
        return [exp(I * theta)]

    def product(self, *args, **kwargs) -> list:
        """Sums up all the charges"""
        return [simplify(reduce(lambda a, b: a*b, args))]

    def sym_product(self, *args, as_tuple=False, **kwargs) -> list:
        """Sums up all the charges, symbolically"""
        gen = self.generators()[0]
        result = self.product(*[gen**x for x in args], **kwargs)

        if as_tuple:
            return [(gen**x, x) for x in result]
        return result