import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from binCorComplement import *

edges = (
    (0,1),
    (0,3),
    (0,4),
    (1,2),
    (1,5),
    (2,3),
    (2,6),
    (3,7),
    (4,5),
    (4,7),
    (5,6),
    (6,7)
    )

# theta_min_val=radians(163)
# theta_max_val=radians(176)

# delta_phi_val=radians(45)

# dDist=.45
detValDict={}

def getDetValues(detIdx,subIdx):
    mySimpleStr=str([detIdx,subIdx])
    if mySimpleStr not in detValDict:
        theta_min_val=radians(theta_min[detIdx])
        theta_max_val=radians(theta_max[detIdx])
        delta_phi_val=radians(delta_phi[detIdx])
        dDist=det_dist[detIdx]/100.0
        shift=delta_phi_val*subIdx
        detValDict[mySimpleStr]=theta_min_val,theta_max_val,delta_phi_val,dDist,shift
    return detValDict[mySimpleStr]

def getVerticies(dDist,theta_min_val,theta_max_val,delta_phi_val,shift):
    delta_r=0.1
    dDDist=dDist+delta_r
    verticies = (
        (dDist*sin(theta_max_val)*cos(delta_phi_val/2+shift),
         dDist*sin(theta_max_val)*sin(delta_phi_val/2+shift),
         dDist*cos(theta_max_val)),
        (dDist*sin(theta_max_val)*cos(-delta_phi_val/2+shift),
         dDist*sin(theta_max_val)*sin(-delta_phi_val/2+shift),
         dDist*cos(theta_max_val)),
        (dDist*sin(theta_min_val)*cos(-delta_phi_val/2+shift),
         dDist*sin(theta_min_val)*sin(-delta_phi_val/2+shift),
         dDist*cos(theta_min_val)),
        (dDist*sin(theta_min_val)*cos(delta_phi_val/2+shift),
         dDist*sin(theta_min_val)*sin(delta_phi_val/2+shift),
         dDist*cos(theta_min_val)),
        
        (dDDist*sin(theta_max_val)*cos(delta_phi_val/2+shift),
         dDDist*sin(theta_max_val)*sin(delta_phi_val/2+shift),
         dDDist*cos(theta_max_val)),
        (dDDist*sin(theta_max_val)*cos(-delta_phi_val/2+shift),
         dDDist*sin(theta_max_val)*sin(-delta_phi_val/2+shift),
         dDDist*cos(theta_max_val)),
        (dDDist*sin(theta_min_val)*cos(-delta_phi_val/2+shift),
         dDDist*sin(theta_min_val)*sin(-delta_phi_val/2+shift),
         dDDist*cos(theta_min_val)),
        (dDDist*sin(theta_min_val)*cos(delta_phi_val/2+shift),
         dDDist*sin(theta_min_val)*sin(delta_phi_val/2+shift),
         dDDist*cos(theta_min_val)),
    )
    return verticies

def drawChimTelesGL(detIdx,subIdx):
    theta_min_val,theta_max_val,delta_phi_val,dDist,shift=getDetValues(detIdx,subIdx)
    verticies=getVerticies(dDist,theta_min_val,theta_max_val,delta_phi_val,shift)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def drawRing(detIdx):
    telesN=teles_num[detIdx]
    for subIdx in range(telesN):
        theta_min_val,theta_max_val,delta_phi_val,dDist,shift=getDetValues(detIdx,subIdx)
        drawChimTelesGL(detIdx,subIdx)
    

def drawAllChimera():
    for i in range(34):
        drawRing(i)
    
def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        # drawChimTelesGL(25,5)
        drawAllChimera()
        # drawRing(15)
        pygame.display.flip()
        pygame.time.wait(10)

main()
