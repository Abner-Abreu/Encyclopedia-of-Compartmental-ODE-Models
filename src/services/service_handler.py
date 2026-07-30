from .article_services import ArticleService
from .data_services import DataService
from .model_services import ModelService
from .param_services import ParamService
from .situation_services import SituationService
from .validation_services import ValidationService
from .compartment_services import CompartmentService

from database import db

from dtos import ModelInfoDto
import logging

logger = logging.getLogger(__name__)

class ServiceHandler:
    """
    Orchestrates the creation of complete models with all related entities.

    This service acts as a facade that coordinates multiple specialized
    services to create a complete model with all its associated data
    in a single operation. It handles the creation of:
        - The model itself
        - Its associated article (creates if not exists)
        - Its associated situation (creates if not exists)
        - Its associated data (creates if not exists, optional)
        - All compartments (creates each if not exists)
        - All parameters (creates each if not exists)

    The ServiceHandler validates all data using the ValidationService
    before attempting any creation operations. All operations are
    performed in a specific order to maintain referential integrity.

    Attributes:
        article (ArticleService): Service for article operations.
        data (DataService): Service for data operations.
        model (ModelService): Service for model operations.
        param (ParamService): Service for parameter operations.
        situation (SituationService): Service for situation operations.
        validation (ValidationService): Service for data validation.
        compartment (CompartmentService): Service for compartment operations.
    """

    def __init__(self):
        """
        Initializes the ServiceHandler with all required sub-services.
        """
        self.article = ArticleService()
        self.data = DataService()
        self.model = ModelService()
        self.param = ParamService()
        self.situation = SituationService()
        self.validation = ValidationService()
        self.compartment = CompartmentService()

    def create_complete(self, model_info: ModelInfoDto) -> bool:
        """
        Creates a complete model with all its associated entities.

        This method orchestrates the creation of a model and all its
        related entities in the correct order. It follows these steps: \n
            1. Validates all input data using ValidationService 
            2. Creates or retrieves the article and links it to the model
            3. Creates or retrieves the situation and links it to the model
            4. Creates or retrieves the data (if provided) and links it
            5. Creates the model
            6. Creates or retrieves all compartments and links them
            7. Creates or retrieves all parameters and links them

        The method uses try/except blocks for each entity to implement
        a "get or create" pattern.

        Args:
            model_info: The ModelInfoDto containing all model data
                and its associated entities.

        Returns:
            bool: True if the model was successfully created, False
                if validation fails or the model already exists.
        """
        # Basic name validation
        if not self.validation.IsValidModelInfo(model_info):
            logger.error(f"Model {model_info.name} not created: Validation Error")
            return False

        with db.atomic():
            # Article
            try:
                self.article.get_by_id(model_info.article.name)
            except Exception:
                self.article.create(
                    name=model_info.article.name,
                    author=model_info.article.author,
                    date=model_info.article.date
                )

            # Situation
            try:
                self.situation.get_by_id(model_info.situation.name)
            except Exception:
                self.situation.create(
                    name=model_info.situation.name,
                    description=model_info.situation.description
                )

            # Data (optional)
            if model_info.data:
                try:
                    self.data.get_by_id(model_info.data.name)
                except Exception:
                    self.data.create(
                        name=model_info.data.name,
                        place=model_info.data.place,
                        date=model_info.data.date
                    )

            # Model
            try:
                self.model.create(name=model_info.name,
                                  situation=model_info.situation.name,
                                  article=model_info.article.name,
                                  data=model_info.data.name)
            except Exception:
                logger.error(f"Model {model_info.name} already exists")
                return False

            # Compartments
            for comp in model_info.compartments:
                try:
                    self.compartment.get_by_id(comp.name)
                except Exception:
                    self.compartment.create(
                        name=comp.name,
                        expression=comp.expression
                    )

                self.compartment.set_relation_to_model(
                    modelName=model_info.name,
                    compartmentName=comp.name
                )

            # Parameters
            for par in model_info.params:
                try:
                    self.param.get_by_id(par.name)
                except Exception:
                    self.param.create(name=par.name)

                self.param.set_relation_to_model(
                    modelName=model_info.name,
                    paramName=par.name,
                    linear=par.linear,
                    meaning=par.meaning,
                    symbol=par.symbol
                )

            logger.info(f"Model {model_info.name} created")
            return True
        return False