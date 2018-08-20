#! /usr/bin/python3
# -*- coding:utf-8 -*-

"""
@author:Hans
@file: SingleGenerateThread.py
@time: 2018/8/20 13:49
@desc: 单个生成二维码线程类
"""

from PyQt5.QtCore import QThread, pyqtSignal
from utils.QRCode import QRCode
import os
import sys

class SingleGenerateThread(QThread):
    signal = pyqtSignal(str)
    
    def __init__(self, content, parent = None):
        super(SingleGenerateThread, self).__init__()
        print('---SingleThread Start---')
        self.content = content
        self.parent = parent

    """
    线程运行生成二维码并缓存起来, 通知主窗口
    """
    def run(self):
        tool = QRCode()
        errorCorrection = self.transferErrorCorrectionValue(self.parent.errorCorrectionValue)
        img = tool.make(self.content, self.parent.logoPath, self.parent.style, errorCorrection)
        img.save(self.parent.config.get('single_qrcode_cache_key'))
        print('生成完成')
        self.signal.emit('OK')



    """
    转化容错值
    """
    def transferErrorCorrectionValue(self, value):
        vdict = {
            7: 1,
            15: 0,
            25: 3,
            30: 2
        }
        return vdict.get(value, 30)