from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
 
import sys
from GLDrawer import *
from BvhParser import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QOpenGLWidget
import platform
 
 
class QTViewer(QOpenGLWidget):
    RED = [1.0, 0.0, 0.0]
    BLUE = [0.0, 0.0, 1.0]
 
    flag = 1
 
    def  __init__(self, fileName, parent = None):
        super(QTViewer, self).__init__(parent)
        self.glDrawer = GLDrawer(fileName)
        self.initUI()

    def initUI(self):
        cfrm = QFrame(self)
        # self.setCentralWidget(cfrm)
        grid = QGridLayout()
        cfrm.setLayout(grid)

        self.drawBtn("프레임 on/off", 20, 650, self.frameOnOff)
        self.playOrStopBtn = self.drawBtn("재생/멈춤", 20, 750, self.glDrawer.switchPlaying)
        self.frameMoveBtn = self.drawBtn("프레임 이동", 120, 750, self.frameMove)
        self.zoomInBtn = self.drawBtn("+", 20, 700, self.glDrawer.zoomIn)
        self.zoomOutBtn = self.drawBtn("-", 50, 700, self.glDrawer.zoomOut)

        self.code_edit = QLineEdit(self)
        self.code_edit.move(220, 755)
        self.code_edit.setText("")

        self.label = QLabel('Frame: '+str(self.glDrawer.curFrame)+"/" + str(self.glDrawer.motion.frames), self)
        self.label.move(350, 755)
        self.label.setStyleSheet("Color : white")
        self.label.resize(self.label.sizeHint())
        self.label.setGeometry(100,100,400,100)

        self.sld = QSlider(Qt.Horizontal, cfrm)
        self.sld.adjustSize()
        self.sld.setTickPosition(1)
        self.sld.setMaximum(self.glDrawer.motion.frames - 1)
        self.sld.setMinimum(0)
        self.sld.valueChanged[int].connect(self.slideFrame)
        grid.addWidget(self.sld, 20, 10, 20, 80)

        #progress bar
        self.pbar = QProgressBar(cfrm)
        self.pbar.adjustSize()
        self.pbar.text()
        grid.addWidget(self.pbar, 20,0,10,80)
        self.timer = QTimer()
        self.step = 1#self.glDrawer.curFrame

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
        self.glDrawer.setFrame(int(frame))
        self.label.setText('Frame: '+str(self.glDrawer.curFrame)+"/" + str(self.glDrawer.motion.frames))
    
    def slideFrame(self):
        frame = self.sld.value()
        self.glDrawer.setFrame(frame)
        self.label.setText('Frame: '+str(self.glDrawer.curFrame)+"/" + str(self.glDrawer.motion.frames))
    
    def progressBar(self):
        self.glDrawer.switchPlaying()
        self.sld.setValue(self.glDrawer.curFrame)
        self.pbar.setValue(self.glDrawer.curFrame)

    def frameOnOff(self):
        self.glDrawer.fill = not self.glDrawer.fill

    def paintGL(self):
 
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
 
        if QTViewer.flag:
            glColor3f(QTViewer.RED[0], QTViewer.RED[1], QTViewer.RED[2])
        else :
            glColor3f(QTViewer.BLUE[0], QTViewer.BLUE[1], QTViewer.BLUE[2])
 
        # glPushMatrix()
        # glTranslatef(0.0, 0.0, -5.0)
        # glRotatef(60.0, 1.0, 1.0, 0.0)
        self.glDrawer.render()
        self.label.setText('Frame: '+str(self.glDrawer.curFrame)+"/" + str(self.glDrawer.motion.frames-1))
        # self.sld.setValue(self.glDrawer.curFrame)
        # self.pbar.setValue(self.glDrawer.curFrame)
        # # self.Draw(1.0, 1.0, 1.0)
        # glPopMatrix()
        glFlush()
        
        self.update()
 
    def mousePressEvent(self, event):
        if QTViewer.flag :
            QTViewer.flag = 0
        else :
            QTViewer.flag = 1
        
 
if __name__=='__main__':
    app = QApplication(sys.argv)
    window = QTViewer("bvhFiles/sample-walk.bvh")
    window.setWindowTitle('QTViewer')
    window.setFixedSize(1200,800)
    window.show()
    sys.exit(app.exec_())
