from typing import Iterable, Tuple
import logging
from enum import Enum

from ..builders import Field


class Renormalizability(Enum):
    SuperRenorm = 0
    Renorm = 1
    NonRenorm = 2


def validate_mass_dim(terms: Iterable[Field], **kwargs) -> Renormalizability:
    """Based on the mass dimension of all the fields in the interactions, calculates
    what level of renormalization the interaction

    Args:
        terms (Iterable[GenericField]): Group of interacting GenericFields

    Returns:
        Renormalizability: Level of renormalization
    """
    if isinstance(terms, (list, tuple)):
        raise TypeError(f"terms must be a iterable of type {type(Field)}")

    terms: Iterable[Field] = terms
    name = kwargs.get("name", "Interaction")
    n_terms = len(terms)
    logging.debug(f"Validating (Mass dim): {name} with {n_terms} terms")

    mass_dim = sum([x.mass_dim for x in terms])

    if mass_dim < 4:
        return Renormalizability.SuperRenorm
    if mass_dim == 4:
        return Renormalizability.Renorm
    return Renormalizability.NonRenorm
