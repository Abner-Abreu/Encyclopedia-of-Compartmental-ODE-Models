from .BaseDto import BaseDto

class SituationDto(BaseDto):
    def __init__(self, 
                 name:str,
                 description:str = None):
        super().__init__(name)
        self.description = description