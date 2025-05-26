# -*- coding: utf-8 -*-
"""FormMain 的 Ui 实现部分
备注：
1. 不需要最大化按钮
2. 按钮的绑定在 FormMain 中"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import Qt

from Controls.MyRoundButton import MyRoundButton
from Modules.Base.ModSetup import ModSetup as Setup


class Ui_FormMain(object):

    def setupUi(self, FormMain: QtWidgets.QWidget):
        # 获取所有需要的设置项
        setup = Setup()
        size = setup.size

        corner_radius = setup.get_settings("corner_radius")
        bg_color = setup.get_settings("ColorBrush5")
        fg_color = setup.get_settings("ColorBrush2")

        FormMain.setObjectName("FormMain")
        FormMain.resize(*size)
        FormMain.setBaseSize(QtCore.QSize(*size))
        FormMain.setStyleSheet(f"background-color: transparent; ")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/.ico/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        FormMain.setWindowIcon(icon)

        # 标题栏 Panel
        self.PanTitle = QtWidgets.QFrame(FormMain)
        self.PanTitle.setGeometry(QtCore.QRect(0, 0, size[0], 48))
        self.PanTitle.setBaseSize(QtCore.QSize(size[0], 48))
        self.PanTitle.setStyleSheet(
            f"""
            QFrame#PanTitle {{
                background-color: {fg_color};
                border-top-left-radius: {corner_radius}px;
                border-top-right-radius: {corner_radius}px;
                border-bottom: none;
            }}
        """
        )
        self.PanTitle.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.PanTitle.setFrameShadow(QtWidgets.QFrame.Plain)
        self.PanTitle.setObjectName("PanTitle")

        # 主 Panel
        self.PanMain = QtWidgets.QFrame(FormMain)
        self.PanMain.setGeometry(QtCore.QRect(0, 48, size[0], (size[1] - 48)))
        self.PanMain.setStyleSheet(
            f"""
            QFrame#PanMain {{
                background-color: {bg_color};
                border-bottom-left-radius: {corner_radius}px;
                border-bottom-right-radius: {corner_radius}px;
                border-top: none;
            }}
        """
        )
        self.PanMain.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.PanMain.setFrameShadow(QtWidgets.QFrame.Plain)
        self.PanMain.setObjectName("PanMain")

        # 标题栏按钮 -- 退出
        self.BtnExit = MyRoundButton(
            self.PanTitle,
            svg_path="Images/BtnTitleClose.svg",
            size=(14, 14),
            tooltip="Exit",
            padding=(7, 7, -10, -10),
        )
        self.BtnExit.setGeometry(QtCore.QRect((size[0] - 50), 12, 13, 13))
        self.BtnExit.setObjectName("BtnExit")

        # 标题栏按钮 -- 最小化
        self.BtnMin = QtWidgets.QPushButton(self.PanTitle)
        self.BtnMin.setGeometry(QtCore.QRect((size[0] - 100), 0, 40, 40))
        self.BtnMin.setStyleSheet("background-color: transparent;")
        self.BtnMin.setText("—")
        self.BtnMin.setObjectName("BtnMin")

        # 标题栏标签 -- 标题
        self.SVGTitle = QSvgWidget(self.PanTitle)
        self.SVGTitle.load("Images/svgtitle.svg")
        self.SVGTitle.setGeometry(QtCore.QRect(0, 4, 120, 40))
        self.SVGTitle.setStyleSheet("background-color: transparent;")
        self.SVGTitle.setObjectName("SVGTitle")

        self.retranslateUi(FormMain)
        QtCore.QMetaObject.connectSlotsByName(FormMain)

    def retranslateUi(self, FormMain: QtWidgets.QWidget):
        _translate = QtCore.QCoreApplication.translate
        FormMain.setWindowTitle(_translate("FormMain", "Plain Craft Launcher 2"))


from Resources import *
