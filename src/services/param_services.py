from peewee import DoesNotExist, IntegrityError

from database import (Model,
                      Param,
                      ModelParam,
                      db)

from dtos import (ParamDto,
                  ModelDto)

import logging

from .base_services import BaseServices

logger = logging.getLogger(__name__)

class ParamService(BaseServices):
    """
    Service class for managing Param entities and their relationships.

    This service provides CRUD operations for Param entities as well as
    methods for managing the relationships between parameters
    and models through the ModelParam junction table. The ModelParam
    relationship stores additional metadata including linearity, symbol,
    and meaning.
    """

    def create(self, name: str):
        """
        Creates a new parameter.

        Args:
            name: Unique identifier of the parameter (primary key).

        Returns:
            Param: The created Param instance.

        Raises:
            ValueError: If a parameter with the same name already exists.
        """
        try:
            param = Param.create(name=name)
            logger.info(f"Param created: {name}")

            return param

        except IntegrityError as e:
            logger.error(f"Error when creating param {name}: {e}")
            raise ValueError(f"A Param with name '{name}' already exists")

    def get_by_id(self, name: str) -> Param:
        """
        Retrieves a parameter by its unique identifier.

        Args:
            name: The unique identifier of the parameter to retrieve.

        Returns:
            Param: The Param instance matching the given ID.

        Raises:
            ValueError: If no parameter is found with the given name.
        """
        try:
            return Param.get_by_id(name)
        except DoesNotExist:
            logger.warning(f"Param {name} not found")
            raise ValueError(f"Param {name} not found")

    def to_list(self) -> list[ParamDto]:
        """
        Retrieves a list of all parameters in the system.

        The parameters are ordered alphabetically by name (ascending).

        Returns:
            list[ParamDto]: A list of ParamDto objects representing
                all parameters in the system.
        """
        query = Param.select()
        query = query.order_by(Param.name.asc())

        result = []
        for res in query:
            result.append(ParamDto(name=res.name))

        return result

    def update(self):
        """
        Updates an existing parameter.

        This method is currently not implemented and serves as a placeholder
        for future functionality.

        Returns:
            None: This method is not yet implemented.
        """
        return

    def delete(self, name: str) -> bool:
        """
        Deletes a parameter and removes all its relationships.

        Args:
            name: The unique identifier of the parameter to delete.

        Returns:
            bool: True if the parameter was successfully deleted.

        Raises:
            ValueError: If no parameter is found with the given name.

        Note:
            This method uses db.atomic() to ensure the operation is
            atomic. If any part of the operation fails, the entire
            transaction is rolled back.
        """
        param = self.get_by_id(name)

        with db.atomic():
            ModelParam.delete().where(
                ModelParam.param == param
            ).execute()

            param.delete_instance()

        logger.info(f"Param deleted: {name}")
        return True

    def get_models(self, name: str) -> list[ModelDto]:
        """
        Retrieves all models associated with a specific parameter.

        Args:
            name: The unique identifier of the parameter.

        Returns:
            list[ModelDto]: A list of ModelDto objects representing all
                models associated with the parameter.

        Raises:
            ValueError: If no parameter is found with the given name.
        """
        param = self.get_by_id(name)

        query = (ModelParam
                 .select(ModelParam, Model)
                 .join(Model)
                 .where(ModelParam.param == param))

        return [
            ModelDto(name=rel.model.name)
            for rel in query
        ]

    def set_relation_to_model(self,
                              modelName: str,
                              paramName: str,
                              linear: bool,
                              meaning: str,
                              symbol: str):
        """
        Creates a relationship between a model and a parameter with metadata.

        This method adds an entry to the ModelParam junction table,
        establishing a relationship between the specified
        model and parameter. The relationship includes additional metadata
        about how the parameter behaves within the model.

        Args:
            modelName: The unique identifier of the model.
            paramName: The unique identifier of the parameter.
            linear: Indicates whether the model is linear with respect
                to this parameter.
            meaning: Physical or mathematical description of the
                parameter's meaning in the context of the model.
            symbol: LaTeX symbol representing the parameter.

        Returns:
            ModelParam: The created ModelParam relationship instance.

        Raises:
            ValueError: If the relationship cannot be created (e.g.,
                duplicate relationship or one of the entities does not exist).
        """
        try:
            model_param = ModelParam.create(
                model=modelName,
                param=paramName,
                linear=linear,
                meaning=meaning,
                symbol=symbol
            )
            logger.info(f"Relation Model: {modelName} - Param: {paramName} created")

            return model_param

        except IntegrityError as e:
            logger.error(f"Error when creating relation Model: {modelName} - Param: {paramName}: {e}")
            raise ValueError(f"A relation Model: {modelName} - Param: {paramName} cannot be created")