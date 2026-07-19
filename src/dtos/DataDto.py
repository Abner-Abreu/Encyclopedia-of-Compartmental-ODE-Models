from .BaseDto import BaseDto
from datetime import date
class DataDto(BaseDto):
    def __init__(self, 
                 name:str,
                 date:date,
                 place:str):
        super().__init__(name)
        self.date = date
        self.place = place