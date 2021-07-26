from sympy import Symbol, Basic, sympify, Matrix
from typing import Dict, Union
from liesym import Group

from ..exceptions import ModelError
# from .raw import Representation


class _BaseModel:
    @property
    def name(self) -> Basic:
        """Name, latex enabled string"""
        return self._name

    @property
    def description(self) -> str:
        """Description of this object"""
        return self._description

    def __init__(self, name, description):
        self._name = name
        self._description = description or ""


class RepresentationModel:
    @property
    def group(self) -> Group:
        """An instance of the group the representation is under"""
        return self._group

    @property
    def rep(self) -> Union[Matrix, Basic]:
        """The representation under self.group"""
        return self._rep

    def __init__(self, rep, group):
        self._rep = rep
        self._group = group


class SymmetryModel(_BaseModel):

    @property
    def group(self) -> Group:
        """An instance of the group"""
        return self._group

    def __init__(self, name, group, description=None):
        self._group = group
        super().__init__(name, description)


class FieldModel(_BaseModel):
    """A base field class that holds information information
    about the class after being parsed.
    """

    @property
    def spin(self) -> Basic:
        """Returns the spin of the field"""
        return self._spin

    @property
    def mass_dim(self) -> Basic:
        """Returns the mass dim for the field, 
        fermions are 3/2 while bosons are 1"""
        return self._mass_dimension

    @property
    def is_fermion(self) -> bool:
        return self._particle_class == "fermion"

    @property
    def is_boson(self) -> bool:
        return self._particle_class == "boson"

    @property
    def representations(self) -> Dict[str, RepresentationModel]:
        """Returns the representations of the field.
        The keys correspond to the gauge field names 
        and the values are dictionary of the charge 
        and representation"""
        return self._representations

    def __init__(
        self,
        name: str,
        spin: str,
        representations: Dict[str, RepresentationModel],
        description=None,
        no_mass=False
    ):
        """Creates a Generic field.

        Args:
            name (str): Name of field. Latex enabled string.
            spin (str): Spin of the field
            representations (Dict[str, Representation]): Dict of fields representations.
            description (str, optional): Optional description of field. Defaults to None.
            no_mass (bool, optional): Flag if field has mass. Defaults to False.
        """
        super().__init__(Symbol(name), description)
        self._representations = representations
        self._particle_class = ""
        self._mass_dimension = None
        self._spin = self._parse_spin(spin)
        self.no_mass = no_mass
        self._raw_name = name

    def _parse_spin(self, spin: str) -> Basic:
        """Ensures spin is integer or half integer"""
        spin_: Basic = sympify(spin)
        if spin_.is_integer and spin_ >= 0:
            self._mass_dimension = sympify("1")
            self._particle_class = "scalar"
            return spin_
        if (2 * spin_).is_integer:
            self._mass_dimension = sympify("3/2")
            self._particle_class = "fermion"
            return spin_
        if spin_ == 0:
            self._mass_dimension = sympify("0")
            self._particle_class = "scalar"
            return spin_
        raise ModelError("Unrecognized Spin")
