# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainmnTFUz.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(480, 800)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(480, 800))
        MainWindow.setMaximumSize(QSize(480, 800))
        icon = QIcon()
        icon.addFile(u":/title/free-icon-tuna-605314.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMinimumSize(QSize(0, 0))
        self.centralwidget.setMaximumSize(QSize(800, 1280))
        self.OnOff_button = QPushButton(self.centralwidget)
        self.OnOff_button.setObjectName(u"OnOff_button")
        self.OnOff_button.setGeometry(QRect(10, 20, 101, 51))
        self.OnOff_button.setAutoFillBackground(False)
        self.OnOff_button.setStyleSheet(u"QPushButton {\n"
"    background-color: white; \n"
"}\n"
"QPushButton:checked {\n"
"    background-color: white;\n"
"}\n"
"")
        icon1 = QIcon()
        icon1.addFile(u":/button/free-icon-switch-off-889758 (1).png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon1.addFile(u":/button/free-icon-switch-on-889754.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.OnOff_button.setIcon(icon1)
        self.OnOff_button.setIconSize(QSize(80, 90))
        self.OnOff_button.setCheckable(True)
        self.OnOff_button.setChecked(True)
        self.OnOff_button.setAutoDefault(False)
        self.OnOff_button.setFlat(True)
        self.background = QLabel(self.centralwidget)
        self.background.setObjectName(u"background")
        self.background.setGeometry(QRect(-210, -63, 1080, 1920))
        self.background.setMinimumSize(QSize(1080, 1920))
        self.background.setMaximumSize(QSize(1080, 1920))
        self.background.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.background.setAutoFillBackground(False)
        self.background.setStyleSheet(u"background-color: white\n"
"\n"
"")
        self.background.setFrameShape(QFrame.Shape.Box)
        self.background.setLineWidth(20)
        self.background.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse)
        self.weather_label = QLabel(self.centralwidget)
        self.weather_label.setObjectName(u"weather_label")
        self.weather_label.setGeometry(QRect(10, 90, 461, 151))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.weather_label.sizePolicy().hasHeightForWidth())
        self.weather_label.setSizePolicy(sizePolicy1)
        self.weather_label.setStyleSheet(u"background-color: rgb(211, 211, 255);\n"
"border-radius: 20px;\n"
"color:black;")
        self.weather_label.setFrameShape(QFrame.Shape.NoFrame)
        self.weather_label.setLineWidth(20)
        self.schedule_label = QLabel(self.centralwidget)
        self.schedule_label.setObjectName(u"schedule_label")
        self.schedule_label.setGeometry(QRect(10, 250, 461, 411))
        self.schedule_label.setStyleSheet(u"background-color:rgb(211, 248, 255);\n"
"border-radius: 20px;\n"
"color:black;")
        self.schedule_label.setFrameShape(QFrame.Shape.NoFrame)
        self.schedule_label.setLineWidth(20)
        self.custom_label = QLabel(self.centralwidget)
        self.custom_label.setObjectName(u"custom_label")
        self.custom_label.setGeometry(QRect(10, 670, 461, 81))
        self.custom_label.setStyleSheet(u"background-color:rgb(255, 251, 210);\n"
"border-radius: 20px;\n"
"color:black;\n"
"")
        self.custom_label.setFrameShape(QFrame.Shape.NoFrame)
        self.custom_label.setLineWidth(20)
        self.profile1_button = QPushButton(self.centralwidget)
        self.profile1_button.setObjectName(u"profile1_button")
        self.profile1_button.setGeometry(QRect(415, 15, 51, 51))
        self.profile1_button.setStyleSheet(u"background-color:white;")
        icon2 = QIcon()
        icon2.addFile(u":/profile/free-icon-user-848006.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.profile1_button.setIcon(icon2)
        self.profile1_button.setIconSize(QSize(40, 50))
        self.profile1_name = QLabel(self.centralwidget)
        self.profile1_name.setObjectName(u"profile1_name")
        self.profile1_name.setGeometry(QRect(415, 60, 51, 16))
        self.profile1_name.setStyleSheet(u"color:black;\n"
"font: 9pt \"\ubb38\uacbd \uac10\ud64d\uc0ac\uacfc\";")
        self.profile1_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile2_name = QLabel(self.centralwidget)
        self.profile2_name.setObjectName(u"profile2_name")
        self.profile2_name.setGeometry(QRect(360, 60, 51, 16))
        self.profile2_name.setStyleSheet(u"color:black;\n"
"font: 9pt \"\ubb38\uacbd \uac10\ud64d\uc0ac\uacfc\";\n"
"")
        self.profile2_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile2_button = QPushButton(self.centralwidget)
        self.profile2_button.setObjectName(u"profile2_button")
        self.profile2_button.setGeometry(QRect(360, 15, 51, 51))
        self.profile2_button.setStyleSheet(u"background-color:white;")
        self.profile2_button.setIcon(icon2)
        self.profile2_button.setIconSize(QSize(40, 50))
        self.profile3_name = QLabel(self.centralwidget)
        self.profile3_name.setObjectName(u"profile3_name")
        self.profile3_name.setGeometry(QRect(300, 60, 51, 16))
        self.profile3_name.setStyleSheet(u"color:black;\n"
"font: 9pt \"\ubb38\uacbd \uac10\ud64d\uc0ac\uacfc\";")
        self.profile3_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile3_button = QPushButton(self.centralwidget)
        self.profile3_button.setObjectName(u"profile3_button")
        self.profile3_button.setGeometry(QRect(300, 15, 51, 51))
        self.profile3_button.setStyleSheet(u"background-color:white;")
        self.profile3_button.setIcon(icon2)
        self.profile3_button.setIconSize(QSize(40, 50))
        self.profile4_name = QLabel(self.centralwidget)
        self.profile4_name.setObjectName(u"profile4_name")
        self.profile4_name.setEnabled(False)
        self.profile4_name.setGeometry(QRect(240, 60, 51, 16))
        self.profile4_name.setStyleSheet(u"color:black;\n"
"font: 9pt \"\ubb38\uacbd \uac10\ud64d\uc0ac\uacfc\";\n"
"")
        self.profile4_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile4_button = QPushButton(self.centralwidget)
        self.profile4_button.setObjectName(u"profile4_button")
        self.profile4_button.setEnabled(True)
        self.profile4_button.setGeometry(QRect(240, 15, 51, 51))
        self.profile4_button.setStyleSheet(u"background-color:white;")
        self.profile4_button.setIcon(icon2)
        self.profile4_button.setIconSize(QSize(40, 50))
        self.profile4_button.setAutoDefault(False)
        self.profile4_button.setFlat(False)
        self.AMADDA = QLabel(self.centralwidget)
        self.AMADDA.setObjectName(u"AMADDA")
        self.AMADDA.setGeometry(QRect(170, 760, 151, 41))
        self.AMADDA.setStyleSheet(u"color:black;\n"
"font: 20pt \"Bradley Hand ITC\";")
        self.AMADDA.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rain_image = QLabel(self.centralwidget)
        self.rain_image.setObjectName(u"rain_image")
        self.rain_image.setGeometry(QRect(170, 110, 31, 31))
        self.rain_image.setPixmap(QPixmap(u":/weather/free-icon-rain-15580411.png"))
        self.rain_image.setScaledContents(True)
        self.uv_image = QLabel(self.centralwidget)
        self.uv_image.setObjectName(u"uv_image")
        self.uv_image.setGeometry(QRect(170, 150, 31, 31))
        self.uv_image.setPixmap(QPixmap(u":/weather/free-icon-uv-protection-7646168.png"))
        self.uv_image.setScaledContents(True)
        self.dust_image = QLabel(self.centralwidget)
        self.dust_image.setObjectName(u"dust_image")
        self.dust_image.setGeometry(QRect(170, 190, 31, 31))
        self.dust_image.setPixmap(QPixmap(u":/weather/free-icon-dust-4383809.png"))
        self.dust_image.setScaledContents(True)
        self.weather_sub_label_2 = QLabel(self.centralwidget)
        self.weather_sub_label_2.setObjectName(u"weather_sub_label_2")
        self.weather_sub_label_2.setGeometry(QRect(160, 100, 181, 131))
        self.weather_sub_label_2.setStyleSheet(u"background-color: rgb(242, 243, 255);\n"
"border-radius: 20px;\n"
"color:black;")
        self.weather_sub_label_2.setFrameShape(QFrame.Shape.NoFrame)
        self.weather_sub_label_2.setLineWidth(20)
        self.weather_sub_label_4 = QLabel(self.centralwidget)
        self.weather_sub_label_4.setObjectName(u"weather_sub_label_4")
        self.weather_sub_label_4.setGeometry(QRect(350, 130, 111, 101))
        self.weather_sub_label_4.setStyleSheet(u"background-color: rgb(242, 243, 255);\n"
"border-radius: 20px;\n"
"color:black;")
        self.weather_sub_label_4.setFrameShape(QFrame.Shape.NoFrame)
        self.weather_sub_label_4.setLineWidth(20)
        self.weather_sub_label_1 = QLabel(self.centralwidget)
        self.weather_sub_label_1.setObjectName(u"weather_sub_label_1")
        self.weather_sub_label_1.setGeometry(QRect(20, 100, 131, 131))
        self.weather_sub_label_1.setStyleSheet(u"background-color: rgb(242, 243, 255);\n"
"border-radius: 20px;\n"
"color:black;")
        self.weather_sub_label_1.setFrameShape(QFrame.Shape.NoFrame)
        self.weather_sub_label_1.setLineWidth(20)
        self.weather_image = QLabel(self.centralwidget)
        self.weather_image.setObjectName(u"weather_image")
        self.weather_image.setGeometry(QRect(50, 120, 61, 61))
        self.weather_image.setPixmap(QPixmap(u":/weather/free-icon-cloudy-1163763.png"))
        self.weather_image.setScaledContents(True)
        self.temp_humid = QLabel(self.centralwidget)
        self.temp_humid.setObjectName(u"temp_humid")
        self.temp_humid.setGeometry(QRect(20, 190, 131, 21))
        self.temp_humid.setStyleSheet(u"color:black;\n"
"font: 7pt \"\ubb38\uacbd \uac10\ud64d\uc0ac\uacfc\";")
        self.temp_humid.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rain_probability = QLabel(self.centralwidget)
        self.rain_probability.setObjectName(u"rain_probability")
        self.rain_probability.setGeometry(QRect(210, 110, 131, 31))
        self.rain_probability.setStyleSheet(u"color:black;\n"
"font: 8pt \"\ubb38\uacbd \uac10\ud64d\uc0ac\uacfc\";")
        self.uv_level = QLabel(self.centralwidget)
        self.uv_level.setObjectName(u"uv_level")
        self.uv_level.setGeometry(QRect(210, 150, 131, 31))
        self.uv_level.setStyleSheet(u"color:black;\n"
"font: 8pt \"\ubb38\uacbd \uac10\ud64d\uc0ac\uacfc\";")
        self.dust_level = QLabel(self.centralwidget)
        self.dust_level.setObjectName(u"dust_level")
        self.dust_level.setGeometry(QRect(210, 195, 131, 21))
        self.dust_level.setStyleSheet(u"color:black;\n"
"font: 8pt \"\ubb38\uacbd \uac10\ud64d\uc0ac\uacfc\";")
        self.weather_item = QLabel(self.centralwidget)
        self.weather_item.setObjectName(u"weather_item")
        self.weather_item.setGeometry(QRect(360, 130, 91, 101))
        self.weather_item.setStyleSheet(u"color:rgb(85, 85, 255);\n"
"font: 700 10pt \"\ubb38\uacbd \uac10\ud64d\uc0ac\uacfc\";")
        self.weather_item.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.schedule_label_schedule = QLabel(self.centralwidget)
        self.schedule_label_schedule.setObjectName(u"schedule_label_schedule")
        self.schedule_label_schedule.setGeometry(QRect(20, 260, 261, 31))
        self.schedule_label_schedule.setStyleSheet(u"background-color: rgb(240, 255, 255);\n"
"border-radius: 15px;\n"
"color:black;")
        self.schedule_label_schedule.setFrameShape(QFrame.Shape.NoFrame)
        self.schedule_label_schedule.setLineWidth(20)
        self.schedule_label_item = QLabel(self.centralwidget)
        self.schedule_label_item.setObjectName(u"schedule_label_item")
        self.schedule_label_item.setGeometry(QRect(290, 260, 171, 31))
        self.schedule_label_item.setStyleSheet(u"background-color: rgb(240, 255, 255);\n"
"border-radius: 15px;\n"
"color:black;")
        self.schedule_label_item.setFrameShape(QFrame.Shape.NoFrame)
        self.schedule_label_item.setLineWidth(20)
        self.schedule_label_1_1 = QLabel(self.centralwidget)
        self.schedule_label_1_1.setObjectName(u"schedule_label_1_1")
        self.schedule_label_1_1.setGeometry(QRect(20, 300, 261, 111))
        self.schedule_label_1_1.setStyleSheet(u"background-color: rgb(240, 255, 255);\n"
"border-radius: 20px;\n"
"color:black;")
        self.schedule_label_1_1.setFrameShape(QFrame.Shape.NoFrame)
        self.schedule_label_1_1.setLineWidth(20)
        self.schedule_label_1_2 = QLabel(self.centralwidget)
        self.schedule_label_1_2.setObjectName(u"schedule_label_1_2")
        self.schedule_label_1_2.setGeometry(QRect(290, 300, 171, 111))
        self.schedule_label_1_2.setStyleSheet(u"background-color: rgb(240, 255, 255);\n"
"border-radius: 20px;\n"
"color:black;")
        self.schedule_label_1_2.setFrameShape(QFrame.Shape.NoFrame)
        self.schedule_label_1_2.setLineWidth(20)
        self.weather_sub_label_3 = QLabel(self.centralwidget)
        self.weather_sub_label_3.setObjectName(u"weather_sub_label_3")
        self.weather_sub_label_3.setGeometry(QRect(350, 100, 111, 21))
        self.weather_sub_label_3.setStyleSheet(u"background-color: rgb(242, 243, 255);\n"
"border-radius: 10px;\n"
"color:black;")
        self.weather_sub_label_3.setFrameShape(QFrame.Shape.NoFrame)
        self.weather_sub_label_3.setLineWidth(20)
        self.schedule_item_title = QLabel(self.centralwidget)
        self.schedule_item_title.setObjectName(u"schedule_item_title")
        self.schedule_item_title.setGeometry(QRect(320, 260, 111, 31))
        self.schedule_item_title.setStyleSheet(u"color:black;\n"
"font: 11pt \"\ubb38\uacbd \uac10\ud64d\uc0ac\uacfc\";")
        self.schedule_item_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.schedule_schedule_title = QLabel(self.centralwidget)
        self.schedule_schedule_title.setObjectName(u"schedule_schedule_title")
        self.schedule_schedule_title.setGeometry(QRect(60, 260, 181, 31))
        self.schedule_schedule_title.setStyleSheet(u"color:black;\n"
"font: 11pt \"\ubb38\uacbd \uac10\ud64d\uc0ac\uacfc\";")
        self.schedule_schedule_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.weather_item_title = QLabel(self.centralwidget)
        self.weather_item_title.setObjectName(u"weather_item_title")
        self.weather_item_title.setGeometry(QRect(360, 90, 91, 41))
        self.weather_item_title.setStyleSheet(u"color:black;\n"
"font: 11pt \"\ubb38\uacbd \uac10\ud64d\uc0ac\uacfc\";")
        self.weather_item_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.schedule_1 = QLabel(self.centralwidget)
        self.schedule_1.setObjectName(u"schedule_1")
        self.schedule_1.setGeometry(QRect(30, 340, 241, 41))
        font = QFont()
        font.setFamilies([u"\ubb38\uacbd \uac10\ud64d\uc0ac\uacfc"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStyleStrategy(QFont.PreferDefault)
        self.schedule_1.setFont(font)
        self.schedule_1.setStyleSheet(u"color:black;\n"
"font: 10pt \"\ubb38\uacbd \uac10\ud64d\uc0ac\uacfc\";")
        self.schedule_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.schedule_label_2_1 = QLabel(self.centralwidget)
        self.schedule_label_2_1.setObjectName(u"schedule_label_2_1")
        self.schedule_label_2_1.setGeometry(QRect(20, 420, 261, 111))
        self.schedule_label_2_1.setStyleSheet(u"background-color: rgb(240, 255, 255);\n"
"border-radius: 20px;\n"
"color:black;")
        self.schedule_label_2_1.setFrameShape(QFrame.Shape.NoFrame)
        self.schedule_label_2_1.setLineWidth(20)
        self.schedule_label_2_2 = QLabel(self.centralwidget)
        self.schedule_label_2_2.setObjectName(u"schedule_label_2_2")
        self.schedule_label_2_2.setGeometry(QRect(290, 420, 171, 111))
        self.schedule_label_2_2.setStyleSheet(u"background-color: rgb(240, 255, 255);\n"
"border-radius: 20px;\n"
"color:black;")
        self.schedule_label_2_2.setFrameShape(QFrame.Shape.NoFrame)
        self.schedule_label_2_2.setLineWidth(20)
        self.schedule_2_item = QLabel(self.centralwidget)
        self.schedule_2_item.setObjectName(u"schedule_2_item")
        self.schedule_2_item.setGeometry(QRect(310, 430, 131, 91))
        self.schedule_2_item.setStyleSheet(u"color:rgb(0, 170, 255);\n"
"font: 700 10pt \"\ubb38\uacbd \uac10\ud64d\uc0ac\uacfc\";")
        self.schedule_2_item.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.schedule_2 = QLabel(self.centralwidget)
        self.schedule_2.setObjectName(u"schedule_2")
        self.schedule_2.setGeometry(QRect(30, 460, 241, 41))
        self.schedule_2.setFont(font)
        self.schedule_2.setStyleSheet(u"color:black;\n"
"font: 10pt \"\ubb38\uacbd \uac10\ud64d\uc0ac\uacfc\";")
        self.schedule_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.schedule_label_3_1 = QLabel(self.centralwidget)
        self.schedule_label_3_1.setObjectName(u"schedule_label_3_1")
        self.schedule_label_3_1.setGeometry(QRect(20, 540, 261, 111))
        self.schedule_label_3_1.setStyleSheet(u"background-color: rgb(240, 255, 255);\n"
"border-radius: 20px;\n"
"color:black;")
        self.schedule_label_3_1.setFrameShape(QFrame.Shape.NoFrame)
        self.schedule_label_3_1.setLineWidth(20)
        self.schedule_label_3_2 = QLabel(self.centralwidget)
        self.schedule_label_3_2.setObjectName(u"schedule_label_3_2")
        self.schedule_label_3_2.setGeometry(QRect(290, 540, 171, 111))
        self.schedule_label_3_2.setStyleSheet(u"background-color: rgb(240, 255, 255);\n"
"border-radius: 20px;\n"
"color:black;")
        self.schedule_label_3_2.setFrameShape(QFrame.Shape.NoFrame)
        self.schedule_label_3_2.setLineWidth(20)
        self.schedule_3 = QLabel(self.centralwidget)
        self.schedule_3.setObjectName(u"schedule_3")
        self.schedule_3.setGeometry(QRect(30, 580, 241, 41))
        self.schedule_3.setFont(font)
        self.schedule_3.setStyleSheet(u"color:black;\n"
"font: 10pt \"\ubb38\uacbd \uac10\ud64d\uc0ac\uacfc\";")
        self.schedule_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.custom_sub_label = QLabel(self.centralwidget)
        self.custom_sub_label.setObjectName(u"custom_sub_label")
        self.custom_sub_label.setGeometry(QRect(20, 680, 441, 61))
        self.custom_sub_label.setStyleSheet(u"background-color: rgb(255, 254, 234);\n"
"border-radius: 20px;\n"
"color:black;")
        self.custom_sub_label.setFrameShape(QFrame.Shape.NoFrame)
        self.custom_sub_label.setLineWidth(20)
        self.custom_item = QLabel(self.centralwidget)
        self.custom_item.setObjectName(u"custom_item")
        self.custom_item.setGeometry(QRect(40, 690, 401, 41))
        self.custom_item.setFont(font)
        self.custom_item.setStyleSheet(u"color:rgb(255, 170, 0);\n"
"font: 10pt \"\ubb38\uacbd \uac10\ud64d\uc0ac\uacfc\";")
        self.custom_item.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.schedule_1_item = QLabel(self.centralwidget)
        self.schedule_1_item.setObjectName(u"schedule_1_item")
        self.schedule_1_item.setGeometry(QRect(310, 310, 131, 91))
        self.schedule_1_item.setStyleSheet(u"color:rgb(0, 170, 255);\n"
"font: 700 10pt \"\ubb38\uacbd \uac10\ud64d\uc0ac\uacfc\";")
        self.schedule_1_item.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.schedule_3_item = QLabel(self.centralwidget)
        self.schedule_3_item.setObjectName(u"schedule_3_item")
        self.schedule_3_item.setGeometry(QRect(310, 550, 131, 91))
        self.schedule_3_item.setStyleSheet(u"color:rgb(0, 170, 255);\n"
"font: 700 10pt \"\ubb38\uacbd \uac10\ud64d\uc0ac\uacfc\";")
        self.schedule_3_item.setAlignment(Qt.AlignmentFlag.AlignCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.background.raise_()
        self.OnOff_button.raise_()
        self.weather_label.raise_()
        self.schedule_label.raise_()
        self.custom_label.raise_()
        self.profile1_button.raise_()
        self.profile1_name.raise_()
        self.profile2_button.raise_()
        self.profile3_button.raise_()
        self.profile4_button.raise_()
        self.AMADDA.raise_()
        self.weather_sub_label_2.raise_()
        self.rain_image.raise_()
        self.uv_image.raise_()
        self.dust_image.raise_()
        self.weather_sub_label_4.raise_()
        self.weather_sub_label_1.raise_()
        self.weather_image.raise_()
        self.temp_humid.raise_()
        self.rain_probability.raise_()
        self.uv_level.raise_()
        self.dust_level.raise_()
        self.weather_item.raise_()
        self.schedule_label_schedule.raise_()
        self.schedule_label_item.raise_()
        self.schedule_label_1_1.raise_()
        self.schedule_label_1_2.raise_()
        self.weather_sub_label_3.raise_()
        self.schedule_item_title.raise_()
        self.schedule_schedule_title.raise_()
        self.weather_item_title.raise_()
        self.schedule_1.raise_()
        self.schedule_label_2_1.raise_()
        self.schedule_label_2_2.raise_()
        self.schedule_2_item.raise_()
        self.schedule_2.raise_()
        self.schedule_label_3_1.raise_()
        self.schedule_label_3_2.raise_()
        self.schedule_3.raise_()
        self.custom_sub_label.raise_()
        self.custom_item.raise_()
        self.schedule_1_item.raise_()
        self.schedule_3_item.raise_()
        self.profile2_name.raise_()
        self.profile3_name.raise_()
        self.profile4_name.raise_()

        self.retranslateUi(MainWindow)
        self.OnOff_button.clicked["bool"].connect(MainWindow.on_off_bt)
        self.profile4_button.clicked.connect(MainWindow.profile_bt4)
        self.profile3_button.clicked.connect(MainWindow.profile_bt3)
        self.profile2_button.clicked.connect(MainWindow.profile_bt2)
        self.profile1_button.clicked.connect(MainWindow.profile_bt1)

        self.OnOff_button.setDefault(False)
        self.profile4_button.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"AMADDA", None))
        self.OnOff_button.setText("")
        self.background.setText("")
        self.weather_label.setText("")
        self.schedule_label.setText("")
        self.custom_label.setText("")
        self.profile1_button.setText("")
        self.profile1_name.setText(QCoreApplication.translate("MainWindow", u"\uc774\uc2b9\ud604", None))
        self.profile2_name.setText(QCoreApplication.translate("MainWindow", u"\ubcf5\uc778\uc218", None))
        self.profile2_button.setText("")
        self.profile3_name.setText(QCoreApplication.translate("MainWindow", u"\uc190\uc8fc\ud615", None))
        self.profile3_button.setText("")
        self.profile4_name.setText(QCoreApplication.translate("MainWindow", u"\uc544\ub9de\ub2e4", None))
        self.profile4_button.setText("")
        self.AMADDA.setText(QCoreApplication.translate("MainWindow", u"AMADDA", None))
        self.rain_image.setText("")
        self.uv_image.setText("")
        self.dust_image.setText("")
        self.weather_sub_label_2.setText("")
        self.weather_sub_label_4.setText("")
        self.weather_sub_label_1.setText("")
        self.weather_image.setText("")
        self.temp_humid.setText(QCoreApplication.translate("MainWindow", u"\uc628\ub3c4: 24\u00b0C    \uc2b5\ub3c4: 30%", None))
        self.rain_probability.setText(QCoreApplication.translate("MainWindow", u"\uac15\uc218\ud655\ub960 30%", None))
        self.uv_level.setText(QCoreApplication.translate("MainWindow", u"\uc790\uc678\uc120 \uc9c0\uc218 3(\ubcf4\ud1b5)", None))
        self.dust_level.setText(QCoreApplication.translate("MainWindow", u"\ubbf8\uc138\uba3c\uc9c0 \ubcf4\ud1b5", None))
        self.weather_item.setText(QCoreApplication.translate("MainWindow", u"\uc120\ud06c\ub9bc\n"
"\n"
"\ub9c8\uc2a4\ud06c", None))
        self.schedule_label_schedule.setText("")
        self.schedule_label_item.setText("")
        self.schedule_label_1_1.setText("")
        self.schedule_label_1_2.setText("")
        self.weather_sub_label_3.setText("")
        self.schedule_item_title.setText(QCoreApplication.translate("MainWindow", u"ITEM", None))
        self.schedule_schedule_title.setText(QCoreApplication.translate("MainWindow", u"SCHEDULE", None))
        self.weather_item_title.setText(QCoreApplication.translate("MainWindow", u"ITEM", None))
        self.schedule_1.setText(QCoreApplication.translate("MainWindow", u"\uc804\uc790\uae30\ud559 \uc911\uac04\uace0\uc0ac\n"
"10:30", None))
        self.schedule_label_2_1.setText("")
        self.schedule_label_2_2.setText("")
        self.schedule_2_item.setText(QCoreApplication.translate("MainWindow", u"\ub178\ud2b8\ubd81\n"
"\n"
"\ubc1c\ud45c\uc790\ub8cc\n"
"\n"
"\ub808\uc774\uc800 \ud3ec\uc778\ud130", None))
        self.schedule_2.setText(QCoreApplication.translate("MainWindow", u"\uc784\ubca0\ub514\ub4dc\uc2dc\uc2a4\ud15c \uc911\uac04\ubc1c\ud45c\n"
"12:00", None))
        self.schedule_label_3_1.setText("")
        self.schedule_label_3_2.setText("")
        self.schedule_3.setText(QCoreApplication.translate("MainWindow", u"\ud48b\uc0b4\n"
"22:00", None))
        self.custom_sub_label.setText("")
        self.custom_item.setText(QCoreApplication.translate("MainWindow", u"\uc774\uc5b4\ud3f0 / \ubcf4\uc870\ubca0\ud130\ub9ac / \uc9c0\uac11 / \ub77c\uc988\ubca0\ub9ac\ud30c\uc774", None))
        self.schedule_1_item.setText(QCoreApplication.translate("MainWindow", u"\ub178\ud2b8\n"
"\n"
"\uacc4\uc0b0\uae30\n"
"\n"
"\ud39c", None))
        self.schedule_3_item.setText(QCoreApplication.translate("MainWindow", u"\ud48b\uc0b4\ud654\n"
"\n"
"\uc6b4\uc804\ubcf5\n"
"\n"
"\ubb3c\ubcd1", None))
    # retranslateUi

