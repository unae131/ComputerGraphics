from scipy.spatial.transform import Rotation as R
from scipy.spatial.transform import Slerp
from Posture import *
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
        rot_mat = R.from_matrix(d1.getJointTransMatrix(node)[:3,:3])
        rot_time = [1]

        slerp = Slerp(rot_time, rot_mat)

        newMat = np.eye(4)
        newMat[:3,:3] = slerp([c]).as_matrix()

        d2.setNodeOrientation(node, newMat)
        
    return d2

    