# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QWidget
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush, QFontMetrics, QPixmap
import os, re

from Modules.Base.ModLogging import ModLogging, LoggingType as LT

from Modules.Base.ModQtFont import ModQtFont


class MyIconTextButton(QPushButton):
    """图标文本按钮
    
    一个左侧显示 SVG 图标、右侧显示文本的按钮，支持悬停效果和点击效果，两端为圆角
    """

    def __init__(self, parent=None, svg_path="", text="", height=36, tooltip="",
                 svg_size=(24, 24),
                 border_width=1, border_color=QColor(255, 255, 255, 0),
                 svg_color=QColor(255, 255, 255, 255),
                 text_color=QColor(255, 255, 255, 255),
                 font_size=10,
                 margin=(16, 0, 16, 0),
                 padding=(4, 0, 4, 0),
                 command=None):
        """
        初始化图标文本按钮

        Args:
            parent: 父控件
            svg_path: SVG 文件路径
            text: 按钮文本
            height: 按钮高度，默认为 36
            tooltip: 鼠标悬停提示文本
            svg_size: SVG 图标大小，默认为 (24, 24)
            border_width: 边框宽度，默认为 1
            border_color: 边框颜色，默认为透明
            svg_color: SVG 图标颜色，默认为白色
            text_color: 文本颜色，默认为白色
            font_size: 文本字体大小，默认为 10
            margin: 按钮内容外边距，格式为 (左, 上, 右, 下)，默认为 (8, 0, 8, 0)
            padding: 图标与文本之间的间距，格式为 (左, 上, 右, 下)，默认为 (4, 0, 4, 0)
            command: 按下按钮时执行的函数

        """
        super().__init__(parent)
        self.logger = ModLogging(module_name='MyIconTextButton')

        # 保存参数
        self.button_height = height
        self._text = text
        self._font_size = font_size
        self._margin = margin
        self._padding = padding
        self._svg_size = svg_size
        self._svg_path = svg_path
        self._text_color = text_color
        self._svg_color = svg_color

        # 设置按钮属性
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

        # 创建水平布局
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(*margin)
        self.layout.setSpacing(padding[0] + padding[2])  # 使用左右内边距作为间距

        # 创建 SVG 控件
        self.svg_widget = QSvgWidget()
        self.svg_widget.setFixedSize(*svg_size)

        # 加载 SVG 文件
        if svg_path:
            self.svg_widget.load(svg_path)

        # 设置 SVG 颜色
        self.setSvgColor(svg_color)

        # 创建文本标签
        self.text_label = QLabel(text)
        self.text_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        
        # 根据文本内容选择字体
        self.updateFont(text, font_size)
        
        # 设置文本颜色
        self.setTextColor(text_color)

        # 添加控件到布局
        self.layout.addWidget(self.svg_widget)
        self.layout.addWidget(self.text_label)

        # 设置圆角边框属性 
        self.border_color = border_color
        self.border_width = border_width
        self.radius = height // 2  # 圆角半径设为高度的一半，实现两端圆角效果

        # 添加状态跟踪
        self.is_hovered = False
        self.is_pressed = False

        # 绑定函数
        if command:
            self.clicked.connect(command)

        # 设置背景颜色（默认透明）
        self.bg_color = QColor(255, 255, 255, 0)
        self.hover_color = QColor(255, 255, 255, 44)
        self.press_color = QColor(255, 255, 255, 255)
        
        # 计算并设置按钮宽度
        self.updateButtonSize()
        
    def containsChinese(self, text):
        """检查文本是否包含中文字符
        
        Args:
            text: 要检查的文本
            
        Returns:
            bool: 如果包含中文字符返回 True，否则返回 False
        """
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                return True
        return False
        
    def updateFont(self, text, font_size):
        """根据文本内容更新字体
        
        Args:
            text: 文本内容
            font_size: 字体大小
        """
        font = ModQtFont.get_font_object(text)
                
        font.setPointSize(font_size)
        self.text_label.setFont(font)

    def updateButtonSize(self):
        """根据文本内容、字体和字号计算并更新按钮宽度"""
        # 创建字体度量对象
        font = self.text_label.font()
        font_metrics = QFontMetrics(font)
        
        # 计算文本宽度
        text_width = font_metrics.width(self._text)
        
        # 计算总宽度：左边距 + SVG宽度 + 间距 + 文本宽度 + 右边距
        total_width = (self._margin[0] + self._svg_size[0] + 
                      (self._padding[0] + self._padding[2]) + 
                      text_width + self._margin[2])
        
        # 设置按钮大小
        self.setFixedSize(total_width, self.button_height)

    def setSvgColor(self, color):
        """设置 SVG 的颜色（仅当 SVG 支持颜色修改时有效）
        
        Args:
            color: QColor 对象或颜色名称字符串
        """
        if isinstance(color, str):
            color = QColor(color)
        
        # 获取当前加载的 SVG 路径
        svg_path = self._svg_path
        
        # 读取 SVG 文件内容
        with open(svg_path, 'r', encoding='utf-8') as file:
            svg_content = file.read()
        
        # 替换 currentColor 为具体的颜色值
        import re
        svg_content = re.sub(r'fill="currentColor"', f'fill="{color.name()}"', svg_content)
        svg_content = re.sub(r'stroke="currentColor"', f'stroke="{color.name()}"', svg_content)
        
        # 使用 QByteArray 和 QSvgRenderer 加载修改后的 SVG
        from PyQt5.QtCore import QByteArray
        from PyQt5.QtSvg import QSvgRenderer
        
        byte_array = QByteArray(svg_content.encode('utf-8'))
        renderer = QSvgRenderer(byte_array)
        self.svg_widget.renderer().load(byte_array)

        
    def setTextColor(self, color):
        """设置文本颜色
        
        Args:
            color: QColor 对象或颜色名称字符串
        """
        if isinstance(color, str):
            color = QColor(color)

        # 设置文本颜色
        self.text_label.setStyleSheet(f"color: {color.name()};")

    def setText(self, text):
        """设置按钮文本
        
        Args:
            text: 文本内容
        """
        self._text = text
        self.text_label.setText(text)
        
        # 更新字体
        self.updateFont(text, self._font_size)
        
        # 更新按钮大小
        self.updateButtonSize()

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
        self._svg_size = size
        self.svg_widget.setFixedSize(*size)
        self.updateButtonSize()  # 更新按钮大小

    def setFontSize(self, size):
        """设置文本字体大小
        
        Args:
            size: 字体大小（点）
        """
        self._font_size = size
        
        # 更新字体
        self.updateFont(self._text, size)
        
        # 更新按钮大小
        self.updateButtonSize()

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
        """重写绘制事件，添加两端圆角矩形边框和背景"""
        # 不调用父类的绘制方法，完全自定义绘制

#       self.logger.write("已触发重绘。", LT.INFO)

        # 创建画笔
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿

        # 根据状态设置背景颜色
        if self.is_pressed:
            # 按下状态
            bg_color = self.press_color
            border_color = QColor(self.border_color)
            border_color.setAlpha(255)  # 按下时边框不透明
            transparent_color = self.get_background_color(self.parentWidget())
            self.setTextColor(transparent_color)
            self.setSvgColor(transparent_color)
        elif self.is_hovered:
            # 悬停状态
            bg_color = self.hover_color
            border_color = QColor(self.border_color)
            border_color.setAlpha(0)  # 悬停时边框透明
            self.setTextColor(self._text_color)
            self.setSvgColor(self._svg_color)
        else:
            # 正常状态
            bg_color = self.bg_color
            border_color = QColor(self.border_color)
            self.setTextColor(self._text_color)
            self.setSvgColor(self._svg_color)

        # 绘制背景
        painter.setBrush(QBrush(bg_color))

        # 设置画笔属性
        pen = QPen(border_color)
        pen.setWidth(self.border_width)
        painter.setPen(pen)

        # 绘制两端圆角矩形边框和背景
        # 圆角半径设为高度的一半，实现两端圆角效果
        painter.drawRoundedRect(self.rect().adjusted(
            self.border_width // 2,
            self.border_width // 2,
            -self.border_width // 2,
            -self.border_width // 2
        ), self.radius, self.radius)

    def setHoverColor(self, color):
        """设置鼠标悬停时的背景颜色
        
        Args:
            color: 颜色值，可以是 QColor 对象或颜色名称字符串
        """
        if isinstance(color, str):
            color = QColor(color)
        self.hover_color = color

    def setPressColor(self, color):
        """设置鼠标按下时的背景颜色
        
        Args:
            color: 颜色值，可以是 QColor 对象或颜色名称字符串
        """
        if isinstance(color, str):
            color = QColor(color)
        self.press_color = color

    def setBackgroundColor(self, color):
        """设置按钮的背景颜色
        
        Args:
            color: 颜色值，可以是 QColor 对象或颜色名称字符串
        """
        if isinstance(color, str):
            color = QColor(color)
        self.bg_color = color
        self.update()  # 触发重绘

    @staticmethod
    def get_background_color(widget: QWidget) -> QColor:
        """获取控件的背景颜色

        Args:
            widget: 控件对象

        Returns:
            背景颜色，QColor 对象
        """
        # 获取样式表
        stylesheet = widget.styleSheet()
        
        # 正则匹配 background-color 属性
        pattern = re.compile(r"background-color:\s*([^;]+)")
        match = pattern.search(stylesheet)
        
        if match:
            color_str = match.group(1)
            # 去除可能存在的空格和引号
            color_str = color_str.strip().strip("'\"")
            if color_str.startswith("qlineargradient"):
                # 如果是渐变色，则返回 Stop 0 的颜色
                color_str = color_str.split("stop:0")[1].split(",")[0].strip()
            color_obj = QColor(color_str)
            return color_obj
        return None
