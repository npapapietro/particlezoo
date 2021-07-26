from sympy import sympify, Matrix
from liesym import SU, SO, Sp, Z, E, Group, LieGroup
from typing import Dict, Union

from ..datamodels import (SymmetryGroup, SymmetryModel,
                          RepresentationModel, GenericField,
                          FieldModel)
from ..extensions import U1
from ..exceptions import ConfigError, ModelError


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


def transform_symmetry(model: SymmetryGroup) -> SymmetryModel:
    """Parses and transforms from raw input model to class model."""
    name = sympify(model.name)
    description = model.description or ""
    group = group_lookup(model.group)
    if group is None:
        raise ModelError(f"{model.group} is unsupported")

    return SymmetryModel(
        name=name,
        group=group,
        description=description
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
    else: # should not be hit unless called directly
        raise ConfigError("Representation must be a string or list")

def transform_field(model: GenericField, lookups: Dict[str, SymmetryModel]) -> FieldModel:
    
    field_reps = {}
    for k, v in model.representations.items():
        group = lookups.get(k)
        if group is None:
            raise ConfigError(f"The symmetry {k} is undefined.")

        # reps can either be matrix or str
        if isinstance(group, LieGroup):
            representation = RepresentationModel(_lg_lookup(group, v), group)
        else:
            representation = RepresentationModel(sympify(v), group)

        field_reps[k] = representation
    
    return FieldModel(
        name=model.name,
        spin=model.spin,
        representations=field_reps,
        description=model.description,
        no_mass=False
    )

        
