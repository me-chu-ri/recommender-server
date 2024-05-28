import numpy as np


class Normalizers:
    @staticmethod
    def min_max_normalization(vec: np.ndarray) -> np.ndarray:
        """
            X - Min(X) / Max(X) - Min(X)
        """
        return (vec - min(vec)) / (max(vec) - min(vec))

    @staticmethod
    def standardize(vec: np.ndarray) -> np.ndarray:
        """
            X - Mean(X) / Std
        """
        return (vec - np.mean(vec)) / np.std(vec, axis=0)
