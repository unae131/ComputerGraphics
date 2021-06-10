from Dynamics.PDController import PDController
import pybullet as p
import pybullet_data
from Drawer.GlDrawer import *
from Bullet.SnakeModel import *

class DrawerConnector():
    def __init__(self, timestep = 0.03, pdControl = True):
        self.client = p.connect(p.GUI) # or p.DIRECT for non-graphical version
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        p.loadURDF("plane.urdf")
        p.setGravity(0, 0, -10)

        self.models = []
        self.timestep = timestep
        p.setTimeStep(timestep)

        if pdControl:
            self.pdController = PDController(500, 1)
        else:
            self.pdController = None

        # for test
        self.addModel(Snake(nodeLength = 0.25))

    def addModel(self, model):
        self.models.append(model)

    def render(self, draw_func = None):
        for model in self.models:
            if self.pdController is None:
                model.move()
            else:
                model.pdControlMove(self.pdController.computeTorque)
        
        if draw_func is not None:
            for model in self.models:
                positions, orientations = model.getWorldPositionsAndOrientations()

                for i in range(len(positions)):
                    x, y, z = positions[i]
                    ori = orientations[i]
                    draw_func(x, y, z, ori, scale = model.nodeLength)

    


