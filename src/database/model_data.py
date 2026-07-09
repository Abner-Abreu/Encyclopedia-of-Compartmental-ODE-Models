from peewee import ForeignKeyField,CompositeKey
from .base import BaseModel
from .model import Model
from .data import Data

class ModelData(BaseModel):

    model = ForeignKeyField(Model, backref='datas')
    data = ForeignKeyField(Data, backref='models')
    
    class Meta:
        primary_key = CompositeKey('model', 'data')