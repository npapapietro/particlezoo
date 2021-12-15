from __future__ import annotations

from typing import NamedTuple

from ..builders import Field


class Node(NamedTuple):
    key: str


class Diagram:
    def __init__(
            self, 
            n_points: int, 
            in_fields: list[Field],
            out_fields: list[Field]):
        self.n_points = n_points
        self.in_fields = in_fields
        self.out_fields = out_fields
        self.n_in = len(in_fields)
        self.n_out = len(out_fields)

    def generate(self):
        if self.n_in == self.n_out and self.n_out == 1:
            if self.in_fields[0] == self.out_fields[0]:
                self._wave_function()
            else:
                self._wave_function_mixing()

    def _wave_function(self):
        pass

    def _wave_function_mixing(self):
        raise NotImplementedError("Wave function mixing not yet implemented")