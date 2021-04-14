from Model.BvhNode import *

class Skeleton():
    def __init__(self):
        self.hierarchy = []
        self.totalChNum = -1
        self.totalNodeNum = 0

    def addNode(self, nodeType, name, parent = None):
        node = BvhNode(nodeType, name, parent)
        node.idx = self.totalNodeNum

        self.totalNodeNum+=1
        self.hierarchy.append(node)

        if nodeType == BvhNode.TYPE_ROOT:
            node.chIdx = 0
            self.totalChNum = 6
        
        elif nodeType != BvhNode.TYPE_END_SITE:
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
