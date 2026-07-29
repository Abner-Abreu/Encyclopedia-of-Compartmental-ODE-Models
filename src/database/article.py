from peewee import CharField, DateTimeField
from .base import BaseModel

class Article(BaseModel):
    """
    Represents a scientific article referenced in the encyclopedia.

    An article is associated with one or more models through the
    ModelArticle relationship table. Each article must have a unique
    name, an author, and a publication date.

    Attributes:
        name (str): Unique identifier and primary key of the article.
        author (str): Full name of the article's author.
        date (datetime): Publication date of the article.
    """
    name = CharField(max_length=100, primary_key=True)
    author = CharField(max_length=100)
    date = DateTimeField()
    
    def __str__(self):
        """
        Returns the string representation of the article.

        Returns:
            str: The unique name of the article.
        """
        return self.name