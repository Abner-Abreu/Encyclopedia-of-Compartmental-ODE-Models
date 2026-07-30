from .BaseDto import BaseDto

from database import Param

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

    @classmethod
    def from_entity(clc,param: Param) -> ParamDto:
        """
        Creates an instance of ParamDto from an Param entity.
        
        Args:
            param (Param): Param entity from which information would
                be obtained.
        
        Returns:
            ParamDto: Dto with full information about the param.
        """
        return ParamDto(
            name=param.name
        )