import numpy as np
from Model.Posture import *
from Model.Motion import *

def lerpPositions(position0, position1, t):
    position0 = np.array(position0)
    position1 = np.array(position1)

    return (1-t) * position0 + t * position1

def slerpOrientations(R0, R1, t):
    R0 = np.array(R0)[:3,:3]
    R1 = np.array(R1)[:3,:3]

    diff = R0.T @ R1

    # log
    theta = t * np.arccos((diff.trace() - 1)/2)
    sinTh = np.sin(theta)

    # TODO
    if sinTh == 0:
        R = np.eye(4)
        # print("theta is k*pi(",theta, ") in slerp")
        if theta == 0:
            R[:3,:3] = R0
        else:
            R[:3,:3] = R1
        return R

    vec = np.array([(diff[2][1] - diff[1][2]),
                    (diff[0][2] - diff[2][0]),
                    (diff[1][0] - diff[0][1])]) / ( 2 * sinTh)
    
    # exp
    cosTh = np.cos(theta)
    _cosTh = 1 - cosTh
    u = vec / np.linalg.norm(vec)
    expR = np.array([[cosTh + u[0]**2 * _cosTh, u[0] * u[1] * _cosTh - u[2] * sinTh, u[0] * u[2] * _cosTh + u[1] * sinTh],
                [u[1] * u[0] * _cosTh + u[2] * sinTh, cosTh + u[1]**2 * _cosTh, u[1] * u[2] * _cosTh-u[0] * sinTh],
                [u[2] * u[0] * _cosTh - u[1] * sinTh, u[2] * u[1] * _cosTh + u[0] * sinTh, cosTh + u[2]**2 * _cosTh]])

    slerped = np.eye(4)
    slerped[:3,:3] = R0 @ expR

    return slerped

def interpolatePostures(P0, P1, t):
    interPosture = Posture(P0.skeleton, P0.data)
    interPosture.data[:3] = lerpPositions(P0.getRootWorldPosition(), P1.getRootWorldPosition(), t)
    interPosture.linkTransMatrices = np.array(P0.linkTransMatrices)

    for i in range(len(P0.jointTransMatrices)):
        interPosture.jointTransMatrices[i] = slerpOrientations(P0.jointTransMatrices[i], P1.jointTransMatrices[i], t)
    return interPosture

def timeWarp(motion, scale_function, start_t = 0, end_t = 198):
    if scale_function(start_t) >= motion.frames:
        return None

    newMotion = Motion(motion.skeleton, end_t - start_t, motion.frame_time)

    i = -1
    for t in range(start_t, end_t):
        i+=1
        frame = scale_function(t)

        if frame >= motion.frames or frame < 0:
            newMotion.frames = i
            newMotion.postures = newMotion.postures[:i]
            return newMotion

        if frame % 1 == 0:
            newMotion.postures[i] = motion.getPosture(int(frame))
            continue

        p0 = motion.getPosture(int(frame))
        p1 = motion.getPosture(int(frame) + 1)
        newMotion.postures[i] = interpolatePostures(p0, p1, frame % 1)
    
    return newMotion

def doubleScale(t):
    return 2*t

def sinScale(t):
    return 198 * np.sin(np.pi / 2 * 1/198 * t)
