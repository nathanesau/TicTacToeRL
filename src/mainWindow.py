from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from mainWidget import *

import qrc_resources # pyrcc5 resources.qrc -o qrc_resources

class MainWindow(QMainWindow):
    def setupActions(self):
        pass

    def setupMenus(self):
        pass

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupActions()
        self.setupMenus()

        self.mainWidget = MainWidget()
        self.mainWidget.setParent(self)

        self.setCentralWidget(self.mainWidget)
        self.resize(500, 725) # board: 500 x 500, info: 500 x 125, menu: 500 x 100
        self.setWindowTitle("TicTacToeRL")
        self.setWindowIcon(QIcon(":icon.png"))
