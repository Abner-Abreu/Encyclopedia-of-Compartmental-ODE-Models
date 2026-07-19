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
    def create(self,name:str):
        try:
            param = Param.create(name=name)
            logger.info(f"Param created: {name}")

            return param
        
        except IntegrityError as e:
            logger.error(f"Error when creating param {name}: {e}")
            raise ValueError(f"A Param with name '{name}' already exists")
        
    def get_by_id(self,name:str) -> Param:
        try:
            return Param.get_by_id(name)
        except DoesNotExist:
            logger.warning(f"Param {name} not finded")
            raise ValueError(f"Param {name} not finded")
        
    def to_list(self) -> list[ParamDto]:

        query = Param.select()
        query = query.order_by(Param.name.asc())

        result = list()
        result = list()
        for res in query:
            result.append(ParamDto(name=res.name))
            
        return result
    
    def update(self):
        return
    
    def delete(self, name:str):
        param = self.get_by_id(name)

        with db.atomic():
            ModelParam.delete().where(
                ModelParam.param == param
            ).execute()
            
            param.delete_instance()
        
        logger.info(f"Article deleted: {name}")
        return True
    
    def get_models(self,name:str) -> list[ModelDto]:
        param = self.get_by_id(name)

        query = (ModelParam
                 .select(ModelParam,Model)
                 .join(Model)
                 .where(ModelParam.param == param))
        
        return [{
            ModelDto(name=rel.model.name)
        }for rel in query]
    
    def set_relation_to_model(self,
                              modelName:str,
                              paramName:str,
                              linear:bool,
                              meaning:str,
                              symbol:str):
        try:
            model_param = ModelParam.create(model=modelName,
                                            param=paramName,
                                            linear=linear,
                                            meaning=meaning,
                                            symbol=symbol)
            logger.info(f"Realtion Model: {modelName} - Param: {paramName} created")

            return model_param
        
        except IntegrityError as e:
            logger.error(f"Error when creating Realtion Model: {modelName} - Param: {paramName}: {e}")
            raise ValueError(f"A Realtion Model: {modelName} - Param: {paramName} cant be created")