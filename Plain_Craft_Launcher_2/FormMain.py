import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QResizeEvent

# 设置工作目录为当前文件所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from FormMain_ui import Ui_FormMain
from Controls.RoundShadow import RoundShadow

class FormMain(RoundShadow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        # 设置窗口大小
        self.resize(900, 550)
        
        # 创建一个容器widget
        self.container = QWidget(self)
        self.container.setGeometry(9, 9, self.width() - 18, self.height() - 18)
        
        # 设置UI
        self.ui = Ui_FormMain()
        self.ui.setupUi(self.container)
        
        # 添加窗口大小变化事件处理
        # 通过重写resizeEvent方法处理窗口大小变化

    def resizeEvent(self, a0: QResizeEvent):
        """处理窗口大小变化"""
        super().resizeEvent(a0)
        # 更新容器大小
        self.container.setGeometry(9, 9, self.width() - 18, self.height() - 18)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    t = FormMain()
    t.show()
    app.exec_()
