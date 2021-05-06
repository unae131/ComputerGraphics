import numpy as np
from Matrix import *
from Model.BvhNode import BvhNode

class Posture():
    def __init__(self, skeleton, data = None):
        self.skeleton = skeleton
        self.jointTransMatrices = np.full(len(skeleton.hierarchy),None)
        self.linkTransMatrices = np.full(len(skeleton.hierarchy), None)
        self.totalTransMatrices = np.full(len(skeleton.hierarchy), None)

        if data is None:
            self.rootWorldPosition = np.array([0,0,0])
        else:
            self.rootWorldPosition = np.array(data[:3])
            
        for node in skeleton.hierarchy:
            self.initLinkTransMatrices(node)
            self.initJointTransMatrices(node, data)
            self.initTotalTransMatrices(node)

        self.rootWorldOrientMatrix = np.eye(4)
        self.rootWorldOrientMatrix[:3,:3] = self.jointTransMatrices[0][:3,:3]

    def initJointTransMatrices(self, node, data):
        M = np.eye(4)

        if node.type == node.TYPE_END_SITE or data is None:
            self.jointTransMatrices[node.idx] = M
            return

        if node.type == node.TYPE_ROOT:
            i = 3
        else:
            i = 0

        for channel in node.channels[-3:]:
            M = M @ self.getChannelmatrix(channel, data[node.chIdx + i])
            i+=1

        if node.type == node.TYPE_ROOT:
            self.rootWorldOrientMatrix = M
            M = self.getRootTransMatrix() @ M

        self.jointTransMatrices[node.idx] = M

    def initLinkTransMatrices(self, node):
        M = np.eye(4)

        if node.type == node.TYPE_ROOT:
            self.linkTransMatrices[node.idx] = M
            return

        M[:3,3] = node.offset

        self.linkTransMatrices[node.idx] = M

    def initTotalTransMatrices(self, node):
        idx = node.idx
        M = np.eye(4, dtype=np.float)
        
        while node is not None:
            M = self.getLinkMatrix(node) @ self.getJointTransMatrix(node) @ M
            node = node.parent

        self.totalTransMatrices[idx] = M

    # def initTotalTransMatrix(self, node, M = None):
    #     self.totalTransMatrices[node.idx] = M

    #     if node.type != node.TYPE_END_SITE:
    #         for n in node.children:
    #             self.initTotalTransMatrix(n)

    # def setJointTransMatrix(self, node, M):
    #     if node.type == node.TYPE_ROOT:
    #         M = self.getRootTransMatrix() @ M
    #     self.jointTransMatrices[node.idx] = M
    #     self.initTotalTransMatrix(node)

    def setRootWorldPosition(self, pos):
        self.rootWorldPosition = np.array(pos)
        self.jointTransMatrices[0][:3,3] = pos

        for node in self.skeleton.hierarchy:
            self.initTotalTransMatrices(node)
        
    def setRootWorldOrientMatrix(self, M):
        self.rootWorldOrientMatrix[:3,:3] = M[:3,:3]
        self.jointTransMatrices[0][:3,:3] = M[:3,:3]

        for node in self.skeleton.hierarchy:
            self.initTotalTransMatrices(node)

    def setNodeOrientation(self, node, M):
        if node.type == BvhNode.TYPE_END_SITE:
            return

        if node.idx == 0:
            self.setRootWorldOrientMatrix(M)
            return
        
        if M.shape != (4,4):
            newM = np.eye(4)
            newM[:3,:3] = M[:3,:3]
            M = newM

        self.jointTransMatrices[node.idx] = M

        for node in self.skeleton.hierarchy:
            self.initTotalTransMatrices(node)

    def getRootWorldPosition(self):
        return self.rootWorldPosition
    
    def getRootWorldOrienMatrix(self):
        return self.rootWorldOrientMatrix

    def getRootTransMatrix(self):
        T = np.eye(4)
        T[:3,3] = self.rootWorldPosition
        return T

    def getJointTransMatrix(self, node):
        return self.jointTransMatrices[node.idx]

    def getLinkMatrix(self, node):
        return self.linkTransMatrices[node.idx]

    def getTotalTransMatrix(self, node):
        return self.totalTransMatrices[node.idx]

    def getChannelmatrix(self, channel, value):
        if channel == BvhNode.CH_XROTATION:
            return getXRotMatrix(value)

        elif channel == BvhNode.CH_YROTATION:
            return getYRotMatrix(value)

        elif channel == BvhNode.CH_ZROTATION:
            return getZRotMatrix(value)

        elif channel == BvhNode.CH_XPOSITION:
            return getTransMatrix(value,0,0)

        elif channel == BvhNode.CH_YPOSITION:
            return getTransMatrix(0,value,0)
        
        elif channel == BvhNode.CH_ZPOSITION:
            return getTransMatrix(0,0,value)

        else:
            raise Exception("Wrong Channels")

    def print(self):
        print(self.rootWorldPosition, self.rootWorldOrientMatrix)
        
    def copy(self):
        newPosture = Posture(self.skeleton)
        newPosture.rootWorldOrientMatrix = np.array(self.rootWorldOrientMatrix)
        newPosture.rootWorldPosition = np.array(self.rootWorldPosition)
        newPosture.linkTransMatrices = np.array(self.linkTransMatrices)

        for i in range(len(self.skeleton.hierarchy)):
            newPosture.jointTransMatrices[i] = np.array(self.jointTransMatrices[i])
            newPosture.totalTransMatrices[i] = np.array(self.totalTransMatrices[i])

        return newPosture