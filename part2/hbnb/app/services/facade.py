from app.persistence.repository import InMemoryRepository
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # users

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        self.user_repo.update(user_id, data)

    # amenities

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()
    
    def get_amenity_by_name(self, name):
        return self.amenity_repo.get_by_attribute('name', name)

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)

    # places

    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repo.add(place)
        place_data["owner"].add_place(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        amenities = place_data.get("amenities")
        if amenities:
            place = self.get_place(place_id)
            for amenity in amenities:
                place.add_amenity(amenity)
            del place_data["amenities"]
        self.place_repo.update(place_id, place_data)

    # reviews

    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repo.add(review)
        review_data["user"].add_review(review)
        review_data["place"].add_review(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        reviews_by_place = []
        reviews = self.get_all_reviews()

        for review in reviews:
            if review.place.id == place_id:
                reviews_by_place.append(review)

        return reviews_by_place

    def update_review(self, review_id, review_data):
        self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        self.review_repo.delete(review_id)
