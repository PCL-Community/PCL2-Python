import json
from typing import Any
from .ModLogging import ModLogging, LoggingType as LT

class ModSetup:
    """写入/读取设置相关的类"""
    def __init__(self):
        self.logger = ModLogging(module_name="ModSetup")
        self.logger.write("ModSetup 加载完成", LT.INFO)
        self.load_settings()

    def setup_settings(self):
        """初始化设置项"""
        self.bg = "#96c0f9"
        self.fg = "#000000"

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
