from peewee import CharField, DateTimeField
from .base import BaseModel

class Article(BaseModel):

    name = CharField(max_length=100, primary_key=True)
    author = CharField(max_length=100)
    date = DateTimeField()
    
    def __str__(self):
        return self.name