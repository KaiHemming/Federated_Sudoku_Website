from flask import Blueprint, request, send_file
from db import sudokuCollection, miracleSudokuLevelsCollection, userCollection
from sudoku_solver import *
import json
import os,io

puzzles_bp = Blueprint('puzzles_bp', __name__)


@puzzles_bp.route('/puzzleNames', methods=['GET'])
def getPuzzleNames():
    sudokus = {}
    index = 0
    sudokuData = sudokuCollection.find({}, {"_id": 0, "name": 1, "gameType": 1, "rating": 1, "id": 1, 'author': 1})
    for sudoku in sudokuData:
        index += 1
        sudokus[index] = sudoku
    return sudokus


@puzzles_bp.route('/miracle-puzzle-names', methods=['GET'])
def getMiraclePuzzleNames():
    sudokus = {}
    index = 0
    sudokuData = miracleSudokuLevelsCollection.find({}, {"_id": 0, "name": 1, "gameType": 1, "rating": 1, "id": 1, "author": 1})
    for sudoku in sudokuData:
        index += 1
        sudokus[index] = sudoku
    return sudokus

@puzzles_bp.route('/getpuzzlename', methods=['GET'])
def getPuzzleName():
    puzzleID = request.args.get('puzzleID')
    if (puzzleID is not None and puzzleID.isdigit()):
        puzzle = sudokuCollection.find({"id": int(puzzleID)})
        list_puzzle = list(puzzle)
        if (len(list_puzzle) == 0):
            puzzle = miracleSudokuLevelsCollection.find({"id": int(puzzleID)})
        return {"name": list_puzzle[0].get("name")}
    else:
        return {"name": "No puzzle name"}

@puzzles_bp.route('/getpuzzle', methods=['GET'])
def getPuzzle():
    puzzleName = request.args.get('puzzleName')
    puzzle = sudokuCollection.find({"name": puzzleName})
    list_puzzle = list(puzzle)
    return {"grid": list_puzzle[0].get("grid"),
            "id": list_puzzle[0].get("id"),
            "author": list_puzzle[0].get("author")}


@puzzles_bp.route('/miracle-sudoku-puzzle', methods=['GET'])
def getMiraclePuzzle():
    puzzleName = request.args.get('puzzleName')
    puzzle = miracleSudokuLevelsCollection.find({"name": puzzleName})
    list_puzzle = list(puzzle)
    return {"grid": list_puzzle[0].get("grid"),"id": list_puzzle[0].get("id"), "author": list_puzzle[0].get("author")}


@puzzles_bp.route('/downloadPuzzle', methods=['GET'])
def downloadPuzzle():
    puzzleName = request.args.get("puzzleName")
    res = {}
    puzzleList = []
    puzzle = sudokuCollection.find_one({"name": puzzleName}, {"_id": 0,
                                                              "rating": 0, "total-raters": 0})
    data = list(puzzle)

    data = {}
    otherInfo = {}
    author = {}

    data['puzzle'] = puzzle['grid']
    data['solution'] = puzzle['solution']
    if userCollection.find_one({'username': puzzle['author']}):
        if "@Group5" not in puzzle['author'] or puzzle['author'] == "group5":
            author['username'] = puzzle['author'] + "@Group5"
            author['display_name'] = puzzle['author']
        else:
            author['username'] = puzzle['author']
    else:
        if "@UnknownGroup" in puzzle['author'] or "group" in puzzle['author']:
            author['username'] = puzzle['author']
        else:
            author['username'] = puzzle['author'] + "@UnknownGroup"
    otherInfo['variant'] = "sudoku"
    otherInfo['id'] = puzzle['id']
    otherInfo['name'] = puzzleName
    otherInfo['data'] = data
    otherInfo['author'] = author
    puzzleList.append(otherInfo)

    fileName = puzzleName + ".json"
    with open(fileName, "w", newline="") as f:
        json.dump(puzzleList[0], f)

    @puzzles_bp.after_request
    def delete(response):
        os.remove("./"+fileName)
        print("delete file")
        return response
    return send_file(fileName, as_attachment=True)


@puzzles_bp.route('/saveposition', methods=['POST'])
def savePosition():
    response_object = {'status': 'success'}
    post_data = request.get_json()

    # https://www.w3schools.com/python/python_mongodb_update.asp
    query = {"username": post_data.get('username')}
    newSavedSudokuPosition = {"$set": {"savedSudokuPosition": post_data.get('sudoku')}}

    if (userCollection.update_one(query, newSavedSudokuPosition) == None):
        response_object["error"] = "0"

    return response_object


@puzzles_bp.route('/api/puzzles', methods=['GET'])
def puzzles():
    if len(request.args) != 0:
        limitNum = int(request.args.get('maxPuzzles'))
    else:
        limitNum = 25
    res = {}
    puzzleList = []
    # get the recent x sudokus
    puzzle = list(sudokuCollection.find({}, {"_id": 0, "id": 1, "grid": 1, "name": 1, "solution": 1, 'author': 1}).sort("id", -1).limit(limitNum))
    for p in puzzle:
        data = {}
        otherInfo = {}
        author = {}

        data['puzzle'] = p['grid']
        data['solution'] = p['solution']
        try:
            if "@Group5" in p['author']:
                author['username'] = p['author']
            else:
                author['username'] = p['author'] + "@Group5"
            author['display_name'] = p['author']
        except:
            author['username'] = 'Unknown'
            author['display_name'] = 'Unknown'
        otherInfo['variant'] = "sudoku"
        otherInfo['id'] = p['id']
        otherInfo['data'] = data
        otherInfo['name'] = p['name']
        otherInfo['author'] = author
        puzzleList.append(otherInfo)

    res['puzzles'] = puzzleList
    return res
@puzzles_bp.route("/addauthor", methods=["GET","POST"])
def add():
    puzzle = list(sudokuCollection.find({}, {"_id": 0,
                                             "rating": 0, "total-raters": 0}))
    miracle = list(miracleSudokuLevelsCollection.find({}, {"_id": 0,
                                             "rating": 0, "total-raters": 0}))
    for p in puzzle:
        try:
            author = p['author']
            print(author)
        except:
            puzzleId = p['id']
            query = {"id" : puzzleId}
            update = {"$set": {"author": "unknown"}}
            sudokuCollection.update_one(query, update)
    for m in miracle:
        try:
            author = m['author']
        except:
            puzzleId = m['id']
            query = {"id" : puzzleId}
            update = {"$set": {"author": "unknown"}}
            miracleSudokuLevelsCollection.update_one(query, update)
        
    newPuzzle = list(sudokuCollection.find({}, {"_id": 0,
                                             "rating": 0, "total-raters": 0}))
    newMiracle = list(miracleSudokuLevelsCollection.find({}, {"_id": 0,
                                                           "rating": 0, "total-raters": 0}))

    return {'puzzle': newPuzzle,",miracle": newMiracle}
