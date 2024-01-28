import datetime
from flask import Blueprint, request, jsonify
from db import commentCollection, sudokuCollection, miracleSudokuLevelsCollection

comment_bp = Blueprint('comment_bp', __name__)


@comment_bp.route("/comment", methods=['POST'])
def comment():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    x = datetime.datetime.now().strftime("%c")
    puzzleName = post_data.get('puzzleName')
    miracle = request.args.get("miracle")
    if miracle == "true":
        puzzleId = miracleSudokuLevelsCollection.find_one({"name": puzzleName}, {"_id": 0, "id": 1})
    else:
        puzzleId = sudokuCollection.find_one({"name": puzzleName}, {"_id": 0, "id": 1})
    puzzleComment = {
        'puzzleId': puzzleId["id"],
        'content': post_data.get('content'),
        'user': post_data.get('user'),
        'date': x
    }
    if commentCollection.insert_one(puzzleComment):
        response_object['error'] = "0"
        return response_object
    else:
        response_object['error'] = '1'
        return response_object
