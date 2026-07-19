from peewee import DoesNotExist, IntegrityError

from database import (Model,
                      Situation,
                      ModelSituation,
                      db)

from dtos import (SituationDto,
                  ModelDto)

import logging

from .base_services import BaseServices

logger = logging.getLogger(__name__)

class SituationService(BaseServices):
    def create(self,name:str,description:str):
        try:
            situation = Situation.create(name=name,description=description)
            logger.info(f"Situation created: {name}")

            return situation
        
        except IntegrityError as e:
            logger.error(f"Error when creating situation {name}: {e}")
            raise ValueError(f"A Situation with name '{name}' already exists")
        
    def get_by_id(self,name:str) -> Situation:
        try:
            return Situation.get_by_id(name)
        except DoesNotExist:
            logger.warning(f"Situation {name} not finded")
            raise ValueError(f"Situation {name} not finded")
        
    def to_list(self) -> list[SituationDto]:

        query = Situation.select()
        query = query.order_by(Situation.name.asc())
        
        result = list()
        for res in query:
            result.append(SituationDto(name=res.name,
                                       description=res.description))
            
        return result
    
    def update(self):
        return
    
    def delete(self, name:str):
        situation = self.get_by_id(name)

        with db.atomic():
            ModelSituation.delete().where(
                ModelSituation.situation == situation
            ).execute()
            
            situation.delete_instance()
        
        logger.info(f"Situation deleted: {name}")
        return True
    
    def get_models(self,name:str) -> list[ModelDto]:
        situation = self.get_by_id(name)

        query = (ModelSituation
                 .select(ModelSituation,Model)
                 .join(Model)
                 .where(ModelSituation.situation == situation))
        
        return [{
            ModelDto(name=rel.model.name)
        }for rel in query]
    
    def set_relation_to_model(self,modelName:str,situationName:str):
        try:
            model_situation = ModelSituation.create(model=modelName,situation=situationName)
            logger.info(f"Realtion Model: {modelName} - Situation: {situationName} created")

            return model_situation
        
        except IntegrityError as e:
            logger.error(f"Error when creating Realtion Model: {modelName} - Situation: {situationName}: {e}")
            raise ValueError(f"A Realtion Model: {modelName} - Situation: {situationName} cant be created")