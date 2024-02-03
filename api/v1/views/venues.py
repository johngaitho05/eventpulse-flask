#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Venues """
from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.venue import Venue


@app_views.route('/venues', methods=['GET'], strict_slashes=False)
def get_venues():
    """
    Retrieves all venue objects
    """
    all_venues = storage.all(Venue).values()
    return jsonify([venue.to_dict(anotate=['country_id']) for venue in all_venues])


@app_views.route('countries/<country_id>/venues', methods=['GET'], strict_slashes=False)
def get_venues_by_country(country_id):
    """
    Retrieves all venue objects
    """
    all_venues = storage.filter(Venue, country_id=country_id).values()
    return jsonify([venue.to_dict() for venue in all_venues])


@app_views.route('/venues/<venue_id>', methods=['GET'], strict_slashes=False)
def get_venue(venue_id):
    """ Retrieves a single venue """
    venue = storage.get(Venue, venue_id)
    if not venue:
        abort(404)

    return jsonify(venue.to_dict(anotate=['country_id']))


@app_views.route('/venues/<venue_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_venue(venue_id):
    """
    Deletes a venue Object
    """

    venue = storage.get(Venue, venue_id)

    if not venue:
        abort(404)

    storage.delete(venue)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/venues', methods=['POST'], strict_slashes=False)
def post_venue():
    """
    Creates a venue
    """
    data = request.get_json()
    if type(data) is not dict:
        abort(400, description="Not a JSON")
    required = ['name', 'room_id', 'address']
    for key in required:
        if key not in data:
            abort(400, description="Missing {} parameter".format(key))

    instance = Venue(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/venues/<venue_id>', methods=['PUT'], strict_slashes=False)
def put_venue(venue_id):
    """
    Updates a venue
    """
    venue = storage.get(Venue, venue_id)

    if not venue:
        abort(404)

    data = request.get_json()

    if type(data) is not dict:
        abort(400, description="Not a JSON")

    venue.update(**data)
    return make_response(jsonify(venue.to_dict()), 200)
