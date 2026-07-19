from .article_services import ArticleService
from .data_services import DataService
from .model_services import ModelService
from .param_services import ParamService
from .situation_services import SituationService
from .validation_services import ValidationService
from .compartment_services import CompartmentService

from dtos import ModelInfoDto
import logging

logger = logging.getLogger(__name__)

class ServiceHandler:
    def __init__(self):
        self.article = ArticleService()
        self.data = DataService()
        self.model = ModelService()
        self.param = ParamService()
        self.situation = SituationService()
        self.validation = ValidationService()
        self.compartment = CompartmentService()

    def create_complete(self, model_info: ModelInfoDto ):
        
        #Basic name validation
        if not self.validation.IsValidModelInfo(model_info):
            logger.error(f"Model {model_info.name} not created: Validation Error")
            return False
        
        #Model
        try:
            self.model.create(model_info.name)        
        except:
            logger.error(f"Model {model_info.name} already exist")
            return False

        #Article
        try:
            self.article.get_by_id(model_info.article.name)
        except:
            self.article.create(name=model_info.article.name,
                                author=model_info.article.author,
                                date=model_info.article.date)
            
        self.article.set_relation_to_model(modelName=model_info.name,
                                           articleName=model_info.article.name)
        
        #Situation
        try:
            self.situation.get_by_id(model_info.situation.name)
        except:
            self.situation.create(name=model_info.situation.name,
                                  description=model_info.situation.description)
            
        self.situation.set_relation_to_model(modelName=model_info.name,
                                             situationName=model_info.situation.name)
        
        #Data
        if model_info.data:
            try:
                self.data.get_by_id(model_info.data.name)
            except:
                self.data.create(name=model_info.data.name,
                                 place=model_info.data.place,
                                 date=model_info.data.date)
            
            self.data.set_relation_to_model(modelName=model_info.name,
                                            dataName=model_info.data.name)
            
        #Compartments
        for comp in model_info.compartments:
            try:
                self.compartment.get_by_id(comp.name)
            except:
                self.compartment.create(name=comp.name,
                                        expression=comp.expression)
            
            self.compartment.set_relation_to_model(modelName=model_info.name,
                                                   compartmentName=comp.name)
        
        #Params
        for par in model_info.params:
            try:
                self.param.get_by_id(par.name)
            except:
                self.param.create(name=par.name)
            
            self.param.set_relation_to_model(modelName=model_info.name,
                                             paramName=par.name,
                                             linear=par.linear,
                                             meaning=par.meaning,
                                             symbol=par.symbol)
            
        logger.info(f"Model {model_info.name} created")
        return True