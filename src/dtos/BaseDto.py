from abc import ABC

class BaseDto(ABC):
    def __init__(self, name:str):
        self.name = name