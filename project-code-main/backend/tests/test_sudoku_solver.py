import sys
sys.path.append('../')
from sudoku_solver import SudokuSolver

# Test that a board with a non-integer is invalid
# Test that the solver class does not mutate the board
def test_non_integer_elements_invalid():
    # board taken from the testcase 1 here: https://leetcode.com/problems/sudoku-solver/description/
    # last accessed 19 Jan 2023 20:36
    board = [
            [None, "3", "4", None, "7", None, None, "1", None],
            ["6", None, None, "1", "9.5", None, "3", "4", "8"],
            [None, "9", "8", None, None, "2", "5", "6", "7"],
            ["8", "5", None, "7", "6", "1", None, "2", "3"],
            ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
            [None, "1", None, "9", "2", "4", "8", "5", None],
            ["9", None, "1", None, "3", None, "2", "8", "4"],
            [None, None, "7", "4", None, "9", "6", "3", "5"],
            [None, None, "5", "2", "8", "6", None, "7", "9"]
        ]

    sudokuSolver = SudokuSolver(board)
    sudokuSolver.solveSudoku(board)

    assert sudokuSolver.isValidBoard == False
    assert sudokuSolver.numberOfSolutions == 0
    assert sudokuSolver.invalidBoardMessage == "The element at position (2, 5) is not an integer between 1 and 9"

    # change the element at (row 1, col 2) to string
    board[0][1]='e'

    sudokuSolver = SudokuSolver(board)
    sudokuSolver.solveSudoku(board)

    assert sudokuSolver.isValidBoard == False
    assert sudokuSolver.numberOfSolutions == 0
    assert sudokuSolver.invalidBoardMessage == "The element at position (1, 2) is not an integer between 1 and 9"

    board[0][1]='3'
    # change the element at (row 1, col 3) to random ascii
    board[0][2]='?'

    sudokuSolver = SudokuSolver(board)
    sudokuSolver.solveSudoku(board)

    assert sudokuSolver.isValidBoard == False
    assert sudokuSolver.numberOfSolutions == 0
    assert sudokuSolver.invalidBoardMessage == "The element at position (1, 3) is not an integer between 1 and 9"

# Testing that a board with 2 equal numbers in a column is invalid
def test_board_two_equal_in_column_invalid():

    board = [
            ["5","3",None,None,"7",None,None,None,None],
            ["6",None,None,"1","9","5",None,None,None],
            [None,"9","8",None,None,None,None,"6",None],
            ["8",None,None,None,"6",None,None,None,"3"],
            ["4",None,None,"8",None,"3",None,None,"1"],
            ["7",None,None,None,"2",None,None,None,"6"],
            [None,"6",None,None,None,None,"2","8",None],
            [None,None,None,"4","7","9",None,None,"5"],
            [None,None,None,None,"8",None,None,"7","9"]
            ]

    sudokuSolver = SudokuSolver(board)
    sudokuSolver.solveSudoku(board)

    assert sudokuSolver.isValidBoard == False
    assert sudokuSolver.numberOfSolutions == 0
    assert sudokuSolver.invalidBoardMessage == "On column 5 there is more than one 7"


# Testing that a board with 2 equal numbers in a row is invalid
def test_board_two_equal_in_row_invalid():

    board = [
            ["5","3",None,None,"7",None,None,"3",None],
            ["6",None,None,"1","9","5",None,None,None],
            [None,"9","8",None,None,None,None,"6",None],
            ["8",None,None,None,"6",None,None,None,"3"],
            ["4",None,None,"8",None,"3",None,None,"1"],
            ["7",None,None,None,"2",None,None,None,"6"],
            [None,"6",None,None,None,None,"2","8",None],
            [None,None,None,"4","1","9",None,None,"5"],
            [None,None,None,None,"8",None,None,"7","9"]
            ]

    sudokuSolver = SudokuSolver(board)
    sudokuSolver.solveSudoku(board)

    assert sudokuSolver.isValidBoard == False
    assert sudokuSolver.numberOfSolutions == 0
    assert sudokuSolver.invalidBoardMessage == "On row 1 there is more than one 3"

# Testing that a board with 2 equal numbers in a box is invalid
def test_board_two_equal_in_box_invalid():

    board = [
            ["5","3",None,None,"7",None,None,None,None],
            ["6","8",None,"1","9","5",None,None,None],
            [None,"9","8",None,None,None,None,"6",None],
            ["8",None,None,None,"6",None,None,None,"3"],
            ["4",None,None,"8",None,"3",None,None,"1"],
            ["7",None,None,None,"2",None,None,None,"6"],
            [None,"6",None,None,None,None,"2","8",None],
            [None,None,None,"4","1","9",None,None,"5"],
            [None,None,None,None,"8",None,None,"7","9"]
            ]

    sudokuSolver = SudokuSolver(board)
    sudokuSolver.solveSudoku(board)

    assert sudokuSolver.isValidBoard == False
    assert sudokuSolver.numberOfSolutions == 0
    assert sudokuSolver.invalidBoardMessage == "In the box that contains the element at the coordinate (3, 3) there is more than one 8"


# Testing that a board with no solution is invalid
def test_solve_board_with_no_solution():
    # board puzzle taken from https://www.reddit.com/r/sudoku/comments/7q76ay/friend_tells_me_that_this_is_unsolvable_sudoku/
    # last accessed 19 Jan 2023 16:49
    board = [
            ["2", None, None, "9", None, None, None, None, None],
            [None, None, None, None, None, None, None, "6", None],
            [None, None, None, None, None, "1", None, None, None],
            ["5", None, "2", "6", None, None, "4", None, "7"],
            [None, None, None, None, None, "4", "1", None, None],
            [None, None, None, None, "9", "8", None, "2", "3"],
            [None, None, None, None, None, "3", None, "8", None],
            [None, None, "5", None, "1", None, None, None, None],
            [None, None, "7", None, None, None, None, None, None],
        ]

    sudokuSolver = SudokuSolver(board)
    sudokuSolver.solveSudoku(board)
    actualSolution = sudokuSolver.solution

    assert sudokuSolver.isValidBoard == False
    assert sudokuSolver.numberOfSolutions == 0
    assert sudokuSolver.invalidBoardMessage == "This sudoku puzzle has no solution."

# Testing that a board with two solutions is invalid
def test_solve_board_with_two_solution():
    # board puzzle taken from https://www.quora.com/Does-a-sudoku-have-multiple-solutions
    # (posted by Rahul Singla)
    # last accessed 19 Jan 2023 20:00
    board = [
            ["9","2","6","5","7","1","4","8","3"],
            ["3","5","1","4","8","6","2","7","9"],
            ["8","7","4","9","2","3","5","1","6"],
            ["5","8","2","3","6","7","1","9","4"],
            ["1","4","9","2","5","8","3","6","7"],
            ["7","6","3","1",None,None,"8","2","5"],
            ["2","3","8","7",None,None,"6","5","1"],
            ["6","1","7","8","3","5","9","4","2"],
            ["4","9","5","6","1","2","7","3","8"],
        ]

    sudokuSolver = SudokuSolver(board)
    sudokuSolver.solveSudoku(board)
    actualSolution = sudokuSolver.solution

    assert sudokuSolver.isValidBoard == False
    assert sudokuSolver.numberOfSolutions == 2
    assert sudokuSolver.invalidBoardMessage == "This sudoku puzzle has multiple solutions."


# Solve a correct easy board
def test_solve_correct_board():
    board = [
        [None, "3", "4", None, "7", None, None, "1", None],
        ["6", None, None, "1", "9", None, "3", "4", "8"],
        [None, "9", "8", None, None, "2", "5", "6", "7"],
        ["8", "5", None, "7", "6", "1", None, "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        [None, "1", None, "9", "2", "4", "8", "5", None],
        ["9", None, "1", None, "3", None, "2", "8", "4"],
        [None, None, "7", "4", None, "9", "6", "3", "5"],
        [None, None, "5", "2", "8", "6", None, "7", "9"]
    ]

    sudokuSolver = SudokuSolver(board)
    sudokuSolver.solveSudoku(board)

    actualSolution = sudokuSolver.solution

    expectedSolution = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9]
    ]
    assert actualSolution == expectedSolution
    assert sudokuSolver.isValidBoard == True
    assert sudokuSolver.numberOfSolutions == 1


# Solve a correct sudoku board
def test_solve_correct_board_normal_behaviour():
# board taken from the testcase 2 here: https://leetcode.com/problems/sudoku-solver/description/
# last accessed 19 Jan 2023 20:36
    board = [
            [None,None,"9","7","4","8",None,None,None],
            ["7",None,None,None,None,None,None,None,None],
            [None,"2",None,"1",None,"9",None,None,None],
            [None,None,"7",None,None,None,"2","4",None],
            [None,"6","4",None,"1",None,"5","9",None],
            [None,"9","8",None,None,None,"3",None,None],
            [None,None,None,"8",None,"3",None,"2",None],
            [None,None,None,None,None,None,None,None,"6"],
            [None,None,None,"2","7","5","9",None,None]
    ]

    sudokuSolver = SudokuSolver(board)
    sudokuSolver.solveSudoku(board)

    actualSolution = sudokuSolver.solution

    expectedSolution = [
        [5, 1, 9, 7, 4, 8, 6, 3, 2],
        [7, 8, 3, 6, 5, 2, 4, 1, 9],
        [4, 2, 6, 1, 3, 9, 8, 7, 5],
        [3, 5, 7, 9, 8, 6, 2, 4, 1],
        [2, 6, 4, 3, 1, 7, 5, 9, 8],
        [1, 9, 8, 5, 2, 4, 3, 6, 7],
        [9, 7, 5, 8, 6, 3, 1, 2, 4],
        [8, 3, 2, 4, 9, 1, 7, 5, 6],
        [6, 4, 1, 2, 7, 5, 9, 8, 3]
    ]
    assert actualSolution == expectedSolution
    assert sudokuSolver.isValidBoard == True
    assert sudokuSolver.numberOfSolutions == 1

# Solve a correct sudoku board with exactly 17 clues
def test_solve_correct_board_minimum_clues():
# board taken from the testcase 2 here: https://leetcode.com/problems/sudoku-solver/description/
# last accessed 19 Jan 2023 20:36
    board = [
            [None,None,None,None,None,"1",None,"4",None],
            ["5",None,None,None,None,None,"6",None,None],
            ["6",None,None,None,None,None,None,None,None],
            ["1","9",None,None,None,None,None,None,"3"],
            [None,None,None,"2","8",None,None,None,None],
            [None,None,None,"4",None,None,None,None,None],
            ["3","5",None,None,"7",None,None,None,None],
            [None,None,None,None,None,None,"4","9",None],
            [None,None,None,None,None,None,"2",None,None]
    ]

    sudokuSolver = SudokuSolver(board)
    sudokuSolver.solveSudoku(board)

    actualSolution = sudokuSolver.solution

    expectedSolution = [
        [9, 8, 7, 6, 3, 1, 5, 4, 2],
        [5, 4, 3, 8, 9, 2, 6, 7, 1],
        [6, 2, 1, 5, 4, 7, 3, 8, 9],
        [1, 9, 4, 7, 5, 6, 8, 2, 3],
        [7, 6, 5, 2, 8, 3, 9, 1, 4],
        [2, 3, 8, 4, 1, 9, 7, 5, 6],
        [3, 5, 2, 9, 7, 4, 1, 6, 8],
        [8, 1, 6, 3, 2, 5, 4, 9, 7],
        [4, 7, 9, 1, 6, 8, 2, 3, 5]
    ]
    assert actualSolution == expectedSolution
    assert sudokuSolver.isValidBoard == True
    assert sudokuSolver.numberOfSolutions == 1

def test_compare_sudoku_against_full_solution_valid():
    board = [
        ["9","2","6","5","7","1","4","8","3"],
        ["3","5","1","4","8","6","2","7","9"],
        ["8","7","4","9","2","3","5","1","6"],
        ["5","8","2","3","6","7","1","9","4"],
        ["1","4","9","2","5","8","3","6","7"],
        ["7","6","3","1","4","9","8","2","5"],
        ["2","3","8","7","9","4","6","5","1"],
        ["6","1","7","8","3","5","9","4","2"],
        ["4","9","5","6","1","2","7","3","8"],
    ]
    actual_solution = [
        ["9","2","6","5","7","1","4","8","3"],
        ["3","5","1","4","8","6","2","7","9"],
        ["8","7","4","9","2","3","5","1","6"],
        ["5","8","2","3","6","7","1","9","4"],
        ["1","4","9","2","5","8","3","6","7"],
        ["7","6","3","1","4","9","8","2","5"],
        ["2","3","8","7","9","4","6","5","1"],
        ["6","1","7","8","3","5","9","4","2"],
        ["4","9","5","6","1","2","7","3","8"],
    ]
    sudoku_solver = SudokuSolver(board)
    assert sudoku_solver.compareToSolution(board, actual_solution, True) == "The solution is correct"

def test_compare_sudoku_against_full_solution_invalid():
    board = [
        ["9","2","6","5","7","1","4","8","3"],
        ["3","5","1","4","8","6","2","7","9"],
        ["8","7","4","9","2","3","5","1","6"],
        ["5","8","2","3","6","7","1","9","4"],
        ["1","4","9","2","5","8","3","6","7"],
        ["7","6","3","1","4","9","8","2","5"],
        ["2","3","8","7","9","4","6","5","1"],
        ["6","1","7","8","3","5","9","4","2"],
        ["4","9","5","6","1","2","7","3","8"],
    ]
    actual_solution = [
        ["9","2","6","5","7","1","4","8","7"],
        ["3","5","1","4","8","6","2","7","9"],
        ["8","7","4","9","2","3","5","1","6"],
        ["5","8","2","3","6","7","1","9","4"],
        ["1","4","9","2","5","8","3","6","7"],
        ["7","6","3","1","4","9","8","2","5"],
        ["2","3","8","7","9","4","6","5","1"],
        ["6","1","7","8","3","5","9","4","2"],
        ["4","9","5","6","1","2","7","3","8"],
    ]
    sudoku_solver = SudokuSolver(board)
    assert sudoku_solver.compareToSolution(board, actual_solution, True) == "Wrong choice at (1, 9)"

def test_compare_sudoku_partial_full_solution_valid():
    board = [
                [None, "3", "4", None, "7", None, None, "1", None],
                ["6", None, None, "1", "9", None, "3", "4", "8"],
                [None, "9", "8", None, None, "2", "5", "6", "7"],
                ["8", "5", None, "7", "6", "1", None, "2", "3"],
                ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
                [None, "1", None, "9", "2", "4", "8", "5", None],
                ["9", None, "1", None, "3", None, "2", "8", "4"],
                [None, None, "7", "4", None, "9", "6", "3", "5"],
                [None, None, "5", "2", "8", "6", None, "7", "9"]
            ]
    actual_solution = [
                [5, 3, 4, 6, 7, 8, 9, 1, 2],
                [6, 7, 2, 1, 9, 5, 3, 4, 8],
                [1, 9, 8, 3, 4, 2, 5, 6, 7],
                [8, 5, 9, 7, 6, 1, 4, 2, 3],
                [4, 2, 6, 8, 5, 3, 7, 9, 1],
                [7, 1, 3, 9, 2, 4, 8, 5, 6],
                [9, 6, 1, 5, 3, 7, 2, 8, 4],
                [2, 8, 7, 4, 1, 9, 6, 3, 5],
                [3, 4, 5, 2, 8, 6, 1, 7, 9]
            ]
    sudoku_solver = SudokuSolver(board)
    # convert the board to string
    sudoku_solver.toStr(actual_solution)
    assert sudoku_solver.compareToSolution(board, actual_solution) == "The solution is correct"

def test_compare_sudoku_against_partial_solution_invalid():
    board = [
                    [None,None,None,None,None,"1",None,"4",None],
                    ["5",None,None,None,None,None,"6",None,None],
                    ["6",None,None,None,None,None,None,None,None],
                    ["1","9",None,None,None,None,None,None,"3"],
                    [None,None,None,"2","8",None,None,None,None],
                    [None,None,None,"4",None,None,None,None,None],
                    ["3","5",None,None,"7",None,None,None,None],
                    [None,None,"7",None,None,None,"4","9",None],
                    [None,None,None,None,None,None,"2",None,None]
            ]
    sudoku_solver = SudokuSolver(board)
    actual_solution = [
                [9, 8, 7, 6, 3, 1, 5, 4, 2],
                [5, 4, 3, 8, 9, 2, 6, 7, 1],
                [6, 2, 1, 5, 4, 7, 3, 8, 9],
                [1, 9, 4, 7, 5, 6, 8, 2, 3],
                [7, 6, 5, 2, 8, 3, 9, 1, 4],
                [2, 3, 8, 4, 1, 9, 7, 5, 6],
                [3, 5, 2, 9, 7, 4, 1, 6, 8],
                [8, 1, 6, 3, 2, 5, 4, 9, 7],
                [4, 7, 9, 1, 6, 8, 2, 3, 5]
            ]
    sudoku_solver.toStr(actual_solution)
    assert sudoku_solver.compareToSolution(board, actual_solution) == "Wrong choice at (8, 3)"