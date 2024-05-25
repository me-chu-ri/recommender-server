import numpy as np

from .norms import Norm


class KNN:
    def __init__(self, k_value: int, dist_strategy: Norm, dim: int):
        self.K = k_value
        self.norm = dist_strategy
        self.dim = dim

    def fit(self, X: list, y: int) -> None:
        # Add data point
        self.__check_dim(X)

        pass

    def predict(self, X: list) -> int:
        # Calculate every distance and find K-Nearest data points
        self.__check_dim(X)

        return 0

    def __check_dim(self, X: list):
        if len(X) != self.dim:
            raise ValueError(f"Dimension of X: {len(X)} is not equal to model's dimension: {self.dim}")