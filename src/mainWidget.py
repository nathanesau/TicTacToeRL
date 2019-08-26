from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from infoWidget import *
from boardWidget import *
from trainDialog import *

class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.infoWidget = InfoWidget()
        self.infoLayout = QHBoxLayout()
        self.infoLayout.addWidget(self.infoWidget)

        self.boardWidget = BoardWidget()
        self.boardLayout = QHBoxLayout()
        self.boardLayout.addWidget(self.boardWidget)

        self.newGameButton = QPushButton()
        self.newGameButton.setText("New Game")
        self.newGameButton.setFont(QFont("Times", 14))
        self.newGameButton.pressed.connect(self.onNewGameButton)
        self.trainButton = QPushButton()
        self.trainButton.setText("Train CPU")
        self.trainButton.setFont(QFont("Times", 14))
        self.trainButton.pressed.connect(self.onTrainButton)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.newGameButton)
        self.buttonLayout.addWidget(self.trainButton)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.infoLayout, 20)
        self.mainLayout.addLayout(self.boardLayout, 65)
        self.mainLayout.addLayout(self.buttonLayout, 15)

        self.setLayout(self.mainLayout)

    def onNewGameButton(self):
        self.boardWidget.clearBoard()
        # cpu makes a move
        board = self.boardWidget.board

    def onTrainButton(self):
        trainDlg = TrainDialog()
        trainDlg.exec()
        
        # update board widget strategy (reload pickle file)
        self.boardWidget.clearBoard()
        self.boardWidget.strategy_o = Strategy(0, 0, 0)
        if os.path.exists(strategyo_file):
            self.boardWidget.strategy_o.qtable = pickle.load(open(strategyo_file, 'rb'))

    def updateInfoWidget(self, winner):
        self.infoWidget.update(winner)