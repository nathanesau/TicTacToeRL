import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from board import *
from strategy import *

import settings
import qrc_resources


def get_x_reward(board):
    winner = board.getWinner()
    return 100 if winner is ID_X else 0 if winner is ID_UNDEFINED else -100


def get_o_reward(board):
    winner = board.getWinner()
    return 100 if winner is ID_O else 0 if winner is ID_UNDEFINED else -100


def playTrainingGame(strategyx, strategyo):
    board = Board()
    curr_statex, next_statex = None, None
    curr_stateo, next_stateo = None, None
    curr_id = ID_X

    while True:

        if curr_id == ID_X:
            curr_statex = tuple(tuple(row) for row in board.data)
            action_spacex = board.getValidMoves(ID_X)
            actionx = strategyx.selectAction(curr_statex, action_spacex)
            board.updateBoard(ID_X, actionx)

            # update o after x goes
            if board.round > 1:
                next_stateo = tuple(tuple(row) for row in board.data)
                rewardo = get_o_reward(board)
                strategyo.update(curr_stateo, next_stateo,
                                 actiono, rewardo, board.isGameOver())

            if board.isGameOver():  # o doesn't get to go again (they have lost) - update x
                next_statex = tuple(tuple(row) for row in board.data)
                rewardx = get_x_reward(board)
                strategyx.update(curr_statex, next_statex,
                                 actionx, rewardx, True)
                return

        else:  # ID_O
            curr_stateo = tuple(tuple(row) for row in board.data)
            action_spaceo = board.getValidMoves(ID_O)
            actiono = strategyo.selectAction(curr_stateo, action_spaceo)
            board.updateBoard(ID_O, actiono)

            # update x after o goes
            next_statex = tuple(tuple(row) for row in board.data)
            rewardx = get_x_reward(board)
            strategyx.update(curr_statex, next_statex, actionx,
                             rewardx, board.isGameOver())

            if board.isGameOver():  # x doesn't get to go again (they have lost) - update o
                next_stateo = tuple(tuple(row) for row in board.data)
                rewardo = get_o_reward(board)
                strategyo.update(curr_stateo, next_stateo,
                                 actiono, rewardo, True)
                return

        curr_id = ID_O if curr_id is ID_X else ID_X  # at end of loop


def trainComputer(numGames, dfx, efx, lrx, dfo, efo, lro, progressBar):
    strategyx = Strategy(dfx, efx, lrx)
    strategyo = Strategy(dfo, efo, lro)

    if os.path.exists(strategyx_file):
        strategyx.qtable = pickle.load(open(strategyx_file, 'rb'))
    if os.path.exists(strategyo_file):
        strategyo.qtable = pickle.load(open(strategyo_file, 'rb'))

    for i in range(numGames):
        percent_done = float(i) / numGames * 100.0
        progressBar.setValue(percent_done)
        playTrainingGame(strategyx, strategyo)

    # pickle save the qtables
    pickle.dump(strategyx.qtable, open(strategyx_file, 'wb'))
    pickle.dump(strategyo.qtable, open(strategyo_file, 'wb'))


class TrainParamWidget(QWidget):
    def __init__(self, df, ef, lr, parent=None):
        super().__init__(parent)

        self.discFactorLabel = QLabel()
        self.discFactorLabel.setText("Discount Factor (between 0 and 1)")

        self.discFactorSB = QDoubleSpinBox()
        self.discFactorSB.setRange(0.0, 1.0)
        self.discFactorSB.setSingleStep(0.1)
        self.discFactorSB.setValue(df)

        self.exploreFactorLabel = QLabel()
        self.exploreFactorLabel.setText("Explore Factor (between 0 and 1)")

        self.exploreFactorSB = QDoubleSpinBox()
        self.exploreFactorSB.setRange(0.0, 1.0)
        self.exploreFactorSB.setSingleStep(0.1)
        self.exploreFactorSB.setValue(ef)

        self.learnRateLabel = QLabel()
        self.learnRateLabel.setText("Learn Factor (between 0 and 1)")

        self.learnRateSB = QDoubleSpinBox()
        self.learnRateSB.setRange(0.0, 1.0)
        self.learnRateSB.setSingleStep(0.1)
        self.learnRateSB.setValue(lr)

        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.discFactorLabel, 1, 1)
        self.mainLayout.addWidget(self.discFactorSB, 1, 2)
        self.mainLayout.addWidget(self.exploreFactorLabel, 2, 1)
        self.mainLayout.addWidget(self.exploreFactorSB, 2, 2)
        self.mainLayout.addWidget(self.learnRateLabel, 3, 1)
        self.mainLayout.addWidget(self.learnRateSB, 3, 2)

        self.setLayout(self.mainLayout)


class TrainDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        discFactorX = settings.readDiscountFactorX()
        exploreFactorX = settings.readExploreFactorX()
        learnRateX = settings.readLearnRateX()
        self.xparamWidget = TrainParamWidget(
            discFactorX, exploreFactorX, learnRateX)
        self.xparamGroupBox = QGroupBox()
        self.xparamGroupBox.setTitle("CPU [X] training parameters")
        self.xparamLayout = QVBoxLayout()
        self.xparamLayout.addWidget(self.xparamWidget)
        self.xparamGroupBox.setLayout(self.xparamLayout)

        discFactorO = settings.readDiscountFactorO()
        exploreFactorO = settings.readExploreFactorO()
        learnRateO = settings.readLearnRateO()
        self.oparamWidget = TrainParamWidget(
            discFactorO, exploreFactorO, learnRateO)
        self.oparamGroupBox = QGroupBox()
        self.oparamGroupBox.setTitle("CPU [O] training parameters")
        self.oparamLayout = QVBoxLayout()
        self.oparamLayout.addWidget(self.oparamWidget)
        self.oparamGroupBox.setLayout(self.oparamLayout)

        self.numTrainGamesLabel = QLabel()
        self.numTrainGamesLabel.setText("Number of training games to play")

        self.numTrainGamesSB = QSpinBox()
        self.numTrainGamesSB.setRange(0, 10000)
        self.numTrainGamesSB.setSingleStep(500)
        self.numTrainGamesSB.setValue(1000)

        self.otherInputsGroupBox = QGroupBox()
        self.otherInputsGroupBox.setTitle("Other inputs")
        self.otherInputsLayout = QHBoxLayout()
        self.otherInputsLayout.addWidget(self.numTrainGamesLabel)
        self.otherInputsLayout.addWidget(self.numTrainGamesSB)
        self.otherInputsGroupBox.setLayout(self.otherInputsLayout)

        self.performTrainingButton = QPushButton()
        self.performTrainingButton.setText("Perform training")
        self.performTrainingButton.pressed.connect(
            self.onPerformTrainingButton)

        self.progressBar = QProgressBar()
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setTextVisible(True)
        self.progressBar.setStyleSheet("background-color: white; color: black")
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setFormat("Testing Progress (%)")
        self.progressBar.hide()

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.xparamGroupBox)
        self.mainLayout.addWidget(self.oparamGroupBox)
        self.mainLayout.addWidget(self.otherInputsGroupBox)
        self.mainLayout.addWidget(self.performTrainingButton)
        self.mainLayout.addWidget(self.progressBar)

        self.setLayout(self.mainLayout)
        self.setWindowTitle("Train Dialog")
        self.setWindowIcon(QIcon(":icon.png"))

        self.saveParamAction = QAction("Save parameters")
        self.saveParamAction.triggered.connect(self.onSaveParamAction)
        self.fileMenu = QMenu("File")
        self.fileMenu.addAction(self.saveParamAction)
        self.menuBar = QMenuBar()
        self.menuBar.addMenu(self.fileMenu)
        self.layout().setMenuBar(self.menuBar)

    def onSaveParamAction(self):
        settings.writeDiscountFactorX(self.xparamWidget.discFactorSB.value())
        settings.writeExploreFactorX(self.xparamWidget.exploreFactorSB.value())
        settings.writeLearnRateX(self.xparamWidget.learnRateSB.value())
        settings.writeDiscountFactorO(self.oparamWidget.discFactorSB.value())
        settings.writeExploreFactorO(self.oparamWidget.exploreFactorSB.value())
        settings.writeLearnRateO(self.oparamWidget.learnRateSB.value())

        msg = QMessageBox()
        msg.setWindowTitle("Saved Parameters")
        msg.setText("Saved the parameter values to settings")
        msg.setWindowIcon(QIcon(":icon.png"))
        msg.exec()


    def onPerformTrainingButton(self):
        self.progressBar.show()
        numGames = self.numTrainGamesSB.value()
        dfx = self.xparamWidget.discFactorSB.value()
        efx = self.xparamWidget.exploreFactorSB.value()
        lrx = self.xparamWidget.learnRateSB.value()
        dfo = self.oparamWidget.discFactorSB.value()
        efo = self.oparamWidget.exploreFactorSB.value()
        lro = self.oparamWidget.learnRateSB.value()
        trainComputer(numGames, dfx, efx, lrx, dfo, efo, lro, self.progressBar)
        self.progressBar.hide()

        msg = QMessageBox()
        msg.setWindowTitle("Training Done")
        msg.setText("Finished all training games")
        msg.setWindowIcon(QIcon(":icon.png"))
        msg.exec()
