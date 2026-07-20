from peewee import ForeignKeyField,CompositeKey, BooleanField, TextField, CharField
from .base import BaseModel
from .model import Model
from .param import Param

class ModelParam(BaseModel):
    """
    Represents the relationship between models and parameters.

    This junction table connects a mathematical model to its parameters,
    storing additional metadata about each relationship.

    The relationship stores important information about how each parameter
    behaves within the model, including whether the relationship is linear,
    the mathematical symbol used, and the physical meaning of the parameter.

    Attributes:
        model (ForeignKeyField): Reference to the associated Model.
        param (ForeignKeyField): Reference to the associated Param.
        linear (BooleanField): Indicates whether the model is linear with
            respect to this parameter.
        meaning (TextField): Physical or mathematical description of the
            parameter's meaning in the context of the model.
        symbol (CharField): LaTeX symbol representing the parameter
            (e.g., '\\alpha', '\\omega_0', '\\pi').

    Relationships:
        - model.backref 'params': Access to all parameters of a given
          model with their relationship metadata.
        - param.backref 'models': Access to all models that use a given
          parameter with their relationship metadata.

    Note:
        This table uses a composite primary key (model, param) to
        ensure uniqueness. Peewee will raise an IntegrityError if you
        attempt to create a duplicate relationship.
    """

    model = ForeignKeyField(Model, backref='params')
    param = ForeignKeyField(Param, backref='models')

    linear = BooleanField()
    meaning = TextField()
    symbol = CharField(max_length=100)
    
    class Meta:
        primary_key = CompositeKey('model', 'param')