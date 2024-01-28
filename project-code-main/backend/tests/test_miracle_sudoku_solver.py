import sys
sys.path.append('../')
from miracle_sudoku_solver import MiracleSudokuSolver

# Tests that the miracle sudoku solver can solve the original miracle sudoku
def test_original_miracle_sudoku():
    # original miracle sudoku board taken from: https://www.popularmechanics.com/science/a32605317/miracle-sudoku-hardest-puzzle-ever/
    # Link last accessed 15/03/2023 at 17:09
    board = [
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, "1", None, None, None, None, None, None],
        [None, None, None, None, None, None, "2", None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
    ]

    sudokuSolver = MiracleSudokuSolver(board)
    assert sudokuSolver.isSolvable(board) == True

    assert sudokuSolver.isValidBoard == True
    assert sudokuSolver.numberOfSolutions == 1
    assert sudokuSolver.solution == [
        ['4','8','3','7','2','6','1','5','9'],
        ['7','2','6','1','5','9','4','8','3'],
        ['1','5','9','4','8','3','7','2','6'],
        ['8','3','7','2','6','1','5','9','4'],
        ['2','6','1','5','9','4','8','3','7'],
        ['5','9','4','8','3','7','2','6','1'],
        ['3','7','2','6','1','5','9','4','8'],
        ['6','1','5','9','4','8','3','7','2'],
        ['9','4','8','3','7','2','6','1','5']
    ]

# Tests that the miracle sudoku solver can solve another miracle sudoku board
def test_second_valid_miracle_sudoku():
    # original miracle sudoku board taken from: https://www.youtube.com/watch?v=Tv-48b-KuxI
    # Link last accessed 15/03/2023 at 17:15
    board = [
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, "4", None, None, None, None],
        [None, None, "3", None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
    ]

    sudokuSolver = MiracleSudokuSolver(board)
    assert sudokuSolver.isSolvable(board) == True

    assert sudokuSolver.isValidBoard == True
    assert sudokuSolver.numberOfSolutions == 1
    assert sudokuSolver.solution == [
        ['9','4','8','3','7','2','6','1','5'],
        ['3','7','2','6','1','5','9','4','8'],
        ['6','1','5','9','4','8','3','7','2'],
        ['4','8','3','7','2','6','1','5','9'],
        ['7','2','6','1','5','9','4','8','3'],
        ['1','5','9','4','8','3','7','2','6'],
        ['8','3','7','2','6','1','5','9','4'],
        ['2','6','1','5','9','4','8','3','7'],
        ['5','9','4','8','3','7','2','6','1']
    ]

# Tests that the miracle sudoku solver can solve another valid miracle sudoku board
def test_third_valid_miracle_sudoku():
    # original miracle sudoku board taken from: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?chlang=en&id=0004E0
    # Link last accessed 15/03/2023 at 17:20
    board = [
        [None, None, None, "3", None, None, None, None, "5"],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, "3", None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, "3", None, None, None, None],
    ]

    sudokuSolver = MiracleSudokuSolver(board)
    assert sudokuSolver.isSolvable(board) == True

    assert sudokuSolver.isValidBoard == True
    assert sudokuSolver.numberOfSolutions == 1
    assert sudokuSolver.solution == [
        ['9','4','8','3','7','2','6','1','5'],
        ['3','7','2','6','1','5','9','4','8'],
        ['6','1','5','9','4','8','3','7','2'],
        ['4','8','3','7','2','6','1','5','9'],
        ['7','2','6','1','5','9','4','8','3'],
        ['1','5','9','4','8','3','7','2','6'],
        ['8','3','7','2','6','1','5','9','4'],
        ['2','6','1','5','9','4','8','3','7'],
        ['5','9','4','8','3','7','2','6','1']
    ]

# Tests that a miracle sudoku with one clue has exactly 8 solutions.
def test_invalid_miracle_sudoku_only_one_clue():
    board = [
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, "5", None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
    ]

    sudokuSolver = MiracleSudokuSolver(board)
    assert sudokuSolver.isSolvable(board) == False
    assert sudokuSolver.invalidBoardMessage == "This board has multiple solutions"
    assert sudokuSolver.isValidBoard == False
    assert sudokuSolver.numberOfSolutions == 8

# Tests that a miracle sudoku with multiple solutions is detected.
def test_invalid_miracle_sudoku_multiple_solutions():
    board = [
        [None, None, None, "3", None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, "3", None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, "3", None, None, None, None],
    ]

    sudokuSolver = MiracleSudokuSolver(board)
    assert sudokuSolver.isSolvable(board) == False
    assert sudokuSolver.invalidBoardMessage == "This board has multiple solutions"
    assert sudokuSolver.isValidBoard == False
    assert sudokuSolver.numberOfSolutions == 2

# Tests that a miracle sudoku with no solutions is detected
def test_invalid_miracle_sudoku_no_solution():
    board = [
        [None, None, None, "3", None, None, None, None, "5"],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, "7", None, None, None, None],
        [None, None, "3", None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, "3", None, None, None, None],
    ]

    sudokuSolver = MiracleSudokuSolver(board)
    assert sudokuSolver.isSolvable(board) == False
    assert sudokuSolver.invalidBoardMessage == "This board has no solution"
    assert sudokuSolver.isValidBoard == False
    assert sudokuSolver.numberOfSolutions == 0

# Tests the code that generated all 72 miracle sudokus that are stored in the database
def test_generate_all_miracle_sudokus():
    solver=MiracleSudokuSolver([[0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0]
                    ])
    solver.solve_miracle_sudoku([[0,0,0,0,0,0,0,0,0],
                                                 [0,0,0,0,0,0,0,0,0],
                                                 [0,0,0,0,0,0,0,0,0],
                                                 [0,0,0,0,0,0,0,0,0],
                                                 [0,0,0,0,0,0,0,0,0],
                                                 [0,0,0,0,0,0,0,0,0],
                                                 [0,0,0,0,0,0,0,0,0],
                                                 [0,0,0,0,0,0,0,0,0],
                                                 [0,0,0,0,0,0,0,0,0]
                                                ], 0,0)

    MIRACLE_SUDOKUS = solver.miracle_sudokus

    # check that there are exactly 72 miracle sudokus
    assert len(MIRACLE_SUDOKUS) == 72

    # for some known miracle sudokus check that they are all part of the solution

    # the first 2 boards are taken from the first 2 tests of this file

    miracle_sudoku_1 = [[9,4,8,3,7,2,6,1,5],
                        [3,7,2,6,1,5,9,4,8],
                        [6,1,5,9,4,8,3,7,2],
                        [4,8,3,7,2,6,1,5,9],
                        [7,2,6,1,5,9,4,8,3],
                        [1,5,9,4,8,3,7,2,6],
                        [8,3,7,2,6,1,5,9,4],
                        [2,6,1,5,9,4,8,3,7],
                        [5,9,4,8,3,7,2,6,1]]

    miracle_sudoku_2 = [[4,8,3,7,2,6,1,5,9],
                        [7,2,6,1,5,9,4,8,3],
                        [1,5,9,4,8,3,7,2,6],
                        [8,3,7,2,6,1,5,9,4],
                        [2,6,1,5,9,4,8,3,7],
                        [5,9,4,8,3,7,2,6,1],
                        [3,7,2,6,1,5,9,4,8],
                        [6,1,5,9,4,8,3,7,2],
                        [9,4,8,3,7,2,6,1,5]]

    # board idea taken from here https://www.reddit.com/r/sudoku/comments/luqsev/miracle_sudoku_solved/?sort=top
    # last accessed 17/03/2023 at 20:31
    miracle_sudoku_3 = [[5,9,4,8,3,7,2,6,1],
                        [8,3,7,2,6,1,5,9,4],
                        [2,6,1,5,9,4,8,3,7],
                        [9,4,8,3,7,2,6,1,5],
                        [3,7,2,6,1,5,9,4,8],
                        [6,1,5,9,4,8,3,7,2],
                        [4,8,3,7,2,6,1,5,9],
                        [7,2,6,1,5,9,4,8,3],
                        [1,5,9,4,8,3,7,2,6]]

    # board taken from here https://www.reddit.com/r/sudoku/comments/weqf6d/miracle_antiknight_antiking_nonconsecutive_sudoku/
    # last accessed 17/03/2023 at 20:36
    miracle_sudoku_4 = [[1,4,7,5,8,2,9,3,6],
                        [5,8,2,9,3,6,4,7,1],
                        [9,3,6,4,7,1,8,2,5],
                        [4,7,1,8,2,5,3,6,9],
                        [8,2,5,3,6,9,7,1,4],
                        [3,6,9,7,1,4,2,5,8],
                        [7,1,4,2,5,8,6,9,3],
                        [2,5,8,6,9,3,1,4,7],
                        [6,9,3,1,4,7,5,8,2]]

    assert (miracle_sudoku_1 in MIRACLE_SUDOKUS) == True
    assert (miracle_sudoku_2 in MIRACLE_SUDOKUS) == True
    assert (miracle_sudoku_3 in MIRACLE_SUDOKUS) == True
    assert (miracle_sudoku_4 in MIRACLE_SUDOKUS) == True
