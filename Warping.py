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

def timeWarp(motion, scale_function, start_t = 0, end_t = 298, s = 1):
    if scale_function == scale and scale(start_t, s) >= motion.frames:
        return None

    elif scale_function != scale and scale_function(start_t) >= motion.frames:
        return None

    newPostures = []
    t = -1
    while True:
        t+=1
        frame = scale_function(t) if scale_function != scale else scale_function(t,s)

        # print(t, frame, motion.frames)
        if frame < start_t or frame > end_t:
            break

        if frame % 1 == 0:
            newPostures.append(motion.getPosture(int(frame)))
            continue

        p0 = motion.getPosture(int(frame))
        p1 = motion.getPosture(int(frame) + 1)
        newPostures.append(interpolatePostures(p0, p1, frame % 1))
    
    newMotion = Motion(motion.skeleton, frames = len(newPostures), frame_time=motion.frame_time)
    newMotion.postures = newPostures
    
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

    m2 = motionWarp(m2, add(m2_first, d), 0, 0, length)

    stitched = Motion(m1.skeleton, frames = m1.frames + m2.frames, frame_time= m1.frame_time)
    # print(m1.frames, m2.frames, stitched.frames)
    stitched.postures[:m1.frames] = m1.postures
    stitched.postures[-m2.frames:] = m2.postures

    return stitched

def blendMotions(m1, m2, m1_step_len, m2_step_len): # length of two motions are same
    m1_step = Motion(m1.skeleton, frames = m1_step_len)
    m1_step.postures = m1.postures[-m1_step_len:]

    m2_step = Motion(m2.skeleton, frames = m2_step_len)
    m2_step.postures = m2.postures[:m2_step_len]

    length = int((m1_step_len + m2_step_len) / 2)

    scaled_m1_step = timeWarp(m1_step, scale, 0, m1_step_len, m1_step_len/length)
    scaled_m2_step = timeWarp(m2_step, scale, 0, m2_step_len, m2_step_len/length)
    length = min(length, len(scaled_m1_step.postures), len(scaled_m2_step.postures))

    scaled_m1_step.frames = scaled_m2_step.frames = length
    scaled_m1_step.postures = scaled_m1_step.postures[-length:]
    scaled_m2_step.postures = scaled_m2_step.postures[:length]

    # print(m1_step_len, m2_step_len, length)
    # print(len(scaled_m1_step.postures), len(scaled_m2_step.postures))
    
    interp_postures = np.full(length, None)
    for t in range(length):
        c = cosTransition(t, length)
        interp_postures[t] = add(scalarMult(c, scaled_m1_step.postures[t]),
                                 scalarMult((1-c), scaled_m2_step.postures[t]))

    front_len = len(m1.postures) - m1_step_len
    rear_len = len(m2.postures) - m2_step_len
    print(front_len, front_len + length, front_len+length +rear_len)

    blend = Motion(m1.skeleton, frames = front_len + length + rear_len, frame_time= m1.frame_time)
    blend.postures[:front_len] = m1.postures[:front_len]
    blend.postures[front_len:front_len + length] = interp_postures
    blend.postures[front_len+length:front_len+length+rear_len] = m2.postures[-rear_len:]

    return blend

def scale(t, s):
    return s*t

def doubleScale(t):
    return 2*t

def halfScale(t):
    return 0.5*t

def sinScale(t):
    return 299 * (np.sin(np.pi * t / 299 - np.pi/2) + 1)

def cosTransition(t, length = 484):
    return 1/2 * np.cos(np.pi/length * t) + 1/2
