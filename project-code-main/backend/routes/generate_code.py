from flask import Blueprint, request, jsonify, json
from cryptography.fernet import Fernet

encrypt_bp = Blueprint('encrypt_bp', __name__)

def encrypt_data(data, secret_key):
    fernet = Fernet(secret_key)
    data_bytes = json.dumps(data).encode('utf-8')
    encrypted_bytes = fernet.encrypt(data_bytes)
    code = encrypted_bytes.decode('utf-8')
    return code

def decrypt_data(code, secret_key):
    fernet = Fernet(secret_key)
    encrypted_bytes = code.encode('utf-8')
    decrypted_bytes = fernet.decrypt(encrypted_bytes)
    data = json.loads(decrypted_bytes.decode('utf-8'))
    return data


@encrypt_bp.route('/generate-code', methods=['POST'])
def encrypt_data_post():
    secret_key = b'V33ID7OcBtYEkNVgCtzEh-MNSB8Tm-b94n4GiKTOW5o='
    code = encrypt_data(request.get_json(), secret_key)
    return jsonify({"code":code})