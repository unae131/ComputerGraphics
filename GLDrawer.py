from Camera import *
from BvhParser import *
from Matrix import *
from Warping import *
from Model.PostureOperator import *

import math
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

class GlDrawer():
    def __init__(self, fileName, kinematics = False,targetJointIdx = 0, targetPos = [0,0,0]):
        self.skeleton, self.motion = readBVHfile(fileName)
        self.camera = Camera()
        self.curFrame = 0
        
        # TODO fill 고치기
        self.fill = False
        self.playing = False

        self.kinematics = kinematics
        self.kine_skel, self.kine_mot = readBVHfile(fileName)

        if targetJointIdx < 0 or targetJointIdx >= len(self.kine_skel.hierarchy):
            self.targetJointIdx = 0
        else:
            self.targetJointIdx = targetJointIdx

        self.targetJoint = self.kine_skel.hierarchy[self.targetJointIdx]
        self.targetPos = targetPos

        # time warp
        # self.motion = timeWarp(self.motion, halfScale, end_t= self.motion.frames)
        # self.motion = timeWarp(self.motion, doubleScale, end_t = self.motion.frames)
        # self.motion = timeWarp(self.motion, sinScale, end_t= self.motion.frames)

        # motion warp
        self.motionWarp = False
        if self.motionWarp:
            targetFrame = 100
            targetJoint = self.skeleton.hierarchy[2]
            self.targetPosture = self.motion.postures[targetFrame].copy()
            self.targetPosture.setNodeOrientation(targetJoint, self.targetPosture.getJointTransMatrix(targetJoint) @ getXRotMatrix(90))
            self.motion = motionWarp(self.motion, self.targetPosture, targetFrame, 80, 130)

        # motion stiching
        motion2 = readBVHfile("bvhFiles/02_04_run.bvh")[1]
        # self.motion = motionStitch(self.motion, motion2, motion2.frames-1)

        # blend motion
        motion2 = motionStitch(self.motion, motion2, motion2.frames-1).cutMotion(len(self.motion.postures), len(self.motion.postures) + len(motion2.postures)-1)
        self.motion = blendMotions(self.motion, motion2, 78, 47)

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

    def setViewPort(self, fovy = 120, aspect = 1, zNear = 1, zFar = 50):
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

        # draw bvhFile
        if self.skeleton is not None:
            glPushMatrix()
            glRotatef(90, 0,1,0)
            glScalef(0.02,0.02,0.02)
            self.setObjectColor(255,0,0)
            self.drawBody(self.skeleton, self.motion)

            glPopMatrix()

        # draw target pos for motion warping
        if self.motionWarp:
            glPushMatrix()
            glScalef(0.02,0.02,0.02)
            glRotatef(90, 0,1,0)
            self.setObjectColor(0,200,200)
            self.drawPosture(self.targetPosture)
            glPopMatrix()

        # lighting
        if lighting:
            self.unsetLighting()

        # kinematics
        if self.kinematics:
            glPushMatrix()
            self.setObjectColor(255, 255,0)
            self.drawBoxGlobal(self.targetPos[0],self.targetPos[1],self.targetPos[2])

            self.setObjectColor(0,255,0)
            
            # fk
            self.drawJointVelocity(self.skeleton, self.motion, self.targetJointIdx)
            self.drawBody(self.kine_skel, self.kine_mot)

            glPopMatrix()

        if self.skeleton is not None and self.playing:
            self.curFrame += 1
            self.curFrame %= self.motion.frames

    def setTargetPos(self, targetPos):
        self.targetPos = np.array(targetPos, dtype = np.float64)

    def setTargetJoint(self, idx):
        self.targetJointIdx = idx
        self.targetJoint = self.kine_skel.hierarchy[self.targetJointIdx]

    def getGlobalPosition(self, skeleton, motion, nodeIdx, frame = -1):        
        node = skeleton.hierarchy[nodeIdx]

        if frame == -1:
            frame = self.curFrame
        
        posture = motion.postures[frame]
        p = posture.getTotalTransMatrix(node) @ np.array([0,0,0,1], dtype=np.float64)
        return p[:3]

    def getGlobalOrientation(self, motion, node, frame = -1):
        if frame == -1:
            frame = self.curFrame

        posture = motion.postures[frame]
        R = np.eye(4, dtype=np.float64)

        while node.type != BvhNode.TYPE_ROOT:
            R = posture.getJointTransMatrix(node) @ R
            node = node.parent

        posture.getJointTransMatrix(node)
        R = posture.rootOrientMatrix @ R

        return R

    def getLinearVelocity(self, p0, p1, time):
        v = np.array(p1) - np.array(p0)
        v /= time

        return v

    def drawJointVelocity(self, skeleton, motion, nodeIdx):
        curP = self.getGlobalPosition(skeleton, motion, nodeIdx)

        if curP is None or self.curFrame == 0:
            return

        lastP = self.getGlobalPosition(skeleton, motion, nodeIdx, frame = self.curFrame - 1)
        v = self.getLinearVelocity(lastP, curP, motion.frame_time)
        self.drawLineGlobal(curP, curP + v)

    def limbIK(self, mid, end): # global target_pos
        skeleton = self.kine_skel
        motion = self.kine_mot
        target_pos = self.targetPos

        if mid is None:
            self.done = True
            return

        t = np.array(target_pos, dtype=np.float64)
        posture = motion.getPosture(self.curFrame)
        
        if mid.parent is None:
            b = self.getGlobalPosition(skeleton, motion, mid.idx)
            c = self.getGlobalPosition(skeleton, motion, end.idx)

            bc = np.linalg.norm(b-c)
            bt = np.linalg.norm(t-b)
            ct = np.linalg.norm(t-c)

            angCBT = getAngle(bc,bt,ct)[2]

            glob_midOrien = self.getGlobalOrientation(motion, mid)
            u = vecNormalize(np.cross(c-b,t-b))
            R_diff_mid = getRotMatrix(b, u, angCBT)
            glob_midOrien = R_diff_mid @ glob_midOrien
            
            M = posture.getTotalTransMatrix(mid)
            M = np.linalg.inv([M])[0]
            local_midOrien = M @ glob_midOrien
            posture.setJointTransMatrix(mid, local_midOrien)

            return

        base = mid.parent

        a = self.getGlobalPosition(skeleton, motion, base.idx)
        b = self.getGlobalPosition(skeleton, motion, mid.idx)
        c = self.getGlobalPosition(skeleton, motion, end.idx)

        ab = np.linalg.norm(a-b)
        bc = np.linalg.norm(b-c)
        ac = np.linalg.norm(c-a)
        ac1 = np.linalg.norm(t-a)

        if ac1 >= ab + bc: # 일직선으로 펴주기
            # base
            bt = np.linalg.norm(t-b)
            angBAT = getAngle(ab,ac1,bt)[2]

            glob_baseOrien = self.getGlobalOrientation(motion, base)
            u = vecNormalize(np.cross(b-a,t-a))
            R_diff_base = getRotMatrix(a, u, angBAT)
            glob_baseOrien = R_diff_base @ glob_baseOrien
            
            M = posture.getTotalTransMatrix(base)
            M = np.linalg.inv([M])[0]
            local_baseOrien = M @ glob_baseOrien
            posture.setJointTransMatrix(base, local_baseOrien)

            #mid
            b = self.getGlobalPosition(skeleton, motion, mid.idx)
            c = self.getGlobalPosition(skeleton, motion, end.idx)
            bt = np.linalg.norm(t-b)
            ct = np.linalg.norm(t-c)
            angCBT = getAngle(bc,bt,ct)[2]
            glob_midOrien = self.getGlobalOrientation(motion, mid)
            u = vecNormalize(np.cross(c-b,t-b))
            R_diff_mid = getRotMatrix(b, u, angCBT)
            glob_midOrien = R_diff_mid @ glob_midOrien
            
            M = posture.getTotalTransMatrix(mid)
            M = np.linalg.inv([M])[0]
            local_midOrien = M @ glob_midOrien
            posture.setJointTransMatrix(mid, local_midOrien)

            self.limbIK(base, end)
            return 
        
        A, B, C = getAngle(bc,ac,ab)
        A1, B1, C1 = getAngle(bc,ac1,ab)
        
        diff_A = (A - A1)*180 / np.pi
        diff_B = (B - B1)*180 / np.pi

        glob_baseOrien = self.getGlobalOrientation(motion, base)
        u = vecNormalize(np.cross(b-a,c-a))
        R_diff_base = getRotMatrix(a,u,diff_A)
        glob_baseOrien = R_diff_base @ glob_baseOrien
        
        # 로컬 계산하여 base에 적용
        M = posture.getTotalTransMatrix(base)
        M = np.linalg.inv([M])[0]
        local_baseOrien = M @ glob_baseOrien
        posture.setJointTransMatrix(base, local_baseOrien)

        b = self.getGlobalPosition(skeleton, motion, mid.idx)
        c = self.getGlobalPosition(skeleton, motion, end.idx)
        glob_midOrien = self.getGlobalOrientation(motion, mid)
        u = vecNormalize(np.cross(a-b,c-b))
        R_diff_mid = getRotMatrix(b, u, diff_B)
        glob_midOrien = R_diff_mid @ glob_midOrien
        
        # 로컬 계산하여 mid에 적용
        M = posture.getTotalTransMatrix(mid)
        M = np.linalg.inv([M])[0]
        local_midOrien = M @ glob_midOrien
        posture.setJointTransMatrix(mid, local_midOrien)

        # step2
        # b = self.getGlobalPosition(mid.idx)
        c = self.getGlobalPosition(skeleton, motion, end.idx)
        ct = np.linalg.norm(c-t)
        angCAT = getAngle(ac1,ac1,ct)[2]

        glob_baseOrien = self.getGlobalOrientation(motion, base)
        u = vecNormalize(np.cross(c-a,t-a))
        R_diff_base = getRotMatrix(a, u, angCAT)
        glob_baseOrien = R_diff_base @ glob_baseOrien
        
        # 로컬 계산하여 base에 적용
        M = posture.getTotalTransMatrix(base)
        M = np.linalg.inv([M])[0]
        local_baseOrien = M @ glob_baseOrien
        posture.setJointTransMatrix(base, local_baseOrien)
