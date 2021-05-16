from sympy import Matrix
from typing import List

from ._models import GaugeModel, FieldModel
from ..exceptions import TemplateError


class ZooKeeper:
    @property
    def name(self):
        return self._name
    
    @property
    def fields(self) -> List[FieldModel]:
        return self._fields

    @property
    def gauges(self) -> List[FieldModel]:
        return self._gauges

    def __init__(
        self,
        name: str,
        gauges: List[GaugeModel],
        fields: List[FieldModel]
    ):
        self._name = name
        self._gauges = gauges
        self._fields = fields
        self._is_valid = False


    def build(self):
        self._validate_gauges_fields()
        self._validate_field_reps()
        return self


    def _validate_gauges_fields(self):
        fields = self._fields
        gauges = self._gauges

        g_keys = [g.key for g in gauges]

        for f in fields:
            reps = f.representations.keys()
            for r in reps:
                if r not in g_keys:
                    raise TemplateError(f"All representations must be defined in gauges. Field: {f.name}")

    def _validate_field_reps(self):
        fields = self._fields
        gauges = self._gauges
        
        for g in gauges:
            for f in fields:
                current = f.representations.get(g.key)
                if not isinstance(current,dict):
                    f._raise_rep_error()

                matrix_rep = current.get('representation')
                dim_rep = current.get("charge")
                
                # lookup algebra repr from backend
                if matrix_rep is None:
                    try:
                        current['representation'] = g.algebra.lookup_rep(dim_rep)
                    except KeyError:
                        raise TemplateError(f"Cannot find representation for {dim_rep}")
                # ensure algebra repr is type of Matrix
                # use charge for dimension
                else:
                    matrix_rep = Matrix([matrix_rep])
                    current['representation'] = matrix_rep
                    current['charge'] = g.algebra.backend.dim_name(matrix_rep)
            



