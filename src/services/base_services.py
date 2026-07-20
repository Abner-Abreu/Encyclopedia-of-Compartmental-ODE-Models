from abc import abstractmethod, ABCMeta

class BaseServices(metaclass=ABCMeta):
    """
    Abstract base class for all service classes.

    This class defines the standard CRUD interface that all service 
    implementations must follow. 

    Methods:
        create(): Creates a new entity.
        get_by_id(): Retrieves an entity by its unique identifier.
        to_list(): Retrieves a list of all entities, optionally filtered.
        update(): Updates an existing entity.
        delete(): Deletes an entity by its identifier.
    """

    @abstractmethod
    def create():
        """
        Creates a new entity.

        This method should create a new entity in the system. The specific
        parameters depend on the implementing service.

        Returns:
            The created entity (type varies by implementation).

        Raises:
            ValueError: If validation fails.
            IntegrityError: If a duplicate entity already exists.
        """
        pass

    @abstractmethod
    def get_by_id():
        """
        Retrieves an entity by its unique identifier.

        Returns:
            The entity matching the given ID.

        Raises:
            DoesNotExist: If no entity is found with the given ID.
        """
        pass

    @abstractmethod
    def to_list():
        """
        Retrieves a list of all entities, optionally with filters.

        Returns:
            list: A list of all entities matching the criteria.
        """
        pass

    @abstractmethod
    def update():
        """
        Updates an existing entity.

        Raises:
            DoesNotExist: If no entity is found with the given ID.
            ValueError: If validation fails.
        """
        pass

    @abstractmethod
    def delete():
        """
        Deletes an entity by its identifier.

        Raises:
            DoesNotExist: If no entity is found with the given ID.
        """
        pass