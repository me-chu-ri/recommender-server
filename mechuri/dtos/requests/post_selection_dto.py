from ..general.weather_dto import WeatherDto
from ..general.location_dto import LocationDto
from ..abstract_dto import Dto


class PostSelectionDto(Dto):
    target_id: str
    menu_id: str
    weather: WeatherDto
    location: LocationDto
