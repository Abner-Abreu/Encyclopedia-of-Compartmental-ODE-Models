from peewee import CharField, ForeignKeyField, IntegerField, TextField
from .base import BaseModel

class Param(BaseModel):

    name = CharField(max_length=100, primary_key=True)
    
    def __str__(self):
        return self.name