import pybullet as p
import numpy as np
from Pybullet.Model import *
from Pybullet.SnakeModel import *
from Pybullet.BulletConnector import *
from scipy.spatial.transform import Rotation as R

import time

if __name__ == "__main__":
    bc = BulletConnector(0.00833333)

    snake = Snake(nodeLength = 0.25, gap = 0.)

    bc.addModel(snake)
    dt = 0.3

    while True:
        bc.render(None)
        
        # drawBoxGlobal(, x, y, z, ori = rotM, scale = 1.)
