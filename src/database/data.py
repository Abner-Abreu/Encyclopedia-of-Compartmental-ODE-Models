from peewee import CharField, DateTimeField, TextField
from .base import BaseModel

class Data(BaseModel):
    """
    Represents a model's experimental data in the encyclopedia.

    A data is associated with one or more models through the
    ModelData relationship table. Each data must have a unique
    name, a place where it was obtained and a date when it was
    obtained.

    Attributes:
        name (str): Unique identifier and primary key of the data.
        place (str): Place where the data was obtained
        date (date): Date when the data was obtained
    """
    name = CharField(max_length=100, primary_key=True)
    place = TextField()
    date = DateTimeField()
    
    def __str__(self):
        """
        Returns the string representation of the data.

        Returns:
            str: The unique name of the data.
        """
        return self.name