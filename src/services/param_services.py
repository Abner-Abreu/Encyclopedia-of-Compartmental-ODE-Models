from peewee import DoesNotExist, IntegrityError
from database import Model,Param,ModelParam,db
from typing import List,Optional,Dict,Any
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
        
    def to_list(self,filters: Optional[Dict[str,Any]] = None) -> List[Param]:

        query = Param.select()

        if filters:
            for field,value in filter:
                if field == 'name__contains':
                    query = query.where(Param.name.contains(value))
                elif field == 'name__startswith':
                    query = query.where(Param.name.startswith(value))

        query = query.order_by(Param.name.asc())
        
        return list(query)
    
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
    
    def get_models(self,name:str) -> List[Model]:
        param = self.get_by_id(name)

        query = (ModelParam
                 .select(ModelParam,Model)
                 .join(Model)
                 .where(ModelParam.param == param))
        
        return list(query)