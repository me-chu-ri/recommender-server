from ..general.weather_dto import WeatherDto
from ..general.location_dto import LocationDto
from ..abstract_dto import Dto


class GetRecommendDto(Dto):
    target_id: str
    temp: float
    precip: float
    humid: float
