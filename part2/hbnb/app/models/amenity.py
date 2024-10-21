from .base import BaseModel


class Amenity(BaseModel):

    def __init__(self, name):
        if name is None:
            raise ValueError("Name is required !")
        super().__init__()
        self.name = name

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("name must be a string !")
        if len(value) > 50 or len(value) <= 0:
            raise ValueError("Name must not be empty and must not exceed 50 characters !")
        self._name = value