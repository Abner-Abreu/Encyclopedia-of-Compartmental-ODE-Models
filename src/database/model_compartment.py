from peewee import ForeignKeyField,CompositeKey
from .base import BaseModel
from .model import Model
from .compartment import Compartment

class ModelCompartment(BaseModel):

    model = ForeignKeyField(Model, backref='compartments')
    compartment = ForeignKeyField(Compartment, backref='models')
    
    class Meta:
        primary_key = CompositeKey('model', 'compartment')