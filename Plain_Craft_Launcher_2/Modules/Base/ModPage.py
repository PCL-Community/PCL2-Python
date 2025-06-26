# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QStackedWidget

from Modules.Base.ModLogging import ModLogging, LoggingType as LT
from Pages.PageLaunch.PageLaunch import PageLaunch
from Pages.PageDownload.PageDownload import PageDownload
from Pages.PageSettings.PageSettings import PageSettings

PAGES = (PageLaunch, PageDownload, PageSettings)


class ModPage:
    """页面管理模块，负责页面切换逻辑"""

    def __init__(self):
        self.logger = ModLogging(module_name="ModPage")
        self.current_page_index = 0

    def switch_page(self, stack_widget: QStackedWidget, page_id: int) -> bool:
        """切换页面
        
        Args:
            stack_widget: QStackedWidget 实例
            page_id: 页面索引，如 0 表示 PageLaunch
            
        Returns:
            bool: 切换是否成功
        """
        # 检查页面索引是否有效
        if page_id < 0 or page_id >= stack_widget.count():
            self.logger.write(f"页面索引 {page_id} 超出范围 (0-{stack_widget.count()-1})", LT.ERROR, "页面切换", "参数错误")
            return False
            
        # 如果当前已经是该页面，则不做任何操作
        if stack_widget.currentIndex() == page_id:
            self.logger.write(f"页面 {page_id} 已是当前页面", LT.INFO, "页面切换", "无需操作")
            return True
            
        # 记录新页面索引
        self.logger.write(f"切换到页面 {page_id}", LT.INFO, "页面切换", "进行中")
        
        # 使用 QStackedWidget 的原生方法切换页面
        try:
            stack_widget.setCurrentIndex(page_id)
            self.current_page_index = page_id
            self.logger.write(f"页面 {page_id} 切换完成", LT.INFO, "页面切换", "完成")
            return True
        except Exception as e:
            self.logger.write(f"切换到页面 {page_id} 失败: {e}", LT.ERROR, "页面切换", "异常")
            return False


class ModPagePanMain(ModPage):
    """主面板页面管理模块，负责将所有页面添加到主面板并管理切换"""
    
    def __init__(self, pan_main: QStackedWidget):
        super().__init__()
        self.pan_main = pan_main
        
        # 初始化所有页面
        for page_class in PAGES:
            page = page_class(self.pan_main)
            self.pan_main.addWidget(page)
    
    def switch_page(self, page_id: int) -> bool:
        """重写切换页面方法，简化调用方式
        
        Args:
            page_id: 页面索引，如 0 表示 PageLaunch
            
        Returns:
            bool: 切换是否成功
        """
        return super().switch_page(self.pan_main, page_id)
