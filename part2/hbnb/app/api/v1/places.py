from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner details'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload

        owner = facade.get_user(place_data.get("owner_id"))
        if not owner:
            return {'error': 'This user does not exist!'}, 400
        
        amenities_id = place_data.get("amenities")
        amenities = []
        for amenity_id in amenities_id:
            existing_amenity = facade.get_amenity(amenity_id)
            if not existing_amenity:
                return {'error': 'One of the amenities does not exist!'}, 400 
            amenities.append(existing_amenity)

        try:
            del place_data["owner_id"]
            place_data["owner"] = owner
            del place_data["amenities"]
            place_data["amenities"] = amenities
            new_place = facade.create_place(place_data)
        except ValueError as err:
            return {'error': str(err)}, 400

        return {
            "id": new_place.id,
            "title": new_place.title,
            "description": new_place.description,
            "price": new_place.price,
            "latitude": new_place.latitude,
            "longitude": new_place.longitude,
            "owner_id": new_place.owner.id
        }, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        places_response = []

        for place in places:
            places_response.append({
                "id": place.id,
                "title": place.title,
                "latitude": place.latitude,
                "longitude": place.longitude
            })

        return places_response, 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        owner = {
            "id": place.owner.id,
            "first_name": place.owner.first_name,
            "last_name": place.owner.last_name,
            "email": place.owner.email
        }

        amenities = []
        for amenity in place.amenities:
            amenities.append({
                "id": amenity.id,
                "name": amenity.name
            })
        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": owner,
            "amenities": amenities
        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload

        existing_place = facade.get_place(place_id)
        if not existing_place:
            return {'error': 'Place not found'}, 404
        
        amenities_id = place_data.get("amenities")
        amenities = []
        if amenities_id is not None:
            for amenity_id in amenities_id:
                existing_amenity = facade.get_amenity(amenity_id)
                if not existing_amenity:
                    return {'error': 'One of the amenities does not exist!'}, 400 
                amenities.append(existing_amenity)
            del place_data["amenities"]
        
        try:
            if len(amenities) > 0:
                place_data["amenities"] = amenities
            facade.update_place(place_id, place_data)
        except ValueError as err:
            return {'error': str(err)}, 400
        
        return {"message": "Place updated successfully"}, 200
