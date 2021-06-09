from Dynamics.Force import DampedSpring, Gravity
from Dynamics.ParticleSystem import Particle, ParticleSystem
import  numpy as np

class Simulator():
    def eulerstep(self, system, timestep):
        system.calculateForce()
        arr = system.getArray()
        newState = arr[:,:6] + timestep * self.derivative(arr)
        system.setParticles(newState)
        system.time += timestep
    
    def derivative(self, arr):
        vel = arr[:,3:6]
        acc = arr[:,6:9] / arr[:,9].reshape((len(arr),1))

        return np.concatenate((vel, acc), axis = 1)

    def midpointMethod(self, system, timestep):
        system.calculateForce()
        arr = system.getArray()
        deltaX = timestep * self.derivative(arr)

        Xarr = np.array(arr)
        Xarr[:,:6] += deltaX/2
        fmid = self.derivative(Xarr) / 2

        newState = arr[:,:6] + timestep * fmid
        system.setParticles(newState)
        system.time += timestep

    def testInit(self, ks = 650, kd = 5, timestep = 0.003):
        self.system = sys =  ParticleSystem([0.,1.,0.])
        self.timestep = timestep
        self.ks = ks
        self.kd = kd
        sys.particles.append(Particle([0.,1.,0.]))
        sys.particles.append(Particle([1.,1.,0.]))
        sys.particles.append(Particle([0.,2.,0.]))
        sys.particles.append(Particle([1.,2.,0.]))
        sys.particles.append(Particle([5.,2.,0.], [-1, -2, 0]))

        sys.particles.append(Particle([2.,4.,0.]))
        # sys.particles.append(Particle([2.,3.,0.]))
        
        sys.forces.append(Gravity(np.array(sys.particles), [0.,-9.8,0.]))

        sys.particles.append(Particle([-4., 2., 0.]))
        sys.particles.append(Particle([-1., 2., 0.]))

        sys.forces.append(DampedSpring(sys.particles[:2], 1, ks, kd))
        sys.forces.append(DampedSpring(sys.particles[2:4], 1, ks, kd))
        sys.forces.append(DampedSpring([sys.particles[0], sys.particles[2]], 1, ks, kd))
        sys.forces.append(DampedSpring([sys.particles[1], sys.particles[3]], 1, ks, kd))
        sys.forces.append(DampedSpring([sys.particles[0], sys.particles[3]], np.sqrt(2), ks, kd))
        sys.forces.append(DampedSpring(sys.particles[1:3], np.sqrt(2), ks, kd))
        # sys.forces.append(DampedSpring(sys.particles[:2], .3, ks, kd))
        sys.forces.append(DampedSpring(sys.particles[-2:], 1, ks, kd))

    def testRender(self, drawer):
        sys = self.system

        for p in sys.particles:
            drawer.drawBoxGlobal(p.position[0], p.position[1], p.position[2])

        for i in range(3):
            for j in range(1,4):
                drawer.drawLineGlobal(sys.particles[i].position, sys.particles[j].position)

        drawer.drawLineGlobal(sys.particles[-2].position, sys.particles[-1].position)

        # pos = sys.particles[-2].position
        # vel = sys.particles[-2].velocity

        iters = round(drawer.motion.frame_time / self.timestep)
        if iters == 0:
            iters = 1
        # print(iters)
        for i in range(iters):
            self.eulerstep(sys, self.timestep)
            # self.midpointMethod(sys, self.timestep)
        # sys.particles[-2].position = pos
        # sys.particles[-2].velocity = vel
        
        
