from .BaseDto import BaseDto

class CompartmentDto(BaseDto):
    def __init__(self, 
                 name:str,
                 expression:str):
        super().__init__(name)
        self.expression = expression