from UI.QtGlWidget import *
from PyQt5 import QtCore, QtWidgets
from Warping import *

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

        self.mtWarpLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.mtWarpLineEdit.setObjectName("mtWarpLineEdit")
        self.mtWarpLineEdit.setGeometry(QtCore.QRect(10, 460, 120, 20))
        self.mtWarpLineEdit.textChanged.connect(self.onMtWarpLineChagned)

        self.mtWarpBtn = QtWidgets.QPushButton(self.centralwidget)
        self.mtWarpBtn.setObjectName("mtWarpBtn")
        self.mtWarpBtn.setGeometry(QtCore.QRect(132, 455, 100, 30))
        self.mtWarpBtn.clicked.connect(self.onMtWarpClicked)

        self.timeWarp2xBtn = QtWidgets.QRadioButton(self.centralwidget)
        self.timeWarp2xBtn.setObjectName("timeWarp2xBtn")
        self.timeWarp2xBtn.setGeometry(QtCore.QRect(234, 455, 100, 20))
        self.timeWarp2xBtn.setChecked(False)
        self.timeWarp2xBtn.clicked.connect(self.on_toggle_2x)

        self.timeWarp0_5xBtn = QtWidgets.QRadioButton(self.centralwidget)
        self.timeWarp0_5xBtn.setObjectName("timeWarp0.5xBtn")
        self.timeWarp0_5xBtn.setGeometry(QtCore.QRect(284, 455, 100, 20))
        self.timeWarp0_5xBtn.setChecked(False)
        self.timeWarp0_5xBtn.clicked.connect(self.on_toggle_halfx)

        self.timeWarpSinxBtn = QtWidgets.QRadioButton(self.centralwidget)
        self.timeWarpSinxBtn.setObjectName("timeWarpSinxBtn")
        self.timeWarpSinxBtn.setGeometry(QtCore.QRect(334, 455, 100, 20))
        self.timeWarpSinxBtn.setChecked(False)
        self.timeWarpSinxBtn.clicked.connect(self.on_toggle_sinx)

        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(520, 407, 100, 20))
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setChecked(False)
        self.radioButton.clicked.connect(self.on_toggle_mode)

        self.springLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.springLineEdit.setObjectName("springLineEdit")
        self.springLineEdit.setGeometry(QtCore.QRect(390, 455, 50, 20))
        self.springLineEdit.textChanged.connect(self.onSpringChanged)

        self.springBtn = QtWidgets.QPushButton(self.centralwidget)
        self.springBtn.setObjectName("springBtn")
        self.springBtn.setGeometry(QtCore.QRect(435, 450, 90, 30))
        self.springBtn.clicked.connect(self.onSpringClicked)

        self.timestepLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.timestepLineEdit.setObjectName("timestepLineEdit")
        self.timestepLineEdit.setGeometry(QtCore.QRect(525, 455, 50, 20))
        self.timestepLineEdit.textChanged.connect(self.onTimestepChanged)

        self.timestepBtn = QtWidgets.QPushButton(self.centralwidget)
        self.timestepBtn.setObjectName("timestepBtn")
        self.timestepBtn.setGeometry(QtCore.QRect(570, 450, 105, 30))
        self.timestepBtn.clicked.connect(self.onTimestepClicked)

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
        MainWindow.setWindowTitle(_translate("MainWindow", "motion blending"))
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
        self.jointLineEdit.setText(_translate("MainWindow", "-1"))
        self.jointBtn.setText(_translate("MainWindow", "타겟조인트"))
        self.mtWarpLineEdit.setText(_translate("MainWindow", "j/f/deg/s/e"))
        self.mtWarpBtn.setText(_translate("MainWindow", "motion warp"))
        self.timeWarp2xBtn.setText(_translate("MainWindow", "2x"))
        self.timeWarp0_5xBtn.setText(_translate("MainWindow", "0.5x"))
        self.timeWarpSinxBtn.setText(_translate("MainWindow", "Sinx"))
        self.springLineEdit.setText(_translate("MainWindow", str(self.openGLWidget.glDrawer.sim.ks)+" " + str(self.openGLWidget.glDrawer.sim.kd)))
        self.springBtn.setText(_translate("MainWindow", "Spring coef"))
        self.timestepLineEdit.setText(_translate("MainWindow", str(self.openGLWidget.glDrawer.sim.timestep)))
        self.timestepBtn.setText(_translate("MainWindow", "Sim Timestep"))

        
    def updateLabel(self, value):
        self.openGLWidget.glDrawer.curFrame = value

    def on_toggle_mode(self):
        if self.radioButton.isChecked():
            self.openGLWidget.glDrawer.fill = False
        else:
            self.openGLWidget.glDrawer.fill = True

    def on_toggle_2x(self):
        if self.timeWarp2xBtn.isChecked():
            self.openGLWidget.glDrawer.drawTimeWarp(doubleScale)
        else:
            self.openGLWidget.glDrawer.drawOriginal()

    def on_toggle_halfx(self):
        if self.timeWarp0_5xBtn.isChecked():
            self.openGLWidget.glDrawer.drawTimeWarp(halfScale)
        else:
            self.openGLWidget.glDrawer.drawOriginal()

    def on_toggle_sinx(self):
        if self.timeWarpSinxBtn.isChecked():
            self.openGLWidget.glDrawer.drawTimeWarp(sinScale)
        else:
            self.openGLWidget.glDrawer.drawOriginal()

    def onChanged(self, frame):
        self.lineEdit.setText(frame)

    def onXYZChanged(self, frame):
        self.xyzLineEdit.setText(frame)

    def onJointChanged(self, frame):
        self.jointLineEdit.setText(frame)

    def onMtWarpLineChagned(self, frame):
        self.mtWarpLineEdit.setText(frame)

    def onSpringChanged(self, frame):
        self.springLineEdit.setText(frame)

    def onTimestepChanged(self, frame):
        self.timestepLineEdit.setText(frame)
        
    def onClicked(self, frame):
        self.openGLWidget.glDrawer.curFrame = int(self.lineEdit.text())

    def onXYZClicked(self, frame):
        target = [float(s) for s in self.xyzLineEdit.text().split(", ")]
        self.openGLWidget.glDrawer.setTargetPos(target)

    def onIKClicked(self, frame):
        # targetJoint= self.openGLWidget.glDrawer.targetJoint
        # self.openGLWidget.glDrawer.limbIK(targetJoint.parent, targetJoint)
        pass

    def onMtWarpClicked(self, frame):
        if self.mtWarpLineEdit.text() == "-1":
            self.openGLWidget.glDrawer.drawOriginal()
            return

        args = self.mtWarpLineEdit.text().split("/")
        joint = int(args[0])
        frame = int(args[1])
        degree = float(args[2])
        start = int(args[3])
        end = int(args[4])
        self.openGLWidget.glDrawer.drawWarpedMotion(joint, frame, degree, start, end)

    def onJointClicked(self, frame):
        self.openGLWidget.glDrawer.setTargetJoint(int(self.jointLineEdit.text()))

    def onSpringClicked(self, frame):
        a = self.springLineEdit.text().split(" ")
        self.openGLWidget.glDrawer.sim.testInit(float(a[0]), float(a[1]))

    def onTimestepClicked(self, frame):
        a = float(self.timestepLineEdit.text())
        self.openGLWidget.glDrawer.sim.testInit(timestep= a)

    def zoomIn_callback(self):
        self.openGLWidget.glDrawer.camera.zoom(0.5)

    def zoomOut_callback(self):
        self.openGLWidget.glDrawer.camera.zoom(-0.5)    
