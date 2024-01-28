from flask import Blueprint, request, jsonify
from db import userCollection

accounts_bp = Blueprint('accounts_bp', __name__)

@accounts_bp.route('/getuserdata', methods = ['GET'])
def getUserData():
    username = request.args.get('username')
    userInfo = userCollection.find({"username": username})
    list_user = list(userInfo)
    return {"username":list_user[0].get("username"),
            "role":list_user[0].get("role"),
            "bio":list_user[0].get("bio")}

@accounts_bp.route('/getuserrole', methods = ['GET'])
def getUserRole():
    username = request.args.get('username')
    userInfo = userCollection.find({"username": username})
    list_user = list(userInfo)
    return {"role":list_user[0].get("role")}

@accounts_bp.route('/getsaveposition', methods=['GET'])
def getSavedPosition():
    username = request.args.get('username')
    userInfo = userCollection.find({"username": username})
    list_user = list(userInfo)
    return {"name": list_user[0].get("savedSudokuPosition").get("name"),
            "grid": list_user[0].get("savedSudokuPosition").get("grid"),
            "miracle": list_user[0].get("savedSudokuPosition").get("miracle")
            }


@accounts_bp.route('/postbio' , methods = ['POST'])
def postBio():
    response_object = {'status':'success'}
    post_data = request.get_json()

    query = {"username":post_data.get('username')}
    newBio = {"$set": {"bio": post_data.get('newBio')}}

    if (userCollection.update_one(query, newBio) == None) :
        response_object["error"] = "0"

    return response_object

@accounts_bp.route('/promote', methods = ['POST'])
def promote():
    response_object = {'status':'success'}
    username = request.args.get("username")

    query = {"username":username}
    promotion = {"$set" : {"role":"admin"}}

    if (userCollection.update_one(query, promotion) == None):
        response_object["error"] = "0"
    
    return response_object