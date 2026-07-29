from peewee import ForeignKeyField,CompositeKey
from .base import BaseModel
from .model import Model
from .article import Article

class ModelArticle(BaseModel):
    """
    Represents the relationship between models and articles.

    This junction table connects a mathematical model to the scientific
    articles that reference or describe it. 

    Attributes:
        model (ForeignKeyField): Reference to the associated Model.
        article (ForeignKeyField): Reference to the associated Article.

    Relationships:
        - model.backref 'articles': Access to all articles associated
          with a given model.
        - article.backref 'models': Access to all models associated
          with a given article.

    Note:
        This table uses a composite primary key (model, article) to
        ensure uniqueness. Peewee will raise an IntegrityError if you
        attempt to create a duplicate relationship.
    """

    model = ForeignKeyField(Model, backref='articles')
    article = ForeignKeyField(Article, backref='models')
    
    class Meta:
        primary_key = CompositeKey('model', 'article')