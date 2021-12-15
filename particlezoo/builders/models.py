from sympy import Symbol, Basic, sympify, Matrix, latex, I, conjugate, symbols
from sympy.physics.quantum import Dagger
from sympy.tensor.tensor import TensorIndexType, TensorIndex, TensorHead
from typing import Dict, Union, Optional
from liesym import Group, LieGroup, E


from ..exceptions import ModelError


class BaseModel(Basic):

    def __new__(cls, name, description=None):
        obj = Basic.__new__(cls, sympify(name))
        obj._description = description or ""
        return obj

    def _repr_latex_(self):
        return self.name._repr_latex_()

    @property
    def name(self) -> Basic:
        """Name, latex enabled string"""
        return self.args[0]

    @property
    def description(self) -> str:
        """Description of this object"""
        return self._description

    def kinetic_term(self, **kwargs) -> Union[str, Basic]:
        """Builds the symbolic expression for this
        terms kinetic energy term.

        Returns:
            Union[str, Basic]: If as_latex will return latex expression
            otherwise it will be a tensor expression.
        """
        pass


class Representation:
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


class Symmetry(BaseModel):

    def __new__(cls,
                name,
                group,
                gauged,
                coupling,
                description=None,
                tag=None):
        obj = super().__new__(cls, Symbol(name), description)
        obj._group = group
        obj._gauged = gauged
        obj._coupling = coupling
        obj._tag = tag
        return obj

    def __init__(self,
                 name: str,
                 group: Group,
                 gauged: bool,
                 coupling: str,
                 description: str = None,
                 tag: str = None
                 ):
        """Creates a symmetry used in the lagrangian.

        Args:
            name (str): Name of the symmetry
            group (Group): The liesym.Group that dictates the symmetry.
            gauged (bool): If this is a gauged symmetry (as opposed to global).
            coupling (str): A coupling coefficient for the symmetry.
            description (str, optional): Description of the symmetry. Defaults to None.
            tag (str, optional): Optional tag for the model, used in latex repr. Defaults to None.
        """

    @property
    def group(self) -> Group:
        """An instance of the group"""
        return self._group

    @property
    def is_gauged(self) -> bool:
        """Returns whether this symmetry is local (gauged) or global."""
        return self._gauged

    @property
    def coupling(self) -> str:
        """The gauge coupling"""
        return self._coupling

    @property
    def is_abelian(self) -> bool:
        # For now this filter works
        return not (isinstance(self.group, LieGroup) and self.group.dimension > 1)

    @property
    def tag(self) -> Optional[str]:
        """The short tag name on the symmetry. `SU(2)_L` would
        have a tag name of `L` Will prioritize tag in equation
        building over name.
        """
        return self._tag

    @property
    def gauge_name(self):
        """Gauge boson name."""
        n = f"A_{self.tag or self.name}"
        if isinstance(self.group, (LieGroup, E)):
            n += "^a"
        return n

    @property
    def gaugino_name(self):
        raise NotImplementedError("Coming Soon?")

    def _kinetic_term(self):
        """Returns tuple of factor, contra and covariant terms"""

        Lorentz = TensorIndexType("Lorentz", dummy_name="L", dim=4)
        mu = TensorIndex("mu", Lorentz)
        nu = TensorIndex("nu", Lorentz)
        A = TensorHead(self.gauge_name, [Lorentz, Lorentz])
        contravariant = A(mu, nu)
        covariant = A(-mu, -nu)
        factor = sympify("-1/4")
        return factor, contravariant, covariant

    def kinetic_term(self, as_latex=True, **kwargs) -> Union[str, Basic]:
        """Returns the kinetic term for the gauge symmetry.

        Args:
            as_latex (bool, Optional): Flag to return as latex string.

        Returns:
            Union[str, Basic]: Latex string or tensor expr
        """
        if not self.is_gauged:
            return None
        fac, contra, co = self._kinetic_term()

        if as_latex:
            fac_tex = latex(fac)
            contra_tex = latex(contra)
            co_tex = latex(co)

            return fac_tex + contra_tex + co_tex
        return fac * contra * co

    def __hash__(self):
        return self.name.__hash__()

    def __eq__(self, other):
        if isinstance(other, Symmetry):
            return self.__hash__() == other.__hash__()
        if isinstance(other, str):
            return str(self.name) == other
        return False


class Field(BaseModel):
    """A base field class that holds information information
    about the class after being parsed.
    """

    def __new__(cls,
                name: str,
                spin: str,
                representations: Dict[str, Representation],
                description=None,
                no_mass=True):
        """Creates a Generic field.

        Args:
            name (str): Name of field. Latex enabled string.
            spin (str): Spin of the field
            representations (Dict[str, Representation]): Dict of fields representations.
            description (str, optional): Optional description of field. Defaults to None.
            no_mass (bool, optional): Flag if field has mass. Defaults to True.

        Examples
        ========
        >>> import particlezoo as zoo
        >>> f = zoo.Field("psi", "1/2", {"U1_x": "q"})
        """
        obj = super().__new__(cls, Symbol(name), description)
        obj._representations = representations
        obj._particle_class = ""
        obj._mass_dimension = None
        obj._spin = Field._parse_spin(obj, spin)
        obj.no_mass = no_mass
        obj._raw_name = name
        return obj

    def __init__(cls,
                 name: str,
                 spin: str,
                 representations: Dict[str, Representation],
                 description=None,
                 no_mass=True):
        """Creates a Generic field.

        Args:
            name (str): Name of field. Latex enabled string.
            spin (str): Spin of the field
            representations (Dict[str, Representation]): Dict of fields representations.
            description (str, optional): Optional description of field. Defaults to None.
            no_mass (bool, optional): Flag if field has mass. Defaults to True.

        Examples
        ========
        >>> import particlezoo as zoo
        >>> f = zoo.Field("psi", "1/2", {"U1_x": "q"})
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
    def representations(self) -> Dict[str, Representation]:
        """Returns the representations of the field.
        The keys correspond to the gauge field names 
        and the values are dictionary of the charge 
        and representation"""
        return self._representations

    @staticmethod
    def _parse_spin(self, spin: str) -> Basic:
        """Ensures spin is integer or half integer"""
        spin_: Basic = sympify(spin)
        if spin_.is_integer and spin_ >= 0:
            self._mass_dimension = sympify("1")
            self._particle_class = "boson"
            return spin_
        if (2 * spin_).is_integer:
            self._mass_dimension = sympify("3/2")
            self._particle_class = "fermion"
            return spin_
        if spin_ == 0:
            self._mass_dimension = sympify("0")
            self._particle_class = "boson"
            return spin_
        raise ModelError("Unrecognized Spin")

    def kinetic_term(self, as_latex=True, compact=True, **kwargs) -> Union[str, Basic]:
        """Returns the kinetic term for the field symmetry.

        Args:
            as_latex (bool, optional): Return as latex string. Defaults to False.
            compact (bool, optional): Returns any covariant derivative term as `D_mu`. Defaults to False.

        Returns:
            Union[str, Basic]: Returns a str or tensor expr
        """
        deriv_co = symbols("\partial_mu")
        deriv_contra = symbols("\partial^mu")
        if compact:
            deriv_co = symbols("D_mu")
            deriv_contra = symbols("D^mu")

        if self.is_boson:
            terms = Dagger(deriv_co*self.name), deriv_contra, self.name
            return "".join([latex(x) for x in terms])
        else:
            terms = I, conjugate(self.name),  deriv_co, symbols(  # type:ignore
                "\gamma^mu"), self.name
            return "".join([latex(x) for x in terms])
        # return ""

    def _kinetic_term(self, mode='symbol', **kwargs) -> Union[str, Basic]:
        if mode not in ['symbol', 'latex', 'diagram', 'diagram-compile']:
            raise ValueError(
                "mode must be one of 'symbol', 'latex', 'diagram', 'diagram-compile'")

        if mode == 'symbol':
            return self._kinetic_symbol()
        return ""

    def _kinetic_symbol(self):
        if self.is_boson:
            return self._ke_symbol_boson()
        return self._key_symbol_fermion()

    def _ke_symbol_boson(self):
        du = symbols("\partial_mu")
        duu = symbols("\partial^mu")
        field = self.name
        return conjugate(du * field), duu, field

    def _key_symbol_fermion(self):
        deriv_co = symbols("\partial_mu")
        return I,  conjugate(self.name),  deriv_co, symbols(
            "\gamma^mu"), self.name

    @property
    def conjugate_name(self):
        if self.is_boson:
            name = str(self.name)
            return Symbol(f"{name}^\dagger")
        else:
            return conjugate(self.name)

    def __hash__(self):
        return self.name.__hash__()

    def __eq__(self, other):
        if isinstance(other, Field):
            return self.__hash__() == other.__hash__()
        return False
