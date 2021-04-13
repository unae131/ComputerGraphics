from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
 
import sys
from BvhPresenter import *
from BvhModel import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QOpenGLWidget
import platform
 
 
class BvhViewer(QOpenGLWidget):

    RED = [1.0, 0.0, 0.0]
    BLUE = [0.0, 0.0, 1.0]
 
    flag = 1
 
    def  __init__(self, fileName, parent = None):
        super(BvhViewer, self).__init__(parent)
        self.bvhController = BVHController()
        self.bvhController.readBVHfile(fileName)
        self.initUI()

    def initUI(self):
        cfrm = QFrame(self)
        # self.setCentralWidget(cfrm)
        grid = QGridLayout()
        cfrm.setLayout(grid)

        self.drawBtn("프레임 on/off", 20, 650, self.frameOnOff)
        self.playOrStopBtn = self.drawBtn("재생/멈춤", 20, 750, self.bvhController.switchPlaying)
        self.frameMoveBtn = self.drawBtn("프레임 이동", 120, 750, self.frameMove)
        self.zoomInBtn = self.drawBtn("+", 20, 700, self.bvhController.zoomIn)
        self.zoomOutBtn = self.drawBtn("-", 50, 700, self.bvhController.zoomOut)

        self.code_edit = QLineEdit(self)
        self.code_edit.move(220, 755)
        self.code_edit.setText("")

        self.label = QLabel('Frame: '+str(self.bvhController.curFrame)+"/" + str(self.bvhController.motion.frames), self)
        self.label.move(350, 755)
        self.label.setStyleSheet("Color : white")
        self.label.resize(self.label.sizeHint())
        self.label.setGeometry(100,100,400,100)

        self.sld = QSlider(Qt.Horizontal, cfrm)
        self.sld.adjustSize()
        self.sld.setTickPosition(1)
        self.sld.setMaximum(self.bvhController.motion.frames - 1)
        self.sld.setMinimum(0)
        self.sld.valueChanged[int].connect(self.slideFrame)
        grid.addWidget(self.sld, 20, 10, 20, 80)

        #progress bar
        self.pbar = QProgressBar(cfrm)
        self.pbar.adjustSize()
        self.pbar.text()
        grid.addWidget(self.pbar, 20,0,10,80)
        self.timer = QTimer()
        self.step = 1#self.bvhController.curFrame

    def drawBtn(self, name, x, y, btn_callback):
        btn = QPushButton(name, self)
        btn.move(x,y)
        # print(self.playOrStopbtn.sizeHint())
        btn.resize(btn.sizeHint())
        btn.clicked.connect(btn_callback)
        # btn.clicked.connect(QCoreApplication.instance().quit)
        self.setGeometry(100,100,200,100)

        return btn

    def frameMove(self):
        frame = self.code_edit.text()
        self.bvhController.setFrame(int(frame))
        self.label.setText('Frame: '+str(self.bvhController.curFrame)+"/" + str(self.bvhController.motion.frames))
    
    def slideFrame(self):
        frame = self.sld.value()
        self.bvhController.setFrame(frame)
        self.label.setText('Frame: '+str(self.bvhController.curFrame)+"/" + str(self.bvhController.motion.frames))
    
    def progressBar(self):
        self.bvhController.switchPlaying()
        self.sld.setValue(self.bvhController.curFrame)
        self.pbar.setValue(self.bvhController.curFrame)

    def frameOnOff(self):
        self.bvhController.fill = not self.bvhController.fill

    def paintGL(self):
 
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
 
        if BvhViewer.flag:
            glColor3f(BvhViewer.RED[0], BvhViewer.RED[1], BvhViewer.RED[2])
        else :
            glColor3f(BvhViewer.BLUE[0], BvhViewer.BLUE[1], BvhViewer.BLUE[2])
 
        # glPushMatrix()
        # glTranslatef(0.0, 0.0, -5.0)
        # glRotatef(60.0, 1.0, 1.0, 0.0)
        self.bvhController.render()
        self.label.setText('Frame: '+str(self.bvhController.curFrame)+"/" + str(self.bvhController.motion.frames-1))
        # self.sld.setValue(self.bvhController.curFrame)
        # self.pbar.setValue(self.bvhController.curFrame)
        # # self.Draw(1.0, 1.0, 1.0)
        # glPopMatrix()
        glFlush()
        
        self.update()
 
    def mousePressEvent(self, event):
        if BvhViewer.flag :
            BvhViewer.flag = 0
        else :
            BvhViewer.flag = 1
        
 
if __name__=='__main__':
    app = QApplication(sys.argv)
    window = BvhViewer("sample-walk.bvh")
    window.setWindowTitle('BvhViewer')
    window.setFixedSize(1200,800)
    window.show()
    sys.exit(app.exec_())
