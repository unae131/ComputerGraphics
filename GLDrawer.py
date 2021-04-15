from Camera import *
from BvhParser import *
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import os
import glfw
from Camera import *

class GLDrawer():
    def __init__(self, fileName):
        self.skeleton, self.motion = readBVHfile(fileName)
        self.camera = Camera()
        self.curFrame = 0
        
        self.fill = True
        self.playing = False

    def createVertexArraySeparate(self, size,r):
        varr = np.array([
            (0,0,1),
            ( -size , r ,  size ),
            (0,0,1),
            (  size , 0 ,  size ),
            (0,0,1),
            (  size , r ,  size ), #size

            (0,0,1),
            ( -size , r ,  size ),
            (0,0,1),
            ( -size , 0 ,  size ),
            (0,0,1),
            (  size , 0 ,  size ), #size

            (0,0,-1),
            ( -size , r , -size ),
            (0,0,-1),
            (  size , r , -size ),
            (0,0,-1),
            (  size , 0 , -size ), #-size

            (0,0,-1),
            ( -size , r , -size ),
            (0,0,-1),
            (  size , 0 , -size ),
            (0,0,-1),
            ( -size , 0 , -size ), #-size

            (0,1,0),
            ( -size , r ,  size ),
            (0,1,0),
            (  size , r ,  size ),
            (0,1,0),
            (  size , r , -size ), #r

            (0,1,0),
            ( -size , r ,  size ),
            (0,1,0),
            (  size , r , -size ),
            (0,1,0),
            ( -size , r , -size ), #r

            (0,-1,0),
            ( -size , 0 ,  size ),
            (0,-1,0),
            (  size , 0 , -size ),
            (0,-1,0),
            (  size , 0 ,  size ), #-r

            (0,-1,0),
            ( -size , 0 ,  size ),
            (0,-1,0),
            ( -size , 0 , -size ),
            (0,-1,0),
            (  size , 0 , -size ), #-r

            (1,0,0),
            (  size , r ,  size ), # size
            (1,0,0),
            (  size , 0 ,  size ),
            (1,0,0),
            (  size , 0 , -size ),

            (1,0,0),
            (  size , r ,  size ),
            (1,0,0),
            (  size , 0 , -size ),
            (1,0,0),
            (  size , r , -size ), #size

            (-1,0,0),
            ( -size , r ,  size ),
            (-1,0,0),
            ( -size , 0 , -size ),
            (-1,0,0),
            ( -size , 0 ,  size ), #-size

            (-1,0,0),
            ( -size , r ,  size ), #-size
            (-1,0,0),
            ( -size , r , -size ),
            (-1,0,0),
            ( -size , 0 , -size ),
        ], 'float32')
        return varr

    def drawLine(self, offset):
        glBegin(GL_LINES)
        glVertex3fv(offset)
        glVertex3fv(np.array([0,0,0.]))
        glEnd()
    
    def drawLineGlobal(self, p0, p1):
        glBegin(GL_LINES)
        glVertex3fv(np.array(p0))
        glVertex3fv(np.array(p1))
        glEnd()

    def drawBoxGlobal(self, x, y, z):
        glPushMatrix()
        glTranslatef(x,y,z)
        glScalef(0.2,0.2,0.2)
        point1 = [0.5, 0.5, -0.5]
        point2 = [0.5, 0.5, 0.5]
        point3 = [0.5, -0.5, 0.5]
        point4 = [0.5, -0.5, -0.5]
        point5 = [-0.5, -0.5, 0.5]
        point6 = [-0.5, 0.5, 0.5]
        point7 = [-0.5, 0.5, -0.5]
        point8 = [-0.5, -0.5, -0.5]
 
        glBegin(GL_QUADS)
 
        glVertex3fv(point1)
        glVertex3fv(point2)
        glVertex3fv(point6)
        glVertex3fv(point7)
 
        glVertex3fv(point3)
        glVertex3fv(point4)
        glVertex3fv(point8)
        glVertex3fv(point5)
 
        glVertex3fv(point2)
        glVertex3fv(point3)
        glVertex3fv(point5)
        glVertex3fv(point6)
 
        glVertex3fv(point7)
        glVertex3fv(point8)
        glVertex3fv(point4)
        glVertex3fv(point1)
 
        glVertex3fv(point6)
        glVertex3fv(point5)
        glVertex3fv(point8)
        glVertex3fv(point7)
 
        glVertex3fv(point1)
        glVertex3fv(point4)
        glVertex3fv(point3)
        glVertex3fv(point2)
 
        glEnd()
        glPopMatrix()
    
    def drawBox(self, offset):
        x = offset[0]
        y = offset[1]
        z = offset[2]

        ab_x = abs(x)
        ab_y = abs(y)
        ab_z = abs(z)

        size = 0.03

        glPushMatrix()

        r = np.sqrt(x*x+y*y+z*z)

        theta = (np.arccos(ab_y/r)*180)/np.pi

        if z != 0:
            pi = (np.arctan(ab_x/ab_z)*180)/np.pi
        else:
            pi = 0

        if y < 0:
            theta = 180 - theta

        if x > 0 and z < 0:
            pi = 180 - pi
        elif x < 0 and z < 0:
            pi += 180
        elif x < 0 and z > 0:
            pi = -pi

        glRotatef(pi,0,1,0)
        glRotatef(theta,1,0,0)

        varr = self.createVertexArraySeparate(size,r)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
        glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
        glDrawArrays(GL_TRIANGLES, 0, int(varr.size/6))

        glPopMatrix()

    def drawBodyNode(self, posture, node):
        if node.type == node.TYPE_END_SITE:
            return

        glPushMatrix()

        L = posture.getLinkMatrix(node)
        R = posture.getJointTransMatrix(node)
        glMultMatrixf((L@R).T)

        for n in node.children:
            self.drawBox(n.offset)
            self.drawBodyNode(posture, n)

        glPopMatrix()

    def drawBody(self):
        posture = self.motion.getPosture(self.curFrame)
        root = self.skeleton.getRoot()

        # draw root
        glPushMatrix()

        J0 = posture.getJointTransMatrix(root)

        glMultMatrixf(J0.T)

        for n in root.children:
            self.drawBox(n.offset)
            self.drawBodyNode(posture, n) 

        glPopMatrix()

    def drawGrid(self):
        glBegin(GL_LINES)
        glColor3ub(100,100,100)
        x = 20.
        y = 0.
        z = 20.
        for i in np.linspace(-x, x, 41):
            glVertex3fv(np.array([i, y, z]))
            glVertex3fv(np.array([i, y, -z]))
        for i in np.linspace(-z, z, 41):
            glVertex3fv(np.array([x, y, i]))
            glVertex3fv(np.array([-x, y, i]))
        glEnd()

    def drawFrame(self):
        glBegin(GL_LINES)
        glColor3ub(255, 0, 0)
        glVertex3fv(np.array([0.,0.,0.]))
        glVertex3fv(np.array([1.,0.,0.]))
        glColor3ub(0, 255, 0)
        glVertex3fv(np.array([0.,0.,0.]))
        glVertex3fv(np.array([0.,1.,0.]))
        glColor3ub(0, 0, 255)
        glVertex3fv(np.array([0.,0.,0]))
        glVertex3fv(np.array([0.,0.,1.]))
        glEnd()

    def switchPlaying(self):
        self.playing = not self.playing

    def setViewport(self, fovy = 120, aspect = 1, zNear = 1, zFar = 50):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(fovy, aspect, zNear, zFar)
        
        # glMatrixMode(GL_MODELVIEW)
        # glLoadIdentity()

        # glMultMatrixf(self.camera.matrix.T)

    def setLighting(self):
        # lighting
        glEnable(GL_LIGHTING)   # try to uncomment: no lighting
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        glEnable(GL_RESCALE_NORMAL)

        # light0 position
        glPushMatrix()
        lightPos = (3.,4.,5.,1.)    # try to change 4th element to 0. or 1.
        glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
        glPopMatrix()

        # light1 position
        glPushMatrix()
        glRotatef(120,0,1,0) # rotate light
        lightPos = (3.,4.,5.,1.)
        glLightfv(GL_LIGHT1, GL_POSITION, lightPos)
        glPopMatrix()

        # light intensity for each color channel
        lightColor = (1.,1.,1.,1.)
        ambientLightColor = (.1,.1,.1,1.)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
        glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

        lightColor = (0.,0.,1.,1.)
        glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor)
        glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor)
        glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)
    
    def unsetLighting(self):
        glDisable(GL_LIGHTING)

    def setObjectColor(self, r, g, b):
        # material reflectance for each color channel
        objectColor = (1.,0.,0.,1.)
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS, 10)
        glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
        glColor3ub(r, g, b) # glColor*() is ignored if lighting is enabled

    def render(self, lighting = True):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        if not self.fill:
            glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
        else:
            glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )

        self.setViewport()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glMultMatrixf(self.camera.matrix.T)

        self.drawFrame()
        self.drawGrid()

        if lighting:
            self.setLighting()

        # draw bvhFile
        glPushMatrix()
        self.setObjectColor(255,0,0)
        
        if self.skeleton != None:
            self.drawBody()
            if self.playing:
                self.curFrame += 1
                self.curFrame %= self.motion.frames
        glPopMatrix()

        if lighting:
            self.unsetLighting()

        # kinematics
        glPushMatrix()
        self.setObjectColor(0,255,0)
        self.drawJointVelocity(2)
        glPopMatrix()

    def getGlobalPosition(self, nodeIdx, frame = -1):
        if self.skeleton == None:
            return None
        
        if nodeIdx >= len(self.skeleton.hierarchy):
            return None

        node = self.skeleton.hierarchy[nodeIdx]

        if node.type == BvhNode.TYPE_END_SITE:
            return None

        if frame == -1:
            frame = self.curFrame
        
        posture = self.motion.postures[frame]

        p = np.array([0., 0., 0., 1.], dtype=np.float64)

        while node.type != BvhNode.TYPE_ROOT:
            p = posture.getLinkMatrix(node) @ posture.getJointTransMatrix(node) @ p
            node = node.parent

        p = posture.getJointTransMatrix(node) @ p

        return p[:3]

    def getLinearVelocity(self, p0, p1, time):
        v = np.array(p1) - np.array(p0)
        v /= time

        return v

    def drawJointVelocity(self, nodeIdx):
        curP = self.getGlobalPosition(nodeIdx)

        if curP is None or self.curFrame == 0:
            return

        lastP = self.getGlobalPosition(nodeIdx, frame = self.curFrame - 1)

        v = self.getLinearVelocity(lastP, curP, self.motion.frame_time)

        self.drawLineGlobal(curP, curP + v)

        

