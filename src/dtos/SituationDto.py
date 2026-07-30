from .BaseDto import BaseDto

from database import Situation

class SituationDto(BaseDto):
    """
    Data Transfer Object for Situation entities.

    This DTO encapsulates the data of a Situation entity for transfer
    between the service layer and the presentation layer (UI).

    Attributes:
        name (str): Unique identifier of the data.
        description (str): Description of the situation
    """
    def __init__(self, 
                 name:str,
                 description:str = None):
        super().__init__(name)
        self.description = description

    @classmethod
    def from_entity(clc, situation: Situation) -> SituationDto:
        """
        Creates an instance of SituationDto from an Situation entity.
        
        Args:
            situation (Situation): Situation entity from which information 
            would be obtained.
        
        Returns:
            SituationDto: Dto with full information about the situation.
        """
        return SituationDto(
            name=situation.name,
            description=situation.description
        )