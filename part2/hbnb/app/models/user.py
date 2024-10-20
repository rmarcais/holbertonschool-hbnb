from .base import BaseModel
import re


class User(BaseModel):

    def __init__(self, first_name, last_name, email, is_admin=False):
        """Initialization"""
        if first_name is None or last_name is None or email is None:
            raise ValueError("Missing required fields !")
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []  # List to store related places
        self.reviews = [] # List of reviews written by the user
    
    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise ValueError("First name must be a string !")
        if len(value) > 50:
            raise ValueError("First name must not exceed 50 characters !")
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str):
            raise ValueError("Last name must be a string !")
        if len(value) > 50:
            raise ValueError("Last name must not exceed 50 characters !")
        self._last_name = value

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        # (Uniqueness of the email is validated in the facade)

        if not isinstance(value, str):
            raise ValueError("Email name must be a string !")
        
        # Regex to validate email format
        email_format = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        if not re.match(email_format, value):
            raise ValueError("Incorrect email format")
        self._email = value
    
    def add_place(self, place):
        """Add a new place to the user"""
        # (The existance of the place is validated in the facade)
        self.places.append(place)
