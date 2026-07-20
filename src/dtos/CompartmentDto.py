from .BaseDto import BaseDto

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