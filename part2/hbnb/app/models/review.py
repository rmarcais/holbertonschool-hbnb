from .base import BaseModel
from .place import Place
from .user import User

class Review(BaseModel):

    def __init__(self, text, rating, place, user):
        if text is None or rating is None or place is None or user is None:
            raise ValueError("Missing required fields !")
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise ValueError("text must be a string !")
        if len(value) > 1000:
            raise ValueError("Text must not exceed 1000 characters !")
        self._text = value

    @property
    def rating(self):
        return self._rating
    
    @rating.setter
    def rating(self, value):
        if not isinstance(value, int):
            raise ValueError("Rating must be an integer !")
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5 !")
        self._rating = value

    @property
    def place(self):
        return self._place
    
    @place.setter
    def place(self, value):
        # (User existance is validated in the facade)
        if not isinstance(value, Place):
            raise ValueError("place must be a Place instance !")
        self._place = value

    @property
    def user(self):
        return self._user
    
    @user.setter
    def user(self, value):
        # (User existance is validated in the facade)
        if not isinstance(value, User):
            raise ValueError("User must be a User instance !")
        self._user = value
