#! /usr/bin/python3
# -*- coding:utf-8 -*-

"""
@author:Hans
@file: AboutDialog.py
@time: 2018/8/20 14:46
@desc: 
"""

from PyQt5.QtWidgets import QDialog, QLabel
from utils.Helper import center

"""
关于弹窗
"""
class AboutDialog(QDialog):

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.initUI()

    def initUI(self):
        style = 'QLabel {font-size: 15px}'
        name = QLabel('作者: Hans', self)
        name.move(150, 50)
        name.setStyleSheet(style)
        email = QLabel('邮箱: hans01@foxmail.com', self)
        email.move(100, 100)
        email.setStyleSheet(style)

        self.setWindowTitle('关于')
        self.setFixedSize(400, 200)
        self.center()

    def center(self):
        center(self)