import numpy as np
from abc import ABC, abstractmethod


class Norm(ABC):
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    @abstractmethod
    def execute(self, p1: np.ndarray, p2: np.ndarray) -> float:
        raise NotImplementedError


class L2Norm(Norm):
    def __init__(self):
        super().__init__('l2norm')

    def execute(self, p1: np.ndarray, p2: np.ndarray) -> float:
        return np.linalg.norm(p1 - p2)


class L1Norm(Norm):
    def __init__(self):
        super().__init__('l1norm')

    def execute(self, p1: np.ndarray, p2: np.ndarray) -> float:
        return np.linalg.norm(p1 - p2, ord=1)
