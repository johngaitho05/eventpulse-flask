#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Users """
from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves the list of all user objects
    """
    all_users = storage.all(User).values()
    return jsonify([user.to_dict() for user in all_users])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ Retrieves a single user """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a user Object
    """

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """
    Creates a user
    """
    data = request.get_json()
    if type(data) is not dict:
        abort(400, description="Not a JSON")

    required_keys = ['email', 'password', 'phone', 'country_id']
    for k in required_keys:
        if k not in data:
            abort(400, description="Missing {}".format(k))
    user = storage.filter(User, email=data.get('email'))
    if user:
        abort(400, description="A user with the given email already exist")

    instance = User(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """
    Updates a user
    """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    data = request.get_json()
    if type(data) is not dict:
        abort(400, description="Not a JSON")

    if 'email' in data:
        del data['email']

    user.update(**data)
    return make_response(jsonify(user.to_dict()), 200)
