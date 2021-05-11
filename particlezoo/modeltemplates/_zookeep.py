
from typing import List

from ._models import GaugeModel, FieldModel
from ..exceptions import TemplateError

class ZooKeeper:
    @property
    def name(self):
        return self._name

    def __init__(
        self,
        name: str,
        gauges: List[GaugeModel],
        fields: List[FieldModel]
    ):
        self._name = name
        self._gauges = gauges
        self._fields = fields

    def build(self):
        self._validate_gauges_fields()


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
                if isinstance(current,dict):
                    dim_rep = current.get('representation')
                    if dim_rep is None:
                        current['representation'] = g.algebra.lookup_rep(dim_rep)


