from flask import Blueprint, request, jsonify
from db import sudokuCollection, miracleSudokuLevelsCollection, leaderboardCollection
from sudoku_solver import *
from miracle_sudoku_solver import *

sudoku_bp = Blueprint('sudoku_bp', __name__)

# Gets solution form either miracle sudoku or sudoku database
def getSolution(miracle, name):
    if miracle=="true":
        solution = miracleSudokuLevelsCollection.find_one({"name": name})
    else:
        solution = sudokuCollection.find_one({"name": name})
    return solution

# Checks a provided sudoku puzzle to see if it is allowed to be added to the site, and if so then the database is added to.
@sudoku_bp.route("/sudoku/check-solution", methods=['POST'])
def check_solution():
    response_object = {'status': 'success'}
    sudoku = request.get_json()
    grid = sudoku["grid"]

    solution = getSolution(sudoku["miracle"], sudoku["name"])

    if solution:
        response_object["message"] = SudokuSolver(grid).compareToSolution(grid, solution["solution"])
    else:
        response_object["error"]="The sudoku could not be found in the database"
    return jsonify(response_object)

@sudoku_bp.route("/sudoku/check-full-solution", methods=['POST'])
def check_full_solution():
    response_object = {'status': 'success'}
    sudoku = request.get_json()
    grid = sudoku["grid"]

    solution = getSolution(sudoku["miracle"], sudoku["name"])

    if solution:
        response_object["message"] = SudokuSolver(grid).compareToSolution(grid, solution["solution"], True)
    else:
        response_object["error"]="The sudoku could not be found in the database"
    return jsonify(response_object)

@sudoku_bp.route("/sudoku/hint", methods=['POST'])
def get_hint():
    response_object = {'status': 'success'}
    sudoku = request.get_json()
    grid = sudoku["grid"]
    if(sudoku["miracle"]!="true"):
        solution = sudokuCollection.find_one({"name": sudoku["name"]})
    else:
        solution = miracleSudokuLevelsCollection.find_one({"name": sudoku["name"]})
    if solution:
        if(sudoku["miracle"]=="true"):
            SudokuSolver(grid).getHint(grid, solution["solution"])
        else:
            MiracleSudokuSolver(grid).getHint(grid, solution["solution"])
        response_object["grid"]= grid
    else:
        response_object["error"]="The sudoku could not be found in the database"
    return jsonify(response_object)


@sudoku_bp.route("/sudoku/miracle-sudoku", methods=['GET'])
def get_miracle_sudoku():
    response_object = {'status': 'success'}
    sudoku = miracleSudokuCollection.find_one()
    response_object["grid"] = sudoku["grid"]
    return jsonify(response_object)

@sudoku_bp.route("/sudoku/rating", methods=['POST'])
def update_rating():
    incoming_sudoku = request.get_json()
    sudokuName = incoming_sudoku['name']
    if(incoming_sudoku['miracle']=="true"):
        sudoku = miracleSudokuLevelsCollection.find_one({'name': sudokuName})
    else:
        sudoku = sudokuCollection.find_one({'name': sudokuName})
    new_rating = incoming_sudoku['rating']
    total_raters = sudoku['total-raters'] + 1
    old_rating = sudoku['rating'] * sudoku['total-raters']
    updated_rating = (old_rating + new_rating) / total_raters

    sudokuCollection.update_one({'name': sudokuName}, {'$set': {'rating': updated_rating, 'total-raters': total_raters}})

    return jsonify({'message': 'Rating updated'})

