import json
from copy import deepcopy
from locale import getdefaultlocale

class ModLanguage:
    def __init__(self) -> None:
        with open("./Resources/language.json", "r", encoding="utf-8") as f:
            self._lang = json.load(f)[self.language]

    @property
    def language(self) -> str:
        if getdefaultlocale()[0] == "zh_CN":
            return "zh-CN"
        else:
            return "en-US"

    def get_text(self, key: str) -> str:
        temp = deepcopy(self._lang)
        for key_item in key.split("."):
            temp = temp[key_item]
        return temp
