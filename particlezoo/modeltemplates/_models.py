from liesym import LieAlgebra
from sympy import Symbol, Basic, sympify, Matrix
from typing import Union, Dict, List

from ..exceptions import TemplateError


class Algebra:
    def __init__(self, algebra: Union[LieAlgebra, None]):
        self._backend = algebra

    def repr_product(self, *reps):
        if self._backend is None:
            return self._phase_product(*reps)
        else:
            return self._backend.tensor_product_decomposition(reps)

    def _phase_product(self, *reps):
        return sum(reps)

    @property
    def backend(self):
        return self._backend

    def lookup_rep(self, symbol: str) -> Union[Matrix, Basic]:
        """Looks up the irrep based on a latex symbol. If this algebra is 
        U1, then the result is a scalar.

        Args:
            symbol (str): Latex formatted symbol of the irrep

        Returns:
            Matrix: Irrep in the dynkin indexed group representation.
        """
        if self._backend is None:
            return sympify(symbol)
        return self._backend.irrep_lookup(Symbol(symbol))


class NumericSymbol:
    """Class that holds numeric and symbolic objects. For variables,
    each variable has a value defined at a reference point.
    If the object is pure symbolic, only the name is required.
    """
    @property
    def name(self) -> Symbol:
        """Return the sympy version of the name"""
        return self._name

    @property
    def value(self) -> Basic:
        """Return numeric value, if supplied for the symbol"""
        return self._value

    @property
    def ref_value(self) -> Basic:
        """Return reference value, if supplied for the symbol. This
        is the number where self.value is defined at."""
        return self._reference_value

    def __init__(self, name, value=None, reference_value=None):
        self._name = Symbol(name)
        self._value = sympify(value)
        self._reference_value = sympify(reference_value)

    @classmethod
    def from_input(cls, arg):
        if isinstance(arg, str):
            return cls(name=arg)
        elif isinstance(arg, dict):
            return cls(**arg)


class GaugeModel:
    """The GaugeModel wraps the algebra with metadata about the gauge group.
    """
    @property
    def name(self) -> Basic:
        """Returns the formatted name of the gauge group."""
        return self._name

    @property
    def coupling_name(self) -> str:
        """Returns the formatted name of the gauge coupling"""
        return self._coupling.name

    @property
    def description(self) -> str:
        """Returns the description (optional)"""
        return self._description or ""

    @property
    def algebra(self) -> Algebra:
        """Returns the algebra"""
        return self._group_type

    def __init__(
        self,
        name: str,
        group_type: Union[str, list],
        coupling: NumericSymbol,
        description=None
    ):
        self._name = Symbol(name)
        self._description = description
        self._group_type = Algebra(group_type)
        self._coupling = coupling
        self.key = name

    def __repr__(self) -> str:
        return f"<Gauge name='{self.name}'>"


class FieldModel:

    @property
    def name(self) -> Symbol:
        """Name of the field"""
        return self._name

    @property
    def spin(self) -> Basic:
        """Returns the spin of the field"""
        return self._spin

    @property
    def description(self) -> str:
        """Returns the description of the field"""
        return self._description or ""

    @property
    def representations(self) -> Dict[str, dict]:
        """Returns the representations of the field.
        The keys correspond to the gauge field names 
        and the values are dictionary of the charge 
        and representation"""
        return self._representations

    def set_representation(self, gauge, rep):
        self._representations[gauge].update({"representation", rep})

    @classmethod
    def from_kwargs(cls, **kwargs):
        """Constructor from kwargs, validates required fields"""
        name = kwargs.get("name")
        spin = kwargs.get("spin")
        if name is None or spin is None:
            raise TemplateError("Field must have a name and spin")

        representations = kwargs.get("representations", [])
        mass = kwargs.get("mass")
        description = kwargs.get("description")

        return cls(
            name=name,
            spin=spin,
            representations=representations,
            mass=mass,
            description=description
        )

    def __init__(
        self,
        name: str,
        spin: str,
        representations: List[Dict],
        mass=None,
        description=None
    ):
        self._raw_name = name
        self._name = Symbol(self._raw_name)
        self._description = description
        self._spin = self._parse_spin(spin)
        self._mass = self._parse_mass(mass)
        self._representations = self._parse_representations(representations)

    def _parse_mass(self, mass):
        if mass is None:
            mass_name = "m_{" + self._raw_name + "}"
            return NumericSymbol(mass_name, 0, 0)
        return NumericSymbol.from_input(mass)

    def _parse_spin(self, spin: str) -> Basic:
        """Ensures spin is integer or half integer"""
        spin = sympify(spin)
        if spin.is_integer and spin >= 0:
            return spin
        if (2 * spin).is_integer:
            return spin

        raise TemplateError("Spin is not integer or half integer")

    def _parse_representations(self, reps: List[Dict]):

        representations = {}
        for rep in reps:
            if 'name' not in rep or not ('charge' in rep or 'representation' in rep):
                self._raise_rep_error()
            rep_new = {**rep}             
            name = rep_new.pop('name')
            representations[name] = rep_new

        # validate unique group names
        if len(set([x['name'] for x in reps])) != len(reps):
            raise TemplateError(
                f"Duplicate representation in {self._raw_name}")
        return representations

    def _raise_rep_error(self):
        raise TemplateError(
            ("fields.representations list items must be a str,str dict with keys:\n"
             "'name': required, \n"
             "'charge' or 'representation': choose one, required"
             ))

    def __repr__(self) -> str:
        return 