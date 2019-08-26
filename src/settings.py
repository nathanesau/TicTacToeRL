from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

ORGANIZATION_NAME = "N+J software"
APPLICATION_NAME = "TicTacToeRL"


def readDiscountFactorX():
    settings = QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
    settings.beginGroup("RLParams")
    discountFactorX = settings.value("discountFactorX", 0.9)
    settings.endGroup()
    return float(discountFactorX)


def writeDiscountFactorX(discountFactorX):
    settings = QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
    settings.beginGroup("RLParams")
    settings.setValue("discountFactorX", discountFactorX)
    settings.endGroup()


def readExploreFactorX():
    settings = QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
    settings.beginGroup("RLParams")
    exploreFactorX = settings.value("exploreFactorX", 0.1)
    settings.endGroup()
    return float(exploreFactorX)


def writeExploreFactorX(exploreFactorX):
    settings = QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
    settings.beginGroup("RLParams")
    settings.setValue("exploreFactorX", exploreFactorX)
    settings.endGroup()


def readLearnRateX():
    settings = QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
    settings.beginGroup("RLParams")
    learnRateX = settings.value("learnRateX", 0.1)
    settings.endGroup()
    return float(learnRateX)


def writeLearnRateX(learnRateX):
    settings = QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
    settings.beginGroup("RLParams")
    settings.setValue("learnRateX", learnRateX)
    settings.endGroup()


def readDiscountFactorO():
    settings = QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
    settings.beginGroup("RLParams")
    discountFactorO = settings.value("discountFactorO", 0.9)
    settings.endGroup()
    return float(discountFactorO)


def writeDiscountFactorO(discountFactorO):
    settings = QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
    settings.beginGroup("RLParams")
    settings.setValue("discountFactorO", discountFactorO)
    settings.endGroup()


def readExploreFactorO():
    settings = QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
    settings.beginGroup("RLParams")
    exploreFactorO = settings.value("exploreFactorO", 0.1)
    settings.endGroup()
    return float(exploreFactorO)


def writeExploreFactorO(exploreFactorO):
    settings = QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
    settings.beginGroup("RLParams")
    settings.setValue("exploreFactorO", exploreFactorO)
    settings.endGroup()


def readLearnRateO():
    settings = QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
    settings.beginGroup("RLParams")
    learnRateO = settings.value("learnRateO", 0.1)
    settings.endGroup()
    return float(learnRateO)


def writeLearnRateO(learnRateO):
    settings = QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
    settings.beginGroup("RLParams")
    settings.setValue("learnRateO", learnRateO)
    settings.endGroup()
