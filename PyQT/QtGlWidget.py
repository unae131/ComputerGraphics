from Drawer.GlDrawer import *
from PyQt5.QtWidgets import QOpenGLWidget
from Drawer.MatplotDrawer import *
 
class QtGlWidget(QOpenGLWidget):
    def  __init__(self, fileName, label, slider, parent = None):
        super(QtGlWidget, self).__init__(parent)
        self.glDrawer = GlDrawer(fileName, kinematics=True,targetPos=[0.,0.,0.])
        # self.matplotDrawer = MatplotDrawer(self.glDrawer.skeleton, self.glDrawer.motion)
        self.label = label
        self.slider = slider
        self.mousePressed = False
        self.panning = False
        self.initUI()

    def initUI(self):
        self.setMouseTracking(True)

    def paintGL(self):
        self.glDrawer.render()
        # self.matplotDrawer.drawPosture(self.glDrawer.skeleton, self.glDrawer.motion.postures[self.glDrawer.curFrame])
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
                self.glDrawer.camera.panning(x_offset, - y_offset)

            self.x = e.x()
            self.y = e.y()

    def mouseDoubleClickEvent(self, e):
        self.panning = not self.panning
