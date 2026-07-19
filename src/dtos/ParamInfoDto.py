from .BaseDto import BaseDto

class ParamInfoDto(BaseDto):
    def __init__(self, 
                 name:str,
                 linear: bool,
                 symbol:str,
                 meaning: str):
        super().__init__(name)
        self.linear = linear
        self.symbol = symbol
        self.meaning = meaning