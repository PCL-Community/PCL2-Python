# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt

from Modules.Base.ModSetup import ModSetup as Setup

class PageLaunchLeft(QWidget):
    """启动页左侧面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("PageLaunchLeft") # 放最前面，不然样式表没用

        
        # 设置固定宽度
        self.setFixedWidth(300)
        self.setFixedHeight(Setup().get_settings('size')[1] - Setup().get_settings('title_height') - 16)
        
        # 使用 setAttribute 确保背景色生效
        self.setAttribute(Qt.WA_StyledBackground, True)
        # 设置样式表
        corner_radius = Setup().get_settings('corner_radius')
        self.setStyleSheet(f"""
            QWidget#PageLaunchLeft {{
                background-color: #ffffff;
                border-bottom-left-radius: {corner_radius}px;
            }}
        """)

        # 设置对齐方式
        self.setContentsMargins(0, 0, 0, 0)
        
        # 添加一个测试标签
        self.label = QLabel("左侧面板测试", self)
        self.label.setGeometry(10, 10, 280, 30)

        self.raise_()
