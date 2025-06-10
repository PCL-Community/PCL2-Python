# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QFrame
import importlib
import sys

from Modules.Base.ModLogging import ModLogging, LoggingType as LT
from Modules.Base.ModSetup import ModSetup as Setup

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
        self.current_page = None
        self._initialized = True
        
    def switch_page(self, pan_main: QFrame, page_name: str) -> bool:
        """切换页面
        
        Args:
            pan_main: 主面板，用于放置页面
            page_name: 页面名称，如 "Launch"
            
        Returns:
            bool: 切换是否成功
        """
        # 如果页面相同，不做任何事情
        if self.current_page == page_name:
            self.logger.write(f"页面 {page_name} 已经是当前页面，无需切换", LT.INFO)
            return True
        
        # 记录新页面名称
        self.logger.write(f"正在切换到页面: {page_name}", LT.INFO)
        
        # 删除 PanMain 中的所有子组件
        for child in pan_main.findChildren(QWidget):
            child.setParent(None)
            child.deleteLater()
        
        # 根据传入的页面名称，实例化对应的页面
        try:
            # 构建页面类的完整路径
            page_class_name = f"Page{page_name}"
            page_module_path = f"Pages.Page{page_name}.{page_class_name}"
            
            # 动态导入模块
            try:
                page_module = importlib.import_module(page_module_path)
                page_class = getattr(page_module, page_class_name)
            except (ImportError, AttributeError) as e:
                self.logger.write(f"无法导入页面模块 {page_module_path}: {e}", LT.ERROR)
                return False
            
            # 实例化页面
            page_instance = page_class(pan_main)
            
            # 设置页面大小
            page_instance.setGeometry(0, 0, pan_main.width(), pan_main.height())
            
            # 确保页面在最上层
            page_instance.raise_()
            
            # 更新当前页面名称
            self.current_page = page_name
            
            self.logger.write(f"成功切换到页面: {page_name}", LT.INFO)
            return True
            
        except Exception as e:
            self.logger.write(f"切换到页面 {page_name} 时发生错误: {e}", LT.ERROR)
            return False
            