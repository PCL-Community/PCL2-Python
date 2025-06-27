from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore

from Modules.Base.ModSetup import ModSetup as Setup
from Modules.Base.ModLogging import ModLogging, LoggingType as LT
from Controls.MyCard import MyCard

setup = Setup()


class PageDownload(QWidget):
    """下载页"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.logger = ModLogging(module_name="PageDownload")
        self.logger.write("加载中", LT.INFO)

        # 先设置objectName
        self.setObjectName("PageDownload")

        # 使用 setAttribute 确保背景色生效
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        # 设置样式表
        self.setStyleSheet(f"""
            QWidget#PageDownload {{
                background-color: transparent;
                border-bottom-left-radius: {Setup().get_settings('corner_radius')}px;
            }}
        """)

        # 初始化左侧 Panel
#       self.PanLeft = PageLaunchLeft(self)
#       self.PanLeft.setGeometry(
#           QtCore.QRect(0, 0, 300, (setup.get_settings("size")[1] - setup.get_settings("title_height"))))
        self.card = MyCard(self, title_text="下载", size=(200, 300), margin=(8, 8, 8, 8), can_collapse=True, objectName="CardDownload")

        
