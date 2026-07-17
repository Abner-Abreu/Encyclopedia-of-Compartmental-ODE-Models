from .article_services import ArticleService
from .data_services import DataService
from .model_services import ModelService
from .param_services import ParamService
from .situation_services import SituationService
from .validation_services import ValidationService
from .compartment_services import CompartmentService

from typing import Dict, Any
from datetime import date

class ServiceHandler:
    def __init__(self):
        self.article = ArticleService()
        self.data = DataService()
        self.model = ModelService()
        self.param = ParamService()
        self.situation = SituationService()
        self.validation = ValidationService()
        self.compartment = CompartmentService()

    def create_complete(self,
                        name:str,
                        compartments: list[Dict[str,str]],
                        parameters: list[Dict[str,Any]],
                        situation_name: str,
                        situation_description: str,
                        article_name: str,
                        article_author: str,
                        article_date: str,
                        data_name: str,
                        data_place: str,
                        data_date: str):
        
        #Basic validation
        if (self.validation.IsValidName(name) == False):
            return False
        elif self.validation.IsValidName(situation_name) == False:
            return False
        elif self.validation.IsValidName(article_name) == False:
            return False
        elif self.validation.IsValidName(article_author) == False:
            return False
        elif self.validation.IsValidName(data_name) == False:
            return False
        elif self.validation.IsValidDate(article_date) == False:
            return False
        elif self.validation.IsValidDate(data_date) == False:
            return False
        try:
            self.model.get_by_id(name)
            return False
        except:
            self.validate_compartments(compartments)
            self.validate_parameters(parameters)

        
        
        return


        
        

    def validate_compartments(self,compartments:list[Dict[str,Any]]):
        for comp in compartments:
            try:
                self.compartment.get_by_id(comp['name'])
                return False
            except:
                continue
        return True
    
    def validate_parameters(self,parameters:list[Dict[str,Any]]):
        for param in parameters:
            try:
                self.compartment.get_by_id(param['name'])
                return False
            except:
                continue
        return True
        