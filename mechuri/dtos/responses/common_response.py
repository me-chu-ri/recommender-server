from ..abstract_dto import Dto


class CommonResponse(Dto):
    def __init__(self, status: bool, message: str):
        self.status: bool = status
        self.message: str = message