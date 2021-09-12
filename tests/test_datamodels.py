import particlezoo as zoo
from liesym import Z


def test_symmetry_formatting():
    z2 = zoo.Symmetry(
        "Z2",
        Z(2),
        False,
        "Test Z2"
    )

    z2_fmt = z2.kinetic_term()

    assert z2_fmt is None
