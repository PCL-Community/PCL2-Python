import json
from copy import deepcopy

class ModLanguage:
    def __init__(self, language: str = "zh-CN") -> None:
        with open("./Resources/language.json", "r", encoding="utf-8") as f:
            self._lang = json.load(f)[language]

    def get_text(self, key: str, lang: str = "zh-CN") -> str:
        temp = deepcopy(self._lang)
        for key_item in key.split("."):
            temp = temp[key_item]
        return temp
