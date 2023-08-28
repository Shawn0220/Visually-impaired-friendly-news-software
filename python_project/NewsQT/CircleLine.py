# -*- coding: utf-8 -*-
import os
import base64
import pandas as pd
# from QSplashScreen import GifSplashScreen
from math import floor, pi, cos, sin
from random import random, randint
from time import time, sleep

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import Qt, QRectF, QSize, pyqtSignal, QTimer
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import predict.predict as predict

# 按钮样式
BtnStyle = "QPushButton{background-color:gray;border:1px groove gray;"\
            "border-radius:20px;padding:1px 4px;border-style: outset;}\n"\
            "QPushButton:hover{background-color:rgb(229, 241, 251); color: black;}\n"\
            "QPushButton:pressed{background-color:rgb(204, 228, 247);border-style: inset;}\n"

# 最小和最大半径、半径阈值和填充圆的百分比
radMin = 10
radMax = 80
filledCircle = 30  # 填充圆的百分比
concentricCircle = 60  # 同心圆百分比
radThreshold = 25  # IFF special, over this radius concentric, otherwise filled
# 最小和最大移动速度
speedMin = 0.3
speedMax = 0.6
# 每个圆和模糊效果的最大透明度
maxOpacity = 0.6

colors = [
    QColor(52, 168, 83),
    QColor(117, 95, 147),
    QColor(199, 108, 23),
    QColor(194, 62, 55),
    QColor(0, 172, 212),
    QColor(120, 120, 120)
]
circleBorder = 10
backgroundLine = colors[0]
backgroundColor = QColor(38, 43, 46)
backgroundMlt = 0.85

lineBorder = 2.5

# 最重要的是：包含它们的整个圆和数组的数目
maxCircles = 8
points = []

# 实验变量
circleExp = 1
circleExpMax = 1.003
circleExpMin = 0.997
circleExpSp = 0.00004
circlePulse = False


# 生成随机整数 a<=x<=b
def randint(a, b):
    return floor(random() * (b - a + 1) + a)


# 生成随机小数
def randRange(a, b):
    return random() * (b - a) + a


# 生成接近a的随机小数
def hyperRange(a, b):
    return random() * random() * random() * (b - a) + a


class Circle:
    def __init__(self, background, width, height):
        self.background = background
        self.x = randRange(-width / 2, width / 2)
        self.y = randRange(-height / 2, height / 2)
        self.radius = hyperRange(radMin, radMax)
        self.filled = (False if randint(
            0, 100) > concentricCircle else 'full') if self.radius < radThreshold else (
                False if randint(0, 100) > concentricCircle else 'concentric')
        self.color = colors[randint(0, len(colors) - 1)]
        self.borderColor = colors[randint(0, len(colors) - 1)]
        self.opacity = 0.05
        self.speed = randRange(speedMin, speedMax)  # * (radMin / self.radius)
        self.speedAngle = random() * 2 * pi
        self.speedx = cos(self.speedAngle) * self.speed
        self.speedy = sin(self.speedAngle) * self.speed
        spacex = abs((self.x - (-1 if self.speedx < 0 else 1) *
                      (width / 2 + self.radius)) / self.speedx)
        spacey = abs((self.y - (-1 if self.speedy < 0 else 1) *
                      (height / 2 + self.radius)) / self.speedy)
        self.ttl = min(spacex, spacey)


def callback():
    print('回调点击')


class CircleLineWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(CircleLineWindow, self).__init__(*args, **kwargs)

        # # 启动动画，模拟耗时操作，一般来说耗时的加载数据应该放到线程
        # for i in range(100):
        #     sleep(0.01)
        #     splash.showMessage('加载进度: %d' % i, Qt.AlignHCenter | Qt.AlignBottom, Qt.white)
        #     QApplication.instance().processEvents()
        # splash.showMessage('初始化完成', Qt.AlignHCenter | Qt.AlignBottom, Qt.white)
        # splash.finish(self)

        # 设置背景颜色
        palette = self.palette()
        palette.setColor(palette.Background, backgroundColor)
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        # 获取屏幕大小
        geometry = QApplication.instance().desktop().availableGeometry()
        self.screenWidth = geometry.width()
        self.screenHeight = geometry.height()
        self._canDraw = True
        self._firstDraw = True
        self._timer = QTimer(self, timeout=self.update)
        self.init()
        self.path = any

        self.SingleNewsClassify = QtWidgets.QWidget(self)
        self.SingleNewsClassify.setObjectName("SingleNewsClassify")

        self.NewsText1_div = QtWidgets.QWidget(self.SingleNewsClassify)
        self.result1_div = QtWidgets.QWidget(self.SingleNewsClassify)

        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)

        self.NewsText1 = QtWidgets.QPlainTextEdit(self.NewsText1_div)
        self.NewsText1.setFont(font)
        self.NewsText1.setPlainText("")
        self.NewsText1.setObjectName("NewsText1")

        self.result1 = QtWidgets.QPlainTextEdit(self.result1_div)
        self.result1.setFont(font)
        self.result1.setObjectName("result1")

        self.submit = QtWidgets.QPushButton(self.SingleNewsClassify)
        self.submit.setFont(font)
        self.submit.setStyleSheet(BtnStyle+"QPushButton{background-color: aquamarine;}")
        self.submit.setObjectName("submit")

        self.clean = QtWidgets.QPushButton(self.SingleNewsClassify)
        self.clean.setFont(font)
        self.clean.setStyleSheet(BtnStyle+"QPushButton{background-color: orange;}")
        self.clean.setObjectName("clean")

        self.cleanResult1 = QtWidgets.QPushButton(self.SingleNewsClassify)
        self.cleanResult1.setFont(font)
        self.cleanResult1.setStyleSheet(BtnStyle + "QPushButton{background-color: orange;}")
        self.cleanResult1.setObjectName("cleanResult1")

        self.label = QtWidgets.QLabel(self.SingleNewsClassify)
        self.label.setFont(font)
        self.label.setStyleSheet("color:white;")
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.SingleNewsClassify)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color:white;")
        self.label_2.setObjectName("label_2")

        # 多条新闻处理
        self.MultiNewsClassify = QtWidgets.QWidget(self)
        self.MultiNewsClassify.hide()
        self.MultiNewsClassify.setObjectName("MultiNewsClassify")

        self.showUploadNews = QAxWidget(self.MultiNewsClassify)
        self.showUploadNews.setObjectName("showUploadNews")
        self.showUploadNews.setStyleSheet("background-color:white")

        self.result2 = QAxWidget(self.MultiNewsClassify)
        self.result2.setObjectName("result2")
        self.result2.setStyleSheet("background-color:white")

        self.upload = QtWidgets.QPushButton(self.MultiNewsClassify)
        self.upload.setFont(font)
        self.upload.setStyleSheet(BtnStyle+"QPushButton{background-color: lightgreen;}")
        self.upload.setObjectName("upload")

        self.submit2 = QtWidgets.QPushButton(self.MultiNewsClassify)
        self.submit2.setFont(font)
        self.submit2.setStyleSheet(BtnStyle+"QPushButton{background-color: aqua;}")
        self.submit2.setObjectName("submit2")

        self.clean2 = QtWidgets.QPushButton(self.MultiNewsClassify)
        self.clean2.setFont(font)
        self.clean2.setStyleSheet(BtnStyle+"QPushButton{background-color: orange;}")
        self.clean2.setObjectName("clean2")

        self.cleanResult2 = QtWidgets.QPushButton(self.MultiNewsClassify)
        self.cleanResult2.setFont(font)
        self.cleanResult2.setStyleSheet(BtnStyle + "QPushButton{background-color: orange;}")
        self.cleanResult2.setObjectName("cleanResult2")

        self.label_3 = QtWidgets.QLabel(self.MultiNewsClassify)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color:white;")
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(self.MultiNewsClassify)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white;")
        self.label_4.setObjectName("label_4")

        font.setBold(True)
        font.setWeight(75)

        self.singleNewsBtn = QtWidgets.QPushButton(self)
        self.singleNewsBtn.setFont(font)
        self.singleNewsBtn.setStyleSheet(BtnStyle+"QPushButton{background-color:lightblue ;}")
        self.singleNewsBtn.setObjectName("singleNewsBtn")

        self.multiNewsBtn = QtWidgets.QPushButton(self)
        self.multiNewsBtn.setFont(font)
        self.multiNewsBtn.setStyleSheet(BtnStyle+"QPushButton{background-color:lightgreen ;}")
        self.multiNewsBtn.setObjectName("multiNewsBtn")

        self.singleNewsBtn.setGeometry(QtCore.QRect(500, 30, 200, 70))
        self.multiNewsBtn.setGeometry(QtCore.QRect(800, 30, 200, 70))

        self.label.setGeometry(QtCore.QRect(280, 130, 120, 40))
        self.label_2.setGeometry(QtCore.QRect(1080, 130, 120, 40))
        self.label_3.setGeometry(QtCore.QRect(280, 130, 120, 40))
        self.label_4.setGeometry(QtCore.QRect(1080, 130, 120, 40))

        self.NewsText1_div.setGeometry(QtCore.QRect(100, 200, 510, 510))
        self.result1_div.setGeometry(QtCore.QRect(880, 200, 510, 510))
        self.NewsText1.setGeometry(QtCore.QRect(10, 10, 480, 480))
        self.result1.setGeometry(QtCore.QRect(10, 10, 480, 480))

        self.showUploadNews.setGeometry(QtCore.QRect(100, 200, 500, 500))
        self.result2.setGeometry(QtCore.QRect(880, 200, 500, 500))

        self.submit.setGeometry(QtCore.QRect(150, 730, 120, 60))
        self.clean.setGeometry(QtCore.QRect(400, 730, 120, 60))
        self.cleanResult1.setGeometry(QtCore.QRect(1090, 730, 120, 60))

        self.upload.setGeometry(QtCore.QRect(70, 730, 120, 60))
        self.submit2.setGeometry(QtCore.QRect(260, 730, 120, 60))
        self.clean2.setGeometry(QtCore.QRect(460, 730, 120, 60))
        self.cleanResult2.setGeometry(QtCore.QRect(1090, 730, 120, 60))

        self.NewsText1_div.setStyleSheet("QWidget{border-radius: 20px;background-color:white}")
        self.result1_div.setStyleSheet("QWidget{border-radius: 20px;background-color:white}")

        self.retranslateUi()
        self.connectSlot()

    def retranslateUi(self):
        self.singleNewsBtn.setText("单条新闻分类")
        self.multiNewsBtn.setText("批量新闻分类")
        self.label.setText("输入新闻")
        self.label_2.setText("分类结果")

        self.submit.setText("提交")
        self.clean.setText("清空")
        self.cleanResult1.setText("清空")

        self.label_3.setText("输入新闻")
        self.label_4.setText("分类结果")

        self.upload.setText("上传")
        self.submit2.setText("提交")
        self.clean2.setText("清空")
        self.cleanResult2.setText("清空")

    def connectSlot(self):

        self.submit.clicked.connect(lambda: self.predict2())
        self.submit2.clicked.connect(lambda: self.predict3())
        self.clean.clicked.connect(lambda: self.clean1())
        self.cleanResult1.clicked.connect(lambda: self.clean_2())
        self.clean2.clicked.connect(lambda: self.clean3())
        self.cleanResult2.clicked.connect(lambda: self.clean4())
        self.upload.clicked.connect(lambda: self.onOpenFile())
        self.multiNewsBtn.clicked.connect(lambda: self.changeMode())
        self.singleNewsBtn.clicked.connect(lambda: self.changeMode2())

    def changeMode(self):
        self.SingleNewsClassify.hide()
        self.MultiNewsClassify.show()
        NotificationWindow.success('提示', '进入批量模式', callback=callback)

    def changeMode2(self):
        self.SingleNewsClassify.show()
        self.MultiNewsClassify.hide()
        NotificationWindow.success('提示', '进入单条模式', callback=callback)

    def predict2(self):
        NotificationWindow.success('提示', '提交成功', callback=callback)
        NotificationWindow.info('提示', '正在分析...', callback=callback)
        print("开始单条新闻分析...")
        news = self.NewsText1.toPlainText()
        result = predict.main(news)
        NotificationWindow.success('提示', '分析完毕', callback=callback)
        self.result1.setPlainText(str(result))

    def predict3(self):
        print("开始批量新闻分析...")
        NotificationWindow.success('提示', '提交成功', callback=callback)
        NotificationWindow.info('提示', '正在分析...', callback=callback)
        # NotificationWindow.info('提示', '数据读取中...', callback=callback)
        print("读取数据"+str(self.path))
        df = pd.read_excel(str(self.path), engine='openpyxl')
        # df = pd.read_excel(self.path, usecols=[0], dtype=str)
        print(df)
        x = df['title'].values + '。' + df['content']
        print("\n转存数据")
        for i in x:
            print(i)

        print("开始分析...")
        result = predict.main2(x)
        NotificationWindow.success('提示', '分析完毕', callback=callback)
        print("打印结果...")
        for i in result:
            print(i)
        result = pd.DataFrame({'类别': result})
        # print(str(self.path))
        # self.showUploadNews.clear()
        # self.showUploadNews.close()
        # work = pd.ExcelWriter(str(self.path))
        result.to_excel("./result.xlsx", sheet_name='result', index=None)
        # work.save()header=None
        NotificationWindow.success('提示', '结果已保存到result.xlsx', callback=callback)
        NotificationWindow.info('提示', '结果打开中...', callback=callback)
        print("结果已保存到:result.xlsx")
        basedir = os.path.abspath(os.path.dirname(__file__))
        self.openOffice2(os.path.join(basedir,"result.xlsx"), 'Excel.Application')
        NotificationWindow.success('提示', '结果读取完毕', callback=callback)
        self.refresh()

    def clean1(self):
        self.NewsText1.setPlainText("")
        NotificationWindow.success('提示', '已清空', callback=callback)

    def clean_2(self):
        self.result1.setPlainText("")
        NotificationWindow.success('提示', '已清空', callback=callback)

    def clean3(self):
        self.showUploadNews.clear()
        NotificationWindow.success('提示', '已清空', callback=callback)
        self.refresh()

    def clean4(self):
        self.result2.clear()
        NotificationWindow.success('提示', '已清空', callback=callback)
        self.refresh()

    def refresh(self):
        self.singleNewsBtn.click()
        self.multiNewsBtn.click()

    def onOpenFile(self):
        NotificationWindow.info('提示', '文件读取中...', callback=callback)
        path, _ = QFileDialog.getOpenFileName(
            self, '请选择文件', '', 'excel(*.xlsx *.xls);;word(*.docx *.doc);;pdf(*.pdf)')
        self.path = path
        print("上传文件"+path)
        if not path:
            return
        if _.find('*.doc'):
            return self.openOffice(path, 'Word.Application')
        if _.find('*.xlsx'):
            return self.openOffice(path, 'Excel.Application')
        if _.find('*.pdf'):
            return self.openPdf(path)
        if _.find('*'):
            return self.openPdf(path)

    def openOffice(self, path, appName):
        NotificationWindow.success('提示', '正在上传...', callback=callback)
        self.showUploadNews.clear()
        # if not self.showUploadNews.setControl(appName):
        #     return QMessageBox.critical(self, '错误', '没有安装  %s' % appName)
        # self.showUploadNews.dynamicCall(
        #     'SetVisible (bool Visible)', 'False')  # 不显示窗体
        # self.showUploadNews.setProperty('DisplayAlerts', False)
        self.showUploadNews.setControl(path)
        NotificationWindow.success('提示', '上传成功', callback=callback)

    def openOffice2(self, path, appName):
        self.result2.clear()
        # if not self.result2.setControl(appName):
        #     return QMessageBox.critical(self, '错误', '没有安装  %s' % appName)
        # self.result2.dynamicCall(
        #     'SetVisible (bool Visible)', 'False')  # 不显示窗体
        # self.result2.setProperty('DisplayAlerts', False)
        self.result2.setControl(path)

    def openPdf(self, path):
        self.showUploadNews.clear()
        if not self.showUploadNews.setControl('Adobe PDF Reader'):
            return QMessageBox.critical(self, '错误', '没有安装 Adobe PDF Reader')
        self.showUploadNews.dynamicCall('LoadFile(const QString&)', path)

    def closeEvent(self, event):
        self.showUploadNews.close()
        self.showUploadNews.clear()
        self.result2.close()
        self.result2.clear()
        del self.showUploadNews
        del self.result2
        super(CircleLineWindow, self).closeEvent(event)

    def init(self):
        points.clear()
        # 链接的最小距离
        self.linkDist = min(self.screenWidth, self.screenHeight) / 2.4
        # 初始化点
        for _ in range(maxCircles * 3):
            points.append(Circle('', self.screenWidth, self.screenHeight))
        self.update()

    def showEvent(self, event):
        super(CircleLineWindow, self).showEvent(event)
        self._canDraw = True

    def hideEvent(self, event):
        super(CircleLineWindow, self).hideEvent(event)
        # 窗口最小化要停止绘制, 减少cpu占用
        self._canDraw = False

    def paintEvent(self, event):
        super(CircleLineWindow, self).paintEvent(event)
        if not self._canDraw:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        self.draw(painter)

    def draw(self, painter):
        # if circlePulse:
        #     if circleExp < circleExpMin or circleExp > circleExpMax:
        #         circleExpSp *= -1
        #     circleExp += circleExpSp

        painter.translate(self.screenWidth / 2, self.screenHeight / 2)

        if self._firstDraw:
            t = time()
        self.renderPoints(painter, points)
        if self._firstDraw:
            self._firstDraw = False
            # 此处有个比例关系用于设置timer的时间，如果初始窗口很小，没有比例会导致动画很快
            t = (time() - t) * 1000 * 2
            # 比例最大不能超过1920/800
            t = int(min(2.4, self.screenHeight / self.height()) * t) - 1
            t = t if t > 15 else 15  # 不能小于15s
            print('start timer(%d msec)' % t)
            # 开启定时器
            self._timer.start(t)

    def drawCircle(self, painter, circle):
        #         circle.radius *= circleExp
        if circle.background:
            circle.radius *= circleExp
        else:
            circle.radius /= circleExp
        radius = circle.radius

        r = radius * circleExp
        # 边框颜色设置透明度
        c = QColor(circle.borderColor)
        c.setAlphaF(circle.opacity)

        painter.save()
        if circle.filled == 'full':
            # 设置背景刷
            painter.setBrush(c)
            painter.setPen(Qt.NoPen)
        else:
            # 设置画笔
            painter.setPen(
                QPen(c, max(1, circleBorder * (radMin - circle.radius) / (radMin - radMax))))

        # 画实心圆或者圆圈
        painter.drawEllipse(circle.x - r, circle.y - r, 2 * r, 2 * r)
        painter.restore()

        if circle.filled == 'concentric':
            r = radius / 2
            # 画圆圈
            painter.save()
            painter.setBrush(Qt.NoBrush)
            painter.setPen(
                QPen(c, max(1, circleBorder * (radMin - circle.radius) / (radMin - radMax))))
            painter.drawEllipse(circle.x - r, circle.y - r, 2 * r, 2 * r)
            painter.restore()

        circle.x += circle.speedx
        circle.y += circle.speedy
        if (circle.opacity < maxOpacity):
            circle.opacity += 0.01
        circle.ttl -= 1

    def renderPoints(self, painter, circles):
        for i, circle in enumerate(circles):
            if circle.ttl < -20:
                # 重新初始化一个
                circle = Circle('', self.screenWidth, self.screenHeight)
                circles[i] = circle
            self.drawCircle(painter, circle)

        circles_len = len(circles)
        for i in range(circles_len - 1):
            for j in range(i + 1, circles_len):
                deltax = circles[i].x - circles[j].x
                deltay = circles[i].y - circles[j].y
                dist = pow(pow(deltax, 2) + pow(deltay, 2), 0.5)
                # if the circles are overlapping, no laser connecting them
                if dist <= circles[i].radius + circles[j].radius:
                    continue
                # otherwise we connect them only if the dist is < linkDist
                if dist < self.linkDist:
                    xi = (1 if circles[i].x < circles[j].x else -
                          1) * abs(circles[i].radius * deltax / dist)
                    yi = (1 if circles[i].y < circles[j].y else -
                          1) * abs(circles[i].radius * deltay / dist)
                    xj = (-1 if circles[i].x < circles[j].x else 1) * \
                        abs(circles[j].radius * deltax / dist)
                    yj = (-1 if circles[i].y < circles[j].y else 1) * \
                        abs(circles[j].radius * deltay / dist)
                    path = QPainterPath()
                    path.moveTo(circles[i].x + xi, circles[i].y + yi)
                    path.lineTo(circles[j].x + xj, circles[j].y + yj)
#                     samecolor = circles[i].color == circles[j].color
                    c = QColor(circles[i].borderColor)
                    c.setAlphaF(min(circles[i].opacity, circles[j].opacity)
                                * ((self.linkDist - dist) / self.linkDist))
                    painter.setPen(QPen(c, (
                        lineBorder * backgroundMlt if circles[i].background else lineBorder) * (
                        (self.linkDist - dist) / self.linkDist)))
                    painter.drawPath(path)


class NotificationIcon:

    Info, Success, Warning, Error, Close = range(5)
    Types = {
        Info: None,
        Success: None,
        Warning: None,
        Error: None,
        Close: None
    }

    @classmethod
    def init(cls):
        cls.Types[cls.Info] = QPixmap(QImage.fromData(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAC5ElEQVRYR8VX0VHbQBB9e/bkN3QQU0FMBSEVYFcQ8xPBJLJ1FWAqOMcaxogfTAWQCiAVRKkgTgfmM4zRZu6QhGzL0p0nDPr17e7bt7tv14RX/uiV48MJgAon+8TiAMRtMFogaqUJxADPwRRzg67kl8+xbWJWANR40iPQSSFgtX/mGQkaDr56V3VAKgGos4s2JXwJoF3naMPvMS+SrpTHs032GwGkdF+DsFMVnJm/oyGGeHico0EjIjpYes+YMyVd6R/flfkpBWCCQ9zaZM2LZDfLMGXsZ5kdI/lYBmINgHHyyLd1mWdBbAFAM/GY7K2WYx1AeB4T6L1N9umbGxZ0qktATaEAdCps48D39oq/LwEw3U5CN92LfczJoewfT7MAywDCaEbAuxeLrh0zz4L+0e4aAJfGy+sP3IMxlH1vpMJoSMCJDXgWtJeJVc6ACs9HBBrYODCJAFdYvAmkPJxnNqMwYht7Bn+T/lGg3z4DGEd3RPhQ54DBvwAOVkeqagRXfTLjh+x7+8sALOtfHLuiYzWOAiLoKbD58mnIGbCmLxUepS6NQmYlUGE0JeCTTXT9JvA9E9sZgO5iIpoyc6/YzcqSwQzgGgBXB7oXpH9klpRSkxY1xW/b7Iu2zk34PILPnazCqEPAtTWA8iZ0HsOu9L0bw4DzCJeNocMGNDpQ3IKO+6NUiJ4ysZNiBv5I3zPnmJmG5oM+wbS+9+qkvGi7NAXGmeUy0ioofa+XA0jH0UaMKpdRWs/adcwMqfV/tenqpqHY/Znt+j2gJi00RUzA201dXaxh9iZdZloJS+9H1otrkbRrD5InFqpPskxEshJQ468CkSmJC+i1HigaaxCAuCljgoDhwPdOjf7rFVxxuJrMkXScjtKc1rOLNpJk6nii5XmYzbngzlZn+RIb40kPJPTBYXUt6VEDJ8Pi6bWpNFb/jFYY6YGpDeKdjBmTKdMcxDGEmP73v2a2Gr/NOycGtglQZ/MPzEqCMLGckJEAAAAASUVORK5CYII=')))
        cls.Types[cls.Success] = QPixmap(QImage.fromData(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACZUlEQVRYR8VXS3LTQBDtVsDbcAPMCbB3limkcAKSG4QFdnaYE2BOQLKzxSLJCeAGSUQheSnfwLmB2VJhXmpExpFHI2sk2RWv5FJPv9evP9NieuIfPzE+VSJw8qt3IMDvmahDoDYxt2UAACXMWIIowR5ffn8TJbaBWRE4CXvHAH9RgKXOgQUI48CfXZbZbiTw8Xe/w3d0zkydMkem91IZpyWOJu5sUXS+kEAqt3B+MNOLOuDqDEBLxxFHk7eza5MfIwEJDjhXTYD1s8zinYlEjsCD7FdNI9cJpEq0RFdPR47AMOzLCn69zegz6UgCP+pmfa8RSKudnPNdgCufTOLDxJtdPP7PoA1Cd8HEL5sSUCCD0B0x8bc1f8Bi6sevcgS2VXh6hMOwDz0gsUddNaxWKRjeuKfE/KlJ9Dq4UYH/o/Ns6scj+bgiMAjdayb26xLQwTfVEwg3gRcf6ARq578KuLo7VDc8psCQqwfjr4EfjYvkrAquFJ56UYpdSkAZSmNd1rrg0leOQFELgvA58OJTxVyRaAJORPOpF6UXnFUR5sDiXjs7UqsOMGMRlrWhTkJXpFL3mNrQZhA1lH3F0TiI5FurUQyMpn58VjhkSqQA4Tbw4nSVW6sBU5VXktXSeONlJH3s8jrOVr9RgVSFuNcWfzlh5n3LoKzMAPxxWuiULiQpiR2sZNnCyzIuWUr5Z1Ml0sgdHFZaShVDuR86/0huL3VXtDk/F4e11vKsTHLSCeKx7bYkW80hjLOrV1GhWH0ZrSlyh2MwdZhYfi8oZeYgLBmUiGd8sfVPM6syr2lUSYGaGBuP3QN6rVUwYV/egwAAAABJRU5ErkJggg==')))
        cls.Types[cls.Warning] = QPixmap(QImage.fromData(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACmElEQVRYR8VXTW7TUBD+xjYSXZFukOIsSE9AskNJJMoJmq4r7OYEwAkabhBOkB/Emt4gVIojdpgbpIumEitX6gKB7UHPkauXxLHfc4F6Z3l+vvnmm/fGhAd+6IHzQwvA9cfOITMfAdQAcx1EdVEAM/tEFADsWyaPn57MfdXClABcT1qnzHSWJiwMzrwgoF91vXGRbS6AH59ajd8hDYmoURQo67tgxoij42rv62KX/04Agu44xmciVMokT32YERgGjquvZ1+y4mQCWPUa0/sk3vQlwqssEFsAVrQbU4XKL/ai2+5PPK6waQ4AOsoDnDARh83NdmwBuJq0fQI9L6p+L7rd3+/5gbAToMPI+FbkIzRRc72mbLcGIFE7jGFRIPHddmZrvstJh1X8CHGv6sxHqe1GkPYCoGcqgcoCAPPCdr2DLQC6wqMoPEj7qdqCNKllxs30sLpjYDluDUDGG5XqhY2sal3w4PiD7c7fJnHShMtJR8zpy/8CALiwndnhBgD1/t+XAXkaZAaUVHwnHulg0W6BNEWlAQD8zna8gQB0Ne70iXCm2j55jCUAei1gxvuaO+uXAcDg7zXHSy640iKUAehOEDJFqDmGQkiPLO5Fv+KADXOqvCuIsrPGsIyQdHou22YeRMJgOdHTQTkAfGk7XrLKrWlAvOhcRgBfWiZ3RQti0zxXuUFXCXMuo0TRitfxugjbIxC5RYzI6s9kIGFh+KLOpiW22id5AUuI8IaisFG4kCQg/sFKJgtPLix3KWXGeRETRbQDuCFCV2spTYMm+2FEI1WBbYIRPTeiqFtqLZeDraaD+qrbkpgQAvfl1WsXU0p/RjIjYYhTkNFgcCVlRlRKoAAc+5aF0V//NVPoc2kTLQZKZ8lx/AMXBmMwuXUwOAAAAABJRU5ErkJggg==')))
        cls.Types[cls.Error] = QPixmap(QImage.fromData(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACrklEQVRYR82XW27aQBSG/4PtiNhIpStouoImKwjZAV1B07coWCpZQcgK6kh2lLeSFZSsIOwgdAdkBaUSEBQDpxpjU9vM+EJR03nDzJz/mzm3GcIrD3plfZQCeD47O1ho2jERNRmoE9AQG2BgBGBAwIiZe5Zh3JPjiG+5oxCAEF5q2iWITnMtRhOYu5XF4mr/9naYtSYXYGLbHQCXhYVTEwlom657rVqvBOB2uz71/a+ldq1SYe6ahnEhc4sSYGzbfQKOt915eh0D/ZrrnqS/SwEmrVYXRJ92Jb4OC+C65rrtuN0NgIltNwF837V4zN5Hy3V70e9NgFZrCKJ3CQDmJ9MwDsW36XzeB/AhA/CHqeuN2WxWX2paX2JraHneeynA+Pz8lCqVbxLjV5brimxAEJxqiEA8CjZVBvFy+bl2c9MV9hInoAw85qFpGEeRYQVEQjzMokcQHWxsiPne8jzh6j8AodGfyqNlHpiGcaKAkIk/gChwm2yYuv5W2FqfwLNtN5bAQ2bwySB83zENo50A8/1McaFRAU72XVek+mpk+D/JlIKI/xkee654uCbIhjVAqZIrgSgpLhiCwN4OAEj4vEB2yDybBCjsAol4ZD0nRdMQSRcUCsKUeNSw4o2mKMRGEOamoVx8FXDZKVosDYNMUHXAsBRnppo8RQcbpTgIGEkhykpFjnWxzGhPQYxt2yHgS/oIlKVYTJxImpG482nz+VG1Wh1N84pMCCGa0ULXHwmoJwCYnyzPW5fn/68dh7EgPbrMMl3gz7gro+n/7EoWD7w4a96l1NnJ1Yz5Lt6wCgFEk0r1CIkbiPnC9DxH5aHcd4FYGD5MOqVOg/muslh0/vphkm63k5eXZvA0I6qD+ZCI3jDzLxANiHn1NNvb6+30aVYgwLeeUsgFW1svsPA3Ncq4MHzVeO8AAAAASUVORK5CYII=')))
        cls.Types[cls.Close] = QPixmap(QImage.fromData(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAeElEQVQ4T2NkoBAwUqifgboGzJy76AIjE3NCWmL0BWwumzV/qcH/f38XpCfHGcDkUVwAUsDw9+8GBmbmAHRDcMlheAGbQnwGYw0DZA1gp+JwFUgKZyDCDQGpwuIlrGGAHHAUGUCRFygKRIqjkeKERE6+oG5eIMcFAOqSchGwiKKAAAAAAElFTkSuQmCC')))

    @classmethod
    def icon(cls, ntype):
        return cls.Types.get(ntype)


class NotificationItem(QWidget):

    closed = pyqtSignal(QListWidgetItem)

    def __init__(self, title, message, item, *args, ntype=0, callback=None, **kwargs):
        super(NotificationItem, self).__init__(*args, **kwargs)
        self.item = item
        self.callback = callback
        layout = QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.bgWidget = QWidget(self)  # 背景控件, 用于支持动画效果
        layout.addWidget(self.bgWidget)

        layout = QGridLayout(self.bgWidget)
        layout.setHorizontalSpacing(15)
        layout.setVerticalSpacing(10)

        # 标题左边图标
        layout.addWidget(
            QLabel(self, pixmap=NotificationIcon.icon(ntype)), 0, 0)

        # 标题
        self.labelTitle = QLabel(title, self)
        font = self.labelTitle.font()
        font.setBold(True)
        font.setPixelSize(22)
        self.labelTitle.setFont(font)

        # 关闭按钮
        self.labelClose = QLabel(self, cursor=Qt.PointingHandCursor, pixmap=NotificationIcon.icon(NotificationIcon.Close))

        # 消息内容
        self.labelMessage = QLabel(message, self, cursor=Qt.PointingHandCursor, wordWrap=True, alignment=Qt.AlignLeft | Qt.AlignTop)
        font = self.labelMessage.font()
        font.setPixelSize(20)
        self.labelMessage.setFont(font)
        self.labelMessage.adjustSize()

        # 添加到布局
        layout.addWidget(self.labelTitle, 0, 1)
        layout.addItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 0, 2)
        layout.addWidget(self.labelClose, 0, 3)
        layout.addWidget(self.labelMessage, 1, 1, 1, 2)

        # 边框阴影
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(12)
        effect.setColor(QColor(0, 0, 0, 25))
        effect.setOffset(0, 2)
        self.setGraphicsEffect(effect)

        self.adjustSize()

        # 5秒自动关闭
        self._timer = QTimer(self, timeout=self.doClose)
        self._timer.setSingleShot(True)  # 只触发一次
        self._timer.start(3000)

    def doClose(self):
        try:
            # 可能由于手动点击导致item已经被删除了
            self.closed.emit(self.item)
        except:
            pass

    def showAnimation(self, width):
        # 显示动画
        pass

    def closeAnimation(self):
        # 关闭动画
        pass

    def mousePressEvent(self, event):
        super(NotificationItem, self).mousePressEvent(event)
        w = self.childAt(event.pos())
        if not w:
            return
        if w == self.labelClose:  # 点击关闭图标
            # 先尝试停止计时器
            self._timer.stop()
            self.closed.emit(self.item)
        elif w == self.labelMessage and self.callback and callable(self.callback):
            # 点击消息内容
            self._timer.stop()
            self.closed.emit(self.item)
            self.callback()  # 回调

    def paintEvent(self, event):
        # 圆角以及背景色
        super(NotificationItem, self).paintEvent(event)
        painter = QPainter(self)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 6, 6)
        painter.fillPath(path, Qt.white)


class NotificationWindow(QListWidget):

    _instance = None

    def __init__(self, *args, **kwargs):
        super(NotificationWindow, self).__init__(*args, **kwargs)
        self.setSpacing(20)
        self.setMinimumWidth(500)
        self.setMaximumWidth(500)
        QApplication.instance().setQuitOnLastWindowClosed(True)
        # 隐藏任务栏,无边框,置顶等
        self.setWindowFlags(self.windowFlags() | Qt.Tool |
                            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # 去掉窗口边框
        self.setFrameShape(self.NoFrame)
        # 背景透明
        self.viewport().setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 不显示滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 获取屏幕高宽
        rect = QApplication.instance().desktop().availableGeometry(self)
        self.setMinimumHeight(rect.height())
        self.setMaximumHeight(rect.height())
        self.move(rect.width() - self.minimumWidth() - 18, 0)

    def removeItem(self, item):
        # 删除item
        w = self.itemWidget(item)
        self.removeItemWidget(item)
        item = self.takeItem(self.indexFromItem(item).row())
        w.close()
        w.deleteLater()
        del item

    @classmethod
    def _createInstance(cls):
        # 创建实例
        if not cls._instance:
            cls._instance = NotificationWindow()
            cls._instance.show()
            NotificationIcon.init()

    @classmethod
    def info(cls, title, message, callback=None):
        cls._createInstance()
        item = QListWidgetItem(cls._instance)
        w = NotificationItem(title, message, item, cls._instance,
                             ntype=NotificationIcon.Info, callback=callback)
        w.closed.connect(cls._instance.removeItem)
        item.setSizeHint(QSize(cls._instance.width() -
                               cls._instance.spacing(), w.height()))
        cls._instance.setItemWidget(item, w)

    @classmethod
    def success(cls, title, message, callback=None):
        cls._createInstance()
        item = QListWidgetItem(cls._instance)
        w = NotificationItem(title, message, item, cls._instance,
                             ntype=NotificationIcon.Success, callback=callback)
        w.closed.connect(cls._instance.removeItem)
        item.setSizeHint(QSize(cls._instance.width() -
                               cls._instance.spacing(), w.height()))
        cls._instance.setItemWidget(item, w)

    @classmethod
    def warning(cls, title, message, callback=None):
        cls._createInstance()
        item = QListWidgetItem(cls._instance)
        w = NotificationItem(title, message, item, cls._instance,
                             ntype=NotificationIcon.Warning, callback=callback)
        w.closed.connect(cls._instance.removeItem)
        item.setSizeHint(QSize(cls._instance.width() -
                               cls._instance.spacing(), w.height()))
        cls._instance.setItemWidget(item, w)

    @classmethod
    def error(cls, title, message, callback=None):
        cls._createInstance()
        item = QListWidgetItem(cls._instance)
        w = NotificationItem(title, message, item,
                             ntype=NotificationIcon.Error, callback=callback)
        w.closed.connect(cls._instance.removeItem)
        width = cls._instance.width() - cls._instance.spacing()
        item.setSizeHint(QSize(width, w.height()))
        cls._instance.setItemWidget(item, w)


if __name__ == '__main__':
    import sys

    # import cgitb
    # sys.excepthook = cgitb.Hook(1, None, 5, sys.stderr, 'text')
    app = QApplication(sys.argv)

    # 启动动画
    # splash = GifSplashScreen()
    # splash.show()

    # 创建显示窗口
    w = CircleLineWindow()
    w.resize(1500, 850)
    w.setWindowTitle("NewsClassify")
    w.setWindowIcon(QIcon("assets/img/baidu.ico"))
    w.show()
    sys.exit(app.exec_())
