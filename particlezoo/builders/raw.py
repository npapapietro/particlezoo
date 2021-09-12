from __future__ import annotations

from typing import Dict, List, NamedTuple, Union, Optional

"""These are the models that appear in the serialized config formats.
"""

class SymmetryGroup(NamedTuple):
    """A symmetry represented by a single group.

    Members:
        description (Optional[str]): Description of the group
        name (str): Unique name for group. Can be latex string.
        group (list[str]): Mathematical group of [type, dim]
        coupling (Optional[str]): Optional coupling if symmetry is gauged.
        gauged (bool): If this is a gauged symmetry (as opposed to a global symmetry)
        tag (Optional[str]): A optional tag. Ex: `U(1)_Y` where tag = `Y`. Supercedes name in equation writing
    """
    description: Optional[str]
    name: str
    group: list[str]
    coupling: Optional[str]
    gauged: bool
    tag: Optional[str]


class GenericField(NamedTuple):
    """A field.

    Members:
        name (str): Name of the field, can be latex string
        spin (str): String spin value
        description (Optional[str]): Description of the field
        representations (Dict[str, Union[str, list]]): Representation of the field. 
        Keys must be in the SymmetryGroup.
    """
    name: str
    spin: str
    description: Optional[str]
    representations: Dict[str, Union[str, list]]


class Configuration(NamedTuple):
    """Parent object for reading in the configuration file.

    Members:
        name (str): Name of the model, can be latex string
        version (Optional[str]): Version of model
        description (Optional[str]): Description of the field
        symmetries (List[SymmetryGroup]): Symmetries of the model
        fields (List[GenericField]): Fields of the model
    """
    name: str
    version: Optional[str]
    description: Optional[str]
    symmetries: List[SymmetryGroup]
    fields: List[GenericField]
