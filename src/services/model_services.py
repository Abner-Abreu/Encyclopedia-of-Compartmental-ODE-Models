from peewee import DoesNotExist, IntegrityError, fn, JOIN

from database import (Model,
                      Compartment, 
                      Param,
                      ModelCompartment,
                      ModelParam,
                      db)

from dtos import (ArticleDto,
                  CompartmentDto,
                  DataDto,
                  ModelDto,
                  ModelInfoDto,
                  ParamInfoDto,
                  SituationDto,
                  FiltersDto)
import logging

from .base_services import BaseServices

logger = logging.getLogger(__name__)

class ModelService(BaseServices):
    """
    Service class for managing Model entities and their relationships.

    This service provides CRUD operations for Model entities as well as
    methods for retrieving all related entities associated with a model:
    compartments, parameters (with metadata), article, situation, and data.
    """

    def create(self, 
               name: str,
               situation: str,
               article: str,
               data: str | None) -> Model:
        """
        Creates a new model.

        Args:
            name: Unique identifier of the model (primary key).

        Returns:
            Model: The created Model instance.

        Raises:
            ValueError: If a model with the same name already exists.
        """
        try:
            model = Model.create(name=name,
                                 situation=situation,
                                 article=article,
                                 data=data)
            logger.info(f"Model created: {name}")

            return model

        except IntegrityError as e:
            logger.error(f"Error when creating model {name}: {e}")
            raise ValueError(f"A model with name '{name}' already exists")

    def get_by_id(self, name: str) -> Model:
        """
        Retrieves a model by its unique identifier.

        Args:
            name: The unique identifier of the model to retrieve.

        Returns:
            Model: The Model instance matching the given ID.

        Raises:
            ValueError: If no model is found with the given name.
        """
        try:
            return Model.get_by_id(name)
        except DoesNotExist:
            logger.warning(f"Model {name} not found")
            raise ValueError(f"Model {name} not found")

    def to_list(self, filters: FiltersDto | None = None) -> list[ModelDto]:
        """
        Retrieves a list of models with optional filtering.

        The filters parameter allows filtering by:
            - Model name (partial match)
            - Associated parameter name (partial match)
            - Associated compartment name (partial match)
            - Associated situation name (partial match)
            - Associated article name (partial match)
            - All parameters linear (boolean)

        Models are ordered alphabetically by name (ascending).

        Args:
            filters: Optional FiltersDto containing filter criteria.

        Returns:
            list[ModelDto]: A list of ModelDto objects representing
                the filtered models.

        Note:
            For filters that involve related entities (parameter, compartment,
            situation, article), subqueries are used to efficiently filter
            the results without joining all tables at once.
        """
        query = Model.select()

        if filters:
            if filters.name_contains:
                query = query.where(Model.name.contains(filters.name_contains))

            if filters.parameter_contains:
                subquery = (ModelParam
                            .select(ModelParam.model)
                            .join(Param, JOIN.LEFT_OUTER)
                            .where(Param.name.contains(filters.parameter_contains)))
                query = query.where(Model.name.in_(subquery))

            if filters.compartment_contains:
                subquery = (ModelCompartment
                            .select(ModelCompartment.model)
                            .join(Compartment, JOIN.LEFT_OUTER)
                            .where(Compartment.name.contains(filters.compartment_contains)))
                query = query.where(Model.name.in_(subquery))

            if filters.situation_contains:
                query = query.where(Model.situation.contains(filters.situation_contains))

            if filters.article_contains:
                query = query.where(Model.article.contains(filters.article_contains))

            if filters.all_linear:
                query = query.where(~fn.EXISTS(
                    ModelParam
                    .select()
                    .where((ModelParam.model == Model.name) &
                           (ModelParam.linear == False))
                ))

        query = query.order_by(Model.name.asc())

        result = list()
        for res in query:
            result.append(ModelDto.from_entity(res))

        return result

    def update(self):
        """
        Updates an existing model.

        This method is currently not implemented and serves as a placeholder
        for future functionality.

        Returns:
            None: This method is not yet implemented.
        """
        return

    def delete(self, name: str) -> bool:
        """
        Deletes a model and removes all its relationships.

        This method deletes the model with the given name and automatically
        removes all associated entries from all junction tables
        (ModelCompartment, ModelParam, ModelArticle, ModelSituation,
        ModelData) before deleting the model itself. The operation is
        performed atomically using a database transaction.

        Args:
            name: The unique identifier of the model to delete.

        Returns:
            bool: True if the model was successfully deleted.

        Raises:
            ValueError: If no model is found with the given name.

        Note:
            This method uses db.atomic() to ensure the operation is
            atomic. If any part of the operation fails, the entire
            transaction is rolled back.
        """
        model = self.get_by_id(name)

        with db.atomic():
            ModelCompartment.delete().where(
                ModelCompartment.model == model
            ).execute()
            ModelParam.delete().where(
                ModelParam.model == model
            ).execute()

            model.delete_instance()

        logger.info(f"Model deleted: {name}")
        return True

    def get_compartments(self, name: str) -> list[CompartmentDto]:
        """
        Retrieves all compartments associated with a model.

        Args:
            name: The unique identifier of the model.

        Returns:
            list[CompartmentDto]: A list of CompartmentDto objects
                representing all compartments associated with the model.

        Raises:
            ValueError: If no model is found with the given name.
        """
        model = self.get_by_id(name)

        query = (ModelCompartment
                 .select(ModelCompartment, Compartment)
                 .join(Compartment)
                 .where(ModelCompartment.model == model))

        result = []
        for res in query:
            result.append(CompartmentDto.from_entity(res.compartment))
        return result

    def get_params(self, name: str) -> list[ParamInfoDto]:
        """
        Retrieves all parameters associated with a model with their metadata.

        Returns parameter information including the parameter name, linearity,
        symbol, and meaning as stored in the ModelParam junction table.

        Args:
            name: The unique identifier of the model.

        Returns:
            list[ParamInfoDto]: A list of ParamInfoDto objects representing
                all parameters associated with the model, including metadata.

        Raises:
            ValueError: If no model is found with the given name.
        """
        model = self.get_by_id(name)

        query = (ModelParam
                 .select(ModelParam, Param)
                 .join(Param)
                 .where(ModelParam.model == model))

        result = []
        for res in query:
            result.append(ParamInfoDto.from_entity(res))
        return result

    def get_article(self, name: str) -> ArticleDto:
        """
        Retrieves the article associated with a model.

        Args:
            name: The unique identifier of the model.

        Returns:
            ArticleDto: The ArticleDto representing the associated
                article.

        Raises:
            ValueError: If no model is found with the given name.
        """
        model = self.get_by_id(name)
        
        return ArticleDto.from_entity(model.article)

    def get_situation(self, name: str) -> SituationDto:
        """
        Retrieves the situation associated with a model.

        Args:
            name: The unique identifier of the model.

        Returns:
            SituationDto: The SituationDto representing the associated
                situation.

        Raises:
            ValueError: If no model is found with the given name.
        """
        model = self.get_by_id(name)

        return SituationDto.from_entity(model.situation)

    def get_data(self, name: str) -> DataDto | None:
        """
        Retrieves the data entry associated with a model.

        Since a model can have multiple data entries through the many-to-many
        relationship, this method returns the first one found (if any).

        Args:
            name: The unique identifier of the model.

        Returns:
            DataDto | None: The DataDto representing the associated data
                entry or None if there is no associated data

        Raises:
            ValueError: If no model is found with the given name.
        """
        model = self.get_by_id(name)

        if model.data:
            return DataDto.from_entity(model.data)
        else:
            return None

    def get_all(self, name: str) -> ModelInfoDto:
        """
        Retrieves complete information about a model.

        This method aggregates all related data (compartments, parameters,
        article, situation, data) into a single ModelInfoDto object.

        Args:
            name: The unique identifier of the model.

        Returns:
            ModelInfoDto: A DTO containing all model data and its
                associated relationships.

        Raises:
            ValueError: If no model is found with the given name.
        """
        model = self.get_by_id(name)

        return ModelInfoDto(
            name=model.name,
            compartments=self.get_compartments(name),
            params=self.get_params(name),
            situation=self.get_situation(name),
            article=self.get_article(name),
            data=self.get_data(name)
        )