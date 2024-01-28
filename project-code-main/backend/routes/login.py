from flask import Blueprint, request, jsonify
from passlib.hash import pbkdf2_sha256
from db import userCollection

login_bp = Blueprint('login_bp', __name__)


@login_bp.route('/login', methods=['POST'])
def login():
    # default when http request is successful
    response_object = {'status': 'success'}

    post_data = request.get_json()
    tempUsername = post_data.get('username'),

    userInfoFront = post_data
    userInfoDB = userCollection.find_one({"username": userInfoFront['username']})
    # if username is registered
    if userInfoDB:
        # if password and username exists:
        if pbkdf2_sha256.verify(userInfoFront['password'], userInfoDB['password']):
            response_object['error'] = userInfoDB['role']  # Returns role of the user.
            return response_object
        else:
            response_object['error'] = '1'
            return response_object
    response_object["error"] = "2"
    return jsonify(response_object)


@login_bp.route('/reset', methods=['POST'])
def reset():
    response_object = {'status': 'success'}

    post_data = request.get_json()
    tempUsername = post_data.get('username')
    tempemail = post_data.get('email')
    password = post_data.get('password')
    query = {'username': tempUsername, 'email': tempemail}

    user = userCollection.find_one(query)
    print(user)

    if user:
        if pbkdf2_sha256.verify(password, user['password']):
            response_object["error"] = "2"
            return response_object
        else:
            update = {"$set": {"password": pbkdf2_sha256.encrypt(password)}}
            userCollection.update_one(query, update)
            response_object["error"] = "0"
            return response_object
    else:
        response_object["error"] = "1"
        return response_object


