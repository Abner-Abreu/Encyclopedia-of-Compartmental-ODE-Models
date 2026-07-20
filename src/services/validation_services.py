from datetime import datetime
import logging

from dtos import (ModelInfoDto,
                  CompartmentDto,
                  ParamDto)


logger = logging.getLogger(__name__)

class ValidationService:
    """
    Service class for validating model data and related entities.

    This service provides validation methods for all entities in the system:
    models, compartments, parameters, articles, situations, and data.
    It ensures that data meets business rules before being persisted to
    the database.

    The service validates:
        - Name length (between 8 and 100 characters)
        - Name is not None or empty
        - Dates are not in the future
        - All fields are properly formatted

    Validation is performed at the DTO level before passing data to
    the service layer for persistence.

    Attributes:
        MIN_NAME_SIZE (int): Minimum allowed length for a name (8 characters).
        MAX_NAME_SIZE (int): Maximum allowed length for a name (100 characters).
        MAX_DATE (datetime): Maximum allowed date (today's date).

    Note:
        All validation methods log warnings for invalid data and
        return False when validation fails. Successful validations
        are logged at INFO level.
    """

    # Name validation constants
    MIN_NAME_SIZE = 8
    MAX_NAME_SIZE = 100

    # Date validation constants
    MAX_DATE = datetime.today()

    def IsValidModelInfo(self, model_info: ModelInfoDto) -> bool:
        """
        Validates all data within a ModelInfoDto.

        This method performs comprehensive validation on all fields
        of the ModelInfoDto, including nested objects (compartments,
        parameters, situation, article, data).

        Args:
            model_info: The ModelInfoDto to validate.

        Returns:
            bool: True if all validation passes, False otherwise.
        """
        if not self.validate_model_info_names(model_info):
            logger.warning("Failed Validation: Name Validation Error")
            return False
        logger.info("Successful Validation")
        return True

    def validate_model_info_names(self, model_info: ModelInfoDto) -> bool:
        """
        Validates all name and date fields within a ModelInfoDto.

        This method calls individual validation methods for each field
        within the ModelInfoDto and its nested objects.

        Args:
            model_info: The ModelInfoDto to validate.

        Returns:
            bool: True if all validation passes, False otherwise.

        Note:
            This method short-circuits and returns False on the first
            validation failure, logging the specific error.
        """
        if not self.IsValidName(model_info.name):
            logger.error(f"Invalid Model Name: {model_info.name}")
            return False
        elif not self.IsValidName(model_info.situation.name):
            logger.error(f"Invalid Situation Name: {model_info.situation.name}")
            return False
        elif not self.IsValidName(model_info.article.name):
            logger.error(f"Invalid Article Name: {model_info.article.name}")
            return False
        elif not self.IsValidName(model_info.article.author):
            logger.error(f"Invalid Article Author: {model_info.article.author}")
            return False
        elif not self.IsValidDate(model_info.article.date):
            logger.error(f"Invalid Article Date: {model_info.article.date}")
            return False
        elif not self.IsValidName(model_info.data.name):
            logger.error(f"Invalid Data Name: {model_info.data.name}")
            return False
        elif not self.IsValidDate(model_info.data.date):
            logger.error(f"Invalid Data Date: {model_info.data.date}")
            return False
        elif not self.validate_compartments_name(model_info.compartments):
            return False
        elif not self.validate_parameters_name(model_info.params):
            return False

        return True

    def validate_compartments_name(self, compartments: list[CompartmentDto]) -> bool:
        """
        Validates all compartment names in a list.

        Args:
            compartments: List of CompartmentDto objects to validate.

        Returns:
            bool: True if all compartment names are valid, False otherwise.

        Note:
            Returns False on the first invalid name found.
        """
        for comp in compartments:
            if not self.IsValidName(comp.name):
                logger.error(f"Invalid Compartment Name: {comp.name}")
                return False
        return True

    def validate_parameters_name(self, parameters: list[ParamDto]) -> bool:
        """
        Validates all parameter names in a list.

        Args:
            parameters: List of ParamDto objects to validate.

        Returns:
            bool: True if all parameter names are valid, False otherwise.

        Note:
            Returns False on the first invalid name found.
        """
        for param in parameters:
            if not self.IsValidName(param.name):
                logger.error(f"Invalid Param Name: {param.name}")
                return False
        return True

    def IsValidName(self, name: str) -> bool:
        """
        Validates a name against length requirements.

        A valid name must:
            - Not be None or empty
            - Be at least MIN_NAME_SIZE characters long
            - Be at most MAX_NAME_SIZE characters long

        Args:
            name: The name string to validate.

        Returns:
            bool: True if the name is valid, False otherwise.
        """
        if name is None:
            logger.error("Name can't be empty")
            return False
        if len(name) >= self.MAX_NAME_SIZE:
            logger.error(f"Invalid name {name}: It must contain at most {self.MAX_NAME_SIZE} characters")
            return False
        if len(name) < self.MIN_NAME_SIZE:
            logger.error(f"Invalid name {name}: it must contain at least {self.MIN_NAME_SIZE} characters")
            return False

        logger.info(f"Name '{name}' is valid")
        return True

    def IsValidDate(self, date: datetime) -> bool:
        """
        Validates a date against business rules.

        A valid date must:
            - Not be None
            - Not be in the future (must be <= today's date)

        Args:
            date: The datetime object to validate.

        Returns:
            bool: True if the date is valid, False otherwise.
        """
        if date is None:
            logger.error("Date can't be empty")
            return False
        if date > self.MAX_DATE:
            logger.error(f"Invalid date {date}: date can't be in the future")
            return False

        logger.info(f"Date '{date}' is valid")
        return True