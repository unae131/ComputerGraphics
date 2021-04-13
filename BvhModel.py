import numpy as np

class BvhNode():
    TYPE_ROOT = "ROOT"
    TYPE_JOINT = "JOINT"
    TYPE_END_SITE = "END SITE"

    CH_XPOSITION = "XPOSITION"
    CH_YPOSITION = "YPOSITION"
    CH_ZPOSITION = "ZPOSITION"
    CH_XROTATION = "XROTATION"
    CH_YROTATION = "YROTATION"
    CH_ZROTATION = "ZROTATION"

    def __init__(self, nodeType, name, parent):
        self.type = nodeType
        self.name = name
        self.parent = parent

        if self.parent != None:
            self.parent.children.append(self)
        self.children = []
        
        self.offset = []
        # self.offsetMatrix = None
        self.channels = []

        self.idx = 0
        self.chIdx = 0

    def setOffset(self, offset):
        self.offset = np.array(offset)

    def setChannels(self, channels):
        self.channels = channels

    def getParent(self):
        return self.parent

    def getChannelNum(self):
        return len(self.channels)

    def hasChildren(self):
        if self.children is None or len(self.children) == 0:
            return False
        
        return True

class Skeleton(BvhNode):
    def __init__(self):
        self.hierarchy = []
        self.totalChNum = -1
        self.totalNodeNum = 0

    def addNode(self, nodeType, name, parent = None):
        node = BvhNode(nodeType, name, parent)
        node.idx = self.totalNodeNum

        self.totalNodeNum+=1
        self.hierarchy.append(node)

        if nodeType == self.TYPE_ROOT:
            node.chIdx = 0
            self.totalChNum = 6
        
        elif nodeType != self.TYPE_END_SITE:
            node.chIdx = self.totalChNum
            self.totalChNum += 3

        else:
            node.chIdx = self.totalChNum
        return node

    def getRoot(self):
        if len(self.hierarchy) == 0:
            return None

        return self.hierarchy[0]

    def countChannels(self, node):
        self.totalChNum += node.getChannelNum()

        for n in node.children:
            self.countChannels(n)

    def getTotalNodeNum(self):
        return len(self.hierarchy)

    def getTotalChannelNum(self):
        if self.totalChNum == -1:
            self.totalChNum = 0
            self.countChannels(self.hierarchy[0])

        return self.totalChNum

    def printHierarchy(self, node, indent = ""):
        print(node.idx, node.chIdx)
        print(indent + node.type, node.name)
        print(indent + "{")

        indent += "\t"

        print(indent + "OFFSET", str(node.offset))
        print(indent + "CHANNELS", str(len(node.channels)), str(node.channels))

        for n in node.children:
            self.printHierarchy(node = n, indent = indent)
        
        indent = indent[:-1]
        print(indent + "}")

class Motion():
    def __init__(self, skeleton, frames = 0, frame_time = 0.01):
        self.skeleton = skeleton
        self.frames = frames
        self.frame_time = frame_time
        self.postures = np.full(frames, None)
        self.curFrame = -1

    def setFrames(self, frames):
        self.frames = frames
        self.postures = np.full(frames, None)

    def setFrameTime(self, frame_time):
        self.frame_time = frame_time

    def setNextPosture(self, data):
        self.curFrame += 1
        self.curFrame %= self.frames
        return self.setPosture(self.curFrame, data)

    def setPosture(self, frame, data):
        if frame >= self.frames:
            return False

        if len(data) != self.skeleton.getTotalChannelNum():
            return False
        
        self.postures[frame] = Posture(self.skeleton, data)
        return True

    def getPosture(self, frame):
        return self.postures[frame]

    def print(self):
        print(self.skeleton)
        print(self.frames)
        print(self.frame_time)
        print(self.postures)

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
                # M = self.getChannelmatrix(channel, data) @ M

            if node.type == node.TYPE_ROOT:
                M = self.getRootTransMatrix() @ M
                # M = M @ self.getRootTransMatrix()

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
