#! /usr/bin/python3
# -*- coding:utf-8 -*-

"""
@author:Hans
@file: GUIClient.py
@time: 2018/7/20 10:16
@desc: 
"""

import sys
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QAction, QHBoxLayout, QVBoxLayout, QTextEdit, QPushButton, QWidget, QLabel, QFrame, QGridLayout, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QPicture, QImage
from utils.QRCode import QRCode
from PIL import Image

class GUIClient(QMainWindow):

    # 视窗配置项
    config = {}
    # 单个生成二维码选项
    single = None
    # 批量生成二维码选项
    batch = None
    # 是否是单个生成状态记录
    is_single = False
    # 单个二维码生成输入框
    singleQRCodeTextEdit = None
    # 单个二维码生成页面
    singleWidget = None
    # 单个二维码预览空间
    previewSquare = None

    """
    **kwargs:
        window_width: 窗口宽
        window_height:  窗口高
        window_title:   窗口标题
        window_icon:    窗口Icon
        spot_icon:  菜单选中点图标
    """
    def __init__(self, **kwargs):
        print('---__init__---')
        super(GUIClient, self).__init__()
        self.initConfig(**kwargs)
        self.initUI()

    """
    初始化传入配置项
    window_width: 窗口宽
    window_height:  窗口高
    window_title:   窗口标题
    window_icon:    窗口Icon
    spot_icon:  菜单选中点图标
    """
    def initConfig(self, **kwargs):
        print('---initConfig---')
        self.config['window_width'] = kwargs.get('window_width', 800)
        self.config['window_height'] = kwargs.get('window_height', 400)
        self.config['window_title'] = kwargs.get('window_title', '二维码生成器')
        self.config['window_icon'] = kwargs.get('window_icon', '../images/icon-qrcode.png')
        self.config['spot_icon'] = QIcon(kwargs.get('spot_icon', '../images/spot.png'))
        self.config['none_icon'] = QIcon('')

    """
    项目初始化
    """
    def initUI(self):
        print('---initUI---')
        self.initMenu() # 初始化菜单
        self.pageRender()   # 界面渲染

        self.resize(self.config['window_width'], self.config['window_height'])   # 设置窗口大小
        self.center()   # 窗口居中
        self.setWindowTitle(self.config['window_title'])   # 窗口标题
        self.setWindowIcon(QIcon(self.config['window_icon']))   # 设置窗口icon
        self.show()

    """
    初始化菜单
    """
    def initMenu(self):
        print('---initMenu---')
        menuBar = self.menuBar()
        menuMenu = menuBar.addMenu('&菜单')
        self.setMenuSingle(self.config.get('spot_icon'))
        self.setMenuBatch(self.config.get('none_icon'))
        menuMenu.addAction(self.single)
        menuMenu.addAction(self.batch)
        menuMenu.addSeparator()
        menuMenu.addAction('设置')
        menuMenu.addSeparator()
        menuMenu.addAction('退出')

    """
    设置单个生成菜单
    """
    def setMenuSingle(self, icon):
        print('---setMenuSingle---')
        if(icon == self.config.get('spot_icon')): self.is_single = True
        self.single = QAction(icon, '单个生成', self)
        self.single.setShortcut('Ctrl+S')
        self.single.triggered.connect(self.chooseGenerateType)

    """
    设置批量生成菜单
    """
    def setMenuBatch(self, icon):
        print('---setMenuBatch---')
        if (icon == self.config.get('spot_icon')): self.is_single = False
        self.batch = QAction(icon, '批量生成', self)
        self.batch.setShortcut('Ctrl+B')
        self.batch.triggered.connect(self.chooseGenerateType)

    """
    菜单点击事件
    - 单个生成
    - 批量生成
    """
    def chooseGenerateType(self, e):
        print('---chooseGenerateType---')
        text = self.sender().text()
        if text == '单个生成':
            if self.is_single: return  # 如果已经是单个生成的状态, 直接返回
            self.single.setIcon(self.config.get('spot_icon'))
            self.batch.setIcon(self.config.get('none_icon'))
            self.is_single = True
            self.singlePageRender()
        elif text == '批量生成':
            if not self.is_single: return # 如果已经是批量生成的状态, 直接返回
            self.single.setIcon(self.config.get('none_icon'))
            self.batch.setIcon(self.config.get('spot_icon'))
            self.is_single = False
            self.batchPageRender()

    """
    界面渲染
    """
    def pageRender(self):
        print('---pageRender---')
        if self.is_single:
            self.singlePageRender()
        else:
            self.batchPageRender()

    """
    渲染单个二维码生成界面
    两个v, 一个h
    """
    def singlePageRender(self):
        print('---singlePageRender---')
        self.singleWidget = QWidget()    # 实例化一个QWidget对象
        self.singleWidget.resize(100, 100)
        self.setCentralWidget(self.singleWidget) # 将其放在 主窗口中间

        # 还是使用绝对定位好
        self.singleQRCodeTextEdit = QTextEdit(self.singleWidget)
        self.singleQRCodeTextEdit.setFontPointSize(16)
        self.singleQRCodeTextEdit.resize(350, 200)
        self.singleQRCodeTextEdit.move(50, 50)
        createButton = QPushButton('生成二维码', self.singleWidget)
        createButton.resize(120, 35)
        createButton.move(281, 270)
        createButton.clicked.connect(self.singleQRCodeCreate)


        preview = QLabel('预览: ', self.singleWidget)  # 预览字符
        preview.move(450, 25)
        preview.resize(100, 20)
        self.previewSquare = QLabel(self.singleWidget)  # 二维码生成显示区域
        self.previewSquare.resize(200, 200)
        self.previewSquare.setStyleSheet("QWidget { background-color: white }")
        self.previewSquare.move(450, 50)
        logo = QPushButton('贴图', self.singleWidget)
        logo.resize(80, 35)
        logo.move(450, 270)
        style = QPushButton('样式', self.singleWidget)
        style.resize(80, 35)
        style.move(570, 270)

    """
    单个二维码生成
    """
    def singleQRCodeCreate(self):
        print('---singleQRCodeCreate---')
        content = self.singleQRCodeTextEdit.toPlainText()   # 获取出入内容
        if content:
            # 生成二维码图像
            QRTool = QRCode()
            # img = QRTool.Usage(content)
            img = Image.open('./utils/halftone-color.png')
            # 展示在预览区
            pixmap = QPixmap.fromImage(QImage.fromData(img))
            self.previewSquare.setPicture(pixmap)
        else:
            QMessageBox.warning(self, '  ', '请输入需要生成二维码的内容')

    """
    渲染批量生成二维码界面
    """
    def batchPageRender(self):
        print('---batchPageRender---')
        pass

    """
    窗口居中
    """
    def center(self):
        print('---center---')
        qr = self.frameGeometry()   # 得到主窗口大小
        cp = QDesktopWidget().availableGeometry().center()  # 获取显示器分辨率, 得到中间点位置
        qr.moveCenter(cp)   # 将窗口中心点放置到qr的中心点
        self.move(qr.topLeft()) # 把窗口左上角的坐标设置为矩形左上角的坐标


if __name__ == '__main__':

    app = QApplication(sys.argv)
    client = GUIClient()
    sys.exit(app.exec_())