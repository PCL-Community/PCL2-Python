from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
import os

# 设置工作目录为当前文件所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from FormMain_ui import Ui_FormMain
from Controls.RoundShadow import RoundShadow

class FormMain(RoundShadow):
    """主窗口"""

    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置窗口大小
        self.resize(900, 550)
        
        # 创建一个容器widget
        self.container = QWidget(self)
        self.container.setGeometry(9, 9, self.width() - 18, self.height() - 18)
        
        # 设置UI
        self.ui = Ui_FormMain()
        self.ui.setupUi(self.container)
        
        # 添加窗口大小变化事件处理
        self.resizeEvent = self.onResize
    
    def onResize(self, event):
        """处理窗口大小变化"""
        super().resizeEvent(event)
        # 更新容器大小
        self.container.setGeometry(9, 9, self.width() - 18, self.height() - 18)


