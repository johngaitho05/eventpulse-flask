#!/usr/bin/python3
""" objects that handles all default RestFul API actions for Amenities"""
from models.event_track import EventTrack
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/event_tracks', methods=['GET'], strict_slashes=False)
def get_event_tracks():
    """
    Retrieves all event_track objects
    """
    all_event_tracks = storage.all(EventTrack).values()
    return jsonify([event_track.to_dict(anotate=['event_id']) for event_track in all_event_tracks])


@app_views.route('events/<event_id>/event_tracks', methods=['GET'], strict_slashes=False)
def get_event_tracks_by_event(event_id):
    """
    Retrieves all event_track objects
    """
    all_event_tracks = storage.filter(EventTrack, event_id=event_id).values()
    return jsonify([event_track.to_dict() for event_track in all_event_tracks])


@app_views.route('/event_tracks/<event_track_id>', methods=['GET'], strict_slashes=False)
def get_event_track(event_track_id):
    """ Retrieves a single event_track """
    event_track = storage.get(EventTrack, event_track_id)
    if not event_track:
        abort(404)

    return jsonify(event_track.to_dict(anotate=['event_id']))


@app_views.route('/event_tracks/<event_track_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_event_track(event_track_id):
    """
    Deletes a event_track Object
    """

    event_track = storage.get(EventTrack, event_track_id)

    if not event_track:
        abort(404)

    storage.delete(event_track)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/event_tracks', methods=['POST'], strict_slashes=False)
def post_event_track():
    """
    Creates a event_track
    """
    data = request.get_json()
    if type(data) is not dict:
        abort(400, description="Not a JSON")

    required = ['title', 'event_id', 'start_date']
    for key in required:
        if key not in data:
            abort(400, description="Missing {} parameter".format(key))

    instance = EventTrack(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict(anotate=['event_id'])), 201)


@app_views.route('/event_tracks/<event_track_id>', methods=['PUT'], strict_slashes=False)
def put_event_track(event_track_id):
    """
    Updates a event_track
    """
    event_track = storage.get(EventTrack, event_track_id)

    if not event_track:
        abort(404)

    data = request.get_json()

    if type(data) is not dict:
        abort(400, description="Not a JSON")

    event_track.update(**data)
    return make_response(jsonify(event_track.to_dict(anotate=['event_id'])), 200)
