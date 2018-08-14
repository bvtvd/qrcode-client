#! /usr/bin/python3
# -*- coding:utf-8 -*-

"""
@author:Hans
@file: GUIClient.py
@time: 2018/7/20 10:16
@desc: 
"""

import sys, time, random, os, shutil
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QAction, QHBoxLayout, QVBoxLayout, QTextEdit, QPushButton, QWidget, QLabel, QFrame, QGridLayout, QMessageBox, QFileDialog, QSlider, QLineEdit, QProgressBar
from PyQt5.QtGui import QIcon, QPixmap, QPicture, QImage
from PyQt5.QtCore import Qt, pyqtSlot
from utils.QRCode import QRCode
from utils.LogoDialog import LogoDialog
from utils.StyleDialog import StyleDialog
from utils.BatchGenerateThread import BatchGenerateThread
from PIL import Image
from utils.Helper import center, getDesktopPath
from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException
import time


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
    # 单个二维码保存路径
    singleSavePath = getDesktopPath()
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
    # 批量文件
    batchFile = None
    # 批量logo 地址
    batchLogoPath = None
    # 批量二维码 样式
    batchStyle = 'normal'
    # 批量二维码生成进度条
    batchProgressBar = None
    # 批量生成二维码尺寸数值
    batchSize = 280

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
        self.config['logo_dir'] = kwargs.get('logo_dir', '../images/logos')
        self.config['style_dir'] = kwargs.get('style_dir', '../images/styles')
        self.config['images_path'] = kwargs.get('images_path', '../images/')
        self.config['storage_path'] = kwargs.get('storage_path', '../storage/')
        self.config['config_path'] = kwargs.get('config_path', '../config/')

    """
    项目初始化
    """
    def initUI(self):
        print('---initUI---')
        self.initMenu() # 初始化菜单
        self.pageRender()   # 界面渲染

        # self.resize(self.config['window_width'], self.config['window_height'])   # 设置窗口大小
        # self.setWindowFlags(Qt.WindowMaximizeButtonHint)
        self.setFixedSize(self.config['window_width'], self.config['window_height'])    # 设置固定窗口大小
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

        # 菜单
        menuMenu = menuBar.addMenu('&菜单')
        self.setMenuSingle(self.config.get('spot_icon'))
        self.setMenuBatch(self.config.get('none_icon'))
        menuMenu.addAction(self.single)
        menuMenu.addAction(self.batch)
        menuMenu.addSeparator()
        # setting = QAction(QIcon(self.getImage('settings.png')), '设置', self)
        # menuMenu.addAction(setting)
        # menuMenu.addSeparator()
        exit = QAction(QIcon(self.getImage('exit.png')), '退出', self)
        exit.triggered.connect(self.close)
        menuMenu.addAction(exit)

        # 帮助
        helpMenu = menuBar.addMenu('&帮助')
        manual = QAction('说明', self)
        about = QAction('关于', self)
        helpMenu.addAction(manual)
        helpMenu.addAction(about)

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
    获取图片路径
    """
    def getImage(self, name):
        return os.path.join(self.config['images_path'], name)

    """
    获取 storage 路径
    """
    def getStorage(self, name):
        return os.path.join(self.config['storage_path'], name)

    """
    获取 config 路径
    """
    def getConfig(self, name):
        return os.path.join(self.config['config_path'], name)

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
        self.singleQRCodePreview()

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
            # errorCorrectionValue 还要转化一次
            if self.style != 'normal' and not self.logoPath:    # 非普通二维码需要背景图片
                QMessageBox.warning(self, '  ', '请在 logo 中选择背景图片', QMessageBox.Ok)
                return

            QRTool = QRCode()
            errorCorrection = self.transferErrorCorrectionValue()
            return QRTool.make(content, self.logoPath, self.style, errorCorrection)

    """
    转化容错值
    """
    def transferErrorCorrectionValue(self):
        vdict = {
            7 : 1,
            15: 0,
            25: 3,
            30: 2
        }
        return vdict.get(self.errorCorrectionValue, 30)


    """
    单个二维码预览
    """
    def singleQRCodePreview(self):
        print('---singleQRCodePreview---')
        self.previewSuqareLoading()
        img = self.singleQRCodeCreate()
        if img:
            img = img.resize((280, 280))
            # 将图片缓存起来
            img.save(self.config.get('single_qrcode_cache_key'))
            # 展示在预览区
            pixmap = QPixmap(self.config.get('single_qrcode_cache_key'))
            self.previewSquare.setPixmap(pixmap)

    """
    预览框加载动画
    """
    def previewSuqareLoading(self):
        print('---previewSuqareLoading---')
        # self.previewSquare.setText(' 正在生成... ')
        # pixmap = QPixmap('./images/loading.png')
        # self.previewSquare.setPixmap(pixmap)
        # self.previewSquare.setStyleSheet('QLabel {  }')

    """
    单个二维码下载
    """
    def singleQRCodeDownload(self):
        print('---singleQRCodeDownload---')
        # self.previewSuqareLoading()
        # return

        img = self.singleQRCodeCreate()
        if img:
            imgName = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + str(random.randint(1000, 9999))
            savePath = os.path.join(self.singleSavePath, imgName)
            fname = QFileDialog.getSaveFileName(self, '保存', savePath, "*.png;;*.jpg;;*.jpeg;;*.gif;;*.bmp")
            img = img.resize((self.pictureSizeValue, self.pictureSizeValue))
            if fname[0]:
                self.singleSavePath = os.path.dirname(fname[0]) # 缓存保存路径
                img.save(fname[0])

    """
    渲染批量生成二维码界面
    """
    def batchPageRender(self):
        print('---batchPageRender---')
        # if not self.batchWidget:  # 重新使用setCentralWidget 之后会导致之前的Widget 被 QMainWindow 删除, 所以需要每次都重新生成新的Widget 然后再赋值
        self.batchWidget = QWidget()
        self.filePathInput = QLineEdit(self.batchWidget)
        self.filePathInput.setReadOnly(True)
        self.filePathInput.resize(720, 40)
        self.filePathInput.move(140, 100)
        self.filePathInput.setStyleSheet('QLineEdit { font-size:14px; }')

        # 下载模板按钮
        downloadTemplateButton = QPushButton('下载批量模板', self.batchWidget)
        downloadTemplateButton.resize(200, 35)
        downloadTemplateButton.move(140, 160)
        downloadTemplateButton.clicked.connect(self.downloadBatchTemplate)

        # 上传文件按钮
        uploadTemplateButton = QPushButton('上传', self.batchWidget)
        uploadTemplateButton.resize(200, 35)
        uploadTemplateButton.move(400, 160)
        uploadTemplateButton.clicked.connect(self.uploadBatchTemplate)

        # 生成二维码按钮
        batchCreateButton = QPushButton('生成', self.batchWidget)
        batchCreateButton.resize(200, 35)
        batchCreateButton.move(660, 160)
        batchCreateButton.clicked.connect(self.batchQRCodeCreate)

        # 选择logo 按钮
        batchLogoButton = QLabel(self.batchWidget)
        batchLogoButton.resize(50, 35)
        batchLogoButton.move(140, 215)
        batchLogoButton.setText('logo: ')
        batchLogoButton.setStyleSheet('QLabel { font-size: 14px }')
        batchLogoButton.setToolTip('点我选择logo')
        batchLogoButton.setCursor(Qt.PointingHandCursor)
        batchLogoButton.mousePressEvent = self.batchChooseLogo

        # logo 贴图 label
        self.batchLogoLabel = QLabel(self.batchWidget)
        self.batchLogoLabel.resize(50, 50)
        self.batchLogoLabel.move(190, 215)
        # self.batchLogoLabel.setStyleSheet('QLabel { background-color: white }')
        self.batchLogoLabel.setCursor(Qt.PointingHandCursor)
        self.batchLogoLabel.mousePressEvent = self.batchChooseLogo

        # 样式按钮
        batchStyleButton = QLabel(self.batchWidget)
        batchStyleButton.resize(50, 35)
        batchStyleButton.move(300, 215)
        batchStyleButton.setText('样式: ')
        batchStyleButton.setStyleSheet('QLabel { font-size: 14px }')
        batchStyleButton.setToolTip('点我选择样式')
        batchStyleButton.setCursor(Qt.PointingHandCursor)
        batchStyleButton.mousePressEvent = self.batchChooseStyle

        # 样式内容label
        self.batchStyleLabel = QLabel(self.batchWidget)
        self.batchStyleLabel.resize(148, 35)
        self.batchStyleLabel.move(350, 215)
        self.batchStyleLabel.setStyleSheet('QLabel { background-color: white; font-size: 14px }')
        self.batchStyleLabel.setText(self.batchStyle)
        self.batchStyleLabel.setCursor(Qt.PointingHandCursor)
        self.batchStyleLabel.mousePressEvent = self.batchChooseStyle

        # 尺寸字样
        batchSizeButton = QLabel('尺寸: ', self.batchWidget)
        batchSizeButton.setGeometry(548, 215, 50, 35)
        batchSizeButton.setStyleSheet('QLabel { font-size: 14px }')

        # 尺寸滑条
        self.batchSizeSlider = QSlider(Qt.Horizontal, self.batchWidget)
        self.batchSizeSlider.setFocusPolicy(Qt.NoFocus)
        self.batchSizeSlider.setMinimum(50)
        self.batchSizeSlider.setMaximum(800)
        self.batchSizeSlider.setValue(self.batchSize)
        self.batchSizeSlider.setGeometry(598, 225, 205, 20)
        self.batchSizeSlider.valueChanged[int].connect(self.batchSizeSliderChanged)

        # 尺寸滑条数值显示
        self.batchSizeLabel = QLabel('{}px'.format(self.batchSize), self.batchWidget)
        self.batchSizeLabel.setGeometry(813, 215, 40, 35)

        # 二维码生成进度条
        self.batchProgressBar = QProgressBar(self.batchWidget)
        self.batchProgressBar.setTextVisible(False)
        self.batchProgressBar.setGeometry(140, 270, 720, 5)
        self.batchProgressBar.setHidden(True)


        # 批量二维码生成日志容器
        self.batchLogBox = QTextEdit(self.batchWidget)
        self.batchLogBox.resize(720, 150)
        self.batchLogBox.move(140, 300)
        self.batchLogBox.setReadOnly(True)  # 只读, 由程序填入数据
        self.batchLogBox.setHidden(True)
        # self.batchLogBox.append('<p style="color: red;margin:2"> 你好</p>')

        self.setCentralWidget(self.batchWidget)

    """
    批量尺寸滑条变动
    """
    def batchSizeSliderChanged(self, value):
        print('---batchSizeSliderChanged---')
        self.batchSize = value
        self.batchSizeLabel.setText('{}px'.format(self.batchSize))

    """
    批量二维码样式选择
    """
    def batchChooseStyle(self, event):
        print('---batchChooseStyle---')
        dialog = StyleDialog(self, styleDir=self.config['style_dir'])
        dialog.styleChosenSignal.connect(self.batchStyleChosen)
        if dialog.exec_():
            pass

    """
    批量二维码样式选中
    """
    def batchStyleChosen(self, style):
        print('---batchStyleChosen---')
        self.batchStyle = style
        self.batchStyleLabel.setText(self.batchStyle)

    """
    批量页面选择logo
    """
    def batchChooseLogo(self, event):
        print('---batchChooseLogo---')
        dialog = LogoDialog(self, logoDir=self.config['logo_dir'])
        dialog.logoChosenSignal.connect(self.batchLogoChosen)  # 绑定自定义事件
        if dialog.exec_():
            pass

    """
    批量logo 选中
    """
    def batchLogoChosen(self, s):
        print('---batchLogoChosen---')
        print(s)
        self.batchLogoPath = s
        if self.batchLogoPath:
            pixmap = QPixmap(self.batchLogoPath).scaled(50, 50)
            self.batchLogoLabel.setPixmap(pixmap)
        else:
            self.batchLogoLabel.setText(' ')


    """
    批量生成二维码
    """
    def batchQRCodeCreate(self):
        print('---batchQRCodeCreate---')
        if self.batchFile:
            try:
                excel = load_workbook(self.batchFile)
            except InvalidFileException:
                QMessageBox.warning(self, ' ', '文件错误, 请上传带 .xlsx 后缀文件', QMessageBox.Ok)
                return

            # 要生成一个保存路径
            # self.batchSavePath = os.path.join(getDesktopPath(), 'pics')
            self.batchSavePath = QFileDialog.getExistingDirectory(self.batchWidget, '选择保存路径', getDesktopPath())
            print(self.batchSavePath)
            # 进度条和日志框 清理
            self.batchProgressBar.setHidden(False)
            self.batchLogBox.setHidden(False)
            self.batchProgressBar.setValue(0)
            self.batchLogBox.clear()

            # 实例化线程
            self.batchGenerateThread = BatchGenerateThread(self)
            # 线程信号处理
            self.batchGenerateThread.signal.connect(self.batchGenerateThreadSignalHandler)
            self.batchGenerateThread.start()    # 开启线程
            self.batchGenerateThread.finished.connect(self.batchGenerateThreadFinished) # 线程结束处理事件
        else:
            QMessageBox.warning(self, ' ', '请先上传文件', QMessageBox.Ok)

    """
    批量生成线程结束事件
    弹出对话框询问是否打开文件夹
    """
    def batchGenerateThreadFinished(self):
        print('---batchGenerateThreadFinished---')
        # messageBox = QMessageBox.information(self, ' ', '执行完成', QMessageBox.Yes | QMessageBox.No)
        messageBox = QMessageBox(self)
        messageBox.setWindowTitle(' ')
        messageBox.setText('执行成功')
        # messageBox.addButton(QPushButton('打开文件夹'), QMessageBox.YesRole)
        # messageBox.addButton(QPushButton('取消'), QMessageBox.NoRole)
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = messageBox.button(QMessageBox.Yes)
        buttonY.setText('打开文件夹')
        buttonN = messageBox.button(QMessageBox.No)
        buttonN.setText('取消')
        messageBox.exec_()
        if messageBox.clickedButton() == buttonY:
            print('点击了yes')
            # 打开文件夹
            print(self.batchSavePath)
            # os.system('explorer.exe "{}"'.format(self.batchSavePath))
            os.startfile(self.batchSavePath)

    """
    批量生成
    """
    def batchGenerateThreadSignalHandler(self, data):
        print('---batchGenerateThreadSignalHandler---')
        data.get('progressBarValue') and self.batchProgressBar.setValue(data.get('progressBarValue'))
        data.get('message') and self.batchLogBox.append(data.get('message'))

    """
    上传批量模板
    """
    def uploadBatchTemplate(self):
        fname = QFileDialog.getOpenFileName(self, '选择批量模板', getDesktopPath())
        if fname[0]:
            self.batchFile = fname[0]
            self.filePathInput.setText(fname[0])
        self.batchProgressBar.setHidden(True)
        self.batchLogBox.clear()
        self.batchLogBox.setHidden(True)

    # 下载批量模板
    def downloadBatchTemplate(self):
        print('---downloadBatchTemplate---')
        name = 'example.xlsx'
        templatePath = self.getStorage(name)
        if os.path.exists(templatePath):
            savePath = os.path.join(getDesktopPath(), name)
            fname = QFileDialog.getSaveFileName(self, '保存',  savePath)
            fname[0] and shutil.copy(templatePath, fname[0])
        else:
            QMessageBox.warning(self, '  ', '批量模板已丢失!', QMessageBox.Ok)


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