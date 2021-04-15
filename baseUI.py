from QtGlViewer import *
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, resize):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(720, 490)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(640, 430, 61, 16))
        self.label.setObjectName("label")

        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(100, 430, 531, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")

        self.openGLWidget = QtViewer("bvhFiles/sample-walk.bvh", label = self.label, slider = self.horizontalSlider, parent = self.centralwidget)
        self.openGLWidget.setGeometry(QtCore.QRect(-1, -21, 721, 411))
        self.openGLWidget.setObjectName("openGLWidget")
        self.openGLWidget.show()

        self.horizontalSlider.setRange(0,self.openGLWidget.glDrawer.motion.frames-1)
        self.horizontalSlider.setPageStep(5)
        self.horizontalSlider.valueChanged.connect(self.updateLabel)
        
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(0, 430, 102, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openGLWidget.glDrawer.switchPlaying)

        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(210, 410, 100, 20))
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setChecked(False)
        self.radioButton.clicked.connect(self.on_toggle_mode)

        self.zoomInButton = QtWidgets.QPushButton(self.centralwidget)
        self.zoomInButton.setGeometry(QtCore.QRect(640, 400, 33, 30))
        self.zoomInButton.setObjectName("zoomInButton")
        self.zoomInButton.clicked.connect(self.zoomIn_callback)

        self.zoomOutButton = QtWidgets.QPushButton(self.centralwidget)
        self.zoomOutButton.setGeometry(QtCore.QRect(670, 400, 33, 30))
        self.zoomOutButton.setObjectName("zoomOutButton")
        self.zoomOutButton.clicked.connect(self.zoomOut_callback)

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 400, 193, 33))
        self.widget.setObjectName("widget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.lineEdit.textChanged.connect(self.onChanged)

        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_3.clicked.connect(self.onClicked)

        MainWindow.setCentralWidget(self.centralwidget)
        
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "시작/멈춤"))
        self.label.setText(_translate("MainWindow", str(self.openGLWidget.glDrawer.curFrame)+"/"+str(self.openGLWidget.glDrawer.motion.frames)))
        self.radioButton.setText(_translate("MainWindow", "Wire Frame"))
        self.lineEdit.setText(_translate("MainWindow", "0"))
        self.pushButton_3.setText(_translate("MainWindow", "이동"))
        self.zoomInButton.setText(_translate("MainWindow", "+"))
        self.zoomOutButton.setText(_translate("MainWindow", "-"))

    def updateLabel(self, value):
        self.openGLWidget.glDrawer.curFrame = value

    def on_toggle_mode(self):
        if self.radioButton.isChecked():
            self.openGLWidget.glDrawer.fill = False
        else:
            self.openGLWidget.glDrawer.fill = True

    def onChanged(self, frame):
        self.lineEdit.setText(frame)

    def onClicked(self, frame):
        self.openGLWidget.glDrawer.curFrame = int(self.lineEdit.text())

    def zoomIn_callback(self):
        self.openGLWidget.glDrawer.camera.zoom(0.5)

    def zoomOut_callback(self):
        self.openGLWidget.glDrawer.camera.zoom(-0.5)    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, 2)
    MainWindow.show()
    sys.exit(app.exec_())
