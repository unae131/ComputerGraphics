from Model.Posture import *
import numpy as np

class PostureOperator():
    def add(o1, d):
        data = np.array(o1.data) + np.array(d.data)
        return Posture(o1.skeleton, data)

    def sub(o2, o1):
        data = np.array(o1.data) - np.array(d.data)
        return Posture(o1.skeleton, data)

    