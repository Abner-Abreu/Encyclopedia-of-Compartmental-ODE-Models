from peewee import DoesNotExist, IntegrityError

from database import (Model,
                      Data,
                      db)

from dtos import (DataDto,
                  ModelDto,
                  SituationDto,
                  ArticleDto)

import logging

from .base_services import BaseServices

logger = logging.getLogger(__name__)

class DataService(BaseServices):
    """
    Service class for managing Data entities and their relationships.

    This service provides CRUD operations for Data entities as well as
    methods for managing the relationships between data entries
    and models through the ModelData junction table.
    """

    def create(self, name: str, place: str, date):
        """
        Creates a new data entry.

        Args:
            name: Unique identifier of the data entry (primary key).
            place: Location where the data was collected.
            date: Date when the data was collected.

        Returns:
            Data: The created Data instance.

        Raises:
            ValueError: If a data entry with the same name already exists.
        """
        try:
            data = Data.create(name=name, place=place, date=date)
            logger.info(f"Data created: {name}")

            return data

        except IntegrityError as e:
            logger.error(f"Error when creating data {name}: {e}")
            raise ValueError(f"A Data with name '{name}' already exists")

    def get_by_id(self, name: str) -> Data:
        """
        Retrieves a data entry by its unique identifier.

        Args:
            name: The unique identifier of the data entry to retrieve.

        Returns:
            Data: The Data instance matching the given ID.

        Raises:
            ValueError: If no data entry is found with the given name.
        """
        try:
            return Data.get_by_id(name)
        except DoesNotExist:
            logger.warning(f"Data {name} not found")
            raise ValueError(f"Data {name} not found")

    def to_list(self) -> list[DataDto]:
        """
        Retrieves a list of all data entries in the system.

        The data entries are ordered alphabetically by name (ascending).

        Returns:
            list[DataDto]: A list of DataDto objects representing
                all data entries in the system.
        """
        query = Data.select()
        query = query.order_by(Data.name.asc())

        result = list()
        for res in query:
            result.append(DataDto.from_entity(res))

        return result

    def update(self):
        """
        Updates an existing data entry.

        This method is currently not implemented and serves as a placeholder
        for future functionality.

        Returns:
            None: This method is not yet implemented.
        """
        return

    def delete(self, name: str) -> bool:
        """
        Deletes a data entry and removes all its relationships.

        Args:
            name: The unique identifier of the data entry to delete.

        Returns:
            bool: True if the data entry was successfully deleted.

        Raises:
            ValueError: If no data entry is found with the given name.

        Note:
            This method uses db.atomic() to ensure the operation is
            atomic. If any part of the operation fails, the entire
            transaction is rolled back.
        """
        data = self.get_by_id(name)

        with db.atomic():
            Model.delete().where(
                Model.data == data
            ).execute()
            
            data.delete_instance()

        logger.info(f"Data deleted: {name}")
        return True

    def get_models(self, name: str) -> list[ModelDto]:
        """
        Retrieves all models associated with a specific data entry.

        Args:
            name: The unique identifier of the data entry.

        Returns:
            list[ModelDto]: A list of ModelDto objects representing all
                models associated with the data entry.

        Raises:
            ValueError: If no data entry is found with the given name.
        """
        data = self.get_by_id(name)

        query = (Model
                 .select()
                 .where(Model.data == data))

        result = list()
        for res in query:
            result.append(ModelDto.from_entity(res))

        return result