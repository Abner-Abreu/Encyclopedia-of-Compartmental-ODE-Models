from typing import List,Optional,Dict,Any
from datetime import datetime,date
import logging

logger = logging.getLogger(__name__)

class ValidationService:

    #Name validation
    MIN_NAME_SIZE = 8
    MAX_NAME_SIZE = 100

    #Date validation
    MAX_DATE = date.today


    def IsValidName(self,name:str) -> bool:
        if name is None:
            logger.error("Name can't be empty")
            return False
        if(name.count >= self.MAX_NAME_SIZE):
            logger.error(f"Invalid name {name}: It must contain at most 100 characters")
            return False
        if(name.count < self.MIN_NAME_SIZE):
            logger.error(f"Invalid name {name}: it must contain at least 8 characters")
            return False
        
        logger.info(f"Name '{name}' is valid")
        return True
    
    def IsValidDate(self,date:date) -> bool:
        if date is None:
            logger.error("Date can't be empty")
            return False
        if(date > self.MAX_DATE):
            logger.error(f"Invalid date {date}: date can't be in the future")
            return False
        
        logger.info(f"Date '{date}' is valid")
        return True