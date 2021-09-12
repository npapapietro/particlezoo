from __future__ import annotations
from particlezoo.builders.lagrangian import Lagrangian

from sympy import sympify, Matrix
from liesym import SU, SO, U1, Sp, Z, E, Group, LieGroup
from typing import Dict, Union

from ..builders import (SymmetryGroup, Symmetry,
                        Representation, GenericField,
                        Field, Configuration)
from ..exceptions import ConfigError, ModelError


def group_lookup(name: list[str]) -> Group:
    """Parses string and returns instance of
    group with proper dimension.

    Args:
        name (list[str]): List of [group type, dim]

    Raises:
        ConfigError: If unsupported group (eg [U, 5]) is passed.

    Returns:
        Group: Instance of group
    """
    [grp, dim] = name

    dim_ = int(dim)
    grp = grp.lower()
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

    raise ConfigError(
        "Unsupported group. Please log an issue to request support.")


def transform_symmetry(model: SymmetryGroup) -> Symmetry:
    """Parses and transforms from raw input model to class model.
    If `gauged` flag isn't passed in the config, will auto set based
    on group type of `LieGroup`, `U1` or `E`.
    """
    description = model.description or ""
    group = group_lookup(model.group)
    gauged = model.gauged

    return Symmetry(
        name=model.name,
        group=group,
        description=description,
        coupling=model.coupling,
        tag=model.tag,
        gauged=isinstance(group, (LieGroup, U1, E)
                          ) if gauged is None else gauged
    )


def _lg_lookup(group: LieGroup, v: Union[str, list]) -> Matrix:

    if isinstance(v, str):
        try:
            return group.algebra.irrep_lookup(v)
        except KeyError:
            raise ModelError(f"No representation, {v}, in {group.group}")
    elif isinstance(group, list):
        representation = Matrix([v])
        if representation.shape != 1:
            representation = representation.transpose()
        return representation
    else:  # should not be hit unless called directly
        raise ConfigError("Representation must be a string or list")


def transform_field(model: GenericField, lookups: Dict[str, Symmetry]) -> Field:

    field_reps = {}
    for k, v in model.representations.items():
        group = lookups.get(k)
        if group is None:
            raise ConfigError(f"The symmetry {k} is undefined.")

        # reps can either be matrix or str
        if isinstance(group, LieGroup):
            representation = Representation(_lg_lookup(group, v), group)
        else:
            representation = Representation(sympify(v), group)

        field_reps[k] = representation

    return Field(
        name=model.name,
        spin=model.spin,
        representations=field_reps,
        description=model.description,
        no_mass=False
    )


def transform_model(cfg: Configuration) -> Lagrangian:
    version = cfg.version
    name = cfg.name
    description = cfg.description

    symmetries = [transform_symmetry(x) for x in cfg.symmetries]
    lookups = {x.name: x for x in symmetries}

    fields = [transform_field(x, lookups) for x in cfg.fields]

    return Lagrangian(
        fields,
        symmetries,
        name, version, description
    )
