from peewee import CharField
from .base import BaseModel

class Model(BaseModel):
    """
    Represents a mathematical model in the encyclopedia.

    A model is the central entity of the system. Each model has a unique
    name and can be associated with multiple related entities:
        - Compartments (through ModelCompartment)
        - Parameters (through ModelParam)
        - Articles (through ModelArticle)
        - Situations (through ModelSituation)
        - Data (through ModelData)

    The model name serves as its primary key and must be unique across
    the entire system.

    Attributes:
        name (str): Unique identifier and primary key of the model.

    Note:
        The `name` field is case-sensitive and is used as the primary key.
        Attempting to create two models with the same name will raise
        an IntegrityError from Peewee.
    """
    name = CharField(max_length=100, primary_key=True)
    
    def __str__(self):
        """
        Returns the string representation of the model.

        Returns:
            str: The unique name of the model.
        """
        return self.name