from .base import BaseModel
from .user import User


class Place(BaseModel):

    def __init__(self, title, description, price, latitude, longitude, owner):
        if title is None or price is None or latitude is None \
            or longitude is None or owner is None:
            raise ValueError("Missing required fields !")
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise ValueError("Title must be a string !")
        if len(value) > 50 or len(value) <= 0:
            raise ValueError("Title must not be empty and must not exceed 100 characters !")
        self._title = value
    
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        if value is not None:
            if not isinstance(value, str):
                raise ValueError("Last name must be a string !")
            if len(value) > 1000:
                raise ValueError("Last name must not exceed 1000 characters !")
        self._description = value

    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        if not isinstance(value, float):
            raise ValueError("Price must be a float !")
        if value < 0:
            raise ValueError("Price must be positive !")
        self._price = value

    @property
    def latitude(self):
        return self._latitude
    
    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, float):
            raise ValueError("Latitude must be a float !")
        if value < -90 or value > 90:
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude
    
    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, float):
            raise ValueError("Longitude must be a float !")
        if value < -180 or value > 180:
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = value

    @property
    def owner(self):
        return self._owner
    
    @owner.setter
    def owner(self, value):
        # (User existance is validated in the facade)
        if not isinstance(value, User):
            raise ValueError("Owner must be a User instance !")
        self._owner = value

    def add_review(self, review):
        """Add a review to the place."""
        # (The existance of the review is validated in the facade)
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        # (The existance of the amenity is validated in the facade)
        self.amenities.append(amenity)
