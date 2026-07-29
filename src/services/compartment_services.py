from peewee import DoesNotExist, IntegrityError

from database import (Model,
                      Compartment,
                      ModelCompartment,
                      db)

from dtos import (CompartmentDto,
                  ModelDto)

import logging

from .base_services import BaseServices

logger = logging.getLogger(__name__)

class CompartmentService(BaseServices):
    """
    Service class for managing Compartment entities and their relationships.

    This service provides CRUD operations for Compartment entities as well as
    methods for managing the relationships between compartments
    and models through the ModelCompartment junction table.
    """

    def create(self, name: str, expression: str):
        """
        Creates a new compartment.

        Args:
            name: Unique identifier of the compartment (primary key).
            expression: Mathematical expression defining the compartment's
                behavior or state in LaTeX notation.

        Returns:
            Compartment: The created Compartment instance.

        Raises:
            ValueError: If a compartment with the same name already exists.
        """
        try:
            compartment = Compartment.create(name=name, expression=expression)
            logger.info(f"Compartment created: {name}")

            return compartment

        except IntegrityError as e:
            logger.error(f"Error when creating compartment {name}: {e}")
            raise ValueError(f"A Compartment with name '{name}' already exists")

    def get_by_id(self, name: str) -> Compartment:
        """
        Retrieves a compartment by its unique identifier.

        Args:
            name: The unique identifier of the compartment to retrieve.

        Returns:
            Compartment: The Compartment instance matching the given ID.

        Raises:
            ValueError: If no compartment is found with the given name.
        """
        try:
            return Compartment.get_by_id(name)
        except DoesNotExist:
            logger.warning(f"Compartment {name} not found")
            raise ValueError(f"Compartment {name} not found")

    def to_list(self) -> list[CompartmentDto]:
        """
        Retrieves a list of all compartments in the system.

        The compartments are ordered alphabetically by name (ascending).

        Returns:
            list[CompartmentDto]: A list of CompartmentDto objects representing
                all compartments in the system.
        """
        query = Compartment.select()
        query = query.order_by(Compartment.name.asc())

        result = []
        for res in query:
            result.append(CompartmentDto(
                name=res.name,
                expression=res.expression
            ))

        return result

    def update(self):
        """
        Updates an existing compartment.

        This method is currently not implemented and serves as a placeholder
        for future functionality.

        Returns:
            None: This method is not yet implemented.
        """
        return

    def delete(self, name: str) -> bool:
        """
        Deletes a compartment and removes all its relationships.

        This method deletes the compartment with the given name and automatically
        removes all associated entries from the ModelCompartment junction table
        before deleting the compartment itself. The operation is performed
        atomically using a database transaction.

        Args:
            name: The unique identifier of the compartment to delete.

        Returns:
            bool: True if the compartment was successfully deleted.

        Raises:
            ValueError: If no compartment is found with the given name.

        Note:
            This method uses db.atomic() to ensure the operation is
            atomic. If any part of the operation fails, the entire
            transaction is rolled back.
        """
        compartment = self.get_by_id(name)

        with db.atomic():
            # Delete all relationships first
            ModelCompartment.delete().where(
                ModelCompartment.compartment == compartment
            ).execute()

            # Delete the compartment itself
            compartment.delete_instance()

        logger.info(f"Compartment deleted: {name}")
        return True

    def get_models(self, name: str) -> list[ModelDto]:
        """
        Retrieves all models associated with a specific compartment.

        Args:
            name: The unique identifier of the compartment.

        Returns:
            list[ModelDto]: A list of ModelDto objects representing all
                models associated with the compartment.

        Raises:
            ValueError: If no compartment is found with the given name.
        """
        compartment = self.get_by_id(name)

        query = (ModelCompartment
                 .select(ModelCompartment, Model)
                 .join(Model)
                 .where(ModelCompartment.compartment == compartment))

        return [
            ModelDto(name=rel.model.name)
            for rel in query
        ]

    def set_relation_to_model(self, modelName: str, compartmentName: str):
        """
        Creates a relationship between a model and a compartment.

        This method adds an entry to the ModelCompartment junction table,
        establishing a relationship between the specified
        model and compartment. The model and compartment must both exist.

        Args:
            modelName: The unique identifier of the model.
            compartmentName: The unique identifier of the compartment.

        Returns:
            ModelCompartment: The created ModelCompartment relationship instance.

        Raises:
            ValueError: If the relationship cannot be created (e.g.,
                duplicate relationship or one of the entities does not exist).
        """
        try:
            model_compartment = ModelCompartment.create(
                model=modelName,
                compartment=compartmentName
            )
            logger.info(f"Relation Model: {modelName} - Compartment: {compartmentName} created")

            return model_compartment

        except IntegrityError as e:
            logger.error(f"Error when creating relation Model: {modelName} - Compartment: {compartmentName}: {e}")
            raise ValueError(f"A relation Model: {modelName} - Compartment: {compartmentName} cannot be created")