from peewee import Model
from .database_config import db

class BaseModel(Model):
    class Meta:
        database = db