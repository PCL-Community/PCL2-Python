from PyQt5.QtGui import QFontDatabase, QFont, QFontMetrics
import os

class ModQtFont:
    @staticmethod
    def contains_chinese(text):
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

    @staticmethod
    def get_font_object(text):
        font = QFont()
        
        if ModQtFont.contains_chinese(text):
            # 中文字体路径
            chinese_font_path = os.path.join("Resources", "Fonts", "FontChinese.ttc")
            if os.path.exists(chinese_font_path):
                font_id = QFontDatabase.addApplicationFont(chinese_font_path)
                font_name = QFontDatabase.applicationFontFamilies(font_id)[0]
                font.setFamily(font_name)
            else:
                raise FileNotFoundError("无法找到字体文件")
        else:
            # 英文字体路径
            english_font_path = os.path.join("Resources", "Fonts", "Font.ttf")
            if os.path.exists(english_font_path):
                font_id = QFontDatabase.addApplicationFont(english_font_path)
                font_name = QFontDatabase.applicationFontFamilies(font_id)[0]
                font.setFamily(font_name)
            else:
                raise FileNotFoundError("无法找到字体文件")

        return font

    @staticmethod
    def get_font_size(self, text, font: QFont):
        font_metrics = QFontMetrics(font)
        
        # 计算文本宽度
        text_width = font_metrics.width(text)

        return text_width


