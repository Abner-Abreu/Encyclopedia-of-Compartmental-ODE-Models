from peewee import DoesNotExist, IntegrityError

from database import (Model,
                      Data,
                      ModelData,
                      db)

from dtos import (DataDto,
                  ModelDto)

import logging

from .base_services import BaseServices

logger = logging.getLogger(__name__)

class DataService(BaseServices):
    def create(self,name:str,place:str,date):
        try:
            data = Data.create(name=name,place=place,date=date)
            logger.info(f"Param created: {name}")

            return data
        
        except IntegrityError as e:
            logger.error(f"Error when creating data {name}: {e}")
            raise ValueError(f"A Data with name '{name}' already exists")
        
    def get_by_id(self,name:str) -> Data:
        try:
            return Data.get_by_id(name)
        except DoesNotExist:
            logger.warning(f"Data {name} not finded")
            raise ValueError(f"Data {name} not finded")
        
    def to_list(self) -> list[DataDto]:

        query = Data.select()
        query = query.order_by(Data.name.asc())
        
        result = list()
        for res in query:
            result.append(DataDto(name=res.name,
                                  date=res.date,
                                  place=res.place))
            
        return result
    
    def update(self):
        return
    
    def delete(self, name:str):
        data = self.get_by_id(name)

        with db.atomic():
            ModelData.delete().where(
                ModelData.data == data
            ).execute()
            
            data.delete_instance()
        
        logger.info(f"Data deleted: {name}")
        return True
    
    def get_models(self,name:str) -> list[ModelDto]:
        data = self.get_by_id(name)

        query = (ModelData
                 .select(ModelData,Model)
                 .join(Model)
                 .where(ModelData.data == data))
        
        return [{
            ModelDto(name=rel.model.name)
        }for rel in query]
    
    def set_relation_to_model(self,modelName:str,dataName:str):
        try:
            model_data = ModelData.create(model=modelName,data=dataName)
            logger.info(f"Realtion Model: {modelName} - Data: {dataName} created")

            return model_data
        
        except IntegrityError as e:
            logger.error(f"Error when creating Realtion Model: {modelName} - Data: {dataName}: {e}")
            raise ValueError(f"A Realtion Model: {modelName} - Data: {dataName} cant be created")