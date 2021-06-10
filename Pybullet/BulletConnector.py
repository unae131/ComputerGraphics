import pybullet as p
import pybullet_data
from Drawer.GlDrawer import *

class BulletConnector():
    def __init__(self, timestep = 0.03):
        self.client = p.connect(p.GUI) # or p.DIRECT for non-graphical version
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        p.loadURDF("plane.urdf")
        p.setGravity(0, 0, -10)

        self.models = []
        self.timestep = timestep
        p.setTimeStep(timestep)
        p.stepSimulation()

        # sin test
        self.waveFront = 0.
        
    def addModel(self, model):
        self.models.append(model)

    def render(self, draw_func = None):
        for model in self.models:
            # model.move()

            targetPositions = self.getSinTarget(p.getNumJoints(model.id), model.nodeLength)
            model.pdControlMove(targetPositions)
        
        if draw_func is not None:
            for model in self.models:
                positions, orientations = model.getWorldPositionsAndOrientations()

                for i in range(len(positions)):
                    x, y, z = positions[i]
                    ori = orientations[i]
                    draw_func(x, y, z, ori, scale = model.nodeLength)

    def getSinTarget(self, numJoints, segmentLength, dt = 1./360., wavePeriod = 1.5, waveLength = 4, waveAmplitude = 0.4):
        scaleStart = 1.0
        waveFront = self.waveFront

        # start waves
        if (waveFront < segmentLength * 4.0):
            scaleStart = waveFront / (segmentLength * 4.0)

        targetPositions = np.full((numJoints, 3), None)
        for joint in range(numJoints):
            segment = joint #self.jointNum - 1 - joint

            # map segment to phase
            phase = (waveFront - (segment + 1) * segmentLength) / waveLength
            phase -= np.floor(phase)
            phase *= np.pi * 2.0

            # map phase to curvature
            pos = np.sin(phase) * scaleStart * waveAmplitude

            targetPositions[joint] = [0., pos, 0.]

        self.waveFront += dt / wavePeriod * waveLength

        return targetPositions


