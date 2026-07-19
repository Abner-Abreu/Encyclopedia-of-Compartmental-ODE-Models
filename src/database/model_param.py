from peewee import ForeignKeyField,CompositeKey, BooleanField, TextField, CharField
from .base import BaseModel
from .model import Model
from .param import Param

class ModelParam(BaseModel):

    model = ForeignKeyField(Model, backref='params')
    param = ForeignKeyField(Param, backref='models')

    linear = BooleanField()
    meaning = TextField()
    symbol = CharField(max_length=100)
    
    class Meta:
        primary_key = CompositeKey('model', 'param')