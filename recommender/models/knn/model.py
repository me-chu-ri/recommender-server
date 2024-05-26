import numpy as np
from collections import Counter

from .norms import Norm, L2Norm


class KNN:
    def __init__(self, dim: int, k_value: int = 3, dist_strategy: Norm = L2Norm()):
        self.K = k_value
        self.norm = dist_strategy
        self.dim = dim
        self.datas: np.ndarray = np.array([])
        self.labels: np.ndarray = np.array([])

    def fit(self, datas: np.ndarray, labels: np.ndarray):
        # size of datas: (n, dim), max n = 1,000
        # size of labels: (n, 1)
        if datas.shape[0] != labels.shape[0]:
            raise ValueError("row of datas and y must match")
        self.datas = datas
        self.labels = labels

    def predict(self, X: np.ndarray) -> int:
        # Calculate every distance and find K-Nearest data points
        # size of X: (1, dim)
        self.__check_dim(X, (1, self.dim))

        dists: list = [self.norm.execute(X, data) for data in self.datas]  # calculate distances
        k_nearest_idx: np.ndarray = np.argsort(dists)[: self.K]  # return sorted idx
        k_nearest_labels: list = [self.labels[idx] for idx in k_nearest_idx]  # k-nearest labels
        counts = Counter(k_nearest_labels).most_common()
        # Order will follow k_nearest_idx's order, so the first one will be the nearest, common neighbor

        return counts[0][0]

    def __check_dim(self, X: np.ndarray, shape: tuple):
        if X.shape != shape:
            raise ValueError(f"Shape of X should be {(1, self.dim)} which is currently {X.shape}")