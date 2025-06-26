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
from Modules.Base.ModSetup import ModSetup as Setup

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
        self.logger.write("窗口基础设置完成", LT.INFO, "初始化", "完成")
        
        # 窗口加载第二步：加载 UI 控件
        # 创建一个容器widget
        self.container = QWidget(self)
        self.container.setGeometry(9, 9, self.width() - 18, self.height() - 18)
        
        # 设置UI
        self.ui = Ui_FormMain()
        self.ui.setupUi(self.container)
        

        self.logger.write("UI控件加载完成", LT.INFO, "初始化", "完成")

        # 窗口加载第三步：链接信号/槽（真的不用设置无边框）
        # 连接按钮事件
        self.ui.BtnExit.clicked.connect(self.close_window)
        self.ui.BtnMin.clicked.connect(self.minimize_window)

        # 记录窗口正常状态下的位置和大小
        self.normal_geometry = self.geometry()
        
        # 初始化拖动相关变量
        self._drag_start_pos = None
        
        # 设置标题栏鼠标追踪
        self.ui.PanTitle.setMouseTracking(True)
        self.ui.PanTitle.mousePressEvent = self.PanTitle_mousePressEvent
        self.ui.PanTitle.mouseMoveEvent = self.PanTitle_mouseMoveEvent
        self.ui.PanTitle.mouseReleaseEvent = self.PanTitle_mouseReleaseEvent

        self.logger.write("窗口样式设置完成", LT.INFO, "初始化", "完成")

        self.logger.write("主窗口初始化完成", LT.INFO, "初始化", "完成")

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
        
        title_height = Setup().get_settings('title_height')
        self.ui.PanTitle.setGeometry(0, 0, self.container.width(), title_height)
        self.ui.PanMain.setGeometry(0, title_height, self.container.width(), self.container.height() - title_height)

        self.ui.BtnMin.setGeometry(QRect((self.container.width() - 96), 8, 64, title_height))
        self.ui.BtnExit.setGeometry(QRect((self.container.width() - 48), 8, 16, title_height))
        
        # 不需要单独更新页面大小，QStackedWidget 会自动调整子组件大小

    def close_window(self):
        """处理窗口关闭（对应的信号：BtnExit.clicked）"""

        self.logger.write("用户点击关闭按钮", LT.INFO, "窗口操作", "进行中")

        try:
            self.close()  # 这会触发QWidget的close事件
            QApplication.processEvents()  # 确保所有待处理的事件都被处理
            QApplication.quit()  # 完全退出应用
        except Exception as e:
            self.logger.write(f"关闭窗口失败：{e}", LT.ERROR, "窗口操作", "异常")
            sys.exit(1)  # 强制结束程序
        finally:
            self.logger.write("窗口已关闭", LT.INFO, "窗口操作", "完成")

    def minimize_window(self):
        """跨平台最小化窗口"""
        self.logger.write("用户点击最小化按钮", LT.INFO, "窗口操作", "进行中")
        self.showMinimized()
    


