from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import test11
from threading import Thread, Lock
lock = Lock()

cap = cv2.VideoCapture(0)

class Ui_plakaokuma(object):
    def setupUi(self, plakaokuma):
        plakaokuma.setObjectName("plakaokuma")
        plakaokuma.resize(1147, 548)
        self.centralwidget = QtWidgets.QWidget(plakaokuma)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 9)
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.video_label = QtWidgets.QLabel(self.centralwidget)
        self.video_label.setText("")
        self.video_label.setPixmap(QtGui.QPixmap(frameconvert()))
        self.video_label.setScaledContents(True)
        self.video_label.setObjectName("video_label")
        self.horizontalLayout.addWidget(self.video_label)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.plaka_text = QtWidgets.QLabel(self.centralwidget)
        self.plaka_text.setMinimumSize(QtCore.QSize(0, 50))
        self.plaka_text.setMaximumSize(QtCore.QSize(16777215, 50))
        self.plaka_text.setObjectName("plaka_text")
        self.verticalLayout.addWidget(self.plaka_text)
        self.plaka_crop = QtWidgets.QLabel(self.centralwidget)
        self.plaka_crop.setMinimumSize(QtCore.QSize(0, 50))
        self.plaka_crop.setMaximumSize(QtCore.QSize(217, 50))
        self.plaka_crop.setStyleSheet("background:red")
        self.plaka_crop.setText("")
        self.plaka_crop.setPixmap(QtGui.QPixmap(qimageCrop))
        self.plaka_crop.setScaledContents(True)
        self.plaka_crop.setObjectName("plaka_crop")
        self.verticalLayout.addWidget(self.plaka_crop)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(5)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(3, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(4, 1, item)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 90)
        self.horizontalLayout.setStretch(1, 10)
        plakaokuma.setCentralWidget(self.centralwidget)

        self.retranslateUi(plakaokuma)
        QtCore.QMetaObject.connectSlotsByName(plakaokuma)

    def retranslateUi(self, plakaokuma):
        _translate = QtCore.QCoreApplication.translate
        plakaokuma.setWindowTitle(_translate("plakaokuma", "Plaka Okuma"))
        self.plaka_text.setText(_translate("plakaokuma", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">PLAKA</span></p></body></html>"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("plakaokuma", "1"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("plakaokuma", "2"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("plakaokuma", "3"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("plakaokuma", "4"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("plakaokuma", "5"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("plakaokuma", "PLAKA"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("plakaokuma", "ZAMAN"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("plakaokuma", "plaka1"))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("plakaokuma", "time1"))
        item = self.tableWidget.item(1, 0)
        item.setText(_translate("plakaokuma", "plaka2"))
        item = self.tableWidget.item(1, 1)
        item.setText(_translate("plakaokuma", "time2"))
        item = self.tableWidget.item(2, 0)
        item.setText(_translate("plakaokuma", "plaka3"))
        item = self.tableWidget.item(2, 1)
        item.setText(_translate("plakaokuma", "time3"))
        item = self.tableWidget.item(3, 0)
        item.setText(_translate("plakaokuma", "plaka4"))
        item = self.tableWidget.item(3, 1)
        item.setText(_translate("plakaokuma", "time4"))
        item = self.tableWidget.item(4, 0)
        item.setText(_translate("plakaokuma", "plaka5"))
        item = self.tableWidget.item(4, 1)
        item.setText(_translate("plakaokuma", "time5"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)

def frameconvert():
    lock.acquire()
    success, FrameOrigin = cap.read()
    lock.release()
    if success:
        frame = FrameOrigin
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h = frame.shape[0]
        w = frame.shape[1]
        d = frame.shape[2]
        d = d*w
        qimage = QtGui.QImage(frame, w, h, d, QtGui.QImage.Format_RGB888)
        return qimage

def update_label():
    while True:
        ui.video_label.setPixmap(QtGui.QPixmap(frameconvert()))
        ui.plaka_crop.setPixmap(QtGui.QPixmap(qimageCrop))

qimageCrop = ""
def frame_send():
    while True:
        global qimageCrop
        lock.acquire()
        success, FrameOrigin1 = cap.read()
        lock.release()
        if success:
            frame = FrameOrigin1
            frame, screenCnt, detected = test11.pre_proc(frame)
            if detected == 1:
                PlateText, PlateCrop = test11.reading(frame, screenCnt)
                if PlateText != None:
                    print(PlateText)
                    h = PlateCrop.shape[0]
                    w = PlateCrop.shape[1]
                    d = w
                    qimageCrop = QtGui.QImage(PlateCrop, w, h, d, QtGui.QImage.Format_Grayscale8)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    plakaokuma = QtWidgets.QMainWindow()
    ui = Ui_plakaokuma()
    ui.setupUi(plakaokuma)
    #plakaokuma.showFullScreen()python
    plakaokuma.show()

    '''timer = QtCore.QTimer()
    timer.timeout.connect(update_label)
    # timer.timeout.connect(frame_send)
    timer.start(1000)'''
    video = Thread(target=update_label)
    frame_read = Thread(target=frame_send)

    frame_read.start()
    video.start()

    sys.exit(app.exec_())