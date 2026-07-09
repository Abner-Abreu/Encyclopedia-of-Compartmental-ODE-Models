from peewee import ForeignKeyField,CompositeKey
from .base import BaseModel
from .model import Model
from .situation import Situation

class ModelSituation(BaseModel):

    model = ForeignKeyField(Model, backref='situations')
    situation = ForeignKeyField(Situation, backref='models')
    
    class Meta:
        primary_key = CompositeKey('model', 'situation')