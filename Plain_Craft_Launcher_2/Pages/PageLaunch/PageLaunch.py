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

        # 先设置objectName
        self.setObjectName("PageLaunch")
        
        # 使用 setAttribute 确保背景色生效
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        # 设置样式表
        self.setStyleSheet(f"""
            QWidget#PageLaunch {{
                background-color: transparent;
                border-bottom-left-radius: {Setup().get_settings('corner_radius')}px;
            }}
        """)


        # 初始化左侧 Panel 
        self.PanLeft = PageLaunchLeft(self)
        self.PanLeft.setGeometry(QtCore.QRect(0, 0, 300, (setup.get_settings("size")[1] - setup.get_settings("title_height"))))


    def resizeEvent(self, event):
        """处理页面大小变化"""
        super().resizeEvent(event)
        # 更新左侧面板高度
        self.PanLeft.setFixedHeight(self.height())
