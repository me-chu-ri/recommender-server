import numpy as np


class Ensembler:
    @staticmethod
    def basic(probs: np.ndarray) -> float:
        return probs.prod()

    @staticmethod
    def basic_lists(probs: np.ndarray) -> np.ndarray:
        return probs.prod(axis=0)  # product rows

    @staticmethod
    def weighted_sum(probs: np.ndarray, weights: np.ndarray) -> np.ndarray:
        if weights.shape != (probs.shape[0], 1):
            raise ValueError("Shape of weights should be (probs.shape[0], 1)")

        return sum(probs * weights)
