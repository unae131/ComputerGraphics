from scipy.spatial.transform import Rotation as R

def computeTorque(kp, kd, curOri, curAngVel, desiredOri, desiredAngVel):
    oriDiff = desiredOri - curOri
    angVelDiff = desiredAngVel - curAngVel
    torque = kp * oriDiff + kd * angVelDiff

    return torque