from GLDrawer import *
from BvhParser import *
from baseUI import *

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QOpenGLWidget
import platform
 
class QtViewer(QOpenGLWidget):
    def  __init__(self, fileName, label, slider, parent = None):
        super(QtViewer, self).__init__(parent)
        self.glDrawer = GLDrawer(fileName)
        self.label = label
        self.slider = slider
        self.mousePressed = False
        self.panning = False
        self.initUI()

    def initUI(self):
        self.setMouseTracking(True)

    def paintGL(self):
        self.glDrawer.render()
        self.label.setText(str(self.glDrawer.curFrame)+"/" + str(self.glDrawer.motion.frames-1))
        self.slider.setValue(self.glDrawer.curFrame)
        self.update()
 
    def mousePressEvent(self, event):
        self.mousePressed = True
        self.x = event.x()
        self.y = event.y()

    def mouseReleaseEvent(self, event):
        self.mousePressed = False

    def mouseMoveEvent(self, e):
        if self.mousePressed:
            x_offset = 0.01*(e.x() - self.x)
            y_offset = 0.05*(e.y() - self.y)

            if not self.panning:
                self.glDrawer.camera.orbit(x_offset, y_offset)

            else:
                self.glDrawer.camera.panning(x_offset, y_offset)

            self.x = e.x()
            self.y = e.y()

    def mouseDoubleClickEvent(self, e):
        self.panning = not self.panning
