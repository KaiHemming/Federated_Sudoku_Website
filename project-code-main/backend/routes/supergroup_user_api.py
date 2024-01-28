from flask import Blueprint, request, jsonify
from routes.generate_code import encrypt_data, decrypt_data

supergroup_user_api_bp = Blueprint('supergroup_user_api_bp', __name__)

@supergroup_user_api_bp.route('/api/user/me', methods=['POST'])
def get_user_data():
    access_token = request.get_json().get('access_token')
    secret_key = b'2SKCP4P9BvPTeVYjRnsv_f6Z9NCjQYDrVyAeCsaSZLE='
    decrypt_access_token = decrypt_data(access_token, secret_key)
    response = {
        "username": decrypt_access_token['username'],
        "origin": {
            "name": "Group 5 - Fantastic Puzzles Fife",
            "url": "https://cs3099user05.host.cs.st-andrews.ac.uk/",
            "id": decrypt_access_token['username']
        }
    }
    return jsonify(response)

