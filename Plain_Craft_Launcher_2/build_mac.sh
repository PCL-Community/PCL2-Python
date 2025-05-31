#!/bin/bash

python3 -m nuitka \
  --standalone \
  --onefile \
  --enable-plugin=pyqt5 \
  --include-package=PyQt5 \
  --include-package=PyQt5.QtSvg \
  --include-package=PyQt5.QtCore \
  --include-package=PyQt5.QtGui \
  --include-package=PyQt5.QtWidgets \
  --output-dir=../dist \
  --follow-imports \
  --remove-output \
  --assume-yes-for-downloads \
  --show-progress \
  --show-memory \
  --include-data-dir=./Images=Images \
  --include-module=_ctypes \
  --macos-create-app-bundle \
  ./Application.py