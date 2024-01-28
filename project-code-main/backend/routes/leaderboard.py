from flask import Blueprint, request, jsonify
from db import userCollection, leaderboardCollection, sudokuCollection, miracleSudokuLevelsCollection

leaderboard_bp = Blueprint('leaderboard_bp', __name__)

@leaderboard_bp.route('/leaderboard', methods=['GET'])
def showLeaderBoard():
    puzzleID = request.args.get('puzzleID')
    leaderboardData = leaderboardCollection.find({"puzzleID": int(puzzleID)})
    scores = {}
    index = 0
    for score in leaderboardData:
        index += 1
        scores[index] = {
            "username": score['username'],
            "time": score['time']
        }

    return {"scores": scores}

@leaderboard_bp.route("/leaderboard/submit", methods=['POST'])
def submit_score():
    sudoku = request.get_json()
    time = sudoku["time"]
    puzzleID = sudoku["puzzleID"]
    username = sudoku["username"]
    
    leaderboardCollection.insert_one({"time": time, "puzzleID": puzzleID, "username": username})
    return jsonify({'message': 'Sudoku submitted'})