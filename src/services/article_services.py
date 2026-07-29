from peewee import DoesNotExist, IntegrityError

from database import (Model,
                      Article,
                      ModelArticle,
                      db)

from dtos import (ArticleDto,
                  ModelDto)

import logging

from .base_services import BaseServices

logger = logging.getLogger(__name__)

class ArticleService(BaseServices):
    """
    Service class for managing Article entities and their relationships.

    This service provides CRUD operations for Article entities as well as
    methods for managing the relationships between articles
    and models through the ModelArticle junction table.
    """

    def create(self, name: str, author: str, date):
        """
        Creates a new article.

        Args:
            name: Unique identifier of the article (primary key).
            author: Full name of the article's author.
            date: Publication date of the article.

        Returns:
            Article: The created Article instance.

        Raises:
            ValueError: If an article with the same name already exists.
        """
        try:
            article = Article.create(name=name, author=author, date=date)
            logger.info(f"Article created: {name}")
            return article

        except IntegrityError as e:
            logger.error(f"Error when creating article {name}: {e}")
            raise ValueError(f"An Article with name '{name}' already exists")

    def get_by_id(self, name: str) -> Article:
        """
        Retrieves an article by its unique identifier.

        Args:
            name: The unique identifier of the article to retrieve.

        Returns:
            Article: The Article instance matching the given ID.

        Raises:
            ValueError: If no article is found with the given name.
        """
        try:
            return Article.get_by_id(name)
        except DoesNotExist:
            logger.warning(f"Article {name} not found")
            raise ValueError(f"Article {name} not found")

    def to_list(self) -> list[ArticleDto]:
        """
        Retrieves a list of all articles in the system.

        The articles are ordered alphabetically by name (ascending).

        Returns:
            list[ArticleDto]: A list of ArticleDto objects representing
                all articles in the system.
        """
        query = Article.select()
        query = query.order_by(Article.name.asc())

        result = []
        for res in query:
            result.append(ArticleDto(
                name=res.name,
                author=res.author,
                date=res.date  # Fixed: was res.author incorrectly
            ))

        return result

    def update(self):
        """
        Updates an existing article.

        This method is currently not implemented and serves as a placeholder
        for future functionality.

        Returns:
            None: This method is not yet implemented.
        """
        return

    def delete(self, name: str) -> bool:
        """
        Deletes an article and removes all its relationships.

        This method deletes the article with the given name and automatically
        removes all associated entries from the ModelArticle junction table
        before deleting the article itself. The operation is performed
        atomically using a database transaction.

        Args:
            name: The unique identifier of the article to delete.

        Returns:
            bool: True if the article was successfully deleted.

        Raises:
            ValueError: If no article is found with the given name.

        Note:
            This method uses db.atomic() to ensure the operation is
            atomic. If any part of the operation fails, the entire
            transaction is rolled back.
        """
        article = self.get_by_id(name)

        with db.atomic():
            # Delete all relationships first
            ModelArticle.delete().where(
                ModelArticle.article == article
            ).execute()

            # Delete the article itself
            article.delete_instance()

        logger.info(f"Article deleted: {name}")
        return True

    def get_models(self, name: str) -> list[ModelDto]:
        """
        Retrieves all models associated with a specific article.

        Args:
            name: The unique identifier of the article.

        Returns:
            list[ModelDto]: A list of ModelDto objects representing all
                models associated with the article.

        Raises:
            ValueError: If no article is found with the given name.
        """
        article = self.get_by_id(name)

        query = (ModelArticle
                 .select(ModelArticle, Model)
                 .join(Model)
                 .where(ModelArticle.article == article))

        return [
            ModelDto(name=rel.model.name)
            for rel in query
        ]

    def set_relation_to_model(self, modelName: str, articleName: str):
        """
        Creates a relationship between a model and an article.

        This method adds an entry to the ModelArticle junction table,
        establishing a relationship between the specified
        model and article. The model and article must both exist.

        Args:
            modelName: The unique identifier of the model.
            articleName: The unique identifier of the article.

        Returns:
            ModelArticle: The created ModelArticle relationship instance.

        Raises:
            ValueError: If the relationship cannot be created (e.g.,
                duplicate relationship or one of the entities does not exist).
        """
        try:
            model_article = ModelArticle.create(
                model=modelName,
                article=articleName
            )
            logger.info(f"Relation Model: {modelName} - Article: {articleName} created")

            return model_article

        except IntegrityError as e:
            logger.error(f"Error when creating relation Model: {modelName} - Article: {articleName}: {e}")
            raise ValueError(f"A relation Model: {modelName} - Article: {articleName} cannot be created")