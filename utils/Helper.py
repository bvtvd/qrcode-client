#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Author  :   Hans
@Contact :   hans01@foxmail.com
@File    :   Helper.py
@Time    :   2018/7/28 11:31
@Desc    :   辅助函数文件
'''
from PyQt5.QtWidgets import QDesktopWidget
import os

"""
窗口居中
"""
def center(obj):
    qr = obj.frameGeometry()  # 得到主窗口大小
    cp = QDesktopWidget().availableGeometry().center()  # 获取显示器分辨率, 得到中间点位置
    qr.moveCenter(cp)  # 将窗口中心点放置到qr的中心点
    obj.move(qr.topLeft())  # 把窗口左上角的坐标设置为矩形左上角的坐标

"""
得到系统桌面路径
"""
def getDesktopPath():
    return os.path.join(os.path.expanduser("~"), 'Desktop')

"""
获取二维码边框大小
"""
def getQRCodeBorder(img, factor = 0.16):
    w, h = img.size
    return int((w * factor)/2)


if __name__ == '__main__':
    print(getDesktopPath())