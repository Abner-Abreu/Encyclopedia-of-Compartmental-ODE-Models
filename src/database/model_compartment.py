from peewee import ForeignKeyField,CompositeKey
from .base import BaseModel
from .model import Model
from .compartment import Compartment

class ModelCompartment(BaseModel):
    """
    Represents the relationship between models and compartments.

    This junction table connects a mathematical model to its associated
    compartments.

    The relationship defines the structural decomposition of a model
    into its constituent compartments.

    Attributes:
        model (ForeignKeyField): Reference to the associated Model.
        compartment (ForeignKeyField): Reference to the associated Compartment.

    Relationships:
        - model.backref 'compartments': Access to all compartments
          associated with a given model.
        - compartment.backref 'models': Access to all models that
          contain a given compartment.

    Note:
        This table uses a composite primary key (model, compartment) to
        ensure uniqueness. Peewee will raise an IntegrityError if you
        attempt to create a duplicate relationship.
    """
    model = ForeignKeyField(Model, backref='compartments')
    compartment = ForeignKeyField(Compartment, backref='models')
    
    class Meta:
        primary_key = CompositeKey('model', 'compartment')