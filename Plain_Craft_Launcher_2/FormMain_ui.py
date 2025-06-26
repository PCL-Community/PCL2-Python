# -*- coding: utf-8 -*-
"""FormMain 的 Ui 实现部分
备注：
1. 不需要最大化按钮
2. 按钮的绑定在 FormMain 中
3. 窗口的边框拖动处理在 RoundShadow 中"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSvg import QSvgWidget

from Controls.MyRoundButton import MyRoundButton
from Controls.MyIconTextButton import MyIconTextButton
from Modules.Base.ModSetup import ModSetup as Setup
from Modules.Base.ModPage import ModPagePanMain
from Modules.Base.ModLanguage import ModLanguage

lang = ModLanguage()


class Ui_FormMain(object):
    def setupUi(self, FormMain: QtWidgets.QWidget):
        # 获取所有需要的设置项
        setup = Setup()
        size = setup.get_settings('size')
        corner_radius = setup.get_settings('corner_radius')

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
        self.PanMain = QtWidgets.QStackedWidget(FormMain)
        self.PanMain.setGeometry(QtCore.QRect(0, title_height, size[0], (size[1] - title_height)))
        self.PanMain.setStyleSheet(f"""
            QStackedWidget#PanMain {{
                background-color: qlineargradient(spread:pad, x1:0.9, y1:0.1, x2:0, y2:1, 
                                              stop:0 {setup.get_settings('ColorBrush5')}, stop:1 {setup.get_settings('ColorBrush6')});
                border-bottom-left-radius: {corner_radius}px;
                border-bottom-right-radius: {corner_radius}px;
            }}
        """)
        self.PanMain.setObjectName("PanMain")
        self.page_manager = ModPagePanMain(self.PanMain) # 初始化必须放在这

        # 标题栏按钮 -- 退出
        self.BtnExit = MyRoundButton(self.PanTitle, svg_path="Images/BtnTitleExit.svg", size=(36, 36), tooltip="Exit")
        self.BtnExit.setGeometry(QtCore.QRect(size[0], 8, 36, 36))
        self.BtnExit.setObjectName("BtnExit")

        # 标题栏按钮 -- 最小化
        self.BtnMin = MyRoundButton(self.PanTitle, svg_path="Images/BtnTitleMin.svg", size=(36, 36), tooltip="Minisize")
        self.BtnMin.setGeometry(QtCore.QRect(size[0], 8, 36, 36))
        self.BtnMin.setObjectName("BtnMin")

        # 标题栏按钮 -- 切换到启动页面
        self.BtnPageLaunch = MyIconTextButton(self.PanTitle, svg_path="Images/BtnTitlePageLaunch.svg",
                                              text=lang.get_text("PanTitle.Pages.Launch"), command=lambda: self.page_manager.switch_page(0))
        self.BtnPageLaunch.setGeometry(QtCore.QRect(300, 8, 0, 0))                                
        self.BtnPageLaunch.setObjectName("BtnPageLaunch")

        # 标题栏按钮 -- 切换到下载页面
        self.BtnPageDownload = MyIconTextButton(self.PanTitle, svg_path="Images/BtnTitlePageDownload.svg",
                                              text=lang.get_text("PanTitle.Pages.Download"), command=lambda: self.page_manager.switch_page(1))
        self.BtnPageDownload.setGeometry(QtCore.QRect(420, 8, 0, 0))                                
        self.BtnPageDownload.setObjectName("BtnPageDownload")

        # 标题栏按钮 -- 切换到设置页面
        self.BtnPageSettings = MyIconTextButton(self.PanTitle, svg_path="Images/BtnTitlePageSettings.svg",
                                              text="设置", command=lambda: self.page_manager.switch_page(2))
        self.BtnPageSettings.setGeometry(QtCore.QRect(540, 8, 0, 0))                                
        self.BtnPageSettings.setObjectName("BtnPageSettings")

        # 标题栏 Svg -- 标题
        self.SVGTitle = QSvgWidget(self.PanTitle)
        self.SVGTitle.load("Images/svgtitle.svg")
        self.SVGTitle.setGeometry(QtCore.QRect(8, 8, 120, 40))
        self.SVGTitle.setStyleSheet("background-color: transparent;")
        self.SVGTitle.setObjectName("SVGTitle")
        
        # 默认显示第一个页面
        self.PanMain.setCurrentIndex(0)

        self.retranslateUi(FormMain)
        QtCore.QMetaObject.connectSlotsByName(FormMain)

    def retranslateUi(self, FormMain: QtWidgets.QWidget):
        _translate = QtCore.QCoreApplication.translate
        FormMain.setWindowTitle(_translate("FormMain", "Plain Craft Launcher 2"))


from Resources import *
