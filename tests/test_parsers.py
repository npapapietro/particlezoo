from particlezoo.parsers import group_lookup
from particlezoo.extensions import U1

from liesym import SU

def test_group_lookup():
    name = "SU_3"

    grp = group_lookup(name)

    assert grp == SU(3)

    name2 = "U_1"
    grp2 = group_lookup(name2)
    assert grp2 == U1()
