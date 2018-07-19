#! /usr/bin/python3
# -*- coding:utf-8 -*-

"""
@author:Hans
@file: qrcode.py
@time: 2018/7/19 11:24
@desc: 
"""

import qrcode
from pyqart import QArtist, QrHalftonePrinter, QrImagePrinter, QrPainter

"""
QR Code Class
"""
class QRCode:

    def __init__(self):
        pass

    """
    基础用法
    """
    def Usage(self, content = ''):
        img = qrcode.make(content)
        return img

    """
    高级用法
    version : 1-40 控制二维码尺寸, 1 为 21 * 21 , 设置为 None 或 fit 为自动设置
    error_correction : 容错率
        ERROR_CORRECT_L : 7%
        ERROR_CORRECT_M : 15%
        ERROR_CORRECT_Q : 25%
        ERROR_CORRECT_H : 30%
    box_size : 表示二维码里每个格子的像素大小
    border : 表示边框的格子厚度是多少（默认是4）
    """
    def AdvancedUsage(self):
        qr = qrcode.QRCode(
            version=40,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=2,
            border=0,
        )
        qr.add_data('Some data')
        qr.make(fit=True)
        img = qr.make_image()
        return img

    """
    生成图像二维码
    具体在研究接口
    https://github.com/7sDream/pyqart/blob/master/README.zh.md
    """
    def HalftoneColorful(self):
        QR_VERSION = 10
        POINT_PIXEL = 3
        painter = QrPainter('你好啊', QR_VERSION)
        # Halftone colorful
        img = QrHalftonePrinter.print(painter, img='e.jpg',point_width=POINT_PIXEL)
        # normal
        # img = QrImagePrinter.print(painter, point_width=POINT_PIXEL)
        return img


    """
    生成二维码
    参数:
    content: 内容
    size: 尺寸
    error_correction: 容错 [7, 15 25, 30]
        ERROR_CORRECT_L = 1
        ERROR_CORRECT_M = 0
        ERROR_CORRECT_Q = 3
        ERROR_CORRECT_H = 2
    """
    def make(self, content, size = 200, error_correction = 2):
        qr = qrcode.QRCode(
            version=1,
            error_correction=error_correction,
            box_size=7,
            border=0,
        )
        qr.add_data(content)
        qr.make(fit=True)
        img = qr.make_image()
        return img.resize((size, size))


if __name__ == '__main__':
    tool = QRCode()
    # tool.make('这就是你的不对了', 800).save('1.png')
    img = tool.HalftoneColorful()
    img.show()