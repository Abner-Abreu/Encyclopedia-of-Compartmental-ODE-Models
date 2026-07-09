from peewee import CharField
from .base import BaseModel

class Model(BaseModel):

    name = CharField(max_length=100, primary_key=True)
    
    def __str__(self):
        return self.name