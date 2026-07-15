from abc import abstractmethod, ABCMeta

class BaseServices(metaclass=ABCMeta):
    @abstractmethod
    def create():
        pass
    @abstractmethod
    def get_by_id():
        pass
    @abstractmethod
    def to_list():
        pass
    @abstractmethod
    def update():
        pass
    @abstractmethod
    def delete():
        pass