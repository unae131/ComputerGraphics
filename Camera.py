import numpy as np
from Matrix import *

class Camera():
    def __init__(self, eye = [0.,-4.,6.], center = [0.,-1.,0.], up = [0.,1.,0.]):
        eye = np.array(eye, dtype=np.float32)
        center = np.array(center,dtype=np.float32)
        up = np.array(up,dtype=np.float32)

        forward = eye - center
        forward = vecNormalize(forward)

        side = np.cross(up, forward)
        side = vecNormalize(side)

        up = np.cross(forward, side)

        pos = [-eye.dot(side), -eye.dot(up), -eye.dot(forward)]

        M = np.eye(4)
        M[:3,0] = side
        M[:3,1] = up
        M[:3,2] = forward
        M[:3,3] = pos

        self.matrix = M
    
    def zoom(self, offset = 0.5):
        side = self.matrix[:3,0]
        up = self.matrix[:3,1]
        forward = self.matrix[:3,2]
        pos = self.matrix[:3,3]

        v = np.array([0.,0.,offset])

        pos += [v.dot(side), v.dot(up), v.dot(forward)]

        self.matrix[:3,3] = pos

    def orbit(self, azimuth, elevation): # degree
        R_Y = np.array([[np.cos(np.radians(azimuth)), 0. , np.sin(np.radians(azimuth)), 0.],
                        [0. , 1. , 0. , 0.],
                        [-np.sin(np.radians(azimuth)), 0., np.cos(np.radians(azimuth)), 0.],
                        [0., 0., 0., 1.]])


        R_X = np.array([[1., 0. , 0., 0.],
                        [0., np.cos(np.radians(elevation)), -np.sin(np.radians(elevation)), 0.],
                        [0., np.sin(np.radians(elevation)), np.cos(np.radians(elevation)), 0.],
                        [0., 0., 0., 1.]])

        self.matrix = R_X @ R_Y @ self.matrix

    def panning(self, x_trans, y_trans):
        T = np.array([[1.,0.,0.,x_trans],
                      [0.,1.,0.,y_trans],
                      [0.,0.,1.,0.],
                      [0.,0.,0.,1.]])

        self.matrix = T @ self.matrix