#! /usr/bin/python3
# -*- coding:utf-8 -*-

"""
@author:Hans
@file: main.py
@time: 2018/7/19 10:47
@desc: 
"""
import sys
from PyQt5.QtWidgets import QApplication
from utils.GUIClient import GUIClient

if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = GUIClient()
    sys.exit(app.exec_())