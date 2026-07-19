from .BaseDto import BaseDto

class ModelDto(BaseDto):
    def __init__(self, name:str):
        super().__init__(name)