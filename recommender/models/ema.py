class EMA:
    def __init__(self, beta: float = 0.7):
        self.beta = beta

    def update(self, old: float, new: float) -> float:
        return old * self.beta + new * (1 - self.beta)
