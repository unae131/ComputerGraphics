import pybullet as p
import pybullet_data
import numpy as np
from Pybullet.Model import *
from scipy.spatial.transform import Rotation as R

class Snake(Model):
    def __init__(self, nodeNum=10, nodeLength = 0.5, gap = 0.):
        self.radius = 0.1
        self.nodeNum = nodeNum
        self.nodeLength = nodeLength
        self.jointNum = self.nodeNum - 1
        self.gap = gap

        jointIndices = np.arange(0, self.jointNum, 1).tolist()
        linkIndices = np.arange(0, self.jointNum, 1).tolist() # base는 별도
        super().__init__(jointIndices, linkIndices)

        nodeId = self.createBox(nodeLength/2)
        self.id = self.createModel(nodeId, 1, [0,0,0.5], p.getQuaternionFromEuler([np.pi/2,0,0]))

        self.changeDynamics()
        self.waveFront = 0.

    def createModel(self, nodeId, baseMass, basePosition, baseQuaternionOrientation):
        linkMasses = []
        linkCollisionShapeIndices = []
        linkVisualShapeIndices = []
        linkPositions = []
        linkOrientations = []
        linkInertialFramePositions = []
        linkInertialFrameOrientations = []
        linkParentIndices = []
        linkJointTypes = []
        linkJointAxis = []
        linkJointAxis = []

        for i in range(self.jointNum):
            linkMasses.append(baseMass) # 0 makes link static
            linkCollisionShapeIndices.append(nodeId)
            linkVisualShapeIndices.append(-1)
            linkPositions.append([0, 0, self.nodeLength + self.gap])
            linkOrientations.append([0, 0, 0, 1])
            linkInertialFramePositions.append([0, 0, 0])
            linkInertialFrameOrientations.append([0, 0, 0, 1])
            linkParentIndices.append(i)
            linkJointTypes.append(p.JOINT_SPHERICAL)
            linkJointAxis.append([0, 1, 0])

        # create rigid objects by shapes
        boneId = p.createMultiBody(baseMass, nodeId, -1, basePosition, baseQuaternionOrientation,
                                    linkMasses=linkMasses,
                                    linkCollisionShapeIndices=linkCollisionShapeIndices,
                                    linkVisualShapeIndices=linkVisualShapeIndices,
                                    linkPositions=linkPositions,
                                    linkOrientations=linkOrientations,
                                    linkInertialFramePositions=linkInertialFramePositions,
                                    linkInertialFrameOrientations=linkInertialFrameOrientations,
                                    linkParentIndices=linkParentIndices,
                                    linkJointTypes=linkJointTypes,
                                    linkJointAxis=linkJointAxis)

        # remove collisions
        for i in range(-1, self.jointNum):
            p.setCollisionFilterGroupMask(boneId, i, 0, 0)
            p.setCollisionFilterPair(0, boneId, -1, i, 1)
        
        return boneId

    def changeDynamics(self, anistropicFriction = [1,0.01,0.01], lateralFriction=2): # default anistropicFriction : move to X dir
        p.changeDynamics(self.id, -1, lateralFriction=lateralFriction, anisotropicFriction=anistropicFriction)

        for i in range(self.jointNum):
            p.changeDynamics(self.id, i, lateralFriction=lateralFriction, anisotropicFriction=anistropicFriction)

    def move(self, steering=0.0, forces = 10, dt = 1./1200., wavePeriod = 1.5, waveLength = 4, waveAmplitude = 0.4):
        segmentLength = self.gap + self.nodeLength
        scaleStart = 1.0
        waveFront = self.waveFront

        # start waves
        if (waveFront < segmentLength * 4.0):
            scaleStart = waveFront / (segmentLength * 4.0)

        # targetPositions = np.full((self.jointNum, 4), None)
        for joint in range(self.jointNum):
            segment = joint #self.jointNum - 1 - joint

            # map segment to phase
            phase = (waveFront - (segment + 1) * segmentLength) / waveLength
            phase -= np.floor(phase)
            phase *= np.pi * 2.0

            # map phase to curvature
            pos = np.sin(phase) * scaleStart * waveAmplitude

            # steering = jointXYZActions[joint*4+1]
            if (steering > 0 and pos < 0):
                pos *= 1.0 / (1.0 + steering)

            if (steering < 0 and pos > 0):
                pos *= 1.0 / (1.0 - steering)

            pos += steering

            p.setJointMotorControlMultiDof(self.id,
                                joint,
                                p.POSITION_CONTROL,
                                # targetPosition=targetPos + m_steering,
                                # targetPosition=[0.,0,targetPos,1.],
                                targetPosition=p.getQuaternionFromEuler([0.,pos, 0.]),
                                force=[forces]) 

        # p.setJointMotorControlMultiDofArray(self.boneId,
        #                                     self.jointIndices,
        #                                     p.POSITION_CONTROL,
        #                                     targetPositions,
        #                                     forces=forces)
        self.waveFront += dt / wavePeriod * waveLength
        
        p.stepSimulation()

