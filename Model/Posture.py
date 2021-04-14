import numpy as np
from Model.BvhNode import BvhNode

class Posture():
    def __init__(self, skeleton, data):
        self.skeleton = skeleton
        self.data = data
        self.jointTransMatrices = np.full(len(skeleton.hierarchy), None)
        self.linkTransMatrices = np.full(len(skeleton.hierarchy), None)

    def getJointTransMatrix(self, node):
        if node.type == node.TYPE_END_SITE:
            return np.eye(4)

        idx = node.idx

        if self.jointTransMatrices[idx] is None:
            M = np.eye(4)

            if node.type == node.TYPE_ROOT:
                i = 3
            else:i = 0
            
            for channel in node.channels[-3:]:
                M = M @ self.getChannelmatrix(channel, self.data[node.chIdx + i])
                i+=1

            if node.type == node.TYPE_ROOT:
                M = self.getRootTransMatrix() @ M

            self.jointTransMatrices[idx] = M

        return self.jointTransMatrices[idx]

    def getRootTransMatrix(self):
        T = np.eye(4)
        T[:3,3] = self.data[:3]

        return T

    def getLinkMatrix(self, node):
        if node.type == node.TYPE_ROOT:
            return np.eye(4)

        idx = node.idx

        if self.linkTransMatrices[idx] is None:
            M = np.eye(4)
            M[:3,3] = node.offset
            self.linkTransMatrices[idx] = M

        return self.linkTransMatrices[idx]

    def getChannelmatrix(self, channel, value):
        if channel == BvhNode.CH_XROTATION:
            return self.getXRotMatrix(value)

        elif channel == BvhNode.CH_YROTATION:
            return self.getYRotMatrix(value)

        elif channel == BvhNode.CH_ZROTATION:
            return self.getZRotMatrix(value)

        elif channel == BvhNode.CH_XPOSITION:
            return self.getXTransMatrix(value)

        elif channel == BvhNode.CH_YPOSITION:
            return self.getYTransMatrix(value)
        
        elif channel == BvhNode.CH_ZPOSITION:
            return self.getZTransMatrix(value)

        else:
            raise Exception("Wrong Channels")

    def getXTransMatrix(self, x):
        T = np.eye(4)
        T[0][3] = x
        return T

    def getYTransMatrix(self, y):
        T = np.eye(4)
        T[1][3] = y
        return T

    def getZTransMatrix(self, z):
        T = np.eye(4)
        T[2][3] = z
        return T

    def getXRotMatrix(self, angle): # degree
        R = np.eye(4)
        angle = angle*np.pi/180
        R[1][1] = R[2][2] = np.cos(angle)
        R[2][1] = np.sin(angle)
        R[1][2] = - R[2][1]
        return R

    def getYRotMatrix(self, angle): # degree
        R = np.eye(4)
        angle = angle*np.pi/180
        R[0][0] = R[2][2] = np.cos(angle)
        R[0][2] = np.sin(angle)
        R[2][0] = - R[0][2]
        return R
    
    def getZRotMatrix(self, angle): # degree
        R = np.eye(4)
        angle = angle*np.pi/180
        R[0][0] = R[1][1] = np.cos(angle)
        R[1][0] = np.sin(angle)
        R[0][1] = - R[1][0]
        return R
