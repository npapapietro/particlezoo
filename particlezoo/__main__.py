from . import *

if __name__ == "__main__":
    import liesym as ls
    from sympy import Matrix
    import logging

    q = Matrix([[1,0]])
    G = Matrix([[1,1]])
    qb = Matrix([[0,1]])

    terms = (q, G, qb)
    group = ls.A(2)
    print(is_gauge_invariant_repr(terms, group, name="test"))
    
