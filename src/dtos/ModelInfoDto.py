from .BaseDto import BaseDto
from .ArticleDto import ArticleDto
from .CompartmentDto import CompartmentDto
from .DataDto import DataDto
from .ParamInfoDto import ParamInfoDto
from .SituationDto import SituationDto

class ModelInfoDto(BaseDto):
    def __init__(self, 
                 name:str,
                 compartments: list[CompartmentDto],
                 params: list[ParamInfoDto],
                 situation: SituationDto,
                 article: ArticleDto,
                 data: DataDto | None
                 ):
        super().__init__(name)
        self.compartments = compartments
        self.params = params
        self.situation = situation
        self.article = article
        self.data = data
