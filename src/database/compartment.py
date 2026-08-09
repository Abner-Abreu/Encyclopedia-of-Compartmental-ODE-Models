from peewee import CharField
from .base import BaseModel

class Compartment(BaseModel):
    """
    Represents a model's compartment in the encyclopedia.

    A compartment is associated with one or more models through the
    ModelCompartment relationship table. Each compartment must have a unique
    name and an expression.

    Attributes:
        name (str): Unique identifier and primary key of the compartment.
    """
    name = CharField(max_length=100, primary_key=True)
    
    def __str__(self):
        """
        Returns the string representation of the compartment.

        Returns:
            str: The unique name of the compartment.
        """
        return self.name