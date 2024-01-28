from flask import Blueprint, request
from routes.minesweeperGenerator import *

mineSweeper_bp = Blueprint('mineSweeper_bp', __name__)


@mineSweeper_bp.route('/getminesweeper', methods=['GET'])
def getMineSweeper():
    difficulty = request.args.get("difficulty")
    if difficulty == "easy":
        row = 8
        col = 8
        mine = 10
    elif difficulty == "medium":
        row = 10
        col = 10
        mine = 40
    elif difficulty == "hard":
        row = 20
        col = 20
        mine = 99
    else:
        row = int(request.args.get('row'))
        col = int(request.args.get('col'))
        mine = int(request.args.get('mine'))

    res_object = generate(row, col, mine)
    return res_object
