from peewee import Model
from .database_config import db

class BaseModel(Model):
    """Base Model Class, sets database necesary for peewee"""
    class Meta:
        database = db