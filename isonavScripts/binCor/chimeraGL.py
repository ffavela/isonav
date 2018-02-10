import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from binCorComplement import *

from random import random
from math import *

from miscellaneous import *

colors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,1,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,0,0),
    (1,1,1),
    (0,1,1),
    )

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

surfaces = (
    # (0,1,2,3),
    # (0,3,7,4),
    # (0,1,5,4),

    # (6,2,3,7),
    (6,7,4,5),
    # (6,5,1,2),
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
        dDist=det_dist[detIdx]/50.0
        shift=delta_phi_val*subIdx
        detValDict[mySimpleStr]=theta_min_val,theta_max_val,delta_phi_val,dDist,shift
    return detValDict[mySimpleStr]

vertValDict={}

def getVerticies4Telescope(dDist,theta_min_val,theta_max_val,delta_phi_val,shift):
    myAwesomeStr=str([dDist,theta_min_val,theta_max_val,delta_phi_val,shift])
    if myAwesomeStr not in vertValDict:
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
        vertValDict[myAwesomeStr]=verticies
    return vertValDict[myAwesomeStr]

def drawSurfaces(verticies,t=0.999):
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x+=1
            # glColor3fv(colors[x])
            # glColor3fv((1,0,0))
            # myColor=(cos(t*pi/2)**2,0,sin(t*pi/2)**2)
            # myColor=(random(),random(),random())
            myColor=convert_to_rgb(0,1,t)
            # myColor=getRgb(0,1,t)
            # print("t = ", t )
            # cmap = cm.autumn
            # myColor=cmap(t)[:3]
            glColor3fv(myColor)
            glVertex3fv(verticies[vertex])
            glColor3fv((1,1,1))
    glEnd()


def getVert4TelesSimple(detIdx,subIdx):
    theta_min_val,theta_max_val,delta_phi_val,dDist,shift=getDetValues(detIdx,subIdx)
    verticies=getVerticies4Telescope(dDist,theta_min_val,theta_max_val,delta_phi_val,shift)
    return verticies

def drawChimTelesGL(detIdx,subIdx,surfStat=False,t=0):
    verticies=getVert4TelesSimple(detIdx,subIdx)
    if surfStat:
        drawSurfaces(verticies,t)
        pass

    # glBegin(GL_LINES)
    # for edge in edges:
    #     for vertex in edge:
    #         glVertex3fv(verticies[vertex])
    # glEnd()


def drawFromGLists(gVerts,gEdges):
    glBegin(GL_LINES)
    for edge in gEdges:
        for vertex in edge:
            glVertex3fv(gVerts[vertex])
    glEnd()


def drawChimTelesGL2(detIdx,subIdx,surfStat=False):
    theta_min_val,theta_max_val,delta_phi_val,dDist,shift=getDetValues(detIdx,subIdx)
    verticies=getVerticies4Telescope(dDist,theta_min_val,theta_max_val,delta_phi_val,shift)
    if surfStat:
        drawSurfaces(verticies,random())

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def drawRing(detIdx,subTDict):
    telesN=teles_num[detIdx]
    for subIdx in range(telesN):
        tVal=subTDict[subIdx]
        drawChimTelesGL(detIdx,subIdx,True,tVal)

def drawAllChimera(tDict):
    # for i in range(34):
    for i in range(11):
        ringT=ring_tags[i]
        subTDict=tDict[ringT]
        drawRing(i,subTDict)

def getTDict(rStr,sTel):
    aDict=getRelAngleDict(rStr,sTel)
    tDict={}
    for ringStr in aDict:
        tDict[ringStr]=[]
        for subTel in aDict[ringStr]:
            tVal=subTel/180
            tDict[ringStr].append(tVal)
    return tDict

def myRelAdd(i,myIntList):
    return tuple([e+i for e in myIntList])

def getGRelList(telesCoordLists,boolSurf=False):
    gTelVertList=[]
    gEdgeList=[]
    tCoordLen=8 #Number of verticies on a single telescope
    myShift=0
    for tCoordPL in telesCoordLists:
        gTelVertList+=tCoordPL

        subRel=[myRelAdd(myShift,myEdgeRel) for myEdgeRel in edges]
        gEdgeList+=subRel
        myShift+=tCoordLen

    return gTelVertList,gEdgeList

def getOptimizedRelList(telesCoordLists):
    gTelVertList,gEdgeList=getGRelList(telesCoordLists)

    #Converting the edge relationship to point relationship and
    #avoiding repeated edges (including reciprocal ones).
    gVertEdgeL=[]

    for edge in gEdgeList:
        pA=gTelVertList[edge[0]]
        pB=gTelVertList[edge[1]]
        edgeVert=(pA,pB)
        edgeVertInv=(pB,pA)

        if edgeVert not in gVertEdgeL and edgeVertInv not in gVertEdgeL:
            gVertEdgeL.append(edgeVert)

    #Now reducing the points that are on gTelVertList since there are
    #many repeated.
    gReduVertL = list(set(gTelVertList))

    #Converting back the points into index relationships using the
    #gReduVertL list.
    gReduEdgeList=[]
    for gVEdge in gVertEdgeL:
        gReduEdgeList.append((gReduVertL.index(gVEdge[0]),\
                              gReduVertL.index(gVEdge[1])))


    #Do somethign similar here for the surface points.

    return gReduVertL,gReduEdgeList

def main():
    tDict=getTDict("S19",18)
    # print(tDict)
    pygame.init()
    display = (1900,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0, -5)
    # glRotatef(120, 0, 1, 0)
    glRotatef(80, 0, 1, 0)

    myVerts0=getVert4TelesSimple(5,6)
    myVerts1=getVert4TelesSimple(5,7)
    myVerts2=getVert4TelesSimple(5,8)
    myVerts3=getVert4TelesSimple(5,9)
    myVerts4=getVert4TelesSimple(5,10)

    myVertsL=[myVerts0,myVerts1,myVerts2,myVerts3,myVerts4]

    # gVerts,gEdges=getGRelList(myVertsL)
    gVerts,gEdges=getOptimizedRelList(myVertsL)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        drawAllChimera(tDict)
        drawFromGLists(gVerts,gEdges)
        # drawChimTelesGL(25,5,True)
        # drawChimTelesGL2(32,20,True)
        # drawRing(15)
        pygame.display.flip()
        pygame.time.wait(10)

main()
