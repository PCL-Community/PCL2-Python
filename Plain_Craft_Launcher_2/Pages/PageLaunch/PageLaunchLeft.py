# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt

from Modules.Base.ModSetup import ModSetup

class PageLaunchLeft(QWidget):
    """启动页左侧面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置固定宽度
        self.setFixedWidth(300)
        
        # 设置背景色 - 使用不同的颜色以便于区分
        self.setStyleSheet("QWidget#PageLaunchLeft { background-color: #ff0000; }")  # 使用红色
        
        # 设置对齐方式
        self.setContentsMargins(0, 0, 0, 0)
        
        # 添加一个测试标签
#       self.label = QLabel("左侧面板测试", self)
#       self.label.setGeometry(10, 10, 280, 30)
#       self.label.setStyleSheet("font-size: 16px; color: #333333;")