from __future__ import annotations

from .models import Field, Symmetry, BaseModel


class Lagrangian:
    

    def __init__(self,
                 particle_contents: list[Field],
                 symmetries: list[Symmetry],
                 name: str,
                 version: str = None,
                 description: str = None
                 ):
        self._particle_contents = particle_contents
        self._symmetries = symmetries
        self._name = name
        self._version = version
        self._description = description

    def _ke_terms(self, contents: list[BaseModel], **kwargs) -> list[str]:
        ke = []
        for x in contents:
            k = x.kinetic_term(**kwargs)
            if k:
                ke.append(k)
        return ke

    def kinetic_term(self, as_latex=True, **kwargs):
        """Returns the latex string for the complete
        kinetic energy term."""
        ke = self._ke_terms(self._particle_contents, as_latex=as_latex)
        fields = " + ".join(ke) if len(ke) > 1 else ke[0]
        
        ke = self._ke_terms(self._symmetries, as_latex=as_latex)
        gauge = " ".join(ke)

        return fields + " " + gauge

    @property
    def abelian_symmetries(self):
        return [x for x in self._symmetries if x.is_abelian]

    @property
    def nonabelian_symmetries(self):
        return [x for x in self._symmetries if not x.is_abelian]

    def _build_graphs(self, field: Field):
        ke_graphs = self._build_ke_graphs(field)

    def _build_ke_graphs(self, field: Field):

        reps = field.representations
        for k, _ in reps.items(): # use rep soon?
            sym = self._get_sym(k)
            if field.is_boson:
                # self._boson_ke_graph(field, sym)
                pass

    # def _boson_ke_graph

    def _get_sym(self, name: str):
        """Utility lookup for getting symmetry"""
        for i in self._symmetries:
            if i == name:
                return i
        raise ValueError("Cannot find symmetry.")