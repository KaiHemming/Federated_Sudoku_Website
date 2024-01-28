import pymongo
# import certifi

# DATABASE
try:
    # client = pymongo.MongoClient("mongodb+srv://N773850:fantastic@cluster1.b4qzrkj.mongodb.net/?retryWrites=true&w=majority")

    #  please don't delete this comment and the import line
    # client = pymongo.MongoClient(
    #     "mongodb+srv://N773850:fantastic@cluster1.b4qzrkj.mongodb.net/?retryWrites=true&w=majority",
    #     tlsCAFile=certifi.where())

# In production switch to the url from below:
     client = pymongo.MongoClient("mongodb://admin:Aigh7eek@0.0.0.0:22564")
except Exception:
    print("Error")

db = client['User_data']
userCollection = db['users']
sudokuCollection = db['sudoku']
commentCollection = db['comment']
miracleSudokuCollection = db['miracle_sudoku']
miracleSudokuLevelsCollection = db['miracle_sudoku_levels']
leaderboardCollection = db['leaderboard_times']