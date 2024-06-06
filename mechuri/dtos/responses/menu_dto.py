from .nutrient_dto import NutrientDto
from ..abstract_dto import Dto
from ...models.models import Menu


class MenuDto(Dto):
    def __init__(self,
                 menu_id: int = -1,
                 name: str = '',
                 code: str = '',
                 major: str = '',
                 middle: str = '',
                 meal_type: str = '',
                 nutrient_dto: NutrientDto = None
                 ):
        self.menu_id: int = menu_id
        self.name: str = name
        self.code: str = code
        self.major: str = major
        self.middle: str = middle
        self.meal_type: str = meal_type
        self.nutrient_dto: NutrientDto = nutrient_dto

    @staticmethod
    def from_entity(entity: Menu):
        return MenuDto(
            entity.id,
            entity.name,
            entity.code,
            entity.major,
            entity.middle,
            entity.meal_type,
            NutrientDto.from_entity(entity.nutrient)
        )