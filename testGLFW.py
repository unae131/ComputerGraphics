import glfw
from OpenGL.GL import *
import numpy as np
from OpenGL.GLU import *

gCamAng = 0

def getXTransMatrix(x):
    T = np.eye(4)
    T[0][3] = x
    return T

def getYTransMatrix(y):
    T = np.eye(4)
    T[1][3] = y
    return T

def getZTransMatrix(z):
    T = np.eye(4)
    T[2][3] = z
    return T

def getXRotMatrix(angle): # degree
    R = np.eye(4)
    R[1][1] = R[2][2] = np.cos(angle * np.pi / 180)
    R[2][1] = np.sin(angle * np.pi / 180)
    R[1][2] = - R[2][1]
    return R

def getYRotMatrix(angle): # degree
    R = np.eye(4)
    R[0][0] = R[2][2] = np.cos(angle * np.pi / 180)
    R[0][2] = np.sin(angle * np.pi / 180)
    R[2][0] = - R[0][2]
    return R

def getZRotMatrix(angle): # degree
    R = np.eye(4)
    R[0][0] = R[1][1] = np.cos(angle * np.pi / 180)
    R[1][0] = np.sin(angle * np.pi / 180)
    R[0][1] = - R[1][0]
    return R

def render(camAng):
    # enable depth test (we'll see details later)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glLoadIdentity()

    # projection transformation
    glOrtho(-1,1, -1,1, -1,1)
    
    # viewing transformation
    gluLookAt(.1*np.sin(camAng),.1, .1*np.cos(camAng), 0,0,0, 0,1,0)
    
    drawFrame()
    
    t = glfw.get_time()
    # modeling transformation
    # blue base transformation
    glPushMatrix()
    
    #glTranslatef(np.sin(t), 0, 0)
    T = getXTransMatrix(np.sin(t))
    print(T)
    glMultMatrixf(T.T)

    # blue base drawing
    glPushMatrix()
    glMultMatrixf([[.2, 0, 0, 0],
                    [0, .2, 0, 0],
                    [0, 0, .2, 0],
                    [0, 0, 0, 1]])
    #glScalef(.2, .2, .2)
    glColor3ub(0, 0, 255)
    
    drawBox()
    
    glPopMatrix()

    # red arm transformation
    glPushMatrix()
    #glRotatef(t*(180/np.pi), 0, 0, 1)
    # glTranslatef(.5, 0, .01)
    R = getZRotMatrix(t*(180/np.pi))
    TX = getXTransMatrix(.5)
    TZ = getZTransMatrix(.01)

    glMultMatrixf((R@TX@TZ).T)

    # red arm drawing
    glPushMatrix()
    glScalef(.5, .1, .1)
    glColor3ub(255, 0, 0)
    drawBox()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()

def drawBox():
    glBegin(GL_QUADS)
    glVertex3fv(np.array([1,1,0.]))
    glVertex3fv(np.array([-1,1,0.]))
    glVertex3fv(np.array([-1,-1,0.]))
    glVertex3fv(np.array([1,-1,0.]))
    glEnd()

def drawFrame():
    # draw coordinate: x in red, y in green, z in blue
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global gCamAng, gComposedM
    
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(640,640,"Hierarchy", None,None)
    
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(gCamAng)
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()