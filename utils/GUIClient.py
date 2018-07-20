#! /usr/bin/python3
# -*- coding:utf-8 -*-

"""
@author:Hans
@file: GUIClient.py
@time: 2018/7/20 10:16
@desc: 
"""

import sys
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication
from PyQt5.QtGui import QIcon

class GUIClient(QMainWindow):


    def __init__(self):
        super(GUIClient, self).__init__()
        self.initUI()

    """
    先做一个 600 * 400 居中的项目
    """
    def initUI(self):
        self.resize(800, 400)   # 设置窗口大小
        self.center()   # 窗口居中
        self.setWindowTitle('二维码生成器')   # 窗口标题
        self.setWindowIcon(QIcon('./images/icon-qrcode.png'))   # 设置窗口icon
        self.show()

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