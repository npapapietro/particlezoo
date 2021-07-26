from typing import Dict, List, NamedTuple, Union, Optional


class SymmetryGroup(NamedTuple):
    """A symmetry represented by a single group.

    Members:
        description (Optional[str]): Description of the group
        name (str): Unique name for group. Can be latex string.
        group (str): Mathematical group

    """
    description: Optional[str]
    name: str
    group: str

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