from peewee import DoesNotExist, IntegrityError
from database import Model,Compartment,ModelCompartment,db
from typing import List,Optional,Dict,Any
import logging

from .base_services import BaseServices

logger = logging.getLogger(__name__)

class CompartmentService(BaseServices):
    def create(self,name:str,expression:str):
        try:
            compartment = Compartment.create(name=name,expression=expression)
            logger.info(f"Param created: {name}")

            return compartment
        
        except IntegrityError as e:
            logger.error(f"Error when creating compartment {name}: {e}")
            raise ValueError(f"A Compartment with name '{name}' already exists")
        
    def get_by_id(self,name:str) -> Compartment:
        try:
            return Compartment.get_by_id(name)
        except DoesNotExist:
            logger.warning(f"Compartment {name} not finded")
            raise ValueError(f"Compartment {name} not finded")
        
    def to_list(self,filters: Optional[Dict[str,Any]] = None) -> List[Compartment]:

        query = Compartment.select()

        if filters:
            for field,value in filter:
                if field == 'name__contains':
                    query = query.where(Compartment.name.contains(value))
                elif field == 'name__startswith':
                    query = query.where(Compartment.name.startswith(value))

        query = query.order_by(Compartment.name.asc())
        
        return list(query)
    
    def update(self):
        return
    
    def delete(self, name:str):
        compartment= self.get_by_id(name)

        with db.atomic():
            ModelCompartment.delete().where(
                ModelCompartment.compartment == compartment
            ).execute()
            
            compartment.delete_instance()
        
        logger.info(f"Compartment deleted: {name}")
        return True
    
    def get_models(self,name:str) -> List[Model]:
        compartment = self.get_by_id(name)

        query = (ModelCompartment
                 .select(ModelCompartment,Model)
                 .join(Model)
                 .where(ModelCompartment.compartment == compartment))
        
        return list(query)
    
    def set_relation_to_model(self,modelName:str,compartmentName:str):
        try:
            model_data = ModelCompartment.create(model=modelName,compartment=compartmentName)
            logger.info(f"Realtion Model: {modelName} - Compartment: {compartmentName} created")

            return model_data
        
        except IntegrityError as e:
            logger.error(f"Error when creating Realtion Model: {modelName} - Compartment: {compartmentName}: {e}")
            raise ValueError(f"A Realtion Model: {modelName} - Compartment: {compartmentName} cant be created")