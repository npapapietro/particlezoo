from __future__ import annotations

from typing import NamedTuple

from ..builders import Field

class Node(NamedTuple):
    key: str


class Diagram(NamedTuple):
    n_points: int
    in_fields: list[Field]
    out_fields: list[Field]