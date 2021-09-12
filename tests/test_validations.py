from sympy import Matrix
import liesym as ls

import particlezoo.validations.gauge_invariance as tp
from particlezoo import Field, Representation


def test_is_gauge_invariant_repr():
    q = Matrix([[1, 0]])
    G = Matrix([[1, 1]])
    qb = Matrix([[0, 1]])

    terms = (q, G, qb)
    group = ls.SU(3)
    assert tp.is_gauge_invariant_repr(terms, group)

    q = Matrix([[1, 0]])
    G = Matrix([[1, 0]])
    qb = Matrix([[0, 1]])

    terms = (q, G, qb)
    group = ls.SU(3)
    assert not tp.is_gauge_invariant_repr(terms, group)


def test_is_gauge_invariant():

    quark = Field(
        "quark",
        "1/2",
        {
            "QCD": Representation(Matrix([[1, 0]]), ls.SU(3)),
            "WEAK": Representation(Matrix([[1]]), ls.SU(2)),
            "Z2": Representation("Z_0", ls.Z(2)),
        }
    )

    quark_bar = Field(
        "quark_bar",
        "1/2",
        {
            "QCD": Representation(Matrix([[0, 1]]), ls.SU(3)),
            "WEAK": Representation(Matrix([[1]]), ls.SU(2)),
            "Z2": Representation("Z_1", ls.Z(2)),
        }
    )

    gluon = Field(
        "gluon",
        "1",
        {
            "QCD": Representation(Matrix([[1, 1]]), ls.SU(3)),
            "Z2": Representation("Z_1", ls.Z(2)),
        }
    )

    assert tp.is_gauge_invariant((quark, gluon, quark_bar)) == (True, "")

    assert tp.is_gauge_invariant((quark, gluon)) == (False, "QCD")
