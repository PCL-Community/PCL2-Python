# -*- coding: utf-8 -*-
"""FormMain 的 Ui 实现部分
备注：
1. 不需要最大化按钮
2. 按钮的绑定在 FormMain 中"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import Qt

from Controls.MyRoundButton import MyRoundButton
from Controls.MyIconTextButton import MyIconTextButton
from Modules.Base.ModSetup import ModSetup as Setup
from Pages.PageLaunch.PageLaunch import PageLaunch
from Modules.Base.ModPage import ModPage as Page


class Ui_FormMain(object):
    def setupUi(self, FormMain: QtWidgets.QWidget):
        # 获取所有需要的设置项
        setup = Setup()
        size = setup.get_settings('size')
        corner_radius = setup.get_settings('corner_radius')
        bg_color = setup.get_settings('ColorBrush5')
        fg_color = setup.get_settings('ColorBrush2')
        self.page_manager = Page()

        FormMain.setObjectName("FormMain")
        FormMain.resize(*size)
        FormMain.setBaseSize(QtCore.QSize(*size))
        FormMain.setStyleSheet(f"background-color: transparent; ")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/.ico/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FormMain.setWindowIcon(icon)

        # 标题栏 Panel
        self.PanTitle = QtWidgets.QFrame(FormMain)
        title_height = setup.get_settings('title_height')
        self.PanTitle.setGeometry(QtCore.QRect(0, 0, size[0], title_height))
        self.PanTitle.setBaseSize(QtCore.QSize(size[0], title_height))
        self.PanTitle.setStyleSheet(f"""
            QFrame#PanTitle {{
                background-color: qlineargradient(spread:pad, x1:0.99, y1:0.01, x2:0, y2:1, 
                                              stop:0 {setup.get_settings('ColorBrush2')}, stop:1 {setup.get_settings('ColorBrush3')});
                border-top-left-radius: {corner_radius}px;
                border-top-right-radius: {corner_radius}px;
                border-bottom: none;
            }}
        """)
        self.PanTitle.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.PanTitle.setFrameShadow(QtWidgets.QFrame.Plain)
        self.PanTitle.setObjectName("PanTitle")

        # 主 Panel
        self.PanMain = QtWidgets.QFrame(FormMain)
        self.PanMain.setGeometry(QtCore.QRect(0, title_height, size[0], (size[1] - title_height)))
        self.PanMain.setStyleSheet(f"""
            QFrame#PanMain {{
                background-color: qlineargradient(spread:pad, x1:0.9, y1:0.1, x2:0, y2:1, 
                                              stop:0 {setup.get_settings('ColorBrush5')}, stop:1 {setup.get_settings('ColorBrush6')});
                border-bottom-left-radius: {corner_radius}px;
                border-bottom-right-radius: {corner_radius}px;
            }}
        """)
        self.PanMain.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.PanMain.setFrameShadow(QtWidgets.QFrame.Plain)
        self.PanMain.setObjectName("PanMain")

        # 标题栏按钮 -- 退出
        self.BtnExit = MyRoundButton(self.PanTitle, svg_path="Images/BtnTitleExit.svg", size=(36, 36), tooltip="Exit")
        self.BtnExit.setGeometry(QtCore.QRect((size[0] - 72), 8, 36, 36))
        self.BtnExit.setObjectName("BtnExit")

        # 标题栏按钮 -- 最小化
        self.BtnMin = MyRoundButton(self.PanTitle, svg_path="Images/BtnTitleMin.svg", size=(36, 36), tooltip="Minisize")
        self.BtnMin.setGeometry(QtCore.QRect((size[0] - 120), 8, 36, 36))
        self.BtnMin.setObjectName("BtnMin")

        # 标题栏按钮 -- 切换到下载页面
        self.BtnPageLaunch = MyIconTextButton(self.PanTitle, svg_path="Images/BtnTitlePageLaunch.svg",
                                              text="Launch",
                                              command=lambda: self.page_manager.switch_page(self.PanMain, 0))
        self.BtnPageLaunch.setGeometry(QtCore.QRect(500, 8, 0, 0))                                
        self.BtnPageLaunch.setObjectName("BtnPageDownload")

        # 标题栏 Svg -- 标题
        self.SVGTitle = QSvgWidget(self.PanTitle)
        self.SVGTitle.load("Images/svgtitle.svg")
        self.SVGTitle.setGeometry(QtCore.QRect(8, 8, 120, 40))
        self.SVGTitle.setStyleSheet("background-color: transparent;")
        self.SVGTitle.setObjectName("SVGTitle")

        self.page = PageLaunch(self.PanMain)
        self.page.setGeometry(QtCore.QRect(0, 0, size[0], (size[1] - title_height)))
        self.page.setObjectName("PageLaunch")
        self.page.raise_()

        self.retranslateUi(FormMain)
        QtCore.QMetaObject.connectSlotsByName(FormMain)

    def retranslateUi(self, FormMain: QtWidgets.QWidget):
        _translate = QtCore.QCoreApplication.translate
        FormMain.setWindowTitle(_translate("FormMain", "Plain Craft Launcher 2"))


from Resources import *
