from peewee import ForeignKeyField,CompositeKey
from .base import BaseModel
from .model import Model
from .article import Article

class ModelArticle(BaseModel):

    model = ForeignKeyField(Model, backref='articles')
    article = ForeignKeyField(Article, backref='models')
    
    class Meta:
        primary_key = CompositeKey('model', 'article')