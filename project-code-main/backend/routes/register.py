from flask import Blueprint, request
from passlib.hash import pbkdf2_sha256
from db import userCollection

register_bp = Blueprint('register_bp', __name__)

@register_bp.route('/registeradmin', methods = ['GET'])
def registerAdmin():
    user = {
        'username': 'Random123',
        'password': pbkdf2_sha256.encrypt('Random123'),
        'email': 'random123@random123.com',
        'role': 'admin',
    }
    if userCollection.find_one({"username": 'Random123'}) != None: # check the username
        return {'success':'already exists'}
    else:
        userCollection.insert_one(user)
        return {'success':'created'}


@register_bp.route('/register', methods=['POST'])
def register():
    # default when http request is successful
    response_object = {'status': 'success'}
    post_data = request.get_json()
    username = post_data.get('username')
    email = post_data.get('email')
    user = {
        'username': username,
        'password': post_data.get('password'),
        'email': email,
        'role': post_data.get('role'),
    }

    user['password'] = pbkdf2_sha256.encrypt(user['password']) # hash the password
    if userCollection.find_one({"username": username}) != None: # check the username
        response_object["error"] = "0"
        return response_object
    elif userCollection.find_one({"email": email}) != None: # check the email
        response_object["error"] = "2"
        return response_object
    else:
        userCollection.insert_one(user)
        response_object["error"] = "1"
        response_object['message'] = 'User detail uploaded, success to register'
        return response_object

@register_bp.route('/register-supergroup-user', methods=['POST'])
def register_supergroup_user():
    # default when http request is successful
    response_object = {'status': 'success'}
    post_data = request.get_json()
    user = {
        'username': post_data.get('username'),
        'role': 'creator',
    }
    if not userCollection.find_one({"username": user['username']}): # check the username
        userCollection.insert_one(user)
    return response_object
