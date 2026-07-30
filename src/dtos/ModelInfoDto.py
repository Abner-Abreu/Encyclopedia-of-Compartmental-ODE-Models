from .ArticleDto import ArticleDto
from .CompartmentDto import CompartmentDto
from .DataDto import DataDto
from .ParamInfoDto import ParamInfoDto
from .SituationDto import SituationDto
from .ModelDto import ModelDto

from database import ModelParam,Compartment, Model

class ModelInfoDto(ModelDto):
    """
    Data Transfer Object for complete model information.

    This DTO encapsulates all the detailed information about a model,
    including its associated compartments, parameters, situation,
    article, and optional data. It is used to transfer comprehensive
    model data from the service layer to the presentation layer (UI)
    for display in detail views or dialogs.

    Unlike the base ModelDto which contains only basic information,
    this DTO provides the full context of a model with all its
    relationships and metadata.

    Attributes:
        name (str): Unique identifier of the model (inherited from BaseDto).
        compartments (list[CompartmentDto]): List of compartments associated
            with the model.
        params (list[ParamInfoDto]): List of parameters associated with
            the model, including metadata (linear, symbol, meaning).
        situation (SituationDto): The situation associated with the model.
        article (ArticleDto): The article associated with the model.
        data (DataDto | None): Optional data entry associated with the model.

    Note:
        This DTO is typically used for displaying detailed model information
        in the UI, such as in the "View Details" dialog. It contains all
        related data in a single object to minimize round trips to the
        service layer.
    """
    def __init__(self, 
                 name:str,
                 compartments: list[CompartmentDto],
                 params: list[ParamInfoDto],
                 situation: SituationDto,
                 article: ArticleDto,
                 data: DataDto | None
                 ):
        super().__init__(name=name,
                         situation=situation,
                         article=article,
                         data=data)
        self.compartments = compartments
        self.params = params

    @classmethod
    def from_entity(clc, model: Model, 
                    compartments: list[Compartment],
                    params: list[ModelParam]) -> ModelInfoDto:
        """
        Creates an instance of ModelInfoDto from database entities.
        
        Args:
            model (Model): Model entity from which information would
                be obtained.
            compartments (list[Compartment]): List of compartments 
                associated to model.
            params (list[Params]): List of params associated to 
                model.
        
        Returns:
            ModelInfoDto: Dto with full information about the model.

        Note:
            Article, Situation and Data attributes are obtained
            directly from the model arg.
        """

        if model.data:
            data = DataDto.from_entity(model.data)
        else:
            data = None

        return ModelInfoDto(
            name=model.name,
            compartments=[{
                CompartmentDto.from_entity(comp)
            }for comp in compartments],
            params=[{
                ParamInfoDto.from_entity(param)
            }for param in params],
            article=ArticleDto.from_entity(model.article),
            situation=SituationDto.from_entity(model.situation),
            data=data
        )
