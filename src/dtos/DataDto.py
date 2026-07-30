from .BaseDto import BaseDto
from datetime import date

from database import Data

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

    @classmethod
    def from_entity(clc,data:Data) -> DataDto:
        """
        Creates an instance of DataDto from an data entity.
        
        Args:
            data (Data): Data entity from which information would
                be obtained.
        
        Returns:
            DataDto: Dto with full information about the data.
        """
        return DataDto(
            name=data.name,
            date=data.name,
            place=data.place
        )