from peewee import DoesNotExist, IntegrityError
from database import Model,Article,ModelArticle,db
from typing import List,Optional,Dict,Any
import logging

from .base_services import BaseServices

logger = logging.getLogger(__name__)

class ArticleService(BaseServices):
    def create(self,name:str,author:str,date):
        try:
            article = Article.create(name=name,author=author,date=date)
            logger.info(f"Article created: {name}")

            return article
        
        except IntegrityError as e:
            logger.error(f"Error when creating article {name}: {e}")
            raise ValueError(f"An Article with name '{name}' already exists")
        
    def get_by_id(self,name:str) -> Article:
        try:
            return Article.get_by_id(name)
        except DoesNotExist:
            logger.warning(f"Article {name} not finded")
            raise ValueError(f"Article {name} not finded")
        
    def to_list(self,filters: Optional[Dict[str,Any]] = None) -> List[Article]:

        query = Article.select()

        if filters:
            for field,value in filter:
                if field == 'name__contains':
                    query = query.where(Article.name.contains(value))
                elif field == 'name__startswith':
                    query = query.where(Article.name.startswith(value))

        query = query.order_by(Article.name.asc())
        
        return list(query)
    
    def update(self):
        return
    
    def delete(self, name:str):
        article = self.get_by_id(name)

        with db.atomic():
            ModelArticle.delete().where(
                ModelArticle.article == article
            ).execute()
            
            article.delete_instance()
        
        logger.info(f"Article deleted: {name}")
        return True
    
    def get_models(self,name:str) -> List[Model]:
        article = self.get_by_id(name)

        query = (ModelArticle
                 .select(ModelArticle,Model)
                 .join(Model)
                 .where(ModelArticle.article == article))
        
        return list(query)

    def set_relation_to_model(self,modelName:str,articleName:str):
        try:
            model_article = ModelArticle.create(model=modelName,article=articleName)
            logger.info(f"Realtion Model: {modelName} - Article: {articleName} created")

            return model_article
        
        except IntegrityError as e:
            logger.error(f"Error when creating Realtion Model: {modelName} - Article: {articleName}: {e}")
            raise ValueError(f"A Realtion Model: {modelName} - Article: {articleName} cant be created")