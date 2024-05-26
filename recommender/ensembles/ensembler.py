import numpy as np


class Ensembler:
    @staticmethod
    def basic(probs: np.ndarray) -> float:
        return probs.prod()

    @staticmethod
    def weighted_sum(probs: np.ndarray, weights: np.ndarray) -> float:
        if probs.shape != weights.shape:
            raise ValueError("Shape of probs and weights must be the same")

        return sum(probs * weights)
