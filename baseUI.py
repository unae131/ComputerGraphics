from QtGlWidget import *
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

        self.openGLWidget = QtGlWidget("bvhFiles/02_04_walk.bvh", label = self.label, slider = self.horizontalSlider, parent = self.centralwidget)
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

        self.zoomInButton = QtWidgets.QPushButton(self.centralwidget)
        self.zoomInButton.setGeometry(QtCore.QRect(640, 400, 33, 30))
        self.zoomInButton.setObjectName("zoomInButton")
        self.zoomInButton.clicked.connect(self.zoomIn_callback)

        self.zoomOutButton = QtWidgets.QPushButton(self.centralwidget)
        self.zoomOutButton.setGeometry(QtCore.QRect(670, 400, 33, 30))
        self.zoomOutButton.setObjectName("zoomOutButton")
        self.zoomOutButton.clicked.connect(self.zoomOut_callback)

        self.xyzLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.xyzLineEdit.setObjectName("xyzLineEdit")
        self.xyzLineEdit.setGeometry(QtCore.QRect(210, 407, 70, 20))
        self.xyzLineEdit.textChanged.connect(self.onXYZChanged)

        self.xyzBtn = QtWidgets.QPushButton(self.centralwidget)
        self.xyzBtn.setObjectName("xyzBtn")
        self.xyzBtn.setGeometry(QtCore.QRect(285, 402, 50, 30))
        self.xyzBtn.clicked.connect(self.onXYZClicked)

        self.limbIKBtn = QtWidgets.QPushButton(self.centralwidget)
        self.limbIKBtn.setObjectName("limbIKBtn")
        self.limbIKBtn.setGeometry(QtCore.QRect(330, 402, 50, 30))
        self.limbIKBtn.clicked.connect(self.onIKClicked)

        self.jointLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.jointLineEdit.setObjectName("jointLineEdit")
        self.jointLineEdit.setGeometry(QtCore.QRect(380, 407, 40, 20))
        self.jointLineEdit.textChanged.connect(self.onJointChanged)

        self.jointBtn = QtWidgets.QPushButton(self.centralwidget)
        self.jointBtn.setObjectName("jointBtn")
        self.jointBtn.setGeometry(QtCore.QRect(420, 402, 80, 30))
        self.jointBtn.clicked.connect(self.onJointClicked)

        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(520, 407, 100, 20))
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setChecked(False)
        self.radioButton.clicked.connect(self.on_toggle_mode)

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
        self.xyzLineEdit.setText(_translate("MainWindow", "0, 0, 0"))
        self.xyzBtn.setText(_translate("MainWindow", "타겟"))
        self.limbIKBtn.setText(_translate("MainWindow", "이동"))
        self.jointLineEdit.setText(_translate("MainWindow", "0"))
        self.jointBtn.setText(_translate("MainWindow", "타겟조인트"))

    def updateLabel(self, value):
        self.openGLWidget.glDrawer.curFrame = value

    def on_toggle_mode(self):
        if self.radioButton.isChecked():
            self.openGLWidget.glDrawer.fill = False
        else:
            self.openGLWidget.glDrawer.fill = True

    def onChanged(self, frame):
        self.lineEdit.setText(frame)

    def onXYZChanged(self, frame):
        self.xyzLineEdit.setText(frame)

    def onJointChanged(self, frame):
        self.jointLineEdit.setText(frame)

    def onClicked(self, frame):
        self.openGLWidget.glDrawer.curFrame = int(self.lineEdit.text())

    def onXYZClicked(self, frame):
        target = [float(s) for s in self.xyzLineEdit.text().split(", ")]
        self.openGLWidget.glDrawer.setTargetPos(target)

    def onIKClicked(self, frame):
        targetJoint= self.openGLWidget.glDrawer.targetJoint
        self.openGLWidget.glDrawer.limbIK(targetJoint.parent, targetJoint)

    def onJointClicked(self, frame):
        self.openGLWidget.glDrawer.setTargetJoint(int(self.jointLineEdit.text()))

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
