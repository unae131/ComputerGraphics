import numpy as np

def getTransMatrix(x, y, z):
    T = np.eye(4)
    T[3,:3] = [x,y,z]
    return T

def getXRotMatrix(angle): # degree
    R = np.eye(4)
    angle = angle*np.pi/180
    R[1][1] = R[2][2] = np.cos(angle)
    R[2][1] = np.sin(angle)
    R[1][2] = - R[2][1]
    return R

def getYRotMatrix(angle): # degree
    R = np.eye(4)
    angle = angle*np.pi/180
    R[0][0] = R[2][2] = np.cos(angle)
    R[0][2] = np.sin(angle)
    R[2][0] = - R[0][2]
    return R

def getZRotMatrix(angle): # degree
    R = np.eye(4)
    angle = angle*np.pi/180
    R[0][0] = R[1][1] = np.cos(angle)
    R[1][0] = np.sin(angle)
    R[0][1] = - R[1][0]
    return R

def vecNormalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
        return v
    return v / norm

def getRotMatrix(pos, vec, rad):
    x,y,z = vec
    w = np.sqrt([y**2 + z**2])[0]

    T = getTransMatrix(pos[0],pos[1],pos[2])

    RX = np.eye(4, dtype=np.float64)
    RX[1][1] = RX[2][2] = z / w
    RX[1][2] = - y/w
    RX[2][1] = y/w

    RY = np.eye(4, dtype=np.float64)
    RY[0][0] = RY[2][2] = w
    RY[0][2]= -x
    RY[2][1] = x

    RZ = getZRotMatrix(rad)

    T_inv, RX_inv, RY_inv = np.linalg.inv([T, RX, RY])

    R_diff = T_inv @ RX_inv @ RY_inv @ RZ @ RY @ RX @ T

    return R_diff

def getAngle(a, b, c):
    if a == 0 or b == 0 or c == 0:
        return 0,0,0
    cosA = (b**2 + c**2 - a**2)/ 2*b*c
    cosB = (a**2 + c**2 - b**2)/ 2*a*c
    cosC = (a**2 + b**2 - c**2)/ 2*a*b
    return np.arccos(cosA),np.arccos(cosB),np.arccos(cosC)

def quaternionToMatrix(q):
    return np.array([[2*(q[0]**2 + q[1]**2) - 1, 2 * (q[1]*q[2] - q[0]*q[3]), 2 * (q[1] * q[3] + q[0] * q[2]), 0.],
                    [2*(q[1]*q[2] + q[0]*q[3]), 2*(q[0]**2 + q[2]**2)-1, 2*(q[2]*q[3] - q[0]*q[1]), 0.],
                    [2*(q[1]*q[3]-q[0]*q[2]), 2*(q[2]*q[3] + q[0]*q[1]), 2*(q[0]**2+q[3]**2)-1, 0.],
                    [0., 0., 0., 1.]])
