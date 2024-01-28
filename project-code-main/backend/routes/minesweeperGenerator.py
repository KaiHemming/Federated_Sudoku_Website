import random


def generate(row, column, mine):
    mines = []  # position of all mines
    returnData = {}

    # generate board
    board = [["0" for i in range(column)] for j in range(row)]
    i = 0
    # insert mines
    while True:
        col = random.randint(0, column - 1)
        r = random.randint(0, row - 1)
        if board[r][col] != "*":
            board[r][col] = "*"
            mines.append([r, col])
            i += 1
        if i == mine:
            break

    # initialise all
    for m in mines:
        r = m[0]
        c = m[1]
        neighbour = [(r - 1, c - 1), (r - 1, c), (r - 1, c + 1),
                     (r, c - 1), (r, c + 1),
                     (r + 1, c - 1), (r + 1, c), (r + 1, c + 1)]

        for n in neighbour:
            if n[0] >= 0 and n[1] >= 0:
                if n[0] < row and n[1] < column:
                    if board[n[0]][n[1]] != "*":
                        num = int(board[n[0]][n[1]])
                        num += 1
                        board[n[0]][n[1]] = str(num)

    returnData['grid'] = board
    returnData['minePosition'] = mines
    returnData['row'] = row
    returnData['col'] = column
    returnData['mines'] = mine

    return returnData
