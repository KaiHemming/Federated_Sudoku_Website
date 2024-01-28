from flask import Blueprint, request, jsonify
from db import sudokuCollection, miracleSudokuLevelsCollection
from miracle_sudoku_solver import MiracleSudokuSolver
from sudoku_solver import SudokuSolver

create_sudoku_bp = Blueprint('create_sudoku_bp', __name__)


# Checks a provided sudoku puzzle to see if it is allowed to be added to the site, and if so then the database is added to.
@create_sudoku_bp.route("/create_sudoku", methods=['POST'])
def create_sudoku():
    response_object = {'status': 'success'}
    sudoku = request.get_json()
    grid = sudoku["grid"]
    sudokuSolver = SudokuSolver(grid)
    sudokuSolver.solveSudoku(grid)
    if sudokuSolver.isValidBoard == True:
        # add puzzle to database
        if not sudokuCollection.find_one({"name": sudoku["name"]}):
                sudokuSolver.toStr(sudokuSolver.solution)
                sudoku["solution"] = sudokuSolver.solution
                sudoku['rating'] = 0
                sudoku['total-raters'] = 0
                sudokuCollection.insert_one(sudoku)
                response_object['error'] = "0"
        else:
                response_object['error'] = "1"
    else:
            response_object['error'] = sudokuSolver.invalidBoardMessage
    return jsonify(response_object)

@create_sudoku_bp.route("/create_sudoku/miracle", methods=['POST'])
def create_miracle_sudoku():
    response_object = {'status': 'success'}
    sudoku = request.get_json()
    grid = sudoku["grid"]
    sudokuSolver = MiracleSudokuSolver(grid)
    if sudokuSolver.isSolvable(grid) == True:
        # add puzzle to database
        if not miracleSudokuLevelsCollection.find_one({"name": sudoku["name"]}):
                sudokuSolver.toStr(sudokuSolver.solution)
                sudoku["solution"] = sudokuSolver.solution
                sudoku['rating'] = 0
                sudoku['total-raters'] = 0
                miracleSudokuLevelsCollection.insert_one(sudoku)
                response_object['error'] = "0"
        else:
                response_object['error'] = "1"
    else:
            response_object['error'] = sudokuSolver.invalidBoardMessage
    return jsonify(response_object)
