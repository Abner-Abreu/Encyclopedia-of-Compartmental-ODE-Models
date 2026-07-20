from peewee import CharField, TextField
from .base import BaseModel

class Situation(BaseModel):
    """
    Represents a model's situation (case of use) in the encyclopedia.

    A situation is associated with one or more models through the
    ModelSituation relationship table. Each situation must have a unique
    name, and a description

    Attributes:
        name (str): Unique identifier and primary key of the situation.
        description (str): Small description of the situation
    """
    name = CharField(max_length=100, primary_key=True)
    description = TextField()
    
    def __str__(self):
        """
        Returns the string representation of the situation.

        Returns:
            str: The unique name of the situation.
        """
        return self.name