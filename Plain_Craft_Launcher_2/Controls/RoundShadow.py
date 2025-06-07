# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QRectF, QPoint
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QColor, QPaintEvent, QCursor

from Modules.Base.ModSetup import ModSetup as Setup

class RoundShadow(QWidget):
    """圆角边框类"""

    def __init__(self):
        super().__init__()
        self.border_width = Setup().get_settings('corner_radius')  # 从设置中获取圆角值
        # 设置 窗口无边框和背景透明 *必须
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 修改窗口标志，添加系统菜单和最小化按钮标志
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint)
        
        # 边框调整大小相关变量
        self.resizing = False
        self.resize_edge = None
        self.resize_start_pos = None
        self.resize_start_geometry = None
        self.border_size = 5  # 边框感应区域大小
        
        # 启用鼠标追踪，以便检测鼠标位置
        self.setMouseTracking(True)
        
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
    
    def get_edge(self, pos):
        """根据鼠标位置确定调整大小的边缘"""
        x, y = pos.x(), pos.y()
        width, height = self.width(), self.height()
        
        # 检查是否在边框区域内
        left_edge = x <= self.border_size
        right_edge = width - x <= self.border_size
        top_edge = y <= self.border_size
        bottom_edge = height - y <= self.border_size
        
        # 确定调整大小的边缘
        if top_edge and left_edge:
            return "top_left"
        elif top_edge and right_edge:
            return "top_right"
        elif bottom_edge and left_edge:
            return "bottom_left"
        elif bottom_edge and right_edge:
            return "bottom_right"
        elif left_edge:
            return "left"
        elif right_edge:
            return "right"
        elif top_edge:
            return "top"
        elif bottom_edge:
            return "bottom"
        else:
            return None
    
    def mousePressEvent(self, event):
        """处理鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            # 检查是否在边框区域
            edge = self.get_edge(event.pos())
            if edge:
                self.resizing = True
                self.resize_edge = edge
                self.resize_start_pos = event.globalPos()
                self.resize_start_geometry = self.geometry()
                event.accept()
                return
        # 如果不是在边框区域，则调用父类方法
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """处理鼠标移动事件"""
        # 如果正在调整大小
        if self.resizing and self.resize_edge:
            # 计算鼠标移动的距离
            delta = event.globalPos() - self.resize_start_pos
            new_geometry = self.resize_start_geometry
            
            # 根据调整的边缘更新几何形状
            if "left" in self.resize_edge:
                new_geometry.setLeft(new_geometry.left() + delta.x())
            if "right" in self.resize_edge:
                new_geometry.setRight(new_geometry.right() + delta.x())
            if "top" in self.resize_edge:
                new_geometry.setTop(new_geometry.top() + delta.y())
            if "bottom" in self.resize_edge:
                new_geometry.setBottom(new_geometry.bottom() + delta.y())
            
            # 设置最小大小限制
            min_width = 300
            min_height = 200
            if new_geometry.width() >= min_width and new_geometry.height() >= min_height:
                self.setGeometry(new_geometry)
            
            event.accept()
            return
        else:
            # 更新鼠标指针形状
            edge = self.get_edge(event.pos())
            if edge:
                if edge in ["left", "right"]:
                    self.setCursor(Qt.SizeHorCursor)
                elif edge in ["top", "bottom"]:
                    self.setCursor(Qt.SizeVerCursor)
                elif edge in ["top_left", "bottom_right"]:
                    self.setCursor(Qt.SizeFDiagCursor)
                elif edge in ["top_right", "bottom_left"]:
                    self.setCursor(Qt.SizeBDiagCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
        
        # 如果不是在调整大小，则调用父类方法
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """处理鼠标释放事件"""
        if event.button() == Qt.LeftButton and self.resizing:
            self.resizing = False
            self.resize_edge = None
            event.accept()
            return
        # 如果不是在调整大小，则调用父类方法
        super().mouseReleaseEvent(event)
