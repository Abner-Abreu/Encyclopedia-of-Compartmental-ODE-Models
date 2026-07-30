from .BaseDto import BaseDto
from .SituationDto import SituationDto
from .DataDto import DataDto
from .ArticleDto import ArticleDto

from database import Model

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

    @classmethod
    def from_entity(clc,model:Model) -> ModelDto:
        """
        Creates an instance of ModelDto from an Model entity.
        
        Args:
            model (Model): Model entity from which information would
                be obtained.
        
        Returns:
            ModelDto: Dto with full information about the model.
        """

        if model.data:
            data = DataDto.from_entity(model.data)
        else:
            data = None

        return ModelDto(
            name=model.name,
            situation=SituationDto.from_entity(model.situation),
            article=ArticleDto.from_entity(model.article),
            data=data
        )