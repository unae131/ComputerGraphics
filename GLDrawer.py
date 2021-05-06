from Camera import *
from BvhParser import *
from Matrix import *
from Warping import *
from Model.PostureOperator import *

import math
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from Kinematics import *

class GlDrawer():
    def __init__(self, fileName, kinematics = False, targetJointIdx = -1, targetPos = [0,0,0]):
        self.skeleton, self.motion = readBVHfile(fileName)
        self.origin_motion = self.motion
        self.camera = Camera()
        self.curFrame = 0
        
        # TODO fill 고치기
        self.fill = False
        self.playing = False

        self.kinematics = kinematics
        self.kine_skel, self.kine_mot = readBVHfile(fileName)

        if targetJointIdx < 0 or targetJointIdx >= len(self.kine_skel.hierarchy):
            self.targetJointIdx = -1
        else:
            self.targetJointIdx = targetJointIdx
            self.targetJoint = self.kine_skel.hierarchy[self.targetJointIdx]
        
        self.targetPos = targetPos
        self.motionWarp = False
        self.timeWarp = False

        # time warp
        # self.motion = timeWarp(self.motion, halfScale, end_t= self.motion.frames)
        # self.motion = timeWarp(self.motion, doubleScale, end_t = self.motion.frames)
        # self.motion = timeWarp(self.motion, sinScale, end_t= self.motion.frames)

        # motion stiching
        motion2 = readBVHfile("bvhFiles/02_04_run.bvh")[1]
        # self.motion = motionStitch(self.motion, motion2, motion2.frames-1)

        # blend motion
        motion2 = motionStitch(self.motion, motion2, motion2.frames-1).cutMotion(len(self.motion.postures), len(self.motion.postures) + len(motion2.postures)-1)
        self.motion = blendMotions(self.motion, motion2, 78, 47)
    
    def drawOriginal(self):
        self.motion = self.origin_motion
        self.motionWarp = False

    def drawTimeWarp(self, func):
        self.motion = timeWarp(self.origin_motion, func, end_t = self.origin_motion.frames)

    def drawWarpedMotion(self, targetJointIdx, targetFrame, degree, start = 80, end = 130):
        self.targetPosture = self.origin_motion.postures[targetFrame].copy()
        targetJoint = self.skeleton.hierarchy[targetJointIdx]
        self.targetPosture.setNodeOrientation(targetJoint, self.targetPosture.getJointTransMatrix(targetJoint) @ getXRotMatrix(degree))
        self.motionWarp = True
        self.motion = motionWarp(self.origin_motion.copy(), self.targetPosture, targetFrame, start, end)

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
        glScalef(0.08,0.08,0.08)
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

    def drawPosture(self, posture):
        root = posture.skeleton.getRoot()

        # draw root
        glPushMatrix()

        J0 = posture.getJointTransMatrix(root)

        glMultMatrixf(J0.T)

        for n in root.children:
            self.drawBox(n.offset)
            self.drawBodyNode(posture, n) 

        glPopMatrix()

    def drawBody(self, skeleton, motion):
        posture = motion.getPosture(self.curFrame)
        root = skeleton.getRoot()

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

    def setViewPort(self, fovy = 140, aspect = 1, zNear = 1, zFar = 20):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(fovy, aspect, zNear, zFar)

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

    def render(self, lighting = False):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        if not self.fill:
            glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
        else:
            glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )

        self.setViewPort()

        # camera
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glMultMatrixf(self.camera.matrix.T)

        self.drawFrame()
        self.drawGrid()

        if lighting:
            self.setLighting()

        glPushMatrix()
        glRotatef(90, 0,1,0)
        glScalef(0.02,0.02,0.02)

        # draw bvhFile
        if self.skeleton is not None:
            glPushMatrix()
            self.setObjectColor(255,0,0)
            self.drawBody(self.skeleton, self.motion)
            glPopMatrix()

        # draw target pos for motion warping
        if self.motionWarp:
            glPushMatrix()
            self.setObjectColor(0,200,200)
            self.drawPosture(self.targetPosture)
            glPopMatrix()

        glPopMatrix()

        # lighting
        if lighting:
            self.unsetLighting()

        # kinematics
        if self.kinematics:
            glPushMatrix()
            self.setObjectColor(255, 255,0)
            
            # fk
            glPushMatrix()
            glRotatef(90, 0,1,0)
            glScalef(0.02,0.02,0.02)
            self.drawJointVelocity(self.skeleton, self.motion, self.targetJointIdx)
            # self.drawBody(self.kine_skel, self.kine_mot)
            glPopMatrix()
            
            self.drawBoxGlobal(self.targetPos[0],self.targetPos[1],self.targetPos[2])
            glPopMatrix()


        if self.skeleton is not None and self.playing:
            self.curFrame += 1
            self.curFrame %= self.motion.frames

    def setTargetPos(self, targetPos):
        self.targetPos = np.array(targetPos, dtype = np.float64)

    def setTargetJoint(self, idx):
        self.targetJointIdx = idx
        self.targetJoint = self.kine_skel.hierarchy[self.targetJointIdx]

    def drawJointVelocity(self, skeleton, motion, nodeIdx):
        if self.curFrame == 0 or nodeIdx == -1:
            return 

        curP = getGlobalPosition(skeleton, motion, nodeIdx, self.curFrame)

        if curP is None:
            return

        lastP = getGlobalPosition(skeleton, motion, nodeIdx, frame = self.curFrame - 1)
        v = getLinearVelocity(lastP, curP, motion.frame_time)
        
        # TODO erase below line
        v = 0.5*v

        self.drawLineGlobal(curP, curP + v)
        # print(v)
