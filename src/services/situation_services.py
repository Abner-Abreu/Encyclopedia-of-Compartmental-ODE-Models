from peewee import DoesNotExist, IntegrityError

from database import (Model,
                      Situation,
                      db)

from dtos import (SituationDto,
                  ModelDto,
                  DataDto,
                  ArticleDto)

import logging

from .base_services import BaseServices

logger = logging.getLogger(__name__)

class SituationService(BaseServices):
    """
    Service class for managing Situation entities and their relationships.

    This service provides CRUD operations for Situation entities as well as
    methods for managing the relationships between situations
    and models through the ModelSituation junction table.
    """

    def create(self, name: str, description: str):
        """
        Creates a new situation.

        Args:
            name: Unique identifier of the situation (primary key).
            description: Detailed description of the situation.

        Returns:
            Situation: The created Situation instance.

        Raises:
            ValueError: If a situation with the same name already exists.
        """
        try:
            situation = Situation.create(name=name, description=description)
            logger.info(f"Situation created: {name}")

            return situation

        except IntegrityError as e:
            logger.error(f"Error when creating situation {name}: {e}")
            raise ValueError(f"A Situation with name '{name}' already exists")

    def get_by_id(self, name: str) -> Situation:
        """
        Retrieves a situation by its unique identifier.

        Args:
            name: The unique identifier of the situation to retrieve.

        Returns:
            Situation: The Situation instance matching the given ID.

        Raises:
            ValueError: If no situation is found with the given name.
        """
        try:
            return Situation.get_by_id(name)
        except DoesNotExist:
            logger.warning(f"Situation {name} not found")
            raise ValueError(f"Situation {name} not found")

    def to_list(self) -> list[SituationDto]:
        """
        Retrieves a list of all situations in the system.

        The situations are ordered alphabetically by name (ascending).

        Returns:
            list[SituationDto]: A list of SituationDto objects representing
                all situations in the system.
        """
        query = Situation.select()
        query = query.order_by(Situation.name.asc())

        result = list()
        for res in query:
            result.append(SituationDto.from_entity(res))

        return result

    def update(self):
        """
        Updates an existing situation.

        This method is currently not implemented and serves as a placeholder
        for future functionality.

        Returns:
            None: This method is not yet implemented.
        """
        return

    def delete(self, name: str) -> bool:
        """
        Deletes a situation and removes all its relationships.

        Args:
            name: The unique identifier of the situation to delete.

        Returns:
            bool: True if the situation was successfully deleted.

        Raises:
            ValueError: If no situation is found with the given name.

        Note:
            This method uses db.atomic() to ensure the operation is
            atomic. If any part of the operation fails, the entire
            transaction is rolled back.
        """
        situation = self.get_by_id(name)

        with db.atomic():
            Model.delete().where(
                Model.situation == situation
            ).execute()

            situation.delete_instance()

        logger.info(f"Situation deleted: {name}")
        return True

    def get_models(self, name: str) -> list[ModelDto]:
        """
        Retrieves all models associated with a specific situation.

        Args:
            name: The unique identifier of the situation.

        Returns:
            list[ModelDto]: A list of ModelDto objects representing all
                models associated with the situation.

        Raises:
            ValueError: If no situation is found with the given name.
        """
        situation= self.get_by_id(name)

        query = (Model
                 .select()
                 .where(Model.situation == situation))

        result = list()
        for res in query:
            result.append(ModelDto.from_entity(res))

        return result