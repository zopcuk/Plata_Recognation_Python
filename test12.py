from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class MainWindow(QtWidgets.QMainWindow):
    def resizeEvent(self, event):
        print("resize")
        QtWidgets.QMainWindow.resizeEvent(self, event)




app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())