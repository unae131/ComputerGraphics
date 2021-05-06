from scipy.spatial.transform import Rotation as R
from scipy.spatial.transform import Slerp
from Model.Posture import *
import numpy as np

def add(o1, d):
    o2 = Posture(o1.skeleton)
    o2.setRootWorldPosition(o1.getRootWorldPosition() + d.getRootWorldPosition())

    for node in o2.skeleton.hierarchy:
        o2.setNodeOrientation(node, o1.getJointTransMatrix(node)@d.getJointTransMatrix(node))
    
    return o2

def sub(o2, o1):
    d = Posture(o1.skeleton)
    d.setRootWorldPosition(o2.getRootWorldPosition() - o1.getRootWorldPosition())
    
    for node in o2.skeleton.hierarchy:
        d.setNodeOrientation(node,o1.getJointTransMatrix(node).T@o2.getJointTransMatrix(node))
    
    return d

def scalarMult(c, d1):
    d2 = Posture(d1.skeleton)
    d2.setRootWorldPosition(c*d1.getRootWorldPosition())

    for node in d1.skeleton.hierarchy:
        rot = R.from_matrix([d1.getJointTransMatrix(node)[:3,:3]])
        rot_vec = c * rot.as_rotvec()

        rot = R.from_rotvec(rot_vec)
        M = rot.as_matrix()


        newMat = np.eye(4)
        newMat[:3,:3] = M

        d2.setNodeOrientation(node, newMat)
        
    return d2

    