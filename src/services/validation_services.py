from datetime import datetime
import logging

from dtos import (ModelInfoDto,
                  CompartmentDto,
                  ParamDto)


logger = logging.getLogger(__name__)

class ValidationService:

    #Name validation
    MIN_NAME_SIZE = 8
    MAX_NAME_SIZE = 100

    #Date validation
    MAX_DATE = datetime.today()

    def IsValidModelInfo(self,model_info: ModelInfoDto) -> bool:
        if not self.validate_model_info_names(model_info):
            logger.warning("Failed Validation: Name Validation Error")
            return False
        logger.info(" Successful Validation")
        return True

    def validate_model_info_names(self, model_info: ModelInfoDto) -> bool:
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

    def validate_compartments_name(self,compartments:list[CompartmentDto]) -> bool:
        for comp in compartments:
            if not self.IsValidName(comp.name):
                logger.error(f"Invalid Compartment Name: {comp.name}")
                return False
        return True
    
    def validate_parameters_name(self,parameters:list[ParamDto]) -> bool:
        for param in parameters:
            if not self.IsValidName(param.name):
                logger.error(f"Invalid Param Name: {param.name}")
                return False
        return True
    
    def IsValidName(self,name:str) -> bool:
        if name is None:
            logger.error("Name can't be empty")
            return False
        if(len(name) >= self.MAX_NAME_SIZE):
            logger.error(f"Invalid name {name}: It must contain at most 100 characters")
            return False
        if(len(name) < self.MIN_NAME_SIZE):
            logger.error(f"Invalid name {name}: it must contain at least 8 characters")
            return False
        
        logger.info(f"Name '{name}' is valid")
        return True
    
    def IsValidDate(self,date:datetime) -> bool:
        if date is None:
            logger.error("Date can't be empty")
            return False
        if date > self.MAX_DATE:
            logger.error(f"Invalid date {date}: date can't be in the future")
            return False
        
        logger.info(f"Date '{date}' is valid")
        return True