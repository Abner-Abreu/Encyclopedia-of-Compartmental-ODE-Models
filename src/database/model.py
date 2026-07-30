from peewee import CharField, ForeignKeyField
from .base import BaseModel
from .article import Article
from .situation import Situation
from .data import Data

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
        article (ForeignKey): Article associated to the model
        situation (ForeignKey): Situation associated to the model
        data (ForeignKey | Null): Optional data associated to the model

    Note:
        The `name` field is case-sensitive and is used as the primary key.
        Attempting to create two models with the same name will raise
        an IntegrityError from Peewee.
    """
    name = CharField(
        max_length=100, 
        primary_key=True
        )
    article = ForeignKeyField(
        Article, 
        backref='models',
        on_delete='SET NULL')
    situation = ForeignKeyField(
        Situation, 
        backref='models',
        on_delete='SET NULL'
        )
    data = ForeignKeyField(
        Data, 
        null=True,
        backref='models',
        on_delete='SET NULL'
        ) 

    def __str__(self):
        """
        Returns the string representation of the model.

        Returns:
            str: The unique name of the model.
        """
        return self.name