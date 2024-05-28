import numpy as np


class EASEr:
    def __init__(self, _lambda: int = 300):
        self.B: np.ndarray = np.array([])
        self._lambda = _lambda

    def fit(self, X: np.ndarray):
        G: np.ndarray = X.T @ X
        diag_indices = np.diag_indices_from(G)
        G[diag_indices] += self._lambda
        P: np.ndarray = np.linalg.inv(G)
        self.B = P / -np.diag(P)
        self.B[diag_indices] = 0

    def predict(self, user_row: np.ndarray) -> np.ndarray:
        return user_row @ self.B
