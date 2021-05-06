import numpy as np
from Model.BvhNode import *
from Model.Posture import *
from Model.Motion import *
from scipy.spatial.transform import Rotation as R
from scipy.spatial.transform import Slerp

def lerpPositions(position0, position1, t):
    position0 = np.array(position0)
    position1 = np.array(position1)

    return (1-t) * position0 + t * position1

def slerpEulerAngles(rotDir, a0, a1, t): # 0~1
    rot_matrices = R.from_euler(rotDir, [a0, a1], degrees=True)
    rot_tiems = [0,1]
    slerp = Slerp(rot_tiems, rot_matrices)

    times = [t]

    interpAngle = slerp(times).as_euler(rotDir, degrees=True).reshape(3,)

    return interpAngle

def interpolatePostures(P0, P1, t):
    skelNodes = P0.skeleton.hierarchy
    interPosture = Posture(P0.skeleton, P0.data)
    interPosture.data[:3] = lerpPositions(P0.getRootWorldPosition(), P1.getRootWorldPosition(), t)
    
    i = -1
    for node in skelNodes:
        if node.type == BvhNode.TYPE_END_SITE:
            continue

        i+=1

        rotDir = ""
        for ch in node.channels[-3:]:
            
            if ch == BvhNode.CH_XROTATION:
                rotDir += 'x'
            elif ch == BvhNode.CH_YROTATION:
                rotDir += 'y'
            else:
                rotDir += 'z'
        interPosture.data[i*3+3: i*3 + 6] = slerpEulerAngles(rotDir, P0.data[i*3+3: i*3 + 6], P1.data[i*3+3:i*3+6], t)
        
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
            break

        if frame % 1 == 0:
            newMotion.postures[i] = motion.getPosture(int(frame))
            continue

        p0 = motion.getPosture(int(frame))
        p1 = motion.getPosture(int(frame) + 1)
        newMotion.postures[i] = interpolatePostures(p0, p1, frame % 1)
    
    newMotion.frames = i
    newMotion.postures = newMotion.postures[:i]
    
    return newMotion

def doubleScale(t):
    return 2*t

def halfScale(t):
    return 0.5*t

def sinScale(t):
    return 198 * np.sin(np.pi / 2 * 1/198 * t)
