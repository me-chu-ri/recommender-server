import numpy as np


class Normalizers:
    @staticmethod
    def min_max_normalization(vec: np.ndarray) -> np.ndarray:
        """
            X - Min(X) / Max(X) - Min(X)
        """
        return Normalizers.min_max_specified_normalization(vec, np.min(vec), np.max(vec))

    @staticmethod
    def min_max_specified_normalization(vec: np.ndarray, _min: float, _max: float) -> np.ndarray:
        if (_max - _min) == 0:  # vec == np.zeros()
            return vec
        return (vec - _min) / (_max - _min)

    @staticmethod
    def min_max_for_scalar(data: float, _min: float, _max: float) -> float:
        if (_max - _min) == 0:  # population of data will be np.zeros()
            return data
        return (data - _min) / (_max - _min)

    @staticmethod
    def standardize(vec: np.ndarray) -> np.ndarray:
        """
            X - Mean(X) / Std
        """
        return (vec - np.mean(vec)) / np.std(vec, axis=0)
