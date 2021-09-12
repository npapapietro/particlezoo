from typing import Iterable, List, Set, Tuple, Union
from liesym import Group, LieGroup
from sympy import Matrix, Symbol
import logging

from ..builders import Field
from ..exceptions import ConfigError


def is_gauge_invariant_repr(terms: Iterable[Union[Matrix, Symbol, str]], group: Group) -> bool:
    """Checks whether terms are guage invariant under chosen gauge group representation.

    Args:
        terms (Iterable[Union[Matrix, Symbol, str]]): Tuple or List of representations. If all are Symbol or str, will use symbolic product
        group (Group): Selected gauge group

    Returns:
        bool: Returns true if terms are guage invariant


    Examples
    ========
    >>> from liesym import SU
    >>> from particlezoo.validations import is_gauge_invariant_repr
    >>> quark = Matrix([[1,0]])
    >>> gluon = Matrix([[1,1]])
    >>> quark_bar = Matrix([[0,1]])
    >>> gauge_group = SU(3)
    >>> is_gauge_invariant_repr((quark_bar, gluon, quark), gauge_group)
    True
    """
    if not isinstance(terms, (list, tuple)):
        raise TypeError(f"terms must be a iterable")

    if all(isinstance(term, str) or isinstance(term, Symbol) for term in terms):
        results = group.sym_product(*terms, as_tuple=True)
    elif all(isinstance(term, Matrix) for term in terms):
        results = group.product(*terms)
    else:
        raise TypeError(f"terms must be a iterable of type {type(Field)}")

    if isinstance(group, LieGroup):
        # If is a lie group, exploit underlying algebra
        return any([group.algebra.dim(x) == 1 for x in results])

    # discrete groups should return scalar list of tuples
    return any([x[1] == 1 for x in results])


def is_gauge_invariant(terms: Iterable[Field], **kwargs) -> Tuple[bool, str]:
    """Checks a group of FieldModels for gauge invariance.

    Args:
        terms (Iterable[FieldModel]): Group of interacting FieldModels

    Raises:
        ConfigError: Error with configuring FieldModel

    Returns:
        Tuple[bool, str]: Returns flag and name of failing gauge group or empty string.
    """
    if not isinstance(terms, list):
        terms = list(terms)

    unique_gauge_groups: Set[str] = set([
        k
        for field in terms
        for k in field.representations.keys()
    ])

    name = kwargs.get("name", "Interaction")
    n_terms = len(terms)
    n_gauges = len(unique_gauge_groups)
    logging.debug(
        f"Validating (Gauges): {name} with {n_terms} terms and {n_gauges} gauges")

    for gauge in sorted(unique_gauge_groups):  # ensure alphabetical
        reps: List[Matrix] = []
        group: List[Group] = []
        for field in terms:
            if (obj := field.representations.get(gauge)):
                reps.append(obj.rep)
                group.append(obj.group)

        if len(set(group)) != 1:
            raise ConfigError(
                "FieldModel.representations matching keys should have matching group")

        gauge_group = group[0]
        if not (is_invar := is_gauge_invariant_repr(reps, gauge_group)):
            return is_invar, gauge

    return True, ""
