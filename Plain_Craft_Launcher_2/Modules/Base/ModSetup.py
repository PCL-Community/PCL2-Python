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
        
        # 获取默认配置文件路径
        import os
        import sys
        if getattr(sys, 'frozen', False):
            # 打包后的路径
            self.default_config_path = os.path.join(os.path.dirname(sys.executable), 'data', 'Config.json')
        else:
            # 开发环境路径
            self.default_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'Config.json')
        
        self.load_settings()
        self.logger.write("设置模块初始化完成", LT.INFO, "初始化", "完成")

    def setup_settings(self):
        """初始化默认设置"""
        # 窗口设置
        self.size = (900, 550)
        self.corner_radius = 8
        self.title_height = 48
        
        # 日志设置
        self.log_level = 'Info'
        
        # 界面颜色设置
        self.ColorBrush1 = '#FFFFFF'
        self.ColorBrush2 = '#F5F6F7'
        self.ColorBrush3 = '#F0F0F0'
        self.ColorBrush4 = '#E1E1E1'
        self.ColorBrush5 = '#D2D2D2'
        self.ColorText1 = '#000000'
        self.ColorText2 = '#333333'
        self.ColorText3 = '#666666'
        
        # 其他设置
        self.language = 'zh_CN'
        self.theme = 'light'
        self.auto_check_update = True
        
        # 配置文件设置
        self.config_path = self.default_config_path

        self.logger.write("默认设置已创建", LT.INFO, "配置", "完成")
        
    def get_config_path(self) -> str:
        """获取当前配置文件路径"""
        return self.config_path
        
    def set_config_path(self, path: str) -> None:
        """设置配置文件路径并保存配置"""
        old_path = self.config_path
        self.config_path = path
        try:
            # 尝试保存到新路径
            self.save_settings(path)
            self.logger.write(f"配置文件路径已更改: {path}", LT.INFO, "配置", "完成")
        except Exception as e:
            # 如果保存失败，恢复原路径
            self.config_path = old_path
            self.logger.write(f"更改配置文件路径失败: {str(e)}", LT.ERROR, "配置", "失败")
            raise

    def load_settings(self, file_path: str = None):
        """读取已经存储的设置"""
        try:
            actual_path = file_path or self.config_path or self.default_config_path
            with open(actual_path, "r") as f:
                settings = json.load(f)
            for key, value in settings.items():
                if not key.startswith('_') and key != 'logger':
                    setattr(self, key, value)
            self.logger.write("配置文件已读取", LT.INFO, "配置", "完成")
        except FileNotFoundError:
            self.logger.write("配置文件不存在", LT.INFO, "配置", "需要初始化")
            self.setup_settings()
            # 初始化后保存默认配置
            self.save_settings(file_path)
        except json.JSONDecodeError as e:
            self.logger.write(f"配置文件格式错误: {str(e)}", LT.ERROR, "配置", "失败")
            self.setup_settings()
            self.save_settings(file_path)
        except Exception as e:
            self.logger.write(f"读取配置文件失败: {str(e)}", LT.ERROR, "配置", "失败")
            self.setup_settings()

    def save_settings(self, file_path: str = None):
        """保存设置"""
        import os
        try:
            actual_path = file_path or self.config_path or self.default_config_path
            # 确保目录存在
            os.makedirs(os.path.dirname(actual_path), exist_ok=True)
            # 过滤掉不需要保存的属性
            settings = {k: v for k, v in self.__dict__.items() 
                       if not k.startswith('_') 
                       and k not in ['logger', 'default_config_path']}
            with open(actual_path, "w") as f:
                json.dump(settings, f, indent=4)
            self.logger.write("配置已保存到文件", LT.INFO, "配置", "完成")
        except Exception as e:
            self.logger.write(f"保存配置文件失败: {str(e)}", LT.ERROR, "配置", "失败")

    def get_settings(self, setting: str):
        """获取设置"""
        return getattr(self, setting, None)

    def set_settings(self, setting: str, value: Any) -> None:
        """设置设置"""
        setattr(self, setting, value)
        self.save_settings()

    def __getitem__(self, key: str) -> Any:
        """启用索引"""
        return self.get_settings(key)

    def __setitem__(self, key: str, value: Any) -> None:
        """启用索引"""
        self.set_settings(key, value)
