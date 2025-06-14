# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QStackedWidget

from Modules.Base.ModLogging import ModLogging, LoggingType as LT
from Pages.PageLaunch.PageLaunch import PageLaunch
from Pages.PageDownload.PageDownload import PageDownload

PAGES = (PageLaunch, PageDownload)


class ModPage:
    """页面管理模块，负责页面切换逻辑"""

    _instance = None

    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super(ModPage, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.logger = ModLogging(module_name="ModPage")
        self.current_page_index = 0
        self._initialized = True

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
            self.logger.write(f"页面索引 {page_id} 超出范围 (0-{stack_widget.count()-1})。", LT.ERROR)
            return False
            
        # 如果当前已经是该页面，则不做任何操作
        if stack_widget.currentIndex() == page_id:
            self.logger.write(f"页面 {page_id} 已经是当前页面，无需切换", LT.INFO)
            return True
            
        # 记录新页面索引
        self.logger.write(f"正在切换到页面索引: {page_id}", LT.INFO)
        
        # 使用 QStackedWidget 的原生方法切换页面
        try:
            stack_widget.setCurrentIndex(page_id)
            self.current_page_index = page_id
            self.logger.write(f"成功切换到页面索引: {page_id}", LT.INFO)
            return True
        except Exception as e:
            self.logger.write(f"切换到页面索引 {page_id} 时发生错误: {e}", LT.ERROR)
            return False
