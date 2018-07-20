#! /usr/bin/python3
# -*- coding:utf-8 -*-

"""
@author:Hans
@file: GUIClient.py
@time: 2018/7/20 10:16
@desc: 
"""

import sys
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QAction
from PyQt5.QtGui import QIcon

class GUIClient(QMainWindow):

    # 视窗配置项
    config = {}
    # 单个生成二维码选项
    single = None
    # 批量生成二维码选项
    batch = None
    # 是否是单个生成状态记录
    is_single = False

    def __init__(self, **kwargs):
        super(GUIClient, self).__init__()
        self.initConfig(**kwargs)
        self.initUI()

    """
    初始化传入配置项
    """
    def initConfig(self, **kwargs):
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
        if(icon == self.config.get('spot_icon')): self.is_single = True
        self.single = QAction(icon, '单个生成', self)
        self.single.setShortcut('Ctrl+S')
        self.single.triggered.connect(self.chooseGenetateType)

    """
    设置批量生成菜单
    """
    def setMenuBatch(self, icon):
        if (icon == self.config.get('spot_icon')): self.is_single = False
        self.batch = QAction(icon, '批量生成', self)
        self.batch.setShortcut('Ctrl+B')
        self.batch.triggered.connect(self.chooseGenetateType)

    """
    菜单点击事件
    - 单个生成
    - 批量生成
    """
    def chooseGenetateType(self, e):
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
        if self.is_single:
            self.singlePageRender()
        else:
            self.batchPageRender()

    """
    渲染单个二维码生成界面
    """
    def singlePageRender(self):
        print('singlePageRender')
        pass

    """
    渲染批量生成二维码界面
    """
    def batchPageRender(self):
        print('batchPageRender')
        pass

    """
    窗口居中
    """
    def center(self):
        qr = self.frameGeometry()   # 得到主窗口大小
        cp = QDesktopWidget().availableGeometry().center()  # 获取显示器分辨率, 得到中间点位置
        qr.moveCenter(cp)   # 将窗口中心点放置到qr的中心点
        self.move(qr.topLeft()) # 把窗口左上角的坐标设置为矩形左上角的坐标


if __name__ == '__main__':

    app = QApplication(sys.argv)
    client = GUIClient()
    sys.exit(app.exec_())