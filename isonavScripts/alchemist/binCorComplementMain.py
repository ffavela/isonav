from binCorComplement import *

# print('Number of arguments:', len(sys.argv), 'arguments.')
# print('Argument List:', str(sys.argv))

myOptions = ["--getRelTheta", "--getDetInRange"]


def checkArgs(argVar):
    if len(argVar) > 1:
        # print("More than one argument introduced")
        myOpt = sys.argv[1]
        # print(myOpt)
        if myOpt in myOptions:
            # print("Valid option")
            return True
        else:
            # print("Invalid option")
            return False


myBool = checkArgs(sys.argv)

# if myBool == True:
#     print("Going ahead")
# else:
#     print("Stopping here")


def checkIfValidAddr(r, t):
    if r not in ring_tags:
        return False
    tagIdx = getTagIndex(r)
    if not isinstance(t, int):
        return False
    if not 0 <= t < teles_num[tagIdx]:
        return False
    return True


if sys.argv[1] == "--getRelTheta":
    myShift = 2
    if len(sys.argv)-myShift == 4:
        # print("Enough number of variables")
        r1 = sys.argv[0+myShift]
        t1 = int(sys.argv[1+myShift])
        # if checkIfValidAddr(r1,t1) == False:
        #     print("Error 1 not a valid address")
        r2 = sys.argv[2+myShift]
        t2 = int(sys.argv[3+myShift])
        # if checkIfValidAddr(r2,t2) == False:
        #     print("Error 2 not a valid address")
        # print(r1,t1,r2,t2)
        myRNorm1 = getNormalVector(r1, t1)
        myRNorm2 = getNormalVector(r2, t2)
        thetaRel = getThetaRel(myRNorm1, myRNorm2)
        print("%3.2f" % degrees(thetaRel))
    else:
        print("Not enough number of variables")


# To be implemented correctly in the future
if sys.argv[1] == "--getDetInRange":
    myShift = 2
    if len(sys.argv)-myShift == 4:
        # print("Enough number of variables")
        r = sys.argv[0+myShift]
        t = int(sys.argv[1+myShift])
        # if checkIfValidAddr(r,t) == False:
        #     print("Error not a valid address")

        relTheta = radians(float(sys.argv[2+myShift]))
        myRange = radians(float(sys.argv[3+myShift]))

# print(getTagIndex("1i"))

# print(getTagIndex("S11"))

# print(getTagIndex("1231S"))

# print(getNormalVector("S24",9))

# rNorm1=getNormalVector("1i",0)
# rNorm2=getNormalVector("S26",8)

# print(degrees(getThetaRel(rNorm1,rNorm2)))

# myAwesomeDict=getRelAngleDict("6i",26)

# printThetaDictNice(myAwesomeDict)


# printThetaDictWithRanges("6i",26, 125,1)

# myNewDict=getThetaDictWithRanges("6i",26, 123,1)
# # print(myNewDict)

# printNewTRDict(myNewDict)

# print("Now trying the new function")
# mTD=getMasterThetaDict("S11",20,30)

# for e in mTD:
#     if mTD[e] == {}:
#         continue
#     print(e)
#     myNewDict=mTD[e]
#     printNewTRDict(myNewDict)
#     print()
