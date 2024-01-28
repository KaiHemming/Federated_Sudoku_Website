import copy
from sudoku_solver import SudokuSolver
from db import miracleSudokuCollection

class MiracleSudokuSolver(SudokuSolver):
    def __init__(self, board):
            SudokuSolver.__init__(self,board)
            self.numberOfMiracles=0
            self.miracle_sudokus=[]

    def check_adjacent_consecutive_move(self, board, x, y, value):
        dx= [-1,0,1,0]
        dy= [0,1,0,-1]
        for l in range(0,4):
            attacked_cell_x=x+dx[l]
            attacked_cell_y=y+dy[l]
            if(attacked_cell_x>=0 and attacked_cell_x<9 and attacked_cell_y>=0 and attacked_cell_y<9):
                if(board[attacked_cell_x][attacked_cell_y]!=0 and abs(board[attacked_cell_x][attacked_cell_y]-value)==1):
                    return False
        return True

    def check_king_move(self, board, x, y, value):
            dx= [-1,-1,-1,0,0,1,1,1]
            dy= [-1,0,1,-1,1,-1,0,1]
            for l in range(0,8):
                attacked_cell_x = x+dx[l]
                attacked_cell_y = y+dy[l]
                if(attacked_cell_x>=0 and attacked_cell_x<9 and attacked_cell_y>=0 and attacked_cell_y<9):
                    if(board[attacked_cell_x][attacked_cell_y]!=0 and board[attacked_cell_x][attacked_cell_y]==value):
                        return False
            return True

    def check_knight_move(self, board, x, y, value):
            dx= [-2,-2,-1,-1,1,1,2,2]
            dy= [1,-1,2,-2,2,-2,1,-1]
            for l in range(0,8):
                attacked_cell_x=x+dx[l]
                attacked_cell_y=y+dy[l]
                if(attacked_cell_x>=0 and attacked_cell_x<9 and attacked_cell_y>=0 and attacked_cell_y<9):
                    if(board[attacked_cell_x][attacked_cell_y]!=0 and board[attacked_cell_x][attacked_cell_y]==value):
                        return False
            return True

    def isSolvable(self, board):
        sudokuData = miracleSudokuCollection.find({}, {"_id": 0})
        for sudoku in sudokuData:
            grid = sudoku["grid"]
            goodSol = True
            for r in range(0,9):
                for c in range(0,9):
                    if board[r][c]!=None and board[r][c]!=str(grid[r][c]):
                        goodSol = False
                        break
            if(goodSol):
                self.toStr(grid)
                self.solution = grid
                self.numberOfSolutions+=1
        if self.numberOfSolutions==0:
            self.invalidBoardMessage = "This board has no solution"
            self.isValidBoard = False
            return False
        elif self.numberOfSolutions>=2:
            self.invalidBoardMessage = "This board has multiple solutions"
            self.isValidBoard = False
            return False
        else:
            self.isValidBoard = True
            return True



    def solve_miracle_sudoku(self, board, x ,y):
        if x==9:
            self.numberOfMiracles+=1
            self.miracle_sudokus.append(copy.deepcopy(board))
            return
        nextX = x+(y+1)//9
        nextY = (y+1) % 9
        if(board[x][y]!=0):
            self.solve_miracle_sudoku(board, nextX, nextY)
        else:
            for digit in range(1,10):
                mask=(1<<digit)
                if (self.rows[x]&mask) == 0 and (self.columns[y]&mask)== 0 and (self.boxes[x//3][y//3]&mask)== 0 and self.check_king_move(board, x, y, digit) and self.check_adjacent_consecutive_move(board, x, y, digit) and self.check_knight_move(board, x, y, digit):
                    board[x][y]=digit
                    self.rows[x]|=mask
                    self.columns[y]|=mask
                    self.boxes[x//3][y//3]|=mask
                    self.solve_miracle_sudoku(board, nextX, nextY)
                    self.rows[x]^=mask
                    self.columns[y]^=mask
                    self.boxes[x//3][y//3]^=mask
                    board[x][y]=0