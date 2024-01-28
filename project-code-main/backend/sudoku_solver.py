import copy
class SudokuSolver:
    def __init__(self, board):
        self.rows = [0]*9
        self.columns = [0]*9
        self.boxes = [[0]*3 for i in range(3)]
        self.solution = [[0]*9 for i in range(9)]
        self.board = board
        self.isValidBoard = True
        self.invalidBoardMessage=""
        self.numberOfSolutions = 0
        self.numberOfMiracles=0
        self.miracle_sudokus=[]

    def toStr(self, board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j]==0:
                    board[i][j]=None
                else:
                    try:
                        board[i][j] = str(board[i][j])
                    except TypeError:
                        pass


    def toInt(self, board):
        digits = {"1","2","3","4","5","6","7","8","9"}
        for row in range(len(board)):
            for col in range(len(board[0])):
                if(board[row][col] in digits):
                    board[row][col] = int(board[row][col])
                elif board[row][col] == None:
                    board[row][col] = 0
                else:
                    self.isValidBoard = False
                    self.invalidBoardMessage= "The element at position ("+str(row+1)+", "+str(col+1)+") is not an integer between 1 and 9"
                    return


    def compareToSolution(self, board, solution, full=False):
        digits = {"1","2","3","4","5","6","7","8","9"}
        for row in range(len(board)):
            for col in range(len(board[0])):
                if((full==True or (board[row][col] in digits)) and board[row][col] != solution[row][col]):
                    return "Wrong choice at ("+str(row+1)+", "+str(col+1)+")"
        return "The solution is correct"

    def initializeBitmasks(self, board):
        self.toInt(board)
        if self.isValidBoard == False:
            return
        for row in range(0,9):
            for col in range(0,9):
                if board[row][col]!=0:
                    bitmask=(1<<board[row][col])
                    if bitmask & self.rows[row] !=0:
                        self.isValidBoard = False
                        self.invalidBoardMessage= "On row "+str(row+1)+" there is more than one "+ str(board[row][col])
                        return
                    self.rows[row]|= bitmask
                    if bitmask & self.columns[col] !=0:
                        self.isValidBoard = False
                        self.invalidBoardMessage = "On column "+str(col+1)+" there is more than one "+ str(board[row][col])
                        return
                    self.columns[col]|=bitmask
                    if bitmask & self.boxes[row//3][col//3] !=0:
                        self.isValidBoard = False
                        self.invalidBoardMessage =  "In the box that contains the element at the coordinate ("+str(row+1)+", "+str(col+1)+") there is more than one "+ str(board[row][col])
                        return
                    self.boxes[row//3][col//3]|=bitmask


    def getHint(self, board, solution):
        hintX=-1
        hintY=-1
        minimumNumberOfPossibilitiesInCell=9
        self.initializeBitmasks(board)
        self.toInt(solution)
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == 0:
                   possibleValuesBitmask=((self.rows[row]|self.columns[col])|self.boxes[row//3][col//3])
                   numberOfPossibilitiesInCell=0
                   for possibleValue in range(1,10):
                      if(((1<<possibleValue)&possibleValuesBitmask)==0):
                        numberOfPossibilitiesInCell+=1
                   if(numberOfPossibilitiesInCell<=minimumNumberOfPossibilitiesInCell):
                      hintX=row
                      hintY=col
                      minimumNumberOfPossibilitiesInCell=numberOfPossibilitiesInCell
        if hintX!=-1:
            board[hintX][hintY]=solution[hintX][hintY]
        self.toStr(board)
        self.toStr(solution)

    def solveSudoku(self, board):
        copyOfBoard = copy.deepcopy(board)
        self.initializeBitmasks(copyOfBoard)
        if self.isValidBoard == False:
           return
        self.recursiveSolve(copyOfBoard, 0, 0)
        if self.numberOfSolutions == 0:
           self.isValidBoard = False
           self.invalidBoardMessage = "This sudoku puzzle has no solution."
        elif self.numberOfSolutions == 2:
           self.isValidBoard = False
           self.invalidBoardMessage = "This sudoku puzzle has multiple solutions."

    def recursiveSolve(self, board, x, y):
        if x==9:
            if self.numberOfSolutions == 1:
                self.numberOfSolutions = 2
            else:
                self.numberOfSolutions = 1
                self.solution = copy.deepcopy(board)
            return
        nextX = x+(y+1)//9
        nextY = (y+1) % 9
        if(board[x][y]!=0):
            self.recursiveSolve(board, nextX, nextY)
        else:
            for digit in range(1,10):
                mask=(1<<digit)
                if (self.rows[x]&mask) == 0 and (self.columns[y]&mask)== 0 and (self.boxes[x//3][y//3]&mask)== 0:
                    board[x][y]=digit
                    self.rows[x]|=mask
                    self.columns[y]|=mask
                    self.boxes[x//3][y//3]|=mask
                    self.recursiveSolve(board, nextX, nextY)
                    if self.numberOfSolutions==2:
                        return
                    self.rows[x]^=mask
                    self.columns[y]^=mask
                    self.boxes[x//3][y//3]^=mask
                    board[x][y]=0