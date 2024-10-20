from app.models.place import Place
from app.models.review import Review
from app.models.user import User

def test_review_creation():
    user = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(title="Cozy Apartment", description="A nice place to stay", price=100.00, latitude=37.7749, longitude=-122.4194, owner=user)

    review = Review(text="This place was great !", rating=5, place=place, user=user)
    assert review.text == "This place was great !"
    assert review.rating == 5
    assert review.user is user
    print("Review creation test passed!")

test_review_creation()