from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from board import *


class PlayerWidget(QWidget):
    def updateWinsLabel(self, wins):
        self.winsLabel.setText("Wins: " + str(wins))

    def updateLossesLabel(self, losses):
        self.lossesLabel.setText("Losses: " + str(losses))

    def updateDrawsLabel(self, draws):
        self.drawsLabel.setText("Draws: " + str(draws))

    def __init__(self, title, parent=None):
        super().__init__(parent)

        self.titleLabel = QLabel()
        self.titleLabel.setText(title)
        self.titleLabel.setFont(QFont("Times", 14))
        self.titleLabel.setStyleSheet("font-weight: bold")

        self.winsLabel = QLabel()
        self.winsLabel.setFont(QFont("Times", 14))
        self.updateWinsLabel(0)

        self.lossesLabel = QLabel()
        self.lossesLabel.setFont(QFont("Times", 14))
        self.updateLossesLabel(0)

        self.drawsLabel = QLabel()
        self.drawsLabel.setFont(QFont("Times", 14))
        self.updateDrawsLabel(0)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addWidget(self.winsLabel)
        self.mainLayout.addWidget(self.lossesLabel)
        self.mainLayout.addWidget(self.drawsLabel)

        self.setLayout(self.mainLayout)


class InfoWidget(QWidget):
    def update(self, winner):
        if winner is ID_X:  # human = X
            self.humanWins += 1
            self.cpuLosses += 1
        elif winner is ID_O:  # cpu = O
            self.humanLosses += 1
            self.cpuWins += 1
        else:  # draw
            self.humanDraws += 1
            self.cpuDraws += 1

        self.humanWidget.updateWinsLabel(self.humanWins)
        self.humanWidget.updateLossesLabel(self.humanLosses)
        self.humanWidget.updateDrawsLabel(self.humanDraws)

        self.cpuWidget.updateWinsLabel(self.cpuWins)
        self.cpuWidget.updateLossesLabel(self.cpuLosses)
        self.cpuWidget.updateDrawsLabel(self.cpuDraws)

    def __init__(self, parent=None):
        self.humanWins = 0
        self.humanDraws = 0
        self.humanLosses = 0

        self.cpuWins = 0
        self.cpuDraws = 0
        self.cpuLosses = 0

        super().__init__(parent)

        self.humanWidget = PlayerWidget("Human: [X]")
        self.cpuWidget = PlayerWidget("CPU: [O]")

        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.humanWidget)
        self.mainLayout.addWidget(self.cpuWidget)

        self.setLayout(self.mainLayout)
