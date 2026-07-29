from peewee import ForeignKeyField,CompositeKey
from .base import BaseModel
from .model import Model
from .situation import Situation

class ModelSituation(BaseModel):
    """
    Represents the many-to-many relationship between models and situations.

    This junction table connects a mathematical model to the situations
    or scenarios under which it is studied.

    Situations define the specific conditions, initial states, or
    environmental factors that are relevant when analyzing a model.

    Attributes:
        model (ForeignKeyField): Reference to the associated Model.
        situation (ForeignKeyField): Reference to the associated Situation.

    Relationships:
        - model.backref 'situations': Access to all situations applicable
          to a given model.
        - situation.backref 'models': Access to all models that are
          studied under a given situation.

    Note:
        This table uses a composite primary key (model, situation) to
        ensure uniqueness. Peewee will raise an IntegrityError if you
        attempt to create a duplicate relationship.
    """
    model = ForeignKeyField(Model, backref='situations')
    situation = ForeignKeyField(Situation, backref='models')
    
    class Meta:
        primary_key = CompositeKey('model', 'situation')