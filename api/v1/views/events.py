#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Events """
from models.event import Event
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from

from api import cloudinary_server


@app_views.route('/events', methods=['GET'], strict_slashes=False)
def get_events():
    """
    Retrieves all event objects
    """
    all_events = storage.all(Event).values()
    return jsonify([event.to_dict(anotate=['venue_id']) for event in all_events])


@app_views.route('venues/<venue_id>/events', methods=['GET'], strict_slashes=False)
def get_events_by_venue(venue_id):
    """
    Retrieves all event objects from a given country
    """

    all_events = storage.filter(Event, venue_id=venue_id).values()
    return jsonify([event.to_dict() for event in all_events])


@app_views.route('countries/<country_id>/events', methods=['GET'], strict_slashes=False)
def get_events_by_country(country_id):
    """
    Retrieves all event objects from a given country
    """

    all_events = storage.filter(Event, venue_id__country_id=country_id).values()
    return jsonify([event.to_dict(anotate=['venue_id']) for event in all_events])


@app_views.route('/events/<event_id>', methods=['GET'], strict_slashes=False)
def get_event(event_id):
    """ Retrieves a single event """
    event = storage.get(Event, event_id)
    if not event:
        abort(404)

    return jsonify(event.to_dict(anotate=['venue_id', 'tracks']))


@app_views.route('/events/<event_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_event(event_id):
    """
    Deletes a event Object
    """

    event = storage.get(Event, event_id)

    if not event:
        abort(404)

    storage.delete(event)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/events', methods=['POST'], strict_slashes=False)
def post_event():
    """
    Creates an event
    """
    data = request.get_json()
    if type(data) is not dict:
        abort(400, description="Not a JSON")
    required = ['title', 'venue_id', 'start_date', 'end_date', 'banner_url']
    to_ignore = ['attendees', 'tracks', 'banner_url']
    for key in to_ignore:
        if key in data:
            del data[key]
    image_file = request.files['banner']
    result = cloudinary_server.uploader.upload(image_file)
    data['banner_url'] = result['secure_url']
    for key in required:
        if key not in data:
            abort(400, description="Missing {} parameter".format(key))

    instance = Event(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict(anotate=['venue_id'])), 201)


@app_views.route('/events/<event_id>', methods=['PUT'], strict_slashes=False)
def put_event(event_id):
    """
    Updates an event
    """
    event = storage.get(Event, event_id)

    if not event:
        abort(404)

    data = request.get_json()

    if type(data) is not dict:
        abort(400, description="Not a JSON")

    event.update(**data)
    return make_response(jsonify(event.to_dict(anotate=['venue_id'])), 200)
