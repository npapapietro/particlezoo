import json
import yaml
import os
from liesym import LieAlgebra, A, B, C, D
from typing import Union, List

from ..exceptions import TemplateError
from ._models import NumericSymbol, GaugeModel, FieldModel
from ._zookeep import ZooKeeper


def _parse_algebra(algebra: Union[str, list]) -> Union[LieAlgebra, None]:
    """Parses algebra and returns none if its abelian or LieAlgebraBackend if
    supported in the liesym module"""
    if isinstance(algebra, str):
        if algebra == "abelian":
            return None
        raise TemplateError("group_type str must be equal to 'abelian'")
    if isinstance(algebra, list):
        if len(algebra) != 2:
            raise TemplateError(
                "group_type list must be in form '[group, dim]'")

        [grp, dim] = algebra

        try:
            dim = int(dim)
            assert dim > 0
        except Exception:
            raise TemplateError("group_type dim must be nonzero numeric")

        if grp.lower() == "su":
            return A(dim-1)
        if grp.lower() == "so":
            if dim % 2 == 0:
                return D(dim // 2)
            return B((dim - 1) // 2)
        if grp.lower() == "sp":
            return C(dim)
        else:
            raise TemplateError("group_type only supports 'SU', 'SO', or 'Sp'")

    raise TemplateError("group_type must be str or list")


class TemplateParser:
    def __init__(self, fpath: str):
        self.template = self._load(fpath)

    def _load(self, fpath: str) -> dict:
        _, ext = os.path.splitext(fpath)
        if ext not in [".json", ".yaml"]:
            raise NotImplementedError("File type not supported")
        with open(fpath) as f:
            if ext == ".json":
                return json.load(f)
            return yaml.load(f)

    def parse(self) -> ZooKeeper:
        name = self.parse_name(self.template)
        gauges = self.parse_gauges(self.template)
        fields = self.parse_fields(self.template)

        return ZooKeeper(
            name,
            gauges,
            fields
        )

    @staticmethod
    def parse_name(template: dict) -> str:
        try:
            return template["name"]
        except KeyError:
            raise TemplateError("Missing template name")

    @staticmethod
    def parse_gauges(template: dict) -> List[GaugeModel]:

        gauges = template.get("gauges", [])

        if len(gauges) == 0:
            # gauge free model? should we support it?
            raise TemplateError("No gauges defined")
        if len(set([x['name'] for x in gauges])) != len(gauges):
            raise TemplateError("Each gauge group name must be unique")

        return [TemplateParser._parse_gauge(x) for x in gauges]

    @staticmethod
    def parse_fields(template: dict) -> List[FieldModel]:
        fields = template.get("fields", [])
        if len(fields) == 0:
            raise TemplateError("No fields defined")
        if len(set([x['name'] for x in fields])) != len(fields):
            raise TemplateError("Each fields name must be unique")

        return [FieldModel(**x) for x in fields]

    @staticmethod
    def _parse_gauge(gauge: dict) -> GaugeModel:
        name = gauge.get("name")
        group_type = gauge.get("group_type")
        coupling = gauge.get("coupling")

        if any([x is None for x in [name, group_type, coupling]]):
            raise TemplateError(
                "Each gauge group must have a 'name', 'group_type' and 'coupling'")

        return GaugeModel(
            name,
            _parse_algebra(group_type),
            NumericSymbol.from_input(coupling),
            description=gauge.get("description")
        )
