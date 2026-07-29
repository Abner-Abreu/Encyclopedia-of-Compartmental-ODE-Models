from .BaseDto import BaseDto
from datetime import date

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