from peewee import DoesNotExist, IntegrityError, fn

from database import (Model,
                      Compartment, 
                      Param,
                      Situation,
                      Data,
                      Article,
                      ModelArticle,
                      ModelCompartment,
                      ModelData,
                      ModelParam,
                      ModelSituation,
                      db)

from dtos import (ArticleDto,
                  CompartmentDto,
                  DataDto,
                  ModelDto,
                  ModelInfoDto,
                  ParamInfoDto,
                  SituationDto,
                  FiltersDto)
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
        
    def to_list(self,filters: FiltersDto | None = None) -> list[ModelDto]:

        query = Model.select()

        if filters:
            if filters.name_contains:
                query = query.where(Model.name.contains(filters.name_contains))
            if filters.parameter_contains:
                query = query.where(Param.name.contains(filters.parameter_contains))
            if filters.compartment_contains:
                query = query.where(Compartment.name.contains(filters.compartment_contains))
            if filters.situation_contains:
                query = query.where(Situation.name.contains(filters.situation_contains))
            if filters.article_contains:
                query = query.where(Article.name.contains(filters.article_contains))
            if filters.all_linear:
                query = query.where(~fn.EXISTS(
                                            ModelParam
                                            .select()
                                            .where((ModelParam.model == Model.name) & 
                                            (ModelParam.linear == False))
                                    ))

        query = query.order_by(Model.name.asc())
        
        result = list()
        for res in query:
            result.append(ModelDto(name=res.name))
            
        return result
    
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
    
    def get_compartments(self,name:str) -> list[CompartmentDto]:
        model = self.get_by_id(name)

        query = (ModelCompartment
                 .select(ModelCompartment, Compartment)
                 .join(Compartment)
                 .where(ModelCompartment.model == model))

        result = list()
        for res in query:
            result.append(CompartmentDto(name=res.compartment.name,
                                         expression=res.compartment.expression))
        return result  
        
    def get_params(self,name:str) -> list[ParamInfoDto]:
        model = self.get_by_id(name)

        query = (ModelParam
                 .select(ModelParam, Param)
                 .join(Param)
                 .where(ModelParam.model == model))

        result = list()
        for res in query:
            result.append(ParamInfoDto(name=res.param.name,
                                        linear=res.linear,
                                        symbol=res.symbol,
                                        meaning=res.meaning))
        return result  
    
    def get_article(self,name:str) -> ArticleDto | None:
        model = self.get_by_id(name)

        query = (ModelArticle
                 .select(ModelArticle, Article)
                 .join(Article)
                 .where(ModelArticle.model == model))

        query = list(query)
        if len(query) > 0:
            result = query[0]
            return ArticleDto(name=result.article.name,
                              author=result.article.author,
                              date=result.article.date)
        else:
            return None     
    
    def get_situation(self,name:str) -> SituationDto | None:
        model = self.get_by_id(name)

        query = (ModelSituation
                 .select(ModelSituation, Situation)
                 .join(Situation)
                 .where(ModelSituation.model == model))

        query = list(query)
        if len(query) > 0:
            result = query[0]
            return SituationDto(name=result.situation.name,
                                description=result.situation.description)
        else:
            return None     
    
    def get_data(self,name:str) -> DataDto | None:
        model = self.get_by_id(name)

        query = (ModelData
                 .select(ModelData, Data)
                 .join(Data)
                 .where(ModelData.model == model))

        query = list(query)
        if len(query) > 0:
            result = query[0]
            return DataDto(name=result.data.name,
                           date=result.data.date,
                           place=result.data.place)
        else:
            return None  
    
    def get_all(self,name:str) -> ModelInfoDto:
        model = self.get_by_id(name)

        return ModelInfoDto(name=model.name,
                            compartments=self.get_compartments(name),
                            params=self.get_params(name),
                            situation=self.get_situation(name),
                            article=self.get_article(name),
                            data=self.get_data(name))