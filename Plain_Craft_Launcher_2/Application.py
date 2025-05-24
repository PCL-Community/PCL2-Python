# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
import sys

from FormMain import FormMain

if __name__ == '__main__':
    app = QApplication(sys.argv)
    t = FormMain()
    t.show()
    app.exec_()
