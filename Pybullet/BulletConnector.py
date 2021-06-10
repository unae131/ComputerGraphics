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

    def addModel(self, model):
        self.models.append(model)

    def render(self, draw_func):
        for model in self.models:
            model.move()
        
        # for model in self.models:
        #     positions, orientations = model.getWorldPositionsAndOrientations()

        #     for i in range(len(positions)):
        #         x, y, z = positions[i]
        #         ori = orientations[i]
        #         draw_func(x, y, z, ori, scale = 0.5)

