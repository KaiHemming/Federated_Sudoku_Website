import json
from flask import Blueprint, request, jsonify
from db import commentCollection, sudokuCollection, miracleSudokuLevelsCollection

commentList_bp = Blueprint('commentList_bp', __name__)


@commentList_bp.route("/commentList", methods=['GET', 'POST'])
def commentList():
    comments = {}
    commentData = commentCollection.find({}, {"_id": 0})
    index = 0
    for comment in commentData:
        index = int(index)
        index += 1
        index = str(index)
        comments[index] = comment

    return comments


@commentList_bp.route("/getComment", methods=['GET', 'POST'])
def getComment():
    cmt = []
    comments = {}

    puzzleName = request.args.get('puzzleName')
    miracle = request.args.get("miracle")
    if miracle == 'true':
        puzzle = miracleSudokuLevelsCollection.find({"name": puzzleName})
    else:
        puzzle = sudokuCollection.find({"name": puzzleName})
    list_puzzle = list(puzzle)

    puzzleId = list_puzzle[0].get('id')
    myQuery = {'puzzleId': puzzleId}

    commentData = commentCollection.find(myQuery, {"_id": 0})
    for comment in commentData:
        temp = comment
        # print(temp)
        # print(cmt)
        cmt.append(temp)

    comments['comment'] = cmt
    list_puzzle[0].update(comments)

    return {"puzzleName": list_puzzle[0].get("name"), 'comments': list_puzzle[0].get('comment'),
            'id': list_puzzle[0].get('id')}

@commentList_bp.route("/deletecomment", methods=['POST'])
def deleteComment():
    response_object = {'status': 'success'}
    miracle = request.args.get('miracle')
    puzzleName = request.args.get('puzzleName')

    if (miracle == True):
        puzzle = miracleSudokuLevelsCollection.find({"name": puzzleName})

    else:
        puzzle = sudokuCollection.find({"name": puzzleName})

    deleteComment = request.get_json()
    puzzleId = list(puzzle)[0].get('id')
    myQuery = {'puzzleId': puzzleId,
                'content': deleteComment.get('content'),
                'user': deleteComment.get('user'),
                'date': deleteComment.get('date')}
    
    commentCollection.delete_one(myQuery)
    return response_object