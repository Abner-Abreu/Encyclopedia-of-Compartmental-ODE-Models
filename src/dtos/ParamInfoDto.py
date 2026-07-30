from .ParamDto import ParamDto

class ParamInfoDto(ParamDto):
    """
    Data Transfer Object for parameter information within a model context.

    This DTO encapsulates the detailed information about a parameter as it
    relates to a specific model. Unlike the base ParamDto which contains
    only basic parameter data, this DTO includes the relationship metadata
    that describes how the parameter behaves within the model context.

    It is used primarily when displaying model details, showing not just
    which parameters a model has, but also their linearity, symbol, and
    physical meaning specific to that model.

    Attributes:
        name (str): Unique identifier of the parameter (inherited from BaseDto).
        linear (bool): Indicates whether the model is linear with respect
            to this parameter.
        symbol (str): Symbol representing the parameter in the
            context of this model (e.g., '\\alpha', '\\omega_0').
        meaning (str): Physical or mathematical description of the
            parameter's meaning in the context of this model.
    """
    def __init__(self, 
                 name:str,
                 linear: bool,
                 symbol:str,
                 meaning: str):
        super().__init__(name)
        self.linear = linear
        self.symbol = symbol
        self.meaning = meaning