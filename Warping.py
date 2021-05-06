import numpy as np
from Model.BvhNode import *
from Model.Posture import *
from Model.Motion import *
from Model.PostureOperator import *
from scipy.spatial.transform import Rotation as R
from scipy.spatial.transform import Slerp

def lerpPositions(position0, position1, t):
    position0 = np.array(position0)
    position1 = np.array(position1)

    return (1-t) * position0 + t * position1

def slerpMatrix(rotDir, R0, R1, t): # 0~1
    rot_matrices = R.from_matrix([R0[:3,:3], R1[:3,:3]])
    rot_tiems = [0,1]
    slerp = Slerp(rot_tiems, rot_matrices)

    times = [t]

    interpR = np.eye(4)
    interpR[:3,:3] = slerp(times).as_matrix()

    return interpR

def interpolatePostures(P0, P1, t): # t : 0~1, have same skel
    newP = Posture(P0.skeleton)
    newP.setRootWorldPosition(lerpPositions(P0.getRootWorldPosition(), P1.getRootWorldPosition(), t))
    
    i = -1
    for node in P0.skeleton.hierarchy:
        i+=1

        if node.type == BvhNode.TYPE_END_SITE:
            continue

        rotDir = ""
        for ch in node.channels[-3:]:
            
            if ch == BvhNode.CH_XROTATION:
                rotDir += 'x'
            elif ch == BvhNode.CH_YROTATION:
                rotDir += 'y'
            else:
                rotDir += 'z'

        newM = slerpMatrix(rotDir,P0.getJointTransMatrix(node), P1.getJointTransMatrix(node), t)
        newP.setNodeOrientation(node, newM)
        
    return newP

def timeWarp(motion, scale_function, start_t = 0, end_t = 298):
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

def motionWarp(motion, targetPos, targetFrame, transStartFrame, transEndFrame):
    warpedMotion = Motion(motion.skeleton, motion.frames, motion.frame_time)
    warpedMotion.postures = motion.postures

    diffPos = sub(targetPos, motion.getPosture(targetFrame))

    frontTransLen = targetFrame - transStartFrame + 1
    for i in range(frontTransLen - 1):
        d = scalarMult(i/(frontTransLen-1), diffPos)
        warpedMotion.postures[transStartFrame + i] = add(warpedMotion.postures[transStartFrame+i], d)

    warpedMotion.postures[targetFrame] = add(warpedMotion.postures[targetFrame], diffPos)

    rearTransLen = transEndFrame - targetFrame
    for i in range(1, rearTransLen+1):
        j = rearTransLen - i
        d = scalarMult(j/rearTransLen, diffPos)
        warpedMotion.postures[targetFrame + i] = add(warpedMotion.postures[targetFrame + i], d)

    return warpedMotion

def motionStitch(m1, m2, length):
    m1_last = m1.postures[m1.frames-1]
    m2_first = m2.postures[0]

    m1_last_p = m1_last.getRootWorldPosition()
    m1_last_R = m1_last.getRootWorldOrienMatrix()
    m2_first_p = m2_first.getRootWorldPosition()
    m2_first_R = m2_first.getRootWorldOrienMatrix()

    diff_p = m1_last_p - m2_first_p
    diff_p[1] = 0

    diff = (m1_last_R @ m2_first_R.T)[:3,:3]
    rotVec = R.from_matrix([diff]).as_rotvec().reshape(3,)
    rotVec[0] = rotVec[2] = 0

    diff_R = np.eye(4)
    diff_R[:3,:3] = R.from_rotvec(rotVec).as_matrix().reshape(3,3)

    for posture in m2.postures:
        p = posture.getRootWorldPosition()
        RotMat = posture.getRootWorldOrienMatrix()
        posture.setRootWorldPosition(diff_R[:3,:3] @ (p - m2_first_p) + m2_first_p + diff_p)
        posture.setRootWorldOrientMatrix(diff_R @ RotMat)

    d = sub(m1_last, m2_first)

    m2 = motionWarp(m2, add(m2_first, d), 0, 0, 200)

    stitched = Motion(m1.skeleton, frames = m1.frames + m2.frames, frame_time= m1.frame_time)
    print(m1.frames, m2.frames, stitched.frames)
    stitched.postures[:m1.frames] = m1.postures
    stitched.postures[-m2.frames:] = m2.postures

    return stitched

def doubleScale(t):
    return 2*t

def halfScale(t):
    return 0.5*t

def sinScale(t):
    return 298 * np.sin(np.pi / 2 * 1/298 * t)

def conScale(t, length = 484):
    return np.cos(np.pi * 1/length * t) + 1
