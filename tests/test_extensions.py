from particlezoo.extensions import U1
from sympy import sympify


def test_u1():
    u1 = U1()

    p = [sympify("-1"), sympify("1/2"), sympify("1/2")]
    result = u1.sym_product(*p)
    assert result[0] == 1