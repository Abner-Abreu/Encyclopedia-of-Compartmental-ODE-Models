from peewee import CharField, TextField
from .base import BaseModel

class Situation(BaseModel):

    name = CharField(max_length=100, primary_key=True)
    description = TextField()
    
    def __str__(self):
        return self.name