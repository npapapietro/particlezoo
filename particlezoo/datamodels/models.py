from sympy import Symbol, Basic, sympify
from typing import Dict, NamedTuple

from ..exceptions import ModelError
from .structs import Representation


class GenericField:
    """A base field class that holds information information
    about the class after being parsed.
    """
    @property
    def name(self) -> Symbol:
        """Name of the field"""
        return self._name

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
    def description(self) -> str:
        """Returns the description of the field"""
        return self._description or ""

    @property
    def representations(self) -> Dict[str, Representation]:
        """Returns the representations of the field.
        The keys correspond to the gauge field names 
        and the values are dictionary of the charge 
        and representation"""
        return self._representations

    def __init__(
        self,
        name: str,
        spin: str,
        representations: Dict[str, Representation],
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
        self._raw_name = name
        self._name = Symbol(self._raw_name)
        self._description = description
        self._mass_dimension = None
        self._particle_class = ""
        self._spin = self._parse_spin(spin)
        self._representations = representations
        self.key = name
        self.no_mass = no_mass

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
