from peewee import CharField, ForeignKeyField, IntegerField, TextField
from .base import BaseModel

class Param(BaseModel):
    """
    Represents a model's param in the encyclopedia.

    A param is associated with one or more models through the
    ModelParam relationship table. Each param must have a unique
    name.

    Attributes:
        name (str): Unique identifier and primary key of the param.
    """
    name = CharField(max_length=100, primary_key=True)
    
    def __str__(self):
        """
        Returns the string representation of the param.

        Returns:
            str: The unique name of the param.
        """
        return self.name