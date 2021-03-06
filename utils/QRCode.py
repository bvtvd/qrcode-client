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
from PIL import Image, ImageDraw

"""
QR Code Class
"""
class QRCode:

    QR_VERSION = 10
    POINT_PIXEL = 4
    BORDER_WIDTH = 33

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
    def HalftoneColorful(self, content = ''):
        QR_VERSION = 10
        POINT_PIXEL = 3
        painter = QrPainter(content, QR_VERSION)
        # Halftone colorful
        # img = QrHalftonePrinter.print(painter, img='e.jpg',point_width=POINT_PIXEL)
        # normal
        img = QrImagePrinter.print(painter, point_width=12, border_width=50)
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
    # def make(self, content, logo = None, size = 200, error_correction = 2):
    #     qr = qrcode.QRCode(
    #         version=1,
    #         error_correction=error_correction,
    #         box_size=12,
    #         border=0,
    #     )
    #     qr.add_data(content)
    #     qr.make(fit=True)
    #     # qr.make()
    #     img = qr.make_image()
    #     img = self.pasteLogo(img, logo)
    #     return img

    """
    生成二维码
    """
    def make(self, content, logo = None, style = 'normal', error_correction = 2):
        img = None
        if style == 'normal':
            img = self.normal(content, logo, error_correction)
        elif style == 'halftone':
            img = self.halftone(content, logo)
        elif style == 'halftoneColorful':
            img = self.halftoneColorful(content, logo)
            print(img.size)
        elif style == 'halftonePixel':
            img = self.halftonePixel(content, logo)
        elif style == 'qart':
            img = self.qart(content, logo)
        elif style == 'qartDataOnly':
            img = self.qartDataOnly(content, logo)
        elif style == 'halfArt':
            img = self.halfArt(content, logo)
        elif style == 'halfArtDataOnly':
            img = self.halfArtDataOnly(content, logo)

        # if border:
        #     img = self.addWhiteBorder(img)

        return img

    """
    给图片加白边
    直接贴图图片易失真
    """
    def addWhiteBorder(self, img, factor = 0.75):
        # 先生成一个图片大小的白底
        w, h = img.size
        back = Image.new('RGBA', (w, h), (255, 255, 255))

        # 计算图片缩放长宽
        newW = int(w * factor)
        img = img.resize((newW, newW), Image.ANTIALIAS)
        # img = img.resize((newW, newW))

        # 计算贴图位置
        x = int((w * (1 - factor)) / 2)
        back.paste(img, (x, x))
        return back


    """
    生成普通二维码
    """
    def normal(self, content, logo,  error_correction = 2):
        qr = qrcode.QRCode(
            version=None,
            error_correction=error_correction,
            box_size=12,
            border=4,
        )
        qr.add_data(content)
        qr.make(fit=True)
        # qr.make()
        img =  qr.make_image()
        return self.pasteLogo(img, logo)

    """
    生成普通二维码2
    """
    def normal2(self, content, logo):
            painter = self.getPainter(content)
            img =  QrImagePrinter.print(painter, point_width=self.POINT_PIXEL, border_width=10)
            # img =  QrImagePrinter.print(painter, point_width=24)
            # img =  QrStringPrinter.print(painter, point_width=24)
            return self.pasteLogo(img, logo)


    """
    给二维码贴logo
    """
    def pasteLogo(self, image, logo):
        if logo:
            image = image.convert('RGBA')

            # 获取二维码宽高
            imgWidth, imgHeight = image.size
            factor = 4
            sizeWidth = int(imgWidth/factor)
            sizeHeight = int(imgHeight/factor)

            # 打开logo
            logo = Image.open(logo)
            # logo = self.circleBorderImage(logo)   # 给 logo 加圆角
            # logo大小重置
            logo = logo.resize((sizeWidth, sizeHeight), Image.ANTIALIAS)
            # logo = logo.resize((sizeWidth, sizeHeight))
            logoWidth, logoHeight = logo.size
            x = int((imgWidth - logoWidth)/2)
            y = int((imgHeight - logoHeight)/2)

            try:
                # 分离通道
                r, g, b , a = logo.split()
                # 将透明通道作为mask 传入
                image.paste(logo, (x, y), mask = a)
            except ValueError:
                # 有的图片没有透明背景通道
                image.paste(logo, (x, y))

        return image

    """
    给图片加圆角
    rad: 半径
    """
    def circleBorderImage(self, logo = None, rad = 10):
        if logo:
            im = logo.convert('RGBA')
            # im = logo
            circle = Image.new('L', (rad * 2, rad * 2), 0)
            draw = ImageDraw.Draw(circle)
            draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
            alpha = Image.new('L', im.size, 255)
            w, h = im.size
            alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
            alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
            alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
            alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
            im.putalpha(alpha)
            return im

    """
    获取 artist
    """
    def getArtist(self, content, background_image, only_data = False):
        return QArtist(content, background_image, self.QR_VERSION, only_data=only_data)

    """
    获取 painter
    """
    def getPainter(self, content):
        return QrPainter(content, self.QR_VERSION)

    """
    Halftone
    @ return: Image
    """
    def halftone(self, content, background_image):
        if background_image:
            painter = self.getPainter(content)
            return QrHalftonePrinter.print(painter, img = background_image, point_width=self.POINT_PIXEL, colorful=False, border_width=self.BORDER_WIDTH)

    """
    Halftone colorful
    @ return : Image
    """
    def halftoneColorful(self, content, background_image):
        if background_image:
            painter = self.getPainter(content)
            return QrHalftonePrinter.print(painter, img=background_image, point_width=self.POINT_PIXEL, border_width=self.BORDER_WIDTH)

    """
    Halftone pixel
    @ return : Image
    """
    def halftonePixel(self, content, background_image):
        if background_image:
            painter = self.getPainter(content)
            return QrHalftonePrinter.print(painter, img=background_image, point_width=self.POINT_PIXEL, colorful=False, pixelization=True, border_width=self.BORDER_WIDTH)

    """
    Qart
    @return : Image
    """
    def qart(self, content, background_image):
        if background_image:
            artist = self.getArtist(content, background_image)
            return QrImagePrinter.print(artist, point_width=self.POINT_PIXEL, border_width=self.BORDER_WIDTH)

    """
    Qart data only
    @ return : Image
    """
    def qartDataOnly(self, content, background_image):
        if background_image:
            artist = self.getArtist(content, background_image, True)
            return QrImagePrinter.print(artist, point_width=self.POINT_PIXEL, border_width=self.BORDER_WIDTH)

    """
    halfArt
    @ return : Image
    """
    def halfArt(self, content, background_image):
        if background_image:
            artist = self.getArtist(content, background_image)
            return QrHalftonePrinter.print(artist, point_width=self.POINT_PIXEL, border_width=self.BORDER_WIDTH)

    """
    halfArt data only
    @return : Image
    """
    def halfArtDataOnly(self, content, background_image):
        if background_image:
            artist = self.getArtist(content, background_image, True)
            return QrHalftonePrinter.print(artist, point_width=self.POINT_PIXEL, border_width=self.BORDER_WIDTH)


if __name__ == '__main__':
    content = 'https://www.jianshu.com/u/ef64b2653e5e'
    background_image = '../images/nana.jpg'
    tool = QRCode()

    img = tool.normal2('1', None)
    img.show()
    # tool.make('这就是你的不对了', 800).show()
    # img = tool.HalftoneColorful('1')
    # img = tool.halftone('你好啊, nana', '../images/nana.jpg')
    # img = tool.halftoneColorful('你好啊, nana', '../images/nana.jpg')
    # img = tool.halftonePixel('你好啊, nana', '../images/nana.jpg')
    # normal
    # img = tool.make(content)
    # img.resize((150, 150)).save('../images/styles/0_normal.jpg')
    #
    # # halftone
    # img = tool.halftone(content, background_image)
    # img.resize((150, 150)).save('../images/styles/1_halftone.jpg')
    #
    # # halftone colorful
    # img = tool.halftoneColorful(content, background_image)
    # img.resize((150, 150)).save('../images/styles/2_halftoneColorful.jpg')
    #
    # # halftone pixel
    # img = tool.halftonePixel(content, background_image)
    # img.resize((150, 150)).save('../images/styles/3_halftonePixel.jpg')
    #
    # # qart
    # img = tool.qart(content, background_image)
    # img.resize((150, 150)).save('../images/styles/4_qart.jpg')
    #
    # # qart data only
    # img = tool.qartDataOnly(content, background_image)
    # img.resize((150, 150)).save('../images/styles/5_qartDataOnly.jpg')
    #
    # # halfArt
    # img = tool.halfArt(content, background_image)
    # img.resize((150, 150)).save('../images/styles/6_halfArt.jpg')
    #
    # # halfArt data only
    # img = tool.halfArtDataOnly(content, background_image)
    # img.resize((150, 150)).save('../images/styles/7_halfArtDataOnly.jpg')