import pygame

import pygame.locals as pgL

import OpenGL.GL as oGLGL
import OpenGL.GLU as oGLU

from PIL import Image

import binCorComplement as bCC

from random import random
import math as m

import miscellaneous as misc

import argparse

colors = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 1, 0),
    (1, 1, 1),
    (0, 1, 1),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 0, 0),
    (1, 1, 1),
    (0, 1, 1),
    )

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (1, 2),
    (1, 5),
    (2, 3),
    (2, 6),
    (3, 7),
    (4, 5),
    (4, 7),
    (5, 6),
    (6, 7)
    )

surfaces = (
    (0, 1, 2, 3),
    (0, 3, 7, 4),
    (0, 1, 5, 4),

    (6, 2, 3, 7),
    (6, 7, 4, 5),
    (6, 5, 1, 2),
    )

# theta_min_val=m.radians(163)
# theta_max_val=m.radians(176)

# delta_phi_val=m.radians(45)

# dDist=.45
detValDict = {}


def getDetValues(detIdx, subIdx):
    mySimpleStr = str([detIdx, subIdx])
    if mySimpleStr not in detValDict:
        theta_min_val = m.radians(bCC.theta_min[detIdx])
        theta_max_val = m.radians(bCC.theta_max[detIdx])
        delta_phi_val = m.radians(bCC.delta_phi[detIdx])
        dDist = bCC.det_dist[detIdx]/50.0
        shift = delta_phi_val*subIdx
        detValDict[mySimpleStr] = theta_min_val, theta_max_val, \
            delta_phi_val, dDist, shift
    return detValDict[mySimpleStr]


vertValDict = {}


def getVerticies4Telescope(dDist, theta_min_val, theta_max_val,
                           delta_phi_val, shift):
    myAwesomeStr = str([dDist, theta_min_val, theta_max_val,
                        delta_phi_val, shift])
    if myAwesomeStr not in vertValDict:
        delta_r = 0.1
        dDDist = dDist+delta_r
        verticies = (
            (dDist*m.sin(theta_max_val)*m.cos(delta_phi_val/2+shift),
             dDist*m.sin(theta_max_val)*m.sin(delta_phi_val/2+shift),
             dDist*m.cos(theta_max_val)),
            (dDist*m.sin(theta_max_val)*m.cos(-delta_phi_val/2+shift),
             dDist*m.sin(theta_max_val)*m.sin(-delta_phi_val/2+shift),
             dDist*m.cos(theta_max_val)),
            (dDist*m.sin(theta_min_val)*m.cos(-delta_phi_val/2+shift),
             dDist*m.sin(theta_min_val)*m.sin(-delta_phi_val/2+shift),
             dDist*m.cos(theta_min_val)),
            (dDist*m.sin(theta_min_val)*m.cos(delta_phi_val/2+shift),
             dDist*m.sin(theta_min_val)*m.sin(delta_phi_val/2+shift),
             dDist*m.cos(theta_min_val)),

            (dDDist*m.sin(theta_max_val)*m.cos(delta_phi_val/2+shift),
             dDDist*m.sin(theta_max_val)*m.sin(delta_phi_val/2+shift),
             dDDist*m.cos(theta_max_val)),
            (dDDist*m.sin(theta_max_val)*m.cos(-delta_phi_val/2+shift),
             dDDist*m.sin(theta_max_val)*m.sin(-delta_phi_val/2+shift),
             dDDist*m.cos(theta_max_val)),
            (dDDist*m.sin(theta_min_val)*m.cos(-delta_phi_val/2+shift),
             dDDist*m.sin(theta_min_val)*m.sin(-delta_phi_val/2+shift),
             dDDist*m.cos(theta_min_val)),
            (dDDist*m.sin(theta_min_val)*m.cos(delta_phi_val/2+shift),
             dDDist*m.sin(theta_min_val)*m.sin(delta_phi_val/2+shift),
             dDDist*m.cos(theta_min_val)),
        )
        vertValDict[myAwesomeStr] = verticies
    return vertValDict[myAwesomeStr]


def drawSurfaces(verticies, t=0.999):
    oGLGL.glBegin(oGLGL.GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x += 1
            # oGLGL.glColor3fv(colors[x])
            # oGLGL.glColor3fv((1,0,0))
            # myColor=(m.cos(t*pi/2)**2,0,m.sin(t*pi/2)**2)
            # myColor=(random(),random(),random())
            if t == "white":
                myColor = (1, 1, 0)
            else:
                myColor = misc.convert_to_rgb(0, 1, t)
            # myColor=getRgb(0,1,t)
            # print("t = ", t )
            # cmap = cm.autumn
            # myColor=cmap(t)[:3]
            oGLGL.glColor3fv(myColor)
            oGLGL.glVertex3fv(verticies[vertex])
            oGLGL.glColor3fv((1, 1, 1))
    oGLGL.glEnd()


def drawSurfacesWColor(verticies, myColor=()):
    oGLGL.glBegin(oGLGL.GL_QUADS)
    for surface in surfaces:
        for vertex in surface:
            oGLGL.glColor3fv(myColor)
            oGLGL.glVertex3fv(verticies[vertex])
            oGLGL.glColor3fv((1, 1, 1))
    oGLGL.glEnd()


def getVert4TelesSimple(detIdx, subIdx):
    theta_min_val, theta_max_val, delta_phi_val, dDist, shift = \
        getDetValues(detIdx, subIdx)
    verticies = getVerticies4Telescope(dDist, theta_min_val,
                                       theta_max_val, delta_phi_val, shift)
    return verticies


def drawChimTelesGL(detIdx, subIdx, surfStat=False, t=0):
    verticies = getVert4TelesSimple(detIdx, subIdx)
    if surfStat:
        drawSurfaces(verticies, t)
    #     pass

    oGLGL.glColor((0, 0, 0))
    oGLGL.glBegin(oGLGL.GL_LINES)
    for edge in edges:
        for vertex in edge:
            oGLGL.glVertex3fv(verticies[vertex])
    oGLGL.glEnd()


def specialDrawChimTelesGL(detIdx, subIdx, myColor=(1, 1, 0), colBool=True):
    verticies = getVert4TelesSimple(detIdx, subIdx)
    if colBool:
        drawSurfacesWColor(verticies, myColor)
    oGLGL.glBegin(oGLGL.GL_LINES)
    for edge in edges:
        for vertex in edge:
            oGLGL.glVertex3fv(verticies[vertex])
    oGLGL.glEnd()


def drawFromGLists(gVerts, gEdges, gSurf=[]):
    myColor = misc.convert_to_rgb(0, 1, 1)
    oGLGL.glBegin(oGLGL.GL_QUADS)
    for surface in gSurf:
        for vertex in surface:
            oGLGL.glColor3fv(myColor)
            oGLGL.glVertex3fv(gVerts[vertex])
            oGLGL.glColor3fv((1, 1, 1))
    oGLGL.glEnd()

    oGLGL.glBegin(oGLGL.GL_LINES)
    for edge in gEdges:
        for vertex in edge:
            oGLGL.glVertex3fv(gVerts[vertex])
    oGLGL.glEnd()


def drawChimTelesGL2(detIdx, subIdx, surfStat=False):
    theta_min_val, theta_max_val, delta_phi_val, dDist, shift = \
        getDetValues(detIdx, subIdx)
    verticies = getVerticies4Telescope(dDist, theta_min_val,
                                       theta_max_val, delta_phi_val, shift)
    if surfStat:
        drawSurfaces(verticies, random())

    oGLGL.glBegin(oGLGL.GL_LINES)
    for edge in edges:
        for vertex in edge:
            oGLGL.glVertex3fv(verticies[vertex])
    oGLGL.glEnd()


def drawRing(detIdx, subTDict):
    telesN = bCC.teles_num[detIdx]
    for subIdx in range(telesN):
        tVal = subTDict[subIdx]
        drawChimTelesGL(detIdx, subIdx, False, tVal)


def specialDrawRing(detIdx, myColor=(0, 0, 1), colorBool=False):
    telesN = bCC.teles_num[detIdx]
    for subIdx in range(telesN):
        specialDrawChimTelesGL(detIdx, subIdx, myColor, colorBool)


def getOptVertStuff4Ring(rNum):
    telesN = bCC.teles_num[rNum]
    gVertL = []
    for j in range(telesN):
        # Get the vertices for all the telescopes in the ring
        telesV = getVert4TelesSimple(rNum, j)
        gVertL.append(telesV)
    gOptVerts, gOptEdges, gOptSurfaces = getOptimizedRelList(gVertL)
    return gOptVerts, gOptEdges


def getVertStuff4Ring(rNum):
    telesN = bCC.teles_num[rNum]
    gVertL = []
    for j in range(telesN):
        # Get the vertices for all the telescopes in the ring
        telesV = getVert4TelesSimple(rNum, j)
        gVertL.append(telesV)
    return gVertL


def getOptVertStuff4Rings(rNumL=[]):
    gVertL = []
    if rNumL == []:  # All of Chimera
        rNumL = range(bCC.maxRing)  # 35=len(bCC.ring_tags)

    for i in rNumL:
        rVertL = getVertStuff4Ring(i)
        gVertL += rVertL
    gOptVerts, gOptEdges, gOptSurfaces = getOptimizedRelList(gVertL)
    return gOptVerts, gOptEdges, gOptSurfaces


def drawAllChimera(tDict):
    # for i in range(bCC.maxRing) # 35=len(bCC.ring_tags):
    # oGLGL.glBegin(oGLGL.GL_LINES)
    for i in range(bCC.maxRing):
        ringT = bCC.ring_tags[i]
        subTDict = tDict[ringT]
        drawRing(i, subTDict)
    # oGLGL.glEnd()


def specialDrawAllChimera(colorL, colorBool=True):
    # oGLGL.glBegin(oGLGL.GL_LINES)
    for i in range(bCC.maxRing):
        ringT = bCC.ring_tags[i]
        myColor = colorL[i]
        specialDrawRing(i, myColor, colorBool)
    # oGLGL.glEnd()


def getTDict(rStr, sTel):
    aDict = bCC.getRelAngleDict(rStr, sTel)
    tDict = {}
    for ringStr in aDict:
        tDict[ringStr] = []
        for subTel in aDict[ringStr]:
            tVal = subTel/180
            tDict[ringStr].append(tVal)
    return tDict


def myRelAdd(i, myIntList):
    return tuple([e+i for e in myIntList])


def getRotation(thing, x):
    return thing[-x:] + thing[:-x]


def getAllRotList(thing):
    allRotL = []
    for i in range(len(thing)):
        rThing = getRotation(thing, i)
        allRotL.append(rThing)
    return allRotL


def checkThingOnList(thing, list2Check):
    rotThingL = getAllRotList(thing)

    for rThing in rotThingL:
        if rThing in list2Check:
            return False

    # Now inverting the thing
    invThing = thing[::-1]
    rotIThingL = getAllRotList(invThing)
    for rIThing in rotIThingL:
        if rIThing in list2Check:
            return False

    # If it made it all the way, then it made it to the list.
    return True


def getGRelList(telesCoordLists, boolSurf=False):
    gTelVertList = []
    gEdgeList = []
    gSurfList = []

    tCoordLen = 8  # Number of verticies on a single telescope
    myShift = 0
    for tCoordPL in telesCoordLists:
        gTelVertList += tCoordPL

        subRel = [myRelAdd(myShift, myEdgeRel) for myEdgeRel in edges]
        gEdgeList += subRel

        subSurfRel = [myRelAdd(myShift, mySurf) for mySurf in surfaces]
        gSurfList += subSurfRel

        myShift += tCoordLen

    return gTelVertList, gEdgeList, gSurfList


def getOptimizedRelList(telesCoordLists):
    gTelVertList, gEdgeList, gSurfList = getGRelList(telesCoordLists)

    # Converting the edge relationship to point relationship and
    # avoiding repeated edges (including reciprocal ones).
    gVertEdgeL = []

    edgeR = range(2)
    for edge in gEdgeList:
        edgeVert = tuple([gTelVertList[edge[i]] for i in edgeR])

        if checkThingOnList(edgeVert, gVertEdgeL):
            gVertEdgeL.append(edgeVert)

    # Doing the same with the surfaces
    gVertSurfL = []

    surfR = range(4)
    # This might be trickier than it looks
    for surf in gSurfList:
        surfVert = tuple([gTelVertList[surf[i]] for i in surfR])

        if checkThingOnList(edgeVert, gVertSurfL):
            gVertSurfL.append(surfVert)

    # Now reducing the points that are on gTelVertList since there are
    # many repeated.
    gReduVertL = list(set(gTelVertList))

    # Converting back the points into index relationships using the
    # gReduVertL list.
    gReduEdgeList = []
    for gVEdge in gVertEdgeL:
        gReduEdgeList.append((gReduVertL.index(gVEdge[0]),
                              gReduVertL.index(gVEdge[1])))

    # Now for the surface points.
    gReduSurfList = []
    for gVSurf in gVertSurfL:
        gReduSurfList.append((gReduVertL.index(gVSurf[0]),
                              gReduVertL.index(gVSurf[1])))

    return gReduVertL, gReduEdgeList, gReduSurfList


def main():
    thAng = 120.0
    print("Hangling the arguments here")
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    # group.add_argument("-g", "--grid", help="draws chimera as a grid")
    group.add_argument("-c", "--colorMap",
                       help="creates a heatmap around a telescope",
                       nargs=2)

    group.add_argument("-g", "--grid",
                       help="draws chimera as a grid",
                       action='store_true')

    parser.add_argument("--thRot",
                        help="The theta angle to rotate chimera.",
                        nargs=1, type=float)

    parser.add_argument("--eRing",
                        help="Colors the ejectile ring.", nargs='+')

    parser.add_argument("--rRing",
                        help="Colors the recoil rings.", nargs='+')

    parser.add_argument("-t", "--teles",
                        help="Colors the recoil rings.",
                        nargs='+', type=int)

    args = parser.parse_args()

    colorL = [(0, 0, 1) for i in range(bCC.maxRing)]
    if args.teles:
        myTelStrAndSubTelL = []
        for aTel in args.teles:
            print("aTel = %d " % (aTel))
            myStr, mySubTel = bCC.getChimAddrFromTelesNum(aTel)
            print(myStr, mySubTel)
            if myStr == "":
                print("Error: " + str(aTel) +
                      " is not a valid telescope")
                return
            myTelStrAndSubTelL.append([bCC.ring_tags.index(myStr),
                                       mySubTel])

    if args.thRot:
        thAng = args.thRot[0]
        # print("thAng = "+str(thAng))

    if (args.colorMap):
        print("The arguments where %s and %s" % (args.colorMap[0],
                                                 args.colorMap[1]))
        rStr = args.colorMap[0]
        sTel = int(args.colorMap[1])
        if rStr not in bCC.ring_tags:
            print("error ring tag not found")
            return
        myIdx = bCC.ring_tags.index(rStr)
        colorL[bCC.ring_tags.index(rStr)] = (1, 0, 0.5)
        if sTel not in range(bCC.teles_num[myIdx]):
            maxNumOfTel = bCC.teles_num[myIdx]
            print("error telescope out of range max number is %d"
                  % maxNumOfTel)
            return
        tDict = getTDict(rStr, sTel)
    elif (args.grid):
        print("Using the grid option")
    else:
        parser.print_help()
        return

    if args.eRing:
        eRingL = args.eRing
        for ejectRing in eRingL:
            if ejectRing not in bCC.ring_tags:
                print("Error "+ejectRing+" is not a valid ring")
                return
    if args.rRing:
        rRingL = args.rRing
        for recRing in rRingL:
            if recRing not in bCC.ring_tags:
                print("Error "+recRing+" is not a valid ring")
                return
    # rStr="S26"
    # sTel=4

    # colorL[bCC.ring_tags.index("S16")]=(0,1,0.5)

    pygame.init()
    width, height = (1900, 600)
    # width, height=(705,303)
    display = (width, height)
    pygame.display.set_mode(display, pgL.DOUBLEBUF | pgL.OPENGL)

    oGLU.gluPerspective(23.0, (display[0]/display[1]), 0.1, 80.0)

    oGLGL.glTranslatef(-1.3, 0.0, -5)
    # glRotatef(120, 0, 1, 0)
    oGLGL.glRotatef(thAng, 0, 1, 0)
    # glclearcolor(190, 190, 190, 1.0) #4 changing the background
    # gVerts,gEdges,gSurf=getOptVertStuff4Rings(range(30))
    # gVerts,gEdges,gSurf=getOptVertStuff4Rings()
    # print(len(gSurf))

    myCount = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # glRotatef(1, 0, 1, 0)
        oGLGL.glClear(oGLGL.GL_COLOR_BUFFER_BIT |
                      oGLGL.GL_DEPTH_BUFFER_BIT)

        # #THIS IS FUNCTIONAL ###
        if (args.colorMap):
            drawAllChimera(tDict)
            specialDrawChimTelesGL(bCC.ring_tags.index(rStr), sTel)
        elif (args.grid):
            specialDrawAllChimera(colorL, False)
        # #THIS IS FUNCTIONAL END ###

        # specialDrawAllChimera(colorL)
        if args.eRing:
            for eRing in args.eRing:
                specialDrawRing(bCC.ring_tags.index(eRing),
                                colorBool=True)
        if args.rRing:
            for recRing in args.rRing:
                specialDrawRing(bCC.ring_tags.index(recRing),
                                myColor=(1, 0, 0), colorBool=True)

        if args.teles:
            for rIndex, subTel in myTelStrAndSubTelL:
                specialDrawChimTelesGL(rIndex, subTel)
        # drawFromGLists(gVerts,gEdges,gSurf)

        # drawChimTelesGL(25,5,True)
        # drawChimTelesGL2(32,20,True)
        # drawRing(15)
        pygame.display.flip()
        pygame.time.wait(10)

        if myCount == 1:
            print("Inside the if")
            oGLGL.glPixelStorei(oGLGL.GL_PACK_ALIGNMENT, 1)
            data = oGLGL.glReadPixels(0, 0, width, height,
                                      oGLGL.GL_RGBA,
                                      oGLGL.GL_UNSIGNED_BYTE)
            image = Image.frombytes("RGBA", (width, height), data)
            image.save('output.png', 'PNG')

        myCount += 1


if __name__ == '__main__':
    main()
