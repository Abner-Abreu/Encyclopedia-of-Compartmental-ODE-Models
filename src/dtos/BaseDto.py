from abc import ABC, abstractmethod

class BaseDto(ABC):
    """
    Abstract base class for all Data Transfer Objects (DTOs).

    This class serves as the foundation for all DTOs in the application,
    DTOs are used to transfer data between the service layer and the 
    presentation layer (UI) without exposing the underlying database 
    models directly.

    Attributes:
        name (str): The unique identifier or name of the entity.
    """
    def __init__(self, name:str):
        self.name = name

    @classmethod
    @abstractmethod
    def from_entity():
        """
        Creates an instance of Dto from a database entity.
        """
        pass