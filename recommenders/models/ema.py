from decimal import Decimal


class EMA:
    def __init__(self, beta: float = 0.7):
        self.beta = beta

    def update(self, old: float, new: float, is_t1: bool = False) -> float:
        if is_t1:
            return new
        return float(Decimal(f'{self.beta}') * Decimal(f'{old}') + (1 - Decimal(f'{self.beta}')) * Decimal(f'{new}'))
