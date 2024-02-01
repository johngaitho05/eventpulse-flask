#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Countrys """
from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.country import Country


@app_views.route('/countries', methods=['GET'], strict_slashes=False)
def get_countries():
    """
    Retrieves all country objects
    """
    all_countries = storage.all(Country).values()
    return jsonify([country.to_dict() for country in all_countries])


@app_views.route('/countries/<country_id>', methods=['GET'], strict_slashes=False)
def get_country(country_id):
    """ Retrieves a single country """
    country = storage.get(Country, country_id)
    if not country:
        abort(404)

    return jsonify(country.to_dict())


@app_views.route('/countries/<country_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_country(country_id):
    """
    Deletes a country Object
    """

    country = storage.get(Country, country_id)

    if not country:
        abort(404)

    storage.delete(country)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/countries', methods=['POST'], strict_slashes=False)
def post_country():
    """
    Creates a country
    """
    data = request.get_json()
    if type(data) is not dict:
        abort(400, description="Not a JSON")

    if 'name' not in data:
        abort(400, description="Missing name parameter")

    country = storage.filter(Country, name=data.get('name'))
    if country:
        abort(400, description="A country with the given name already exist")

    instance = Country(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/countries/<country_id>', methods=['PUT'], strict_slashes=False)
def put_country(country_id):
    """
    Updates a country
    """
    country = storage.get(Country, country_id)

    if not country:
        abort(404)

    data = request.get_json()

    if type(data) is not dict:
        abort(400, description="Not a JSON")

    country.update(**data)
    return make_response(jsonify(country.to_dict()), 200)
