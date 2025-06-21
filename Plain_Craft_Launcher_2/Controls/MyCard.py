from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt, QRect, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPixmap, QColor
from Modules.Base.ModQtFont import ModQtFont
from Controls.MyRoundButton import MyRoundButton

class MyCard(QWidget):
    """卡片控件
    定义一个白色背景的卡片控件，四端圆角，可以设置标题和大小，可折叠、展开。"""
    def __init__(self, parent: QWidget = None, title_text: str = None, objectName: str = None,
                 size: tuple = (200, 300), margin: tuple = (8, 8, 8, 8), can_fold: bool = True) -> None: 
        super().__init__(parent)
        self.font_manager = ModQtFont()

        # 状态：normal 或 folded
        self.status = "normal"

        self.fold_enabled = can_fold
        self.parent = parent

        # 保存原始尺寸和折叠后的尺寸
        self._original_size = size
        self._folded_size = (size[0], 30)  # 折叠后高度为30，宽度不变
        
        # 设置初始尺寸
        self.setFixedSize(*size)
        self.objectName = objectName if objectName else title_text
        self.setObjectName(self.objectName)

        
        # 设置样式
        self.setStyleSheet(f"QWidget #{self.objectName} {{background-color: #FFFFFF; border-radius: 8px;}}")
        
        # 标题相关
        self._title_text = title_text
        self.title_label = QLabel(self, text=title_text)
        self.title_label.setStyleSheet("QLabel {font-size: 16px;font-weight: bold;color: #000000;background-color: transparent;}")
        self.title_label.setFont(self.font_manager.get_font_object(title_text))
        self.title_label.move(margin[0], margin[1])
        
        # 创建折叠/展开按钮
        if self.fold_enabled:
            self.btn_fold_toggle = MyRoundButton(self, svg_path="Images/BtnCardToggleNormal.svg", size=(32, 32))
            # 将按钮放在右上角
            self.btn_fold_toggle.move(size[0] - margin[2] - 20, margin[1])
            # 连接按钮点击事件
            self.btn_fold_toggle.clicked.connect(self.toggle_fold)
        
        # 创建动画对象
        self.animation = QPropertyAnimation(self, b"size")
        self.animation.setDuration(300)  # 动画持续时间300毫秒
        self.animation.setEasingCurve(QEasingCurve.OutCubic)  # 设置缓动曲线
    
    def toggle_fold(self):
        """切换折叠/展开状态"""
        if not self.fold_enabled:
            return
            
        if self.status == "normal":
            # 当前是展开状态，需要折叠
            self.fold()
        else:
            # 当前是折叠状态，需要展开
            self.unfold()
    
    def fold(self):
        """折叠卡片"""
        if self.status == "folded" or not self.fold_enabled:
            return
            
        # 设置动画
        self.animation.setStartValue(self.size())
        self.animation.setEndValue(QRect(0, 0, *self._folded_size).size())
        
        # 更新按钮文本
        self.btn_fold_toggle.setSvgPath("Images/BtnCardToggleCollapsed.svg")
        
        # 开始动画
        self.animation.start()
        
        # 更新状态
        self.status = "folded"
        
        # 隐藏子控件（除了标题和折叠按钮）
        for child in self.children():
            if child != self.title_label and child != self.btn_fold_toggle:
                child.hide()
    
    def unfold(self):
        """展开卡片"""
        if self.status == "normal" or not self.fold_enabled:
            return
            
        # 设置动画
        self.animation.setStartValue(self.size())
        self.animation.setEndValue(QRect(0, 0, *self._original_size).size())
        
        # 更新按钮文本
        self.btn_fold_toggle.setText("↑")
        
        # 开始动画
        self.animation.start()
        
        # 更新状态
        self.status = "normal"
        
        # 显示之前隐藏的子控件
        for child in self.children():
            child.show()
    
    def resizeEvent(self, event):
        """重写大小调整事件，确保按钮始终在右上角"""
        super().resizeEvent(event)
        
        if hasattr(self, 'btn_fold_toggle'):
            # 更新按钮位置到右上角
            self.btn_fold_toggle.move(self.width() - self.btn_fold_toggle.width() - 8, 8)
        
