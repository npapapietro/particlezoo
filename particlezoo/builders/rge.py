from .lagrangian import Lagrangian


class RGE:

    def __init__(self, lagrangian: Lagrangian):
        self.lagrangian = lagrangian

    def _gauge_beta_func(self, key: str):
        pass