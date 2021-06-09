import matplotlib.pyplot as plt
from BvhParser import *
import numpy as np

class MatplotDrawer():

    def __init__(self, skeleton, motion, curFrame = 0):
        cmin, cmax = 0, 2
        self.color = np.array([(cmax - cmin) * np.random.random_sample() + cmin for i in range(len(skeleton.hierarchy))])
        self.skeleton = skeleton
        self.motion = motion
        self.curFrame = curFrame

    def drawCurrentPosture(self):
        posture = self.motion.getPosture(self.curFrame)
        self.drawPosture(self.skeleton, posture)
    
    def drawPosture(self, skeleton, posture):
        xs, ys, zs = [],[],[]
        for node in skeleton.hierarchy:
            position = posture.getTotalTransMatrix(node) @ np.array([0.,0.,0.,1.])
            xs.append(position[0])
            ys.append(position[1])
            zs.append(position[2])

        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(xs, ys, zs, c=self.color, marker='o', s=15, cmap='Greens')

if __name__ == "__main__":
    skeleton, motion = readBVHfile("bvhFiles/sample-walk.bvh")
    drawer = MatplotDrawer(skeleton, motion)

    while True:
        drawer.drawCurrentPosture()
        drawer.curFrame = (drawer.curFrame + 1) % motion.frames


