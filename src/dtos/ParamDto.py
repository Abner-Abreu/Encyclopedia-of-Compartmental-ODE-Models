from .BaseDto import BaseDto

class ParamDto(BaseDto):
    def __init__(self, name:str):
        super().__init__(name)