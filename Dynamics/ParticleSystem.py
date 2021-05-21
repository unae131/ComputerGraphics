import numpy as np
from Dynamics.Force import *

class Particle():
    def __init__(self, pos, vel = [0.,0.,0.], force = [0.,0.,0.], mass = 1.):
        self.position = np.array(pos)
        self.velocity = np.array(vel)
        self.force = np.array(force)
        self.mass = mass
    
    def setPosition(self, pos):
        self.position = np.array(pos)

    def setVelocity(self, vel):
        self.velocity = np.array(vel)

    def setForce(self, force):
        self.force = np.array(force)

    def print(self):
        print("pvfm: ", self.position, self.velocity, self.force, self.mass)

class ParticleSystem():
    EPSILON = 0.0001

    def __init__(self, groundN = [0.,0.,1.]):
        self.particles = []
        self.time = 0.
        self.forces = []
        self.groundN = np.array(groundN)

    def calculateForce(self):
        for force in self.forces:
            force.apply()

        self.detectCollision(N = self.groundN)

    def detectCollision(self, N, P = np.array([0.,0.,0.])):
        contactingParticles = []

        for p in self.particles:
            constraint1 = np.dot((p.position- P), N)
            constratin2 = np.dot(N, p.velocity)

            if np.linalg.norm(constraint1) < self.EPSILON and np.linalg.norm(constratin2) < self.EPSILON: # contact
                print("contacting", p.position)
                contactingParticles.append(p)

            elif constraint1 < self.EPSILON and constratin2 < 0: # collision
                self.responseCollision(p, N)
                contactingParticles.append(p)
        
        Contact(contactingParticles).apply()
        Friction(contactingParticles).apply()
    
    def responseCollision(self, p, N, k = .8):
        Vn = np.dot(N, p.velocity) * N
        Vt = p.velocity - Vn
        p.velocity = Vt - k*Vn

    def getArray(self):
        arr = []
        for p in self.particles:
            arr.append(np.concatenate((p.position, p.velocity, p.force,[p.mass])))

        return np.array(arr)

    def setParticles(self, arr):
        for i in range(len(arr)):
            self.particles[i].setPosition(arr[i][:3])
            self.particles[i].setVelocity(arr[i][3:6])
            self.particles[i].setForce([0.,0.,0.])
        
    def print(self):
        for p in self.particles:
            p.print()
