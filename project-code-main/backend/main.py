from flask import Flask, jsonify, request, url_for, redirect, make_response, session, json
from flask_cors import CORS
from passlib.hash import pbkdf2_sha256

from routes.accounts import accounts_bp
from routes.login import login_bp
from routes.register import register_bp
from routes.leaderboard import leaderboard_bp
from routes.create_sudoku import create_sudoku_bp
from routes.puzzles import puzzles_bp
from routes.sudoku import sudoku_bp
from routes.comment import comment_bp
from routes.commentList import commentList_bp
from routes.oauth import oauth_bp
from routes.generate_code import encrypt_bp
from routes.supergroup_user_api import supergroup_user_api_bp
from routes.mineSweeper import mineSweeper_bp

from db import miracleSudokuCollection, userCollection, miracleSudokuLevelsCollection
from miracle_sudoku_solver import MiracleSudokuSolver

app = Flask(__name__)

app.config.from_object(__name__)
app.secret_key = "sudoku"


# cross-origin resource sharing
CORS(app)
CORS(app, resources={r"/*": {'origins': "*"}})
CORS(app, resources={r'/*': {'origins': '/backend', "allow_headers": "Access-Control-Allow-Origin"}})
CORS(app, resources={r'/*': {'origins': ' http://localhost:8080', "allow_headers": "Access-Control-Allow-Origin"}})
# CORS(app, resources={r'/*': {'origins': '/127.0.0.1:5000', "allow_headers": "Access-Control-Allow-Origin"}})


USER = []

app.register_blueprint(accounts_bp)
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(leaderboard_bp)
app.register_blueprint(create_sudoku_bp)
app.register_blueprint(puzzles_bp)
app.register_blueprint(sudoku_bp)
app.register_blueprint(comment_bp)
app.register_blueprint(commentList_bp)
app.register_blueprint(oauth_bp)
app.register_blueprint(encrypt_bp)
app.register_blueprint(supergroup_user_api_bp)
app.register_blueprint(mineSweeper_bp)

# This route returns a Python dictionary which stores all the client_id values of all other federation members.
@app.route("/client_id_list", methods=['POST'])
def getClientIDList():
    group_name = request.get_json()["group_name"]
    clientIDList = {
        "group01": "cs3099-g1",
        "group02": "aces_g2",
        "group03": "cs3099group03",
        "group04": "cs3099-g4",
        "group06": "g6",
        "group07": "aces-g7",
        "group08": "aces-eight",
        "group09": "aces-g9"
    }

    return jsonify({"client_id": clientIDList[group_name]})

# This route checks if the inputted username and password exist and are correct in the database and returns a response.
@app.route('/federation_login', methods=['POST'])
def federation_login():
    response_object = {'status': 'success'}

    post_data = request.get_json()

    userInfoFront = post_data
    userInfoDB = userCollection.find_one({"username": userInfoFront['username']})
    
    response_object['error'] = '1'
    if pbkdf2_sha256.verify(userInfoFront['password'], userInfoDB['password']):
        response_object['error'] = '0'
    return response_object

# # TODO: UNCOMMENT THIS CODE WHEN PUTTING THE WEBSITE ON THE SCHOOL SERVER FOR THE FIRST TIME
# solver=MiracleSudokuSolver([[0,0,0,0,0,0,0,0,0],
#                      [0,0,0,0,0,0,0,0,0],
#                      [0,0,0,0,0,0,0,0,0],
#                      [0,0,0,0,0,0,0,0,0],
#                      [0,0,0,0,0,0,0,0,0],
#                      [0,0,0,0,0,0,0,0,0],
#                      [0,0,0,0,0,0,0,0,0],
#                      [0,0,0,0,0,0,0,0,0],
#                      [0,0,0,0,0,0,0,0,0]
#                     ])
# solver.solve_miracle_sudoku([[0,0,0,0,0,0,0,0,0],
#                                                  [0,0,0,0,0,0,0,0,0],
#                                                  [0,0,0,0,0,0,0,0,0],
#                                                  [0,0,0,0,0,0,0,0,0],
#                                                  [0,0,0,0,0,0,0,0,0],
#                                                  [0,0,0,0,0,0,0,0,0],
#                                                  [0,0,0,0,0,0,0,0,0],
#                                                  [0,0,0,0,0,0,0,0,0],
#                                                  [0,0,0,0,0,0,0,0,0]
#                                                 ], 0,0)
#
# MIRACLE_SUDOKUS = solver.miracle_sudokus
#
# for miracle_sudoku in MIRACLE_SUDOKUS:
#      miracleSudokuCollection.insert_one({"grid": miracle_sudoku})


if __name__ == "__main__":
    app.run(host='localhost', debug=True, port = 27017)
    # app.run(host='localhost', debug=True)
