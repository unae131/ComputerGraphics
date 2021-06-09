from abc import *
import numpy as np

class Force(metaclass=ABCMeta):
    def __init__(self, particles = []):
        self.particles = list(particles)

    def addParticle(self, p):
        self.particles.append(p)

    def deleteParticle(self, p):
        try:
            self.particles.remove(p)
        except ValueError:
            print("ValueError")

    @abstractmethod
    def apply(self):
        pass

class Gravity(Force):
    def __init__(self, particles, g = [0.,0.,-9.8]):
        self.particles = particles
        self.G = np.array(g)

    def apply(self):
        for p in self.particles:
            p.force += p.mass * self.G

class DampedSpring(Force):
    def __init__(self, particles, r, ks = 650, kd = 5):
        super().__init__(particles)
        self.KS = ks
        self.KD = kd
        self.r = r

    def apply(self):
        for i in range(len(self.particles)-1):
            for j in range(i+1, len(self.particles)):
                p1 = self.particles[i]
                p2 = self.particles[j]

                deltaX = p1.position - p2.position
                norm_deltaX = np.linalg.norm(deltaX)
                deltaV = p1.velocity - p2.velocity

                f1 = -(self.KS*(norm_deltaX - self.r) 
                        + self.KD * (np.dot(deltaV, deltaX) / norm_deltaX))*deltaX/norm_deltaX
                
                p1.force += f1
                p2.force -= f1

class Contact(Force):
    def __init__(self, particles = [], norm_vec = [0.,0.,1.]):
        super().__init__(particles)
        self.norm_vec = np.array(norm_vec)

    def apply(self):
        for p in self.particles:
            Fn = np.dot(self.norm_vec, p.force) * self.norm_vec
            Ft = p.force - Fn
            p.force -= Ft

class Friction(Force):
    def __init__(self, particles, us = 1.5, uk = 0.6, norm_vec = [0.,0.,1.]):
        super().__init__(particles)
        self.US = us
        self.UK = uk
        self.norm_vec = np.array(norm_vec)

    def apply(self): #힘이 아래로 향해야함
        for p in self.particles:
            Fn = np.dot(self.norm_vec, p.force) * self.norm_vec

            if p.velocity.sum() == 0: # 정지마찰
                p.force -= self.US * np.linalg.norm(Fn)
                continue
            
            Vn = np.dot(self.norm_vec, p.velocity) * self.norm_vec
            Vt = p.velocity - Vn
            norm_Vt = np.linalg.norm(Vt)

            if norm_Vt != 0:
                p.force -= self.UK * np.linalg.norm(Fn) * Vt / np.linalg.norm(Vt)

