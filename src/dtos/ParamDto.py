from .BaseDto import BaseDto

class ParamDto(BaseDto):
    """
    Data Transfer Object for Param entities.

    This DTO encapsulates the data of a Param entity for transfer
    between the service layer and the presentation layer (UI).

    Attributes:
        name (str): Unique identifier of the param.
    """
    def __init__(self, name:str):
        super().__init__(name)