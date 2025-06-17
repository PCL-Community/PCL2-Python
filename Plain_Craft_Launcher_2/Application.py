# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from tkinter import messagebox  # 这里怕使用 PyQT 再报错，先用比较稳定的 tkinter
import sys
from traceback import format_exc
from Modules.Base.ModLanguage import ModLanguage

from FormMain import FormMain

if __name__ == '__main__':
    try: 
        app = QApplication(sys.argv)
        t = FormMain()
        t.show()
        app.exec_()
    except Exception as e:
        try: 
            messagebox.showerror(ModLanguage().get_text("application.error"), format_exc())
        except:
            messagebox.showerror("应用程序启动时发生重大异常", format_exc())  # 连 ModLanguage 都炸了，知道这次压不住了。
