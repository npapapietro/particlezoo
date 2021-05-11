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

    def lookup_rep(self, rep_dim: str) -> Matrix:
        """Performs as lookup from the common dimensional 
        names for representations to the dynkin indexed vector.
        """
        return None


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
        self._spin = sympify(spin)
        self._mass = self._parse_mass(mass)
        print(representations)
        self._representations = self._parse_representations(representations)

    def _parse_mass(self, mass):
        if mass is None:
            mass_name = "m_{" + self._raw_name + "}"
            return NumericSymbol(mass_name, 0, 0)
        return NumericSymbol.from_input(mass)

    def _parse_representations(self, reps: List[Dict]):
        
        try:
            # validate unique group names
            if len(set([x['name'] for x in reps])) != len(reps):
                raise TemplateError(
                    f"Duplicate representation in {self._raw_name}")

            representations = {}
            for rep in reps:  
                rep_new = {**rep}             
                name = rep_new.pop('name')
                r = rep_new.get("representation")                
                if r is not None:
                    rep_new['representation'] = Matrix([r])
                representations[name] = rep_new
            return representations

        except KeyError as e:
            raise TemplateError(
                "Representations keys are 'name', 'charge' and 'representations' (optional)")
