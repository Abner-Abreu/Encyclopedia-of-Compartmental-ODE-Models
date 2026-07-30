from .BaseDto import BaseDto
from datetime import date

from database import Article

class ArticleDto(BaseDto):
    """
    Data Transfer Object for Article entities.

    This DTO encapsulates the data of an Article entity for transfer
    between the service layer and the presentation layer (UI).

    Attributes:
        name (str): Unique identifier of the article.
        author (str): Full name of the article's author.
        date (date): Publication date of the article.
    """
    def __init__(self, 
                 name:str,
                 author:str,
                 date:date):
        super().__init__(name)
        self.author = author
        self.date = date
    
    @classmethod
    def from_entity(clc,article: Article) -> ArticleDto:
        """
        Creates an instance of ArticleDto from an Article entity.
        
        Args:
            article (Article): Article entity from which information would
                be obtained.
        
        Returns:
            ArticleDto: Dto with full information about the article.
        """
        return ArticleDto(
            name=article.name,
            author=article.author,
            date=article.date
        )