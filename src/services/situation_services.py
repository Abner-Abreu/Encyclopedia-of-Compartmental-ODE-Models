from peewee import DoesNotExist, IntegrityError
from database import Model,Situation,ModelSituation,db
from typing import List,Optional,Dict,Any
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
        
    def to_list(self,filters: Optional[Dict[str,Any]] = None) -> List[Situation]:

        query = Situation.select()

        if filters:
            for field,value in filter:
                if field == 'name__contains':
                    query = query.where(Situation.name.contains(value))
                elif field == 'name__startswith':
                    query = query.where(Situation.name.startswith(value))

        query = query.order_by(Situation.name.asc())
        
        return list(query)
    
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
    
    def get_models(self,name:str) -> List[Model]:
        situation = self.get_by_id(name)

        query = (ModelSituation
                 .select(ModelSituation,Model)
                 .join(Model)
                 .where(ModelSituation.situation == situation))
        
        return list(query)