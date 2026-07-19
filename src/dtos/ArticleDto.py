from .BaseDto import BaseDto
from datetime import date

class ArticleDto(BaseDto):
    def __init__(self, 
                 name:str,
                 author:str,
                 date:date):
        super().__init__(name)
        self.author = author
        self.date = date