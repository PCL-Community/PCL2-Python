# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush

class MyRoundButton(QPushButton):
    """圆形 SVG 图标按钮
    
    一个可以显示 SVG 图标的圆形按钮，支持悬停效果和点击效果
    """
    
    def __init__(self, parent=None, svg_path="", size=(36, 36), tooltip="", 
                 svg_size=None,
                 border_width=1, border_color=QColor(255, 255, 255, 0),
                 svg_color=QColor(255, 255, 255, 255),
                 margin=(0, 0, 0, 0),
                 padding=(0, 0, 0, 0)):
        """初始化圆形 SVG 按钮
        
        Args:
            parent: 父控件
            svg_path: SVG 文件路径
            size: 按钮大小，默认为 (36, 36)
            tooltip: 鼠标悬停提示文本
            svg_size: SVG 图标大小，默认与按钮大小相同
            border_width: 边框宽度，默认为 1
            border_color: 边框颜色，默认为透明
            svg_color: SVG 图标颜色，默认为白色
            margin: SVG 图标外边距，格式为 (左, 上, 右, 下)，默认为 (0, 0, 0, 0)
            padding: SVG 图标内边距，格式为 (左, 上, 右, 下)，默认为 (0, 0, 0, 0)
        """
        # 如果提供了svg_size，则按钮尺寸应该比svg尺寸大8px
        if svg_size is not None:
            size = (svg_size[0] + 8, svg_size[1] + 8)
            
        super().__init__(parent)
        # 设置按钮属性
        self.setFixedSize(*size)
        self.setToolTip(tooltip)
        self.setCursor(Qt.PointingHandCursor)
        
        # 设置样式 
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: transparent;
            }
            QPushButton:pressed {
                background-color: transparent;
            }
        """)
        
        # 创建 SVG 控件
        self.svg_widget = QSvgWidget(self)
        
        # 加载 SVG 文件
        self.svg_widget.load(svg_path)
        
        # 设置 SVG 控件大小和位置
        # 如果没有指定SVG大小，则默认为按钮大小减8px
        if svg_size is None:
            svg_size = (size[0] - 8, size[1] - 8)
        self.svg_size = svg_size
        self.margin = margin  # 设置外边距 (左, 上, 右, 下)
        self.padding = padding  # 设置内边距 (左, 上, 右, 下)
        self.centerSvg()  # 居中 SVG 图标
        
        self.setSvgColor(svg_color)
        
        # 设置圆形边框属性 
        self.border_color = border_color  
        self.border_width = border_width
        
        # 添加状态跟踪
        self.is_hovered = False
        self.is_pressed = False
        
        # 设置背景颜色（默认透明）
        self.bg_color = QColor(255, 255, 255, 0)
        
    def centerSvg(self):
        """居中显示 SVG 图标，考虑边距和内边距设置
        
        当 padding 值为负值时，不做压缩而是直接在对应的位置裁剪
        """
        # 计算 SVG 控件的位置，使其在按钮中居中
        button_width, button_height = self.width(), self.height()
        svg_width, svg_height = self.svg_size
        left_margin, top_margin, right_margin, bottom_margin = self.margin
        left_padding, top_padding, right_padding, bottom_padding = self.padding
        
        # 计算可用空间（考虑外边距）
        available_width = button_width - left_margin - right_margin
        available_height = button_height - top_margin - bottom_margin
        
        # 处理 padding 值
        # 对于正值 padding，减小 SVG 显示大小
        # 对于负值 padding，不减小 SVG 显示大小，而是在后续步骤中通过位置调整实现裁剪效果
        width_reduction = max(0, left_padding) + max(0, right_padding)
        height_reduction = max(0, top_padding) + max(0, bottom_padding)
        
        # 计算实际 SVG 显示大小
        actual_svg_width = min(svg_width - width_reduction, available_width)
        actual_svg_height = min(svg_height - height_reduction, available_height)
        
        # 确保 SVG 尺寸不为负值
        actual_svg_width = max(actual_svg_width, 0)
        actual_svg_height = max(actual_svg_height, 0)
        
        # 计算基础居中位置（考虑外边距）
        base_x = left_margin + (available_width - actual_svg_width) / 2
        base_y = top_margin + (available_height - actual_svg_height) / 2
        
        # 应用负值 padding 的裁剪效果
        # 负值的左/上 padding 会使 SVG 向左/上移动，实现左/上裁剪
        # 负值的右/下 padding 不影响位置，但会在后续步骤中扩大 SVG 尺寸
        x_offset = min(0, left_padding)  # 负值左 padding 导致向左偏移
        y_offset = min(0, top_padding)   # 负值上 padding 导致向上偏移
        
        # 计算最终位置（应用偏移）
        final_x = base_x + x_offset
        final_y = base_y + y_offset
        
        # 计算最终尺寸（考虑负值 padding 导致的尺寸扩大）
        # 负值的右/下 padding 会使 SVG 向右/下扩展，实现右/下裁剪
        width_expansion = abs(min(0, left_padding)) + abs(min(0, right_padding))
        height_expansion = abs(min(0, top_padding)) + abs(min(0, bottom_padding))
        
        final_width = actual_svg_width + width_expansion
        final_height = actual_svg_height + height_expansion
        
        # 确保不超出按钮边界
        final_width = min(final_width, button_width - left_margin - right_margin)
        final_height = min(final_height, button_height - top_margin - bottom_margin)
        
        # 设置 SVG 控件的几何位置
        self.svg_widget.setGeometry(
            int(final_x), 
            int(final_y), 
            int(final_width), 
            int(final_height)
        )
        
    def setMargin(self, margin):
        """设置 SVG 图标的外边距
        
        Args:
            margin: (左, 上, 右, 下) 边距值的元组
        """
        self.margin = margin
        self.centerSvg()  # 更新 SVG 位置
        
    def setPadding(self, padding):
        """设置 SVG 图标的内边距
        
        Args:
            padding: (左, 上, 右, 下) 内边距值的元组
        """
        self.padding = padding
        self.centerSvg()  # 更新 SVG 位置
        
    def resizeEvent(self, event):
        """重写调整大小事件，确保 SVG 图标始终居中"""
        super().resizeEvent(event)
        self.centerSvg()
        
    def setSvgColor(self, color):
        """设置 SVG 的颜色（仅当 SVG 支持颜色修改时有效）
        
        Args:
            color: QColor 对象或颜色名称字符串
        """
        if isinstance(color, str):
            color = QColor(color)
            
        # 通过样式表设置 SVG 颜色
        self.svg_widget.setStyleSheet(f"background-color: transparent; color: {color.name()};")
        
    def setSvgPath(self, svg_path):
        """更新 SVG 图标
        
        Args:
            svg_path: SVG 文件路径
        """
        # 加载 SVG 文件
        self.svg_widget.load(svg_path)
        
    def setSvgSize(self, size):
        """设置 SVG 图标的大小
        
        Args:
            size: (width, height) 元组
        """
        self.svg_size = size
        self.centerSvg()  # 更新 SVG 位置
        
    def setBorderColor(self, color):
        """设置边框颜色
        
        Args:
            color: QColor 对象或颜色名称字符串
        """
        if isinstance(color, str):
            color = QColor(color)
        self.border_color = color
        self.update()  # 触发重绘
        
    def setBorderWidth(self, width):
        """设置边框宽度
        
        Args:
            width: 边框宽度（像素）
        """
        self.border_width = width
        self.update()  # 触发重绘
        
    def enterEvent(self, event):
        """鼠标进入事件"""
        self.is_hovered = True
        self.update()  # 触发重绘
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        """鼠标离开事件"""
        self.is_hovered = False
        self.update()  # 触发重绘
        super().leaveEvent(event)
        
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self.is_pressed = True
            self.update()  # 触发重绘
        super().mousePressEvent(event)
        
    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if event.button() == Qt.LeftButton:
            self.is_pressed = False
            self.update()  # 触发重绘
        super().mouseReleaseEvent(event)
        
    def paintEvent(self, event):
        """重写绘制事件，添加圆形边框和背景"""
        # 不调用父类的绘制方法，完全自定义绘制
        
        # 创建画笔
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        
        # 根据状态设置背景颜色
        if self.is_pressed:
            # 按下状态 - 50% 透明度
            bg_color = QColor(255, 255, 255, 44)
            border_color = QColor(self.border_color)
            border_color.setAlpha(127)
        elif self.is_hovered:
            # 悬停状态 - 50% 透明度
            bg_color = QColor(255, 255, 255, 44)
            border_color = QColor(self.border_color)
            # border_color.setAlpha(127) 这里边框做成全透明更好看
            border_color.setAlpha(0)
        else:
            # 正常状态 - 完全透明
            bg_color = QColor(255, 255, 255, 0)
            border_color = QColor(self.border_color)
        
        # 绘制背景
        painter.setBrush(QBrush(bg_color))
        
        # 设置画笔属性
        pen = QPen(border_color)
        pen.setWidth(self.border_width)
        painter.setPen(pen)
        
        # 绘制圆形边框和背景
        painter.drawEllipse(self.rect().adjusted(
            self.border_width // 2,
            self.border_width // 2,
            -self.border_width // 2,
            -self.border_width // 2
        ))
        
    def setHoverColor(self, color):
        """设置鼠标悬停时的背景颜色
        
        Args:
            color: 颜色值，可以是 rgba 格式
        """
        if isinstance(color, str):
            color = QColor(color)
        self.hover_color = color
        
    def setAnimated(self, animated=True):
        """设置是否启用动画效果
        
        Args:
            animated: 是否启用动画
        """
        if animated:
            # 创建缩放动画
            self.animation = QPropertyAnimation(self, b"geometry")
            self.animation.setDuration(100)
            self.animation.setEasingCurve(QEasingCurve.OutCubic)
            
            # 连接鼠标事件
            self._original_enter_event = self.enterEvent
            self._original_leave_event = self.leaveEvent
            
            self.enterEvent = self._animated_enter_event
            self.leaveEvent = self._animated_leave_event
        else:
            # 移除动画效果
            if hasattr(self, '_original_enter_event') and hasattr(self, '_original_leave_event'):
                self.enterEvent = self._original_enter_event
                self.leaveEvent = self._original_leave_event
            
    def _animated_enter_event(self, event):
        """鼠标进入事件（带动画）"""
        # 调用原始的 enterEvent 来处理状态
        self._original_enter_event(event)
        
        # 保存原始几何信息
        rect = self.geometry()
        
        # 计算放大后的几何信息（放大 5%）
        center_x = rect.x() + rect.width() / 2
        center_y = rect.y() + rect.height() / 2
        new_width = rect.width() * 1.05
        new_height = rect.height() * 1.05
        new_x = center_x - new_width / 2
        new_y = center_y - new_height / 2
        
        # 设置动画
        self.animation.setStartValue(rect)
        self.animation.setEndValue(QRect(new_x, new_y, new_width, new_height))
        self.animation.start()
        
    def _animated_leave_event(self, event):
        """鼠标离开事件（带动画）"""
        # 调用原始的 leaveEvent 来处理状态
        self._original_leave_event(event)
        
        # 获取当前几何信息
        current_rect = self.geometry()
        
        # 计算原始几何信息
        center_x = current_rect.x() + current_rect.width() / 2
        center_y = current_rect.y() + current_rect.height() / 2
        orig_width = current_rect.width() / 1.05
        orig_height = current_rect.height() / 1.05
        orig_x = center_x - orig_width / 2
        orig_y = center_y - orig_height / 2
        
        # 设置动画
        self.animation.setStartValue(current_rect)
        self.animation.setEndValue(QRect(orig_x, orig_y, orig_width, orig_height))
        self.animation.start()