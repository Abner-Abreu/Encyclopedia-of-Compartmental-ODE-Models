from .BaseDto import BaseDto

class ModelDto(BaseDto):
    """
    Data Transfer Object for Model entities.

    This DTO encapsulates the data of a Model entity for transfer
    between the service layer and the presentation layer (UI).

    Attributes:
        name (str): Unique identifier of the model.
    """
    def __init__(self, name:str):
        super().__init__(name)