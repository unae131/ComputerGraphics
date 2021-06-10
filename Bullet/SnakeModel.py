import pybullet as p
import numpy as np
from Bullet.Model import *
from scipy.spatial.transform import Rotation as R

class Snake(Model):
    def __init__(self, numNodes=10, nodeLength = 0.5, gap = 0.):
        self.radius = 0.1
        self.numNodes = numNodes
        self.numJoints = numNodes - 1
        self.nodeLength = nodeLength
        self.jointNum = self.numNodes - 1
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

    def move(self):
        p.setJointMotorControlMultiDofArray(self.id,
                            self.jointIndices,
                            p.POSITION_CONTROL,
                            targetPositions= self.getSinTargetPositions())

        p.stepSimulation()

    def pdControlMove(self, controller, targetPositions = None, targetVelocities = None):
        numJoints = p.getNumJoints(self.id)

        if targetPositions is None: # default sin move
            targetPositions = []

            for pos in self.getSinTargetPositions():
                axis, ang = p.getAxisAngleFromQuaternion(pos)
                targetPositions.append(np.array(axis) * ang)

        if targetVelocities is None:
            targetVelocities = np.full((numJoints, 3), 0.)

        curPositions = []
        curVelocities = []

        for jointState in p.getJointStatesMultiDof(self.id, self.jointIndices):
            state = list(jointState)
            
            axis, ang = p.getAxisAngleFromQuaternion(state[0])

            curPositions.append(np.array(ang * np.array(axis)))
            curVelocities.append(np.array(state[1]))
        
        torques = []
        for i in range(numJoints):
            torques.append(controller.computeTorque(curPositions[i], curVelocities[i], targetPositions[i], targetVelocities[i]))

        p.setJointMotorControlMultiDofArray(self.id,
                                            self.jointIndices,
                                            p.TORQUE_CONTROL,
                                            forces=torques)
        p.stepSimulation()

    def getSinTargetPositions(self, dt = 1./360., wavePeriod = 1.5, waveLength = 4, waveAmplitude = 0.4):
        segmentLength = self.nodeLength + self.gap
        scaleStart = 1.0
        waveFront = self.waveFront

        # start waves
        if (waveFront < segmentLength * 4.0):
            scaleStart = waveFront / (segmentLength * 4.0)

        targetPositions = np.full((self.numJoints), None)
        for joint in range(self.numJoints):
            segment = joint #self.jointNum - 1 - joint

            # map segment to phase
            phase = (waveFront - (segment + 1) * segmentLength) / waveLength
            phase -= np.floor(phase)
            phase *= np.pi * 2.0

            # map phase to curvature
            pos = np.sin(phase) * scaleStart * waveAmplitude

            targetPositions[joint] = p.getQuaternionFromEuler([0., pos, 0.])

        self.waveFront += dt / wavePeriod * waveLength

        return targetPositions
