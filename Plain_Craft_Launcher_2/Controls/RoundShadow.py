# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QColor, QPaintEvent

from Modules.Base.ModSetup import mod_setup as setup

class RoundShadow(QWidget):
    """圆角边框类"""

    def __init__(self):
        super().__init__()
        self.border_width = setup.corner_radius # 从设置中获取圆角值
        # 设置 窗口无边框和背景透明 *必须
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 修改窗口标志，添加系统菜单和最小化按钮标志
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint)
        
    def paintEvent(self, a0: QPaintEvent):
        # 阴影
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        pat = QPainter(self)
        pat.setRenderHint(pat.Antialiasing)
        pat.fillPath(path, QBrush(Qt.white))
        color = QColor(0, 0, 0, 30)
        for i in range(10):
            i_path = QPainterPath()
            i_path.setFillRule(Qt.WindingFill)
            ref = QRectF(10 - i, 10 - i, self.width() - (10 - i) * 2, self.height() - (10 - i) * 2)
            i_path.addRoundedRect(ref, self.border_width, self.border_width)
            pat.setPen(color)
            pat.drawPath(i_path)
        # 圆角
        pat2 = QPainter(self)
        pat2.setRenderHint(pat2.Antialiasing)  # 抗锯齿
        pat2.setBrush(Qt.white)
        pat2.setPen(Qt.transparent)
        rect = self.rect()
        rect.setLeft(9)
        rect.setTop(9)
        rect.setWidth(rect.width() - 9) 
        rect.setHeight(rect.height() - 9) 
        pat2.drawRoundedRect(rect, self.border_width, self.border_width)  # 使用动态获取的圆角值
