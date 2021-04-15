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