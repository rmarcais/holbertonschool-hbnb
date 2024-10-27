from app.models.place import Place
from app.models.review import Review
from app.models.user import User

import unittest
from app import create_app
from app.models.user import User

class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_review(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "james.doe@example.com"
        })
        user_id = response_user.json.get("id")

        response_place = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": user_id,
            "amenities": []
        })
        place_id = response_place.json.get("id")

        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id
        })

        self.assertEqual(response.status_code, 201)

    def test_create_review_invalid_data(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": "bad id",
            "place_id": "bad id"
        })
        self.assertEqual(response.status_code, 400)

    def test_review_creation(self):
        user = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
        place = Place(title="Cozy Apartment", description="A nice place to stay", price=100.00, latitude=37.7749, longitude=-122.4194, owner=user, amenities=[])

        review = Review(text="This place was great !", rating=5, place=place, user=user)
        assert review.text == "This place was great !"
        assert review.rating == 5
        assert review.user is user
        print("Review creation test passed!")

    # TODO: Test all review endpoints with positive/negative scenarios