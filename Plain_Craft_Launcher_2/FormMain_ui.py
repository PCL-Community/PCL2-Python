from PyQt5 import QtCore, QtGui, QtWidgets
from Modules.Base.ModSetup import ModSetup as Setup

class Ui_FormMain(object):
    def setupUi(self, FormMain: QtWidgets.QWidget):
        FormMain.setObjectName("FormMain")
        FormMain.resize(900, 550)
        FormMain.setBaseSize(QtCore.QSize(900, 550))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/.ico/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FormMain.setWindowIcon(icon)
        self.PanTitle = QtWidgets.QFrame(FormMain)
        self.PanTitle.setGeometry(QtCore.QRect(0, 0, 900, 40))
        self.PanTitle.setBaseSize(QtCore.QSize(900, 40))
        self.PanTitle.setStyleSheet(f"background-color: {Setup().get_settings('bg')};")
        self.PanTitle.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.PanTitle.setFrameShadow(QtWidgets.QFrame.Raised)
        self.PanTitle.setObjectName("PanTitle")
        self.PanMain = QtWidgets.QFrame(FormMain)
        self.PanMain.setGeometry(QtCore.QRect(0, 40, 901, 511))
        self.PanMain.setStyleSheet("background-color: skyblue;")
        self.PanMain.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.PanMain.setFrameShadow(QtWidgets.QFrame.Raised)
        self.PanMain.setObjectName("PanMain")

        self.retranslateUi(FormMain)
        QtCore.QMetaObject.connectSlotsByName(FormMain)

    def retranslateUi(self, FormMain: QtWidgets.QWidget):
        _translate = QtCore.QCoreApplication.translate
        FormMain.setWindowTitle(_translate("FormMain", "Plain Craft Launcher 2"))

from Resources import *
