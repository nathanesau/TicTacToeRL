ID_UNDEFINED = 0
ID_X = 1
ID_O = 2

class Board:
    def __init__(self):
        self.data = [[0, 0, 0],[0, 0, 0], [0, 0, 0]]
        self.round = 0

    def getValidMoves(self, id):
        valid_moves = []
        for row in range(3):
            for col in range(3):
                if self.data[row][col] == ID_UNDEFINED:
                    valid_moves.append((row, col))
        return valid_moves

    def updateBoard(self, id, move):
        self.data[move[0]][move[1]] = id
        self.round += 1

    def getWinner(self):
        for id in [ID_X, ID_O]:
            for i in range(3):
                # check rows
                if self.data[i][0] == id and self.data[i][1] == id and self.data[i][2] == id:
                    return id
                # check cols
                if self.data[0][i] == id and self.data[1][i] == id and self.data[2][i] == id:
                    return id
            # check diag
            if self.data[0][0] == id and self.data[1][1] == id and self.data[2][2] == id:
                return id
            if self.data[0][2] == id and self.data[1][1] == id and self.data[2][0] == id:
                return id
        return ID_UNDEFINED
                

    def isBoardFull(self):
        for row in self.data:
            for e in row:
                if e == ID_UNDEFINED:
                    return False
        return True 

    def isGameOver(self):
        return self.getWinner() != ID_UNDEFINED or self.isBoardFull()

    def __str__(self):
        s = ""
        for i in range(3):
            for j in range(3):
                s += str(self.data[i][j])
                if j != 2:
                    s += " "
            if i  != 2:
                s += "\n"
        return s