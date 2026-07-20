from .BaseDto import BaseDto

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