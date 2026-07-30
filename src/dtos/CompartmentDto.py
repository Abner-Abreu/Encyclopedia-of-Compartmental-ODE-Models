from .BaseDto import BaseDto

from database import Compartment

class CompartmentDto(BaseDto):
    """
    Data Transfer Object for Compartment entities.

    This DTO encapsulates the data of a Compartment entity for 
    transfer between the service layer and the presentation 
    layer (UI).

    Attributes:
        name (str): Unique identifier of the compartment.
        expression (str): Mathematical expression of the compartment.
    """
    def __init__(self, 
                 name:str,
                 expression:str):
        super().__init__(name)
        self.expression = expression
    
    @classmethod
    def from_entity(clc,compartment: Compartment) -> CompartmentDto:
        """
        Creates an instance of CompartmentDto from a Compartment entity.
        
        Args:
            compartment (Compartment): Compartment entity from which information would
                be obtained.
        
        Returns:
            CompartmentDto: Dto with full information about the compartment.
        """
        return CompartmentDto(
            name=compartment.name,
            expression=compartment.expression
        )