#! /usr/bin/python3
# -*- coding:utf-8 -*-

"""
@author:Hans
@file: StyleDialog.py
@time: 2018/8/1 15:30
@desc: 样式弹窗
"""

from PyQt5.QtWidgets import QDialog, QListWidget, QListView, QListWidgetItem, QPushButton
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import QSize, pyqtSignal, Qt, QPoint
from utils.Helper import center
import os

class StyleDialog(QDialog):

    styleDir = './image/styles'
    stylePathList = []
    styleChosenSignal = pyqtSignal(str)

    def __init__(self, parent = None, styleDir = './image/styles'):
        super(StyleDialog, self).__init__(parent)
        self.styleDir = styleDir
        self.initUI()

    def initUI(self):
        self.styleList = QListWidget(self)
        self.styleList.setFixedWidth(600)
        self.styleList.setFixedHeight(350)
        self.styleList.setViewMode(QListView.IconMode)
        self.styleList.setMovement(QListView.Static)
        self.styleList.setIconSize(QSize(110, 110))
        self.styleList.setSpacing(18)

        self.readStyles()

        # 确定按钮
        self.confirmButton = QPushButton('确定', self)
        self.confirmButton.setFocusPolicy(Qt.NoFocus)
        self.confirmButton.resize(120, 30)
        self.confirmButton.move(460, 360)
        self.confirmButton.clicked.connect(self.styleConfirmed)


        self.setWindowTitle('选择样式')
        self.setFixedSize(600, 400)
        self.center()

    """
    样式确认选择
    """
    def styleConfirmed(self):
        print('---styleConfirmed---')
        style = self.stylePathList[self.styleList.currentRow()]
        print(style)
        self.styleChosenSignal.emit(style)
        self.close()


    """
    读取样式
    """
    def readStyles(self):
        self.stylePathList.clear()
        self.styleList.clear()
        for parent, dirnames, filenames in os.walk(self.styleDir):
            for filename in filenames:
                name = self.getFilenameKey(filename)
                file_path = os.path.join(parent, filename)
                style = QListWidgetItem(self.styleList)
                style.setIcon(QIcon(file_path))
                style.setText(name)
                self.stylePathList.append(name)

    """
    获取文件名中的key
    """
    def getFilenameKey(self, name):
        return name.split('.')[0].split('_')[1]

    def center(self):
        center(self)