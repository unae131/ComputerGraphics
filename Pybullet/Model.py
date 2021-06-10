from Dynamics.RigidSystem import computeTorque
from abc import *
import pybullet as p
import numpy as np
from Dynamics.RigidSystem import *


class Model(metaclass=ABCMeta):
    def __init__(self, linkIndices, jointIndices):
        self.jointIndices = jointIndices
        self.linkIndices = linkIndices # base는 별도
        self.id = -1

    @abstractmethod
    def createModel(self):
        pass

    def createBox(self,halfHeight = 0.5): # goal box
        id = p.createCollisionShape(p.GEOM_BOX, halfExtents=[halfHeight, halfHeight, halfHeight])
        return id

    def createCylinder(self, radius = 0.2, height = 0.3):
        id = p.createCollisionShape(p.GEOM_CYLINDER, radius=radius, height=height)
        return id

    def getWorldPositionsAndOrientations(self):
        basePos, baseOri = p.getBasePositionAndOrientation(self.id)

        positions = [list(basePos)]
        orientations = [list(baseOri)]

        for state in p.getLinkStates(self.id, self.linkIndices):
            positions.append(list(state[0]))
            orientations.append(list(state[1]))

        matrice = []
        for i in range(len(positions)):
            rotM = np.eye(4)
            rotM[:3,:3] = np.reshape(p.getMatrixFromQuaternion(orientations[i]), (3,3))
            matrice.append(rotM)

        return positions, matrice

    def pdControlMove(self, targetPositions, targetVelocities = None):
        # 3-dof인 것들만 고려함
        
        numJoints = p.getNumJoints(self.id)

        if targetVelocities is None:
            targetVelocities = np.full((numJoints, 3), 0.)

        curPositions = []
        curVelocities = []

        for jointState in p.getJointStatesMultiDof(self.id, self.jointIndices):
            state = list(jointState)
            
            axis, ang = p.getAxisAngleFromQuaternion(state[0])
            rotvec = ang * np.array(axis)

            curPositions.append(np.array(rotvec))
            curVelocities.append(np.array(state[1]))
        
        kp, kd = 500, 1
        torques = []
        for i in range(numJoints):
            torques.append(computeTorque(kp, kd, curPositions[i], curVelocities[i], targetPositions[i], targetVelocities[i]))

        p.setJointMotorControlMultiDofArray(self.id,
                                            self.jointIndices,
                                            p.TORQUE_CONTROL,
                                            forces=torques)

        p.stepSimulation()