# -*- coding: utf-8 -*-
import json
from typing import Any
from .ModLogging import ModLogging, LoggingType as LT

class ModSetup:
    """写入/读取设置相关的类"""
    _instance = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super(ModSetup, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        self.logger = ModLogging(module_name="ModSetup")
        self.load_settings()
        self.logger.write("ModSetup 加载完成", LT.INFO)

    def setup_settings(self):
        """初始化设置项"""
        self.ColorBrush0 = "#ffffff"
        self.ColorBrush1 = "#343d4a"
        self.ColorBrush2 = "#0b5bcb"
        self.ColorBrush3 = "#1370f3"
        self.ColorBrush4 = "#4890f5"
        self.ColorBrush5 = "#96c0f9"
        self.ColorBrush6 = "#d5e6fd"
        self.ColorBrush7 = "#e0eafd"
        self.ColorBrush8 = "#eaf2fe"
        self.ColorBrushBg0 = "#96c0f9"
        self.ColorBrushBg1 = "#bee0eafd"
        self.corner_radius = 10
        self.size = (900, 550)
        self.title_height = 48

        self.logger.write("设置初始化完成", LT.INFO)

    def load_settings(self, file_path:str="./data/Config.json"):
        """读取已经存储的设置"""
        try:
            with open(file_path, "r") as f:
                settings = json.load(f)
            for key, value in settings.items():
                setattr(self, key, value)

            self.logger.write("设置文件读取成功", LT.INFO)
        except FileNotFoundError:
            self.logger.write("设置文件未找到，进行初始化", LT.INFO)
            self.setup_settings()           

    def save_settings(self, file_path:str="./data/Config.json"):
        """保存设置"""
        settings = self.__dict__
        with open(file_path, "w") as f:
            json.dump(settings, f)

        self.logger.write("设置文件保存成功", LT.INFO)

    def get_settings(self, setting: str):
        """获取设置"""
        return getattr(self, setting, None)
    
    def set_settings(self, setting: str, value: Any) -> None:
        """设置设置"""
        setattr(self, setting, value)
        self.save_settings()

    def __getitem__(self, key: str) -> Any:
        """重载 [] 运算符"""
        return self.get_settings(key)

    def __setitem__(self, key: str, value: Any) -> None:
        """重载 [] 运算符"""
        self.set_settings(key, value)
