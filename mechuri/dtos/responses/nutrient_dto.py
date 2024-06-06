from ..abstract_dto import Dto
from ...models.models import Nutrient


class NutrientDto(Dto):
    def __init__(self,
                 energy: float = -99,
                 carbohydrate: float = -99,
                 protein: float = -99,
                 fat: float = -99,
                 sugar: float = -99,
                 sodium: float = -99
                 ):
        self.energy: float = energy
        self.carbohydrate: float = carbohydrate
        self.protein: float = protein
        self.fat: float = fat
        self.sugar: float = sugar
        self.sodium: float = sodium

    @staticmethod
    def from_entity(entity: Nutrient):
        return NutrientDto(
            entity.energy,
            entity.carbohydrate,
            entity.protein,
            entity.fat,
            entity.sugar,
            entity.sodium
        )