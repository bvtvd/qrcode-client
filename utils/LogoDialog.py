#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Author  :   Hans
@Contact :   hans01@foxmail.com
@File    :   LogoDialog.py
@Time    :   2018/7/28 11:21
@Desc    :   logo 弹窗
'''

from PyQt5.QtWidgets import QDialog, QListWidget, QListView, QListWidgetItem, QPushButton, QFileDialog, QMessageBox, QMenu
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import QSize, pyqtSignal, Qt, QPoint
from utils.Helper import center
import os
import shutil
import re

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

        # self.logoList.currentItemChanged.connect(self.logoChosen)
        # 添加右键菜单
        self.logoList.setContextMenuPolicy(3)
        self.logoList.customContextMenuRequested[QPoint].connect(self.mouseMenu)

        # 上传按钮
        self.uploadButton = QPushButton('上传', self)
        self.uploadButton.setFocusPolicy(Qt.NoFocus)
        self.uploadButton.resize(120, 30)
        # self.uploadButton.setStyleSheet("QPushButton { border: 2px solid #333;border-radius: 5px }")
        self.uploadButton.move(20, 360)
        self.uploadButton.clicked.connect(self.upload)

        # 清除按钮
        self.clearButton = QPushButton('不使用logo', self)
        self.clearButton.setFocusPolicy(Qt.NoFocus)
        self.clearButton.resize(120, 30)
        self.clearButton.move(320, 360)
        self.clearButton.clicked.connect(self.logoClear)

        # 确定按钮
        self.confirmButton = QPushButton('确定', self)
        self.confirmButton.setFocusPolicy(Qt.NoFocus)
        self.confirmButton.resize(120, 30)
        self.confirmButton.move(460, 360)
        self.confirmButton.clicked.connect(self.logoConfirmed)

        self.setWindowTitle('选择logo')
        self.setFixedSize(600, 400)
        self.center()

    """
    右键菜单
    右键删除logo
    """
    def mouseMenu(self, point):
        print('---mouseMenu---')
        item = self.logoList.itemAt(point)
        if item:
            menu = QMenu(self)  # 添加菜单
            deleteAction = menu.addAction('删除')     # 添加菜单选项
            action = menu.exec_(QCursor.pos())  # 执行菜操作
            if action == deleteAction:
                self.deleteLogo(self.logoList.currentRow())

    """
    删除logo 文件
    """
    def deleteLogo(self, index):
        print('---deleteLogo---')
        file_path = self.logoPathList[index]
        if file_path:
            # 删除文件
            os.remove(file_path)
            # 重新读取 logo 列表
            self.readLogos()

    """
    清除logo, 不使用logo
    """
    def logoClear(self):
        print('---logoClear---')
        self.logoChosenSignal.emit(None)
        self.close()

    """
    logo 确认选择
    """
    def logoConfirmed(self):
        print('---logoConfirmed---')
        self.logoPath = self.logoPathList[self.logoList.currentRow()]
        self.logoChosenSignal.emit(self.logoPath)
        self.close()

    """
    上传logo
    os.path.splitext(path)[1] 
    """
    def upload(self):
        print('---upload---')
        fname = QFileDialog.getOpenFileName(self, '选择上传logo', '', '*.png;*.jpg;*.jpeg;*.gif;*.bmp')
        file_path = fname[0]
        if file_path:
            # QMessageBox.warning(self, '  ', '出错了', QMessageBox.Ok)
            ext = os.path.splitext(file_path)[1]
            if ext not in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
                QMessageBox.warning(self, '  ', '不支持该格式文件, 请上传 png, jpg, jpeg, gif, bmp 格式图片', QMessageBox.Ok)
                return
            # 将上传图片复制到logo文件夹
            lastLogoPath = self.logoPathList[len(self.logoPathList) - 1]
            # 获取路径中数字
            result = re.search('(\d+)', lastLogoPath)
            number = result.group()
            newNumber = int(number) + 1
            newPath = os.path.join(self.logoDir, 'icon_' + str(newNumber) + ext)
            # 复制
            shutil.copyfile(file_path, newPath)
            # 重新读取logo
            self.readLogos()

    """
    读取logo
    """
    def readLogos(self):
        self.logoPathList = []
        self.logoList.clear()
        for parent, dirnames, filenames in os.walk(self.logoDir, followlinks=True):
            for filename in filenames:
                file_path = os.path.join(parent, filename)
                logo = QListWidgetItem(self.logoList)
                logo.setIcon(QIcon(file_path))
                self.logoPathList.append(file_path) # 将 logo 路径放入列表

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