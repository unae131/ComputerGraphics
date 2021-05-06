import numpy as np
from Model.Posture import Posture

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
        frame = frame % self.frames
        return self.postures[frame]

    def cutMotion(self, start, end):
        cut = Motion(self.skeleton, end - start + 1, self.frame_time)
        cut.postures = self.postures[start: end+1]
        return cut
        
    def print(self):
        print(self.skeleton)
        print(self.frames)
        print(self.frame_time)
        print(self.postures)