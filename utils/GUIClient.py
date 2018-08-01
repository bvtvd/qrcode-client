#! /usr/bin/python3
# -*- coding:utf-8 -*-

"""
@author:Hans
@file: GUIClient.py
@time: 2018/7/20 10:16
@desc: 
"""

import sys
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QAction, QHBoxLayout, QVBoxLayout, QTextEdit, QPushButton, QWidget, QLabel, QFrame, QGridLayout, QMessageBox, QFileDialog, QSlider
from PyQt5.QtGui import QIcon, QPixmap, QPicture, QImage
from PyQt5.QtCore import Qt, pyqtSlot
from utils.QRCode import QRCode
from utils.LogoDialog import LogoDialog
from utils.StyleDialog import StyleDialog
from PIL import Image
import time, random
from utils.Helper import center


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
    # 批量二维码生成页面
    batchWidget = None
    # 单个二维码生成滑条数值
    pictureSizeValue = 280
    # 单个二维码生成容错率滑条数值
    errorCorrectionValue = 30
    # logo 路径
    logoPath = None
    # 二维码样式
    style = 'normal'

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
    single_qrcode_cache_key: 单个二维码缓存路径
    """
    def initConfig(self, **kwargs):
        print('---initConfig---')
        self.config['window_width'] = kwargs.get('window_width', 800)
        self.config['window_height'] = kwargs.get('window_height', 400)
        self.config['window_title'] = kwargs.get('window_title', '二维码生成器')
        self.config['window_icon'] = kwargs.get('window_icon', '../images/icon-qrcode.png')
        self.config['spot_icon'] = QIcon(kwargs.get('spot_icon', '../images/spot.png'))
        self.config['none_icon'] = QIcon('')
        self.config['single_qrcode_cache_key'] = kwargs.get('single_qrcode_cache_key', '../storage/single_qrcode_cache.png')
        self.config['logo_dir'] = kwargs.get('logo_dir', './images/logos')
        self.config['style_dir'] = kwargs.get('style_dir', './images/styles')

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
        # if not self.singleWidget:
        self.singleWidget = QWidget()    # 实例化一个QWidget对象

        # 还是使用绝对定位好
        self.singleQRCodeTextEdit = QTextEdit(self.singleWidget)
        self.singleQRCodeTextEdit.setFontPointSize(14)
        self.singleQRCodeTextEdit.resize(570, 280) #(350, 200)
        self.singleQRCodeTextEdit.move(50, 50)
        createButton = QPushButton('生成二维码', self.singleWidget)
        createButton.resize(120, 35)
        createButton.move(501, 350)
        createButton.clicked.connect(self.singleQRCodePreview)

        preview = QLabel('预览: ', self.singleWidget)  # 预览字符
        preview.move(670, 25)
        preview.resize(100, 20)
        self.previewSquare = QLabel(self.singleWidget)  # 二维码生成显示区域
        self.previewSquare.resize(280, 280)
        self.previewSquare.setStyleSheet("QWidget { background-color: white }")
        self.previewSquare.move(670, 50)
        logo = QPushButton('logo', self.singleWidget)
        logo.resize(80, 35)
        logo.move(670, 350)
        logo.clicked.connect(self.chooseLogo)
        style = QPushButton('样式', self.singleWidget)
        style.resize(80, 35)
        style.move(770, 350)
        style.clicked.connect(self.chooseStyle)
        download = QPushButton('下载', self.singleWidget)
        download.resize(80, 35)
        download.move(873, 350)
        download.clicked.connect(self.singleQRCodeDownload)
        # 图片尺寸滑条
        pictureSizeTitle = QLabel('尺寸: ', self.singleWidget)
        pictureSizeTitle.resize(40, 20)
        pictureSizeTitle.move(670, 400)
        pictureSize = QSlider(Qt.Horizontal, self.singleWidget)
        pictureSize.setFocusPolicy(Qt.NoFocus)
        pictureSize.setMinimum(50)
        pictureSize.setMaximum(800)
        pictureSize.setValue(self.pictureSizeValue)
        pictureSize.setGeometry(710, 400, 205, 20)
        pictureSize.valueChanged[int].connect(self.singleQRCodePictureSizeSliderChanged)
        # 滑条数值显示
        self.pictureSizeLabel = QLabel('{}px'.format(self.pictureSizeValue), self.singleWidget)
        self.pictureSizeLabel.resize(40, 20)
        self.pictureSizeLabel.move(930, 400)
        # 容错率滑条
        errorCorrectionTitle = QLabel('容错: ', self.singleWidget)
        errorCorrectionTitle.resize(40, 20)
        errorCorrectionTitle.move(670, 430)
        self.errorCorrection = QSlider(Qt.Horizontal, self.singleWidget)
        self.errorCorrection.setFocusPolicy(Qt.NoFocus)
        self.errorCorrection.setMinimum(7)
        self.errorCorrection.setMaximum(30)
        self.errorCorrection.setValue(self.errorCorrectionValue)
        self.errorCorrection.setGeometry(710, 430, 205, 20)
        self.errorCorrection.valueChanged[int].connect(self.singleQRCodeErrorCorrectionSliderChanged)
        self.errorCorrectionLabel = QLabel('{}%'.format(self.errorCorrectionValue), self.singleWidget)
        self.errorCorrectionLabel.resize(40, 20)
        self.errorCorrectionLabel.move(930, 430)

        # self.singleWidget.setStyleSheet('QWidget { background-color: black }')
        self.setCentralWidget(self.singleWidget)  # 将其放在 主窗口中间


    """
    选择样式
    """
    def chooseStyle(self):
        print("---chooseStyle---")
        dialog = StyleDialog(self, styleDir=self.config['style_dir'])
        dialog.styleChosenSignal.connect(self.styleChosen)
        if dialog.exec_():
            pass

    """
    样式被选中
    """
    def styleChosen(self, style):
        print('---styleChosen---')
        self.style = style
        self.singleQRCodePreview() # 生成预览二维码

    """
    选择logo
    """
    def chooseLogo(self):
        print('---chooseLogo---')
        dialog = LogoDialog(self, logoDir=self.config['logo_dir'])
        dialog.logoChosenSignal.connect(self.logoChosen)    # 绑定自定义事件
        if dialog.exec_():
            pass


    """
    logo 被选中
    """
    def logoChosen(self, s):
        print('---GUIClient.logoChosen---')
        self.logoPath = s
        self.singleQRCodePreview()  # 生成预览二维码

    """
    单个二维码生成容错率滑条滚动    
    """
    def singleQRCodeErrorCorrectionSliderChanged(self, value):
        print('---singleQRCodeErrorCorrectionSliderChanged---')
        if value < 13:
            self.errorCorrectionValue = 7
        elif value >= 13 and value < 21:
            self.errorCorrectionValue = 15
        elif value >= 21 and value < 27:
            self.errorCorrectionValue = 25
        elif value >=27:
            self.errorCorrectionValue = 30

        self.errorCorrection.setValue(self.errorCorrectionValue)
        self.errorCorrectionLabel.setText('{}%'.format(self.errorCorrectionValue))

    """
    单个二维码生成图片大小滑条滚动
    """
    def singleQRCodePictureSizeSliderChanged(self, value):
        print('---singleQRCodePictureSizeSliderChanged---')
        self.pictureSizeValue = value
        self.pictureSizeLabel.setText('{}px'.format(self.pictureSizeValue))

    """
    单个二维码生成
    """
    def singleQRCodeCreate(self):
        print('---singleQRCodeCreate---')
        content = self.singleQRCodeTextEdit.toPlainText()   # 获取出入内容
        if content:
            # 生成二维码图像
            QRTool = QRCode()
            return QRTool.make(content, self.logoPath)

    """
    单个二维码预览
    """
    def singleQRCodePreview(self):
        print('---singleQRCodePreview---')
        img = self.singleQRCodeCreate()
        if img:
            img = img.resize((280, 280))
            # 将图片缓存起来
            img.save(self.config.get('single_qrcode_cache_key'))
            # 展示在预览区
            pixmap = QPixmap(self.config.get('single_qrcode_cache_key'))
            self.previewSquare.setPixmap(pixmap)

    """
    单个二维码下载
    """
    def singleQRCodeDownload(self):
        print('---singleQRCodeDownload---')
        img = self.singleQRCodeCreate()
        if img:
            imgName = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + str(random.randint(1000, 9999))
            fname = QFileDialog.getSaveFileName(self, '保存', imgName, "*.png;;*.jpg;;*.jpeg;;*.gif;;*.bmp")
            fname[0] and img.save(fname[0])

    """
    渲染批量生成二维码界面
    """
    def batchPageRender(self):
        print('---batchPageRender---')
        # if not self.batchWidget:  # 重新使用setCentralWidget 之后会导致之前的Widget 被 QMainWindow 删除, 所以需要每次都重新生成新的Widget 然后再赋值
        self.batchWidget = QWidget()
        temp = QLabel('批量页面', self.batchWidget)

        print(self.batchWidget)
        self.setCentralWidget(self.batchWidget)

    """
    窗口居中
    """
    def center(self):
        print('---center---')
        # qr = self.frameGeometry()   # 得到主窗口大小
        # cp = QDesktopWidget().availableGeometry().center()  # 获取显示器分辨率, 得到中间点位置
        # qr.moveCenter(cp)   # 将窗口中心点放置到qr的中心点
        # self.move(qr.topLeft()) # 把窗口左上角的坐标设置为矩形左上角的坐标
        center(self)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    client = GUIClient()
    sys.exit(app.exec_())