import numpy as np
from Matrix import *
from Model.BvhNode import BvhNode

class Posture():
    def __init__(self, skeleton, data):
        self.skeleton = skeleton
        self.data = data

        self.jointTransMatrices = np.full(len(skeleton.hierarchy), None)
        self.linkTransMatrices = np.full(len(skeleton.hierarchy), None)
        self.totalTransMatrices = np.full(len(skeleton.hierarchy), None)
        
        for node in skeleton.hierarchy:
            self.getJointTransMatrix(node)
            self.getLinkMatrix(node)
            self.getTotalTransMatrix(node)

    def setJointTransMatrix(self, node, M):
        if node.type == node.TYPE_ROOT:
            M = self.getRootTransMatrix() @ M
        self.jointTransMatrices[node.idx] = M
        self.initTotalTransMatrix(node)

    def initTotalTransMatrix(self, node, M = None):
        self.totalTransMatrices[node.idx] = M

        if node.type != node.TYPE_END_SITE:
            for n in node.children:
                self.initTotalTransMatrix(n)

    def getTotalTransMatrix(self, node):
        idx = node.idx

        if self.totalTransMatrices[idx] is None:
            M = np.eye(4, dtype=np.float)
            
            while node is not None:
                M = self.getLinkMatrix(node) @ self.getJointTransMatrix(node) @ M
                node = node.parent

            self.totalTransMatrices[idx] = M

        return self.totalTransMatrices[idx]

    def getRootWorldPosition(self):
        return self.data[:3]

    def getRootTransMatrix(self):
        T = np.eye(4)
        T[:3,3] = self.data[:3]

        return T

    def getJointTransMatrix(self, node):
        idx = node.idx

        if self.jointTransMatrices[idx] is None:
            M = np.eye(4)
            if node.type == node.TYPE_END_SITE:
                self.jointTransMatrices[idx] = M

            if node.type == node.TYPE_ROOT:
                i = 3
            else:
                i = 0
            
            for channel in node.channels[-3:]:
                M = M @ self.getChannelmatrix(channel, self.data[node.chIdx + i])
                i+=1

            if node.type == node.TYPE_ROOT:
                self.rootOrientMatrix = M
                M = self.getRootTransMatrix() @ M

            self.jointTransMatrices[idx] = M

        return self.jointTransMatrices[idx]

    def getLinkMatrix(self, node):
        idx = node.idx

        if self.linkTransMatrices[idx] is None:
            M = np.eye(4)

            if node.type != node.TYPE_ROOT:
                M[:3,3] = node.offset
            self.linkTransMatrices[idx] = M

        return self.linkTransMatrices[idx]

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
