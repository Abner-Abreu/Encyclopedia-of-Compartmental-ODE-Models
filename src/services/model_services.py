from peewee import DoesNotExist, IntegrityError, fn
from database import (Model,Compartment, Param,Situation,Data,Article,
                      ModelArticle,ModelCompartment,ModelData,ModelParam,ModelSituation,
                      db)
from typing import List,Optional,Dict,Any
import logging

from .base_services import BaseServices

logger = logging.getLogger(__name__)

class ModelService(BaseServices):
    def create(self,name:str):
        try:
            model = Model.create(name=name)
            logger.info(f"Model created: {name}")

            return model
        
        except IntegrityError as e:
            logger.error(f"Error when creating model {name}: {e}")
            raise ValueError(f"A model with name '{name}' already exists")
        
    def get_by_id(self,name:str) -> Model:
        try:
            return Model.get_by_id(name)
        except DoesNotExist:
            logger.warning(f"Model {name} not finded")
            raise ValueError(f"Model {name} not finded")
        
    def to_list(self,filters: Optional[Dict[str,Any]] = None) -> List[Model]:

        query = Model.select()

        if filters:
            if filters['name__contains']:
                query = query.where(Model.name.contains(filters['name__contains']))
            if filters['parameter__contains']:
                query = query.where(Param.name.contains(filters['parameter__contains']))
            if filters['compartment__contains']:
                query = query.where(Compartment.name.contains(filters['compartment__contains']))
            if filters['situation__contains']:
                query = query.where(Situation.name.contains(filters['situation__contains']))
            if filters['article__contains']:
                query = query.where(Article.name.contains(filters['article__contains']))
            if filters['all__linear']:
                query = query.where(~fn.EXISTS(
                                            ModelParam
                                            .select()
                                            .where((ModelParam.model == Model.name) & 
                                            (ModelParam.lineal == False))
                                    ))

        query = query.order_by(Model.name.asc())
        
        return list(query)
    
    def update(self):
        return
    
    def delete(self, name:str):
        model = self.get_by_id(name)

        with db.atomic():
            ModelCompartment.delete().where(
                ModelCompartment.model == model
            ).execute()
            ModelParam.delete().where(
                ModelParam.model == model
            ).execute()
            ModelArticle.delete().where(
                ModelArticle.model == model
            ).execute()
            ModelSituation.delete().where(
                ModelSituation.model == model
            ).execute()
            ModelData.delete().where(
                ModelData.model == model
            ).execute()
            
            model.delete_instance()
        
        logger.info(f"Model deleted: {name}")
        return True
    
    def get_compartments(self,name:str) -> List[Dict[str, Any]]:
        model = self.get_by_id(name)

        query = (ModelCompartment
                 .select(ModelCompartment, Compartment)
                 .join(Compartment)
                 .where(ModelCompartment.model == model))

        return [{
            'name': rel.compartment.name,
            'expression': rel.compartment.expression
        } for rel in query]
        
    def get_params(self,name:str) -> List[Dict[str,Any]]:
        model = self.get_by_id(name)

        query = (ModelParam
                 .select(ModelParam, Param)
                 .join(Param)
                 .where(ModelParam.model == model))

        return [{
            'name': rel.param.name,
            'lineal': rel.lineal,
            'symbol': rel.symbol,
            'meaning': rel.meaning
        } for rel in query]   
    
    def get_article(self,name:str) -> List[Dict[str,Any]]:
        model = self.get_by_id(name)

        query = (ModelArticle
                 .select(ModelArticle, Article)
                 .join(Article)
                 .where(ModelArticle.model == model))

        return [{
            'name': rel.article.name,
            'author': rel.article.author,
            'date': rel.article.date
        } for rel in query]   
    
    def get_situation(self,name:str) -> List[Dict[str,Any]]:
        model = self.get_by_id(name)

        query = (ModelSituation
                 .select(ModelSituation, Situation)
                 .join(Situation)
                 .where(ModelSituation.model == model))

        return [{
            'name': rel.situation.name,
            'description': rel.situation.description
        } for rel in query]   
    
    def get_data(self,name:str) -> List[Dict[str,Any]]:
        model = self.get_by_id(name)

        query = (ModelData
                 .select(ModelData, Data)
                 .join(Data)
                 .where(ModelData.model == model))

        return [{
            'name': rel.data.name,
            'date': rel.data.date,
            'place': rel.data.place
        } for rel in query]   
    
    def get_all(self,name:str) -> Dict[str,Any]:
        model = self.get_by_id(name)

        return {
            'name': model.name,
            'compartments': self.get_compartments(name),
            'params': self.get_params(name),
            'situation': self.get_situation(name),
            'article': self.get_article(name),
            'data': self.get_data(name)
        }