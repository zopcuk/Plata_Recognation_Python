# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'videotest.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!

import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
#import datetime
from PIL.ImageQt import ImageQt
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QLabel, QSizePolicy, QApplication
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import sys
#from PIL import Image as Img

cap = cv2.VideoCapture("9102_Trim.mp4")
def framecache():
    success, FrameOrigin = cap.read()
    #cv2.imwrite("frame.jpg", FrameOrigin)
    frame = FrameOrigin
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h = frame.shape[0]
    w = frame.shape[1]
    d = frame.shape[2]
    d = d*w
    qimage = QtGui.QImage(frame, w, h, d, QtGui.QImage.Format_RGB888)
    return qimage

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(908, 600)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap.fromImage(framecache()))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 2, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_2.setText(_translate("Form", "PushButton"))
        self.pushButton.setText(_translate("Form", "PushButton"))

def update_label():
    #current_time = str(datetime.datetime.now().time())
    #ui.label.setText("")
    ui.label.setPixmap(QtGui.QPixmap.fromImage(framecache()))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()

    timer = QtCore.QTimer()
    timer.timeout.connect(update_label)
    timer.start(10)

    sys.exit(app.exec_())

