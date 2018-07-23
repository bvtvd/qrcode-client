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

    config = {
        'window_width': 1000,
        'window_height': 500,
        'window_title': '二维码生成器',
        'window_icon': './images/icon-qrcode.png',
        'spot_icon': './images/spot.png',
        'single_qrcode_cache_key': './storage/single_qrcode_cache.png'
    }

    app = QApplication(sys.argv)
    client = GUIClient(**config)
    sys.exit(app.exec_())