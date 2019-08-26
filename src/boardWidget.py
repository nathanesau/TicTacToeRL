from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from tttSquare import *
from strategy import *
from board import *

# currently, only strategyo
def getCpuMove(strategyo, board):
    curr_stateo = tuple(tuple(row) for row in board.data)
    action_spaceo = board.getValidMoves(ID_O)
    actiono = strategyo.selectAction(curr_stateo, action_spaceo)
    return actiono


class BoardWidget(QWidget):
    def clearBoard(self):
        self.board = Board()
        self.redrawBoard()

    def redrawBoard(self):  # draw self.board
        for i in range(3):
            symbol = "X" if self.board.data[0][i] is 1 else "O" if self.board.data[0][i] is 2 else ""
            self.row1Squares[i].setText(symbol)
        for i in range(3):
            symbol = "X" if self.board.data[1][i] is 1 else "O" if self.board.data[1][i] is 2 else ""
            self.row2Squares[i].setText(symbol)
        for i in range(3):
            symbol = "X" if self.board.data[2][i] is 1 else "O" if self.board.data[2][i] is 2 else ""
            self.row3Squares[i].setText(symbol)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.strategy_o = Strategy(0, 0, 0)
        if os.path.exists(strategyo_file):
            self.strategy_o.qtable = pickle.load(open(strategyo_file, 'rb'))
        self.board = Board()

        self.row1Squares = [TTTSquare(1, col, self) for col in range(1, 4)]
        self.row2Squares = [TTTSquare(2, col, self) for col in range(1, 4)]
        self.row3Squares = [TTTSquare(3, col, self) for col in range(1, 4)]

        self.row1Layout = QHBoxLayout()
        self.row1Layout.setSpacing(0)
        for square in self.row1Squares:
            self.row1Layout.addWidget(square)

        self.row2Layout = QHBoxLayout()
        self.row2Layout.setSpacing(0)
        for square in self.row2Squares:
            self.row2Layout.addWidget(square)

        self.row3Layout = QHBoxLayout()
        self.row3Layout.setSpacing(0)
        for square in self.row3Squares:
            self.row3Layout.addWidget(square)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.addLayout(self.row1Layout)
        self.mainLayout.addLayout(self.row2Layout)
        self.mainLayout.addLayout(self.row3Layout)

        self.setLayout(self.mainLayout)

    def onSquareClicked(self, square):
        if self.board.data[square.row - 1][square.col - 1] != ID_UNDEFINED:
            return

        if self.board.isGameOver(): # new game should be pressed first
            return

        # human action (if necessary)
        if not self.board.isGameOver():
            self.board.updateBoard(ID_X, (square.row - 1, square.col - 1))
            self.redrawBoard()

        # cpu action (if necessary)
        if not self.board.isGameOver():
            cpu_move = getCpuMove(self.strategy_o, self.board)
            self.board.updateBoard(ID_O, cpu_move)
            self.redrawBoard()

        if self.board.isGameOver():
            msgBox = QMessageBox()
            
            winner = self.board.getWinner()
            if winner is ID_UNDEFINED:
                msgBox.setText("Game ended in a draw")
            elif winner is ID_X:
                msgBox.setText("Human [X] won the game")
            else:
                msgBox.setText("CPU [O] won the game")
                
            msgBox.setWindowTitle("Game result")
            msgBox.setWindowIcon(QIcon(":icon.png"))
            msgBox.exec()

            self.parent().updateInfoWidget(winner)