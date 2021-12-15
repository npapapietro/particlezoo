from __future__ import annotations

from particlezoo.builders.models import Symmetry
from typing import Union
from sympy.printing.latex import latex
from tikzfeynwrap import TikzFeynWrap
import string

from ..builders import Symmetry, Field



class FeynmanDiagram:
    def __init__(self, **kwargs):
        self.allowed = [
            "charged scalar",
            "scalar",
            "majorana",
            "anti majorana",
            "gluon",
            "photon",
            "ghost",
            "charged boson"
        ]
        self.wrapper = TikzFeynWrap(**kwargs).startup()

    
    def __call__(self, ins: list, outs: list, horizontal: tuple):
        # p_ins = self._parse_ints(ins)
        pass

    def _construct(self, items):
        n = len(items)
        if n < 3:
            return
        a, b ,c = items
        


    def _create_line(self, line_type=None):
        if line_type:
            if line_type in self.allowed:
                return f"-- [{line_type}]"
            else:
                raise ValueError("Bad tikz-feynman option")
        return "--"
        

    def _create_vertex(self, key, name=None):
        if name:
            return f"{key} [particle=\({name}\)]"
        return key

    # def _parse_ints(self, ins):
    #     h1 = None
    #     fields = []
    #     for i, a in enumerate(ins):
    #         l = string.ascii_lowercase[i]
    #         if i == 0:
    #             h1 = l
    #         if isinstance(a, str):
    #             fields.append(f"{l} [particle={{\({a}\)}}]")
    #         elif isinstance(a, (tuple, list)):
    #             n,t = a
    #             fields.append(f"[{t}] {l} [particle={{\({n}\)}}]")
    #         else:
    #             raise TypeError("Expected list[str | tuple | list]")

    #     return 


def boson_kinetic_energy(field: Field, symmetry: Symmetry) -> tuple:
    pass

def fermion_kinetic_energy(field: Field, symmetry: Symmetry) -> tuple:
    pass

def wave_function_tree(
    field: Union[Field, Symmetry],
    override_line=None
    ):

    if override_line:
        allowed = [
            "charged scalar",
            "scalar",
            "majorana",
            "anti majorana",
            "gluon",
            "photon",
            "ghost",
            "charged boson"
        ]
        if override_line not in allowed:
            raise ValueError("overrideline must be in" + ",\n".join(allowed))
    
    line_type = None
    edge_label = None


    # if isinstance(field, Field):
    #     name = latex(field.name, mode='plain')
    #     if field.is_boson:
    #         tex += f"a -- [charged scalar, edge label=\({name}\)] b"
    #     else:
    #         tex += f"a -- [fermion, edge label=\({name}\)] b"
    # elif isinstance(field, Symmetry):
    #     if not field.is_gauged:
    #         return ""
    #     name = latex(field.gauge_name, mode='plain')
    #     tex += f"a -- [charged scalar, edge label=\({name}\)] b"
        
    # tex = "\\feynmandiagram[horizontal=a to b]{"


    # tex += "};"

def _id_gen():
    i = -1
    def _get_id():
        nonlocal i
        i += 1
        return "a" + str(i)
    return _get_id