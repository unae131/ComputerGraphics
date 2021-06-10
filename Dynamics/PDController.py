class PDController():
    def __init__(self, kp, kd):
        self.kp = kp
        self.kd = kd

    def computeTorque(self, curOri, curAngVel, desiredOri, desiredAngVel):
        oriDiff = desiredOri - curOri
        angVelDiff = desiredAngVel - curAngVel
        torque = self.kp * oriDiff + self.kd * angVelDiff

        return torque