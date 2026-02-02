# A complementary script for angle calculations with reference of a
# detector

import math as m
import numpy as np

##################################################################
# Chimera's info ###########################################
##################################################################
minRing = 0
maxRing = 35  # len(of_any_of_the_lists)

thetaVals = [1.4, 2.2, 3.1, 4.1, 5.2, 6.4, 7.8, 9.3, 10.8, 12.3, 13.8,
             15.3, 17.00, 19.00, 21.00, 23.00, 25.50, 28.50, 34, 42,
             50, 58, 66, 74, 82, 90, 98, 106, 114, 122, 130, 138, 146,
             156.5, 169.5]

theta_min = [1., 1.8, 2.6, 3.6, 4.6, 5.8, 7.0, 8.5, 10., 11.5, 13.,
             14.5, 16., 18., 20., 22., 24., 27., 30., 38., 46., 54.,
             62., 70., 78., 86., 94., 102., 110., 118., 126., 134.,
             142., 150., 163.]

theta_max = [1.8, 2.6, 3.6, 4.6, 5.8, 7., 8.5, 10., 11.5, 13., 14.5,
             16., 18., 20., 22., 24., 27., 30., 38., 46., 54., 62., 70.,
             78., 86., 94., 102., 110., 118., 126., 134., 142., 150.,
             163., 176.]

ring_tags = ["1i", "1e", "2i", "2e", "3i", "3e", "4i", "4e", "5i",
             "5e", "6i", "6e", "7i", "7e", "8i", "8e", "9i", "9e",
             "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17",
             "S18", "S19", "S20", "S21", "S22", "S23", "S24", "S25",
             "S26"]

# The distance from the sphere center to the detectors (cm)
det_dist = [350, 350, 300, 300, 250, 250, 210, 210, 180, 180, 160,
            160, 140, 140, 120, 120, 100, 100, 40, 40, 40, 40, 40, 40,
            40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40]

thickVar = 300
thick_Si = [220, 220, thickVar, thickVar, thickVar, thickVar,
            thickVar, thickVar, 275, 275, 275, 275, 275, 275, 275, 275,
            thickVar, thickVar, 275, 275, 275, 275, 275, 275, 275, 275,
            275, 275, 275, 275, 275, 275, 275, 275, 275]

teles_num = [16, 16, 24, 24, 32, 32, 40, 40, 40, 40, 48, 48, 48, 48,
             48, 48, 48, 48, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32,
             32, 32, 32, 32, 16, 8]

delta_phi = [22.5, 22.5, 15, 15, 11.25, 11.25, 9, 9, 9, 9, 7.5, 7.5,
             7.5, 7.5, 7.5, 7.5, 7.5, 7.5, 11.25, 11.25, 11.25, 11.25,
             11.25, 11.25, 11.25, 11.25, 11.25, 11.25, 11.25, 11.25,
             11.25, 11.25, 11.25, 22.5, 45]

firstTelL = [0, 16, 32, 56, 80, 112, 144, 184, 224, 264, 304, 352,
             400, 448, 496, 544, 592, 640, 688, 720, 752, 784, 816, 848,
             880, 912, 944, 976, 1008, 1040, 1072, 1104, 1136, 1168, 1184]

lastTelL = [15, 31, 55, 79, 111, 143, 183, 223, 263, 303, 351, 399,
            447, 495, 543, 591, 639, 687, 719, 751, 783, 815, 847, 879, 911,
            943, 975, 1007, 1039, 1071, 1103, 1135, 1167, 1183, 1191]

dOmega = [0.133, 0.209, 0.247, 0.326, 0.373, 0.458, 0.549, 0.660,
          0.756, 0.870, 0.813, 0.902, 1.337, 1.485, 1.639, 1.785, 2.950,
          3.270, 15.313, 18.313, 21.000, 23.250, 25.063, 26.375, 27.125,
          27.438, 27.125, 26.375, 25.063, 23.250, 21.00, 18.313, 15.313,
          35.438, 31.813]


def createNormalTable():
    """Just creating the normal vectors for each detector"""
    pass


def getNormalVector(ringStr, subDect):
    """Given ring and detector address it returns a corresponding normal
vector

    """
    idx1 = getTagIndex(ringStr)
    idx2 = subDect
    theta = m.radians(thetaVals[idx1])
    phi = m.radians(delta_phi[idx1]*idx2)

    xNorm = m.sin(theta)*m.cos(phi)
    yNorm = m.sin(theta)*m.sin(phi)
    zNorm = m.cos(theta)

    rNorm = np.array([xNorm, yNorm, zNorm])

    return rNorm


def getRelativeAngleList(dAddress):
    """Returns a list of the angles for all the detectors"""
    pass

# Maybe there is some library that does this better... find it!


def getThetaRel(rNorm1, rNorm2):
    """Gets the relative thetaRel angle, for two normalized vectors,
via the dot product

    """
    myDot = np.dot(rNorm1, rNorm2)
    thetaRel = m.acos(myDot)
    return thetaRel


def getPhiRel(rNorm1, rNorm2):
    """Finding the relative phi"""
    # Might be useful so think about it, might need a reference zero
    # for this
    pass


def getNormRDict():
    """Gets a list of dicts of the thetaRel angles with the chosen
detector"""
    myThetaDict = {}
    for i in range(len(ring_tags)):
        iTag = ring_tags[i]
        myThetaDict[iTag] = []
        # print(iTag)
        # print(teles_num[i])
        for myInternalIdx in range(teles_num[i]):
            # myThetaDict[iTag].append(myInternalIdx)
            myNormV = getNormalVector(iTag, myInternalIdx)
            myThetaDict[iTag].append(myNormV)

        # print(myThetaDict[iTag])
    return myThetaDict


def getRelAngleDict(rStr, dNum):
    """Gets a list of dicts of the thetaRel angles with the chosen
detector"""
    rNormRef = getNormalVector(rStr, dNum)
    myThetaDict = {}
    for i in range(len(ring_tags)):
        iTag = ring_tags[i]
        myThetaDict[iTag] = []
        # print(iTag)
        # print(teles_num[i])
        for myInternalIdx in range(teles_num[i]):
            # myThetaDict[iTag].append(myInternalIdx)
            myNormV = getNormalVector(iTag, myInternalIdx)
            thetaRel = getThetaRel(rNormRef, myNormV)

            myThetaDict[iTag].append(m.degrees(thetaRel))

        # print(myThetaDict[iTag])
    return myThetaDict


def getDetInRThetaRange():
    """Gets the detectors that are in a relative angular range"""
    pass

# def printDict(myDict):
#     for eTag in myAwesomeDict:
#         print(eTag)
#         print(myAwesomeDict[eTag])


def getMasterThetaDict(rStr, dNum, partition):
    if partition <= 5 or partition > 2*180:
        print("Bad partition angle ranges become... ugly ;-)")

    theta = 0
    dTheta = (180.0/partition)/2
    masterThetaDict = {}
    for i in range(partition):
        theta += 2*dTheta
        masterThetaDict[theta] = getThetaDictWithRanges(rStr, dNum,
                                                        theta, dTheta)
    return masterThetaDict


def getThetaDictWithRanges(rStr, dNum, angVal, dTheta=3.0):
    myAwesomeDict = getRelAngleDict(rStr, dNum)
    myNewDict = {}
    # rNorm=getNormalVector(rStr,dNum)
    minAng = angVal-dTheta
    if minAng <= 0:
        minAng = 0

    maxAng = angVal+dTheta
    if maxAng >= 180:
        maxAng = 180

    for eTag in myAwesomeDict:
        for i in range(len(myAwesomeDict[eTag])):
            myAngle = myAwesomeDict[eTag][i]
            if minAng <= myAngle <= maxAng:
                if eTag not in myNewDict:
                    myNewDict[eTag] = []
                myNewDict[eTag].append([i, myAngle])
    return myNewDict


def printNewTRDict(myNewDict):
    for tagStr in myNewDict:
        for val in myNewDict[tagStr]:
            print("%s\t%d\t%2.2f" % (tagStr, val[0], val[1]))
    return

# def getThetaRangesDict(rStr, dNum, partition):
#     if  partition <= 5 or partition > 2*180:
#         print("Bad partition angle ranges become... ugly ;-)")


def getTagIndex(tagStr):
    for i in range(len(ring_tags)):
        if tagStr == ring_tags[i]:
            return i
    return None


def getChimAddrFromTelesNum(telesNum):
    myStr = ""
    mySubTel = 0
    if not 0 <= telesNum < 1192:
        return myStr, mySubTel
    firstVal, nextVal = 0, 0
    myVal = 0

    for i in range(len(teles_num)):
        nextVal = firstVal+teles_num[i]
        if firstVal <= telesNum < nextVal:
            myStr = ring_tags[i]
            mySubTel = telesNum-firstVal
            break
        myVal += 1
        firstVal = nextVal
    return myStr, mySubTel
