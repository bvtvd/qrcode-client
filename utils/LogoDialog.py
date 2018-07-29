#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Author  :   Hans
@Contact :   hans01@foxmail.com
@File    :   LogoDialog.py
@Time    :   2018/7/28 11:21
@Desc    :
'''

from PyQt5.QtWidgets import QDialog, QListWidget, QListView, QListWidgetItem, QDialogButtonBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, pyqtSignal, Qt, pyqtSlot
from utils.Helper import center
import os

"""
贴图弹窗
"""
class LogoDialog(QDialog):

    logoDir = './image/logos'
    logoPathList = []
    logoChosenSignal = pyqtSignal(str)

    def __init__(self, parent = None, logoDir = './image/logos'):
        super(LogoDialog, self).__init__(parent)
        self.logoDir = logoDir
        self.initUI()

    def initUI(self):
        self.logoList = QListWidget(self)
        self.logoList.setFixedWidth(600)
        self.logoList.setFixedHeight(350)
        self.logoList.setViewMode(QListView.IconMode)
        self.logoList.setMovement(QListView.Static)
        self.logoList.setIconSize(QSize(50, 50))
        self.logoList.setSpacing(12)

        self.readLogos()

        self.setWindowTitle('选择logo')
        self.resize(600, 400)
        self.center()

    """
    读取logo
    """
    def readLogos(self):
        self.logoPathList = []
        for parent, dirnames, filenames in os.walk(self.logoDir, followlinks=True):
            for filename in filenames:
                file_path = os.path.join(parent, filename)
                logo = QListWidgetItem(self.logoList)
                logo.setIcon(QIcon(file_path))
                self.logoPathList.append(file_path) # 将 logo 路径放入列表
        print(self.logoPathList)
        self.logoList.currentItemChanged.connect(self.logoChosen)

    """
     logo 选中事件
    """
    def logoChosen(self, current, previous):
        print('---LogoDialog.logoChosen---')
        self.logoPath = self.logoPathList[self.logoList.row(current)]
        self.logoChosenSignal.emit(self.logoPath)


    def getLogoPath(self):
        return self.logoPath

    """
    居中显示
    """
    def center(self):
        center(self)