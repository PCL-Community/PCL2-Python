from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore

from Pages.PageLaunch.PageLaunchLeft import PageLaunchLeft
from Modules.Base.ModSetup import ModSetup as Setup
from Modules.Base.ModLogging import ModLogging, LoggingType as LT



setup = Setup()


class PageLaunch(QWidget):
    """启动页"""
    def __init__(self, parent=None):
        super().__init__(parent)

        self.logger = ModLogging(module_name="PageLaunch")
        self.logger.write("启动页加载中", LT.INFO)

        # 使用明确的样式表
        self.setStyleSheet("QWidget#PageLaunch { background-color: #000000; }")

        # 初始化左侧 Panel 
        self.PanLeft = PageLaunchLeft(self)
        self.PanLeft.setGeometry(QtCore.QRect(0, 0, 300, (setup.get_settings("size")[1] - setup.get_settings("title_height"))))
