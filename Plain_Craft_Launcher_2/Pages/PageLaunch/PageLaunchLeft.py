# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from Modules.Base.ModSetup import ModSetup

class PageLaunchLeft(QWidget):
    """启动页左侧面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置固定宽度
        self.setFixedWidth(300)
        
        # 设置背景色
        self.setStyleSheet(f"background-color: {ModSetup().get_settings('ColorBrush0')};")
        
        # 设置对齐方式
        self.setContentsMargins(0, 0, 0, 0)