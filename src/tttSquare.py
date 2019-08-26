from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class TTTSquare(QLabel):
    def __init__(self, row, col, parent=None):
        super().__init__(parent)
        self.row = row
        self.col = col
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont("Times", 36))
        self.setStyleSheet("font-weight: bold")

        square_num = 3 * (self.row - 1) + self.col
        if square_num % 2:
            self.setStyleSheet("background-color: white")
        else:
            self.setStyleSheet("background-color: grey")

    def mousePressEvent(self, event):
        self.parent().onSquareClicked(self)