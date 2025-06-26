# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from PyQt5 import QtCore

from Modules.Base.ModSetup import ModSetup as Setup
from Modules.Base.ModLogging import ModLogging, LoggingType as LT
from Controls.MyCard import MyCard

setup = Setup()

class PageSettings(QWidget):
    """设置页"""
    def __init__(self, parent=None):
        super().__init__(parent)

        self.logger = ModLogging(module_name="PageSettings")
        self.logger.write("设置页面初始化", LT.INFO, "页面加载", "进行中")

        # 设置objectName
        self.setObjectName("PageSettings")
        
        # 使用 setAttribute 确保背景色生效
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        
        # 设置样式表
        setup = Setup()
        self.setStyleSheet(f"""
            QWidget#PageSettings {{
                background-color: qlineargradient(spread:pad, x1:0.9, y1:0.1, x2:0, y2:1, 
                                              stop:0 {setup.get_settings('ColorBrush5')}, 
                                              stop:1 {setup.get_settings('ColorBrush6')});
                border-bottom-left-radius: {setup.get_settings('corner_radius')}px;
            }}
        """)

        # 创建主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)

        # 创建日志设置卡片
        log_card = MyCard(self, "日志设置", size=(400, 200))
        log_layout = QVBoxLayout()
        log_layout.setContentsMargins(20, 20, 20, 20)
        log_layout.setSpacing(15)

        # 添加日志级别选择
        level_layout = QVBoxLayout()
        level_label = QLabel("日志警告级别：")
        level_label.setStyleSheet("""
            QLabel {
                color: #343d4a;
                font-size: 14px;
                margin-bottom: 4px;
            }
        """)
        
        self.level_combo = QComboBox()
        self.level_combo.setStyleSheet("""
            QComboBox {
                background-color: rgba(255, 255, 255, 0.9);
                border: 1px solid rgba(19, 112, 243, 0.5);
                border-radius: 4px;
                padding: 5px 10px;
                color: #343d4a;
                font-size: 14px;
            }
            QComboBox:hover {
                border: 1px solid rgba(19, 112, 243, 0.8);
                background-color: rgba(255, 255, 255, 1);
            }
            QComboBox:focus {
                border: 1px solid #1370f3;
                background-color: rgba(255, 255, 255, 1);
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: url(Images/BtnCardToggleNormal.svg);
                width: 12px;
                height: 12px;
            }
            QComboBox::down-arrow:hover {
                image: url(Images/BtnCardToggleCollapsed.svg);
            }
        """)
        self.level_combo.addItems(['Info', 'Warn', 'Error', 'Fatal'])
        # 设置当前选中的日志级别
        current_level = setup.get_settings('log_level')
        self.level_combo.setCurrentText(current_level)
        self.level_combo.currentTextChanged.connect(self.on_log_level_changed)

        level_layout.addWidget(level_label)
        level_layout.addWidget(self.level_combo)
        level_layout.setContentsMargins(0, 10, 0, 10)
        log_layout.addLayout(level_layout)

        log_card.setContentLayout(log_layout)
        layout.addWidget(log_card)
        layout.addStretch()

    def on_log_level_changed(self, level):
        """处理日志级别变化"""
        # 将字符串转换为LoggingType枚举
        log_level = getattr(LT, level.upper())
        
        # 更新日志级别
        ModLogging.set_log_level(log_level)
        
        # 保存设置
        setup = Setup()
        setup.log_level = level
        setup.save_settings()
        
        self.logger.write(f"日志级别已更改为：{level}", LT.INFO, "设置更改", "完成")