# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect

from Modules.Base.ModLogging import ModLogging, LoggingType as LT

# 设置工作目录为当前文件所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from FormMain_ui import Ui_FormMain
from Controls.RoundShadow import RoundShadow

class FormMain(RoundShadow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        # 初始化日志
        self.logger = ModLogging(module_name="FormMain")
        
        # 设置窗口标志，确保最小化时显示在任务栏
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint)
        
        # 窗口加载第一步：基础
        # 设置窗口大小
        self.resize(900, 550)
        self.logger.write("窗口加载第一步完成", LT.INFO)
        
        # 窗口加载第二步：加载 UI 控件
        # 创建一个容器widget
        self.container = QWidget(self)
        self.container.setGeometry(9, 9, self.width() - 18, self.height() - 18)
        
        # 设置UI
        self.ui = Ui_FormMain()
        self.ui.setupUi(self.container)
        

        self.logger.write("窗口加载第二步完成", LT.INFO)

        # 窗口加载第三步：链接信号/槽（真的不用设置无边框）
        # 连接按钮事件
        self.ui.BtnExit.clicked.connect(self.close_window)
        self.ui.BtnMin.clicked.connect(self.minimize_window)
        
        # 记录窗口是否最大化
        self.is_maximized = False
        # 记录窗口正常状态下的位置和大小
        self.normal_geometry = self.geometry()
        
        # 初始化拖动相关变量
        self._drag_start_pos = None
        
        # 设置标题栏鼠标追踪
        self.ui.PanTitle.setMouseTracking(True)
        self.ui.PanTitle.mousePressEvent = self.PanTitle_mousePressEvent
        self.ui.PanTitle.mouseMoveEvent = self.PanTitle_mouseMoveEvent
        self.ui.PanTitle.mouseReleaseEvent = self.PanTitle_mouseReleaseEvent

        self.logger.write("窗口加载第三步完成", LT.INFO)

        self.logger.write("FormMain 加载完成", LT.INFO)

    def PanTitle_mousePressEvent(self, event):
        """处理标题栏鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self._drag_start_pos = event.globalPos() - self.pos()
            event.accept()

    def PanTitle_mouseMoveEvent(self, event):
        """处理标题栏鼠标移动事件"""
        if self._drag_start_pos is not None:
            self.move(event.globalPos() - self._drag_start_pos)
            event.accept()

    def PanTitle_mouseReleaseEvent(self, event):
        """处理标题栏鼠标释放事件"""
        if event.button() == Qt.LeftButton:
            self._drag_start_pos = None
            event.accept()

    def resizeEvent(self, a0: QResizeEvent):
        """处理窗口大小变化"""
        super().resizeEvent(a0)
        # 更新容器大小
        self.container.setGeometry(9, 9, self.width() - 18, self.height() - 18)
        
        # 更新面板大小
        self.ui.PanTitle.setGeometry(0, 0, self.container.width(), 40)
        self.ui.PanMain.setGeometry(0, 40, self.container.width(), self.container.height() - 40)

    def close_window(self):
        """处理窗口关闭（对应的信号：BtnExit.clicked）"""

        self.logger.write("按下按钮：BtnExit，正在尝试关闭窗口", LT.INFO)

        try:
            self.close()  # 这会触发QWidget的close事件
            QApplication.processEvents()  # 确保所有待处理的事件都被处理
            QApplication.quit()  # 完全退出应用
        except Exception as e:
            self.logger.write(f"关闭窗口时发生错误：{e}，尝试强制结束程序", LT.ERROR)
            sys.exit(1)  # 强制结束程序
        finally:
            self.logger.write("窗口关闭", LT.INFO)

    def minimize_window(self):
        """跨平台最小化窗口"""
        self.logger.write("按下按钮：BtnMin，正在尝试最小化窗口", LT.INFO)
        self.showMinimized()
    
    def toggle_maximize_window(self):
        """切换窗口最大化/还原状态"""
        if self.isMaximized():
            self.restore_window()
        else:
            self.maximize_window()
    
    def maximize_window(self):
        """跨平台最大化窗口"""
        self.logger.write("按下按钮：BtnMax，正在尝试最大化窗口", LT.INFO)
        # 保存当前窗口位置和大小（如果需要）
        self.showMaximized()
    
    def restore_window(self):
        """跨平台还原窗口"""
        self.logger.write("按下按钮：BtnMax，正在尝试还原窗口", LT.INFO)
        self.showNormal()


