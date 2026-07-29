from .BaseDto import BaseDto
from datetime import date
class DataDto(BaseDto):
    """
    Data Transfer Object for Data entities.

    This DTO encapsulates the data of a Data entity for transfer
    between the service layer and the presentation layer (UI).

    Attributes:
        name (str): Unique identifier of the data.
        date (date): Date when the data was obtained.
        place (str): Place where the data was obtained.
    """
    def __init__(self, 
                 name:str,
                 date:date,
                 place:str):
        super().__init__(name)
        self.date = date
        self.place = place