from peewee import CharField, DateTimeField, TextField
from .base import BaseModel

class Data(BaseModel):

    name = CharField(max_length=100, primary_key=True)
    place = TextField()
    date = DateTimeField()
    
    def __str__(self):
        return self.name