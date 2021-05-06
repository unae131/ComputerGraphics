from Model.BvhNode import *
from Matrix import *
import numpy as np

class Kinematics():
    def __init__(self, skeleton, motion):
        self.skel = skeleton
        self.motion = motion
        self.targetJointIdx = 0

    def setTargetPos(self, targetPos):
        self.targetPos = np.array(targetPos, dtype = np.float64)

    def setTargetJoint(self, idx):
        self.targetJointIdx = idx
        self.targetJoint = self.skel.hierarchy[self.targetJointIdx]

    def getGlobalPosition(self, skeleton, motion, nodeIdx, frame):        
        node = skeleton.hierarchy[nodeIdx]
        posture = motion.postures[frame]
        p = posture.getTotalTransMatrix(node) @ np.array([0,0,0,1], dtype=np.float64)
        return p[:3]

    def getGlobalOrientation(self, motion, node, frame):
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

    def drawJointVelocity(self, skeleton, motion, nodeIdx, frame, drawer):
        curP = self.getGlobalPosition(skeleton, motion, nodeIdx, frame)

        if curP is None or frame == 0:
            return

        lastP = self.getGlobalPosition(skeleton, motion, nodeIdx, frame = self.curFrame - 1)
        v = self.getLinearVelocity(lastP, curP, motion.frame_time)
        drawer.drawLineGlobal(curP, curP + v)

    def limbIK(self, mid, end, frame): # global target_pos
        skeleton = self.skel
        motion = self.motion
        target_pos = self.targetPos

        if mid is None:
            self.done = True
            return

        t = np.array(target_pos, dtype=np.float64)
        posture = motion.getPosture(frame)
        
        if mid.parent is None:
            b = self.getGlobalPosition(skeleton, motion, mid.idx, frame)
            c = self.getGlobalPosition(skeleton, motion, end.idx, frame)

            bc = np.linalg.norm(b-c)
            bt = np.linalg.norm(t-b)
            ct = np.linalg.norm(t-c)

            angCBT = getAngle(bc,bt,ct)[2]

            glob_midOrien = self.getGlobalOrientation(motion, mid, frame)
            u = vecNormalize(np.cross(c-b,t-b))
            R_diff_mid = getRotMatrix(b, u, angCBT)
            glob_midOrien = R_diff_mid @ glob_midOrien
            
            M = posture.getTotalTransMatrix(mid)
            M = np.linalg.inv([M])[0]
            local_midOrien = M @ glob_midOrien
            posture.setJointTransMatrix(mid, local_midOrien)

            return

        base = mid.parent

        a = self.getGlobalPosition(skeleton, motion, base.idx, frame)
        b = self.getGlobalPosition(skeleton, motion, mid.idx, frame)
        c = self.getGlobalPosition(skeleton, motion, end.idx, frame)

        ab = np.linalg.norm(a-b)
        bc = np.linalg.norm(b-c)
        ac = np.linalg.norm(c-a)
        ac1 = np.linalg.norm(t-a)

        if ac1 >= ab + bc: # 일직선으로 펴주기
            # base
            bt = np.linalg.norm(t-b)
            angBAT = getAngle(ab,ac1,bt)[2]

            glob_baseOrien = self.getGlobalOrientation(motion, base, frame)
            u = vecNormalize(np.cross(b-a,t-a))
            R_diff_base = getRotMatrix(a, u, angBAT)
            glob_baseOrien = R_diff_base @ glob_baseOrien
            
            M = posture.getTotalTransMatrix(base)
            M = np.linalg.inv([M])[0]
            local_baseOrien = M @ glob_baseOrien
            posture.setJointTransMatrix(base, local_baseOrien)

            #mid
            b = self.getGlobalPosition(skeleton, motion, mid.idx, frame)
            c = self.getGlobalPosition(skeleton, motion, end.idx, frame)
            bt = np.linalg.norm(t-b)
            ct = np.linalg.norm(t-c)
            angCBT = getAngle(bc,bt,ct)[2]
            glob_midOrien = self.getGlobalOrientation(motion, mid, frame)
            u = vecNormalize(np.cross(c-b,t-b))
            R_diff_mid = getRotMatrix(b, u, angCBT)
            glob_midOrien = R_diff_mid @ glob_midOrien
            
            M = posture.getTotalTransMatrix(mid)
            M = np.linalg.inv([M])[0]
            local_midOrien = M @ glob_midOrien
            posture.setJointTransMatrix(mid, local_midOrien)

            self.limbIK(base, end, frame)
            return 
        
        A, B, C = getAngle(bc,ac,ab)
        A1, B1, C1 = getAngle(bc,ac1,ab)
        
        diff_A = (A - A1)*180 / np.pi
        diff_B = (B - B1)*180 / np.pi

        glob_baseOrien = self.getGlobalOrientation(motion, base, frame)
        u = vecNormalize(np.cross(b-a,c-a))
        R_diff_base = getRotMatrix(a,u,diff_A)
        glob_baseOrien = R_diff_base @ glob_baseOrien
        
        # 로컬 계산하여 base에 적용
        M = posture.getTotalTransMatrix(base)
        M = np.linalg.inv([M])[0]
        local_baseOrien = M @ glob_baseOrien
        posture.setJointTransMatrix(base, local_baseOrien)

        b = self.getGlobalPosition(skeleton, motion, mid.idx, frame)
        c = self.getGlobalPosition(skeleton, motion, end.idx, frame)
        glob_midOrien = self.getGlobalOrientation(motion, mid, frame)
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
        c = self.getGlobalPosition(skeleton, motion, end.idx, frame)
        ct = np.linalg.norm(c-t)
        angCAT = getAngle(ac1,ac1,ct)[2]

        glob_baseOrien = self.getGlobalOrientation(motion, base, frame)
        u = vecNormalize(np.cross(c-a,t-a))
        R_diff_base = getRotMatrix(a, u, angCAT)
        glob_baseOrien = R_diff_base @ glob_baseOrien
        
        # 로컬 계산하여 base에 적용
        M = posture.getTotalTransMatrix(base)
        M = np.linalg.inv([M])[0]
        local_baseOrien = M @ glob_baseOrien
        posture.setJointTransMatrix(base, local_baseOrien)
