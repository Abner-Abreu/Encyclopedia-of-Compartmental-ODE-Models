from peewee import CharField, TextField
from .base import BaseModel

class Compartment(BaseModel):
    
    name = CharField(max_length=100, primary_key=True)
    expression = TextField()
    
    def __str__(self):
        return self.name