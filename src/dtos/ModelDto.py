from .BaseDto import BaseDto
from .SituationDto import SituationDto
from .DataDto import DataDto
from .ArticleDto import ArticleDto

class ModelDto(BaseDto):
    """
    Data Transfer Object for Model entities.

    This DTO encapsulates the data of a Model entity for transfer
    between the service layer and the presentation layer (UI).

    Attributes:
        name (str): Unique identifier of the model.
        situation (SituationDto): Dto of the situation associated
            to the model
        article (ArticleDto): Dto of the article associated
            to the model  
        data (DataDto): Dto of the article associated
            to the model
    """
    def __init__(self, name:str,
                 situation: SituationDto,
                 article: ArticleDto,
                 data: DataDto | None):
        super().__init__(name)
        self.situation = situation
        self.article = article
        self.data = data