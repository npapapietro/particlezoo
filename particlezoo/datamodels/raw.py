from liesym import Group
from typing import Dict, List, NamedTuple, Union
from sympy import Matrix, Basic


class Representation(NamedTuple):
    """The representation of a field under a single Group.

    Members:
        rep (Union[str, list]): Raw representation
        group (str): Name of group
    """
    rep: Union[str, list]
    group: str


class SymmetryGroup(NamedTuple):
    """A symmetry represented by a single group.

    Members:
        description (str): Description of the group
        group (str): Name of group
    """
    description: str
    group: str

class GenericField(NamedTuple):
    """A generic field.

    Members:
        name (str): Name of the field, can be latex string
        spin (str): String spin value
        description (str): Description of the field
        representations (Dict[str, Representation]): Representation of the field. 
        Keys must be in the SymmetryGroup.
    """
    name: str
    spin: str
    description: str
    representations: Dict[str, Representation]

class ConfigurationFile(NamedTuple):
    """Parent object for reading in the configuration file."""
    name: str
    description: str
    symmetries: List[SymmetryGroup]
    fields: List[GenericField]