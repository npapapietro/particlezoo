from liesym import SU, SO, Sp, Z, E, Group

from particlezoo.extensions import U1

def group_lookup(name: str) -> Group:
    """Parses string and returns instance of
    group with proper dimension.

    Args:
        name (str): String name of from {GroupName}_{dimension}

    Returns:
        Group: Instance of group
    """
    grp, dim = name.lower().split("_")
    dim_ = int(dim)

    if grp == "su":
        return SU(dim_)
    if grp == "so":
        return SO(dim_)
    if grp == "sp":
        return Sp(dim_)
    if grp == "e":
        return E(dim_)
    if grp == "z":
        return Z(dim_)
    if grp == "u" and dim_ == 1:
        return U1()