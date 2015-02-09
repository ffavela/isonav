from math import *
from loadingStuff import *
#important constant
# c=3*10**8
c=299792458

#utility functions for nuclear physics reactions

def getKey(pNum):
    for e in iDict:
        if iDict[e][0]==pNum:
            return e
    return False

def getPnum(key):
    return iDict[key][0]
        
def getNnum(key,a):
    return a-getPnum(key)

def printElemList():
    i=0
    for e in listStuff:
        print i,e
        i+=1

def checkIsoExistence(key1,a1,key2,a2):
    if key1 not in iDict or key2 not in iDict:
        print "Error: keys have to be in the dictionary"
        return False

    if a1 not in iDict[key1][1] or a2 not in iDict[key2][1]:
        print "Error: isotopes have to exist"
        return False
    return True

print "Populating dictionary"
iDict=populateDict()


def reaction(key1,a1,key2,a2):
    #Think about meoizing
    isoExist=checkIsoExistence(key1,a1,key2,a2)
    if not isoExist or isoExist=="Decay":
        return False

    aTot=a1+a2
    pTot=getPnum(key1)+getPnum(key2)
    nTot=aTot-pTot

    aRes=aTot
    pRes=pTot

    aEject=0
    pEject=0

    aVal=aTot
    pVal=pTot
    initialMass=iDict[key1][1][a1][0]+iDict[key2][1][a2][0]
    eCoef=938.41
    reactionList=[]
    rKey=getKey(pRes)
    eKey='None'
    maxLoop=1000#More than this and it should return
    iterator=0
    while True:
        if iterator>maxLoop:
            return reactionList
        iterator+=1
        #If dict loaded don't worry about this for now
        if not (rKey and eKey):
            pRes-=1
            pEject+=1
            continue
        #Ending of ignore block

        if aRes in iDict[rKey][1] and aEject in iDict[eKey][1]:
            finalMass=iDict[eKey][1][aEject][0]+iDict[rKey][1][aRes][0]
            Q=(initialMass-finalMass)*eCoef
            newVal=[eKey,aEject,rKey,aRes,Q]
            newValP=[rKey,aRes,eKey,aEject,Q]#Avoiding repetition
            if newVal not in reactionList and newValP not in reactionList:
                reactionList.append(newVal)
            aRes-=1
            aEject+=1
        else:
            pRes-=1
            pEject+=1
            rKey=getKey(pRes)
            eKey=getKey(pEject)
            aRes=aTot-pEject
            aEject=pEject
            if not (rKey and eKey):
                #It appears to happen in big vs big nuclei
                continue

            while aRes not in iDict[rKey][1] or aEject not in iDict[eKey][1]:
                if pRes<=pTot/2-1:
                    return reactionList
                rKey=getKey(pRes)
                eKey=getKey(pEject)
            
                aRes-=1
                aEject+=1
                if iterator>maxLoop:
                    return reactionList
                iterator+=1

        rKey=getKey(pRes)
        eKey=getKey(pEject)

def nReaction(key1,a1,key2,a2):
    ls=reaction(key1,a1,key2,a2)
    if ls==[]:
        print "Nuclei might be too big"
    if ls==False:
        print "An error ocurred"
        return False
    #Sort the list elements in terms of their 
    #Q value
    ls.sort(key=lambda x: x[4],reverse=True)
    return ls

#Not yet perfect, only uses Q
#Not any beta decays
def QDecay(key1,a1):
    decayCand=nReaction(key1,a1,'None',0)
    if decayCand==False:
        return False
    decays=[val for val in decayCand if val[-1]>0]
    return decays

#Prints out all the possible neg Q's
def QStable(key1,a1):
    decayCand=nReaction(key1,a1,'None',0)
    if decayCand==False:
        return False
    decays=[val for val in decayCand if val[-1]<0]
    return decays


#Print out the first unstable elements
#(in terms of Q)
def firstQPos(val=5):
    fQListX=[]
    fQListY=[]
    for i in range(117):
        k=getKey(i+1)
        print i+1,k
        if k==False:
            continue
        for iso in iDict[k][1]:
            d=QDecay(k,iso)
            if d==False:
                continue
            if d!=[]:
                fQListX.append(i+1)
                fQListY.append(iso)
                val-=1
                print "Here!",iso #,d
                print iso #,d
                break
            else:#Just testing
                fQListX.append(i+1)
                fQListY.append(0)
            if val<=0:
                return fQListX,fQListY
    return fQListX,fQListY

def firstNoQNeg(val=5):
    fQDict={}
    for i in range(117):
        k=getKey(i+1)
        print i+1,k
        if k==False:
            continue
        for iso in iDict[k][1]:
            d=QStable(k,iso)
        if d==False:
            continue
        if d!=[]:
            fQDict[k]=[i+1,iso]
            val-=1
            print "Here again!",iso,d
            print iso #,d
        if val<=0:
            return fQDict
    return fQDict

def checkReaction(key1,a1,key2,a2,eject,aEject,res,aRes):
    if not checkIsoExistence(key1,a1,key2,a2):
        print "Entered first cond"
        return False

    if not checkIsoExistence(eject,aEject,res,aRes):
        print "Entered second cond"
        return False
    reactionStuffa=[eject,aEject,res,aRes]
    reactionStuffb=[res,aRes,eject,aEject]
    retList=nReaction(key1,a1,key2,a2)
    for ret in retList:
        if reactionStuffa==ret[:-1] or reactionStuffb==ret[:-1]:
            return ret
    print "Reaction is invalid"
    return False

def pSReaction(key1,a1,key2,a2,eject,aEject,res,aRes,ELab=2.0,ang=10):
    react=sReaction(key1,a1,key2,a2,eject,aEject,res,aRes,ELab,ang)
    # print react
    if react==False:
        return
    print "The normal solution is"
    print react[0]
    if react[1]==False and 'None' not in [key1,key2]:
        return
    if react[1]!=False:
        print "The excited levels are"
        for j in react[1]:
            print j


def sReaction(key1,a1,key2,a2,eject,aEject,res,aRes,ELab=2.0,ang=10):
    react=checkReaction(key1,a1,key2,a2,eject,aEject,res,aRes)
    if ELab<=0:
        print "Lab energy has to be positive"
        return False

    if not react:
        return False

    if eject=='None' or res=='None':
        print "Reaction must have at least 2 final elements"
        return False
    Q=react[-1]

    miF=getEMass(key1,a1)
    mtF=getEMass(key2,a2)

    meF=getEMass(eject,aEject)
    mrF=getEMass(res,aRes)

    veo,vRo,Vcm,Ef=getCoef(miF,mtF,meF,mrF,eject,aEject,res,aRes,ELab)
    popLevels=getPopLevels(res,aRes,Ef)
    # print "Normal solution is"
    solution=[]
    solution.append(solveNum(ang,veo,vRo,Vcm,meF,mrF))

    levelList=exLevReact(popLevels,ang,miF,mtF,meF,mrF,eject,aEject,res,aRes,ELab)
    solution.append(levelList)
    return solution
    # if levList == False:
    #     return
    # for e in levList:
    #     print e
    #####

    # print "Checking for second solution again"
    # secSol=checkSecSol(miF,mtF,meF,mrF,ELab)
    # print "secSol#########"
    # print secSol
    # print "The final values for",res,"are"
    # print Q
    # solution=solveNum(ang,vRo,veo,Vcm,mrF,meF)
    # print solution

    # print "The excited level solutions are"

    # #######
    # exLevReact(popLevels,ang,mtF,miF,mrF,meF,res,eject,aEject,aRes,ELab)
    # #####

def checkSecSol(miF,mtF,meF,mrF,ELab):
    Q=getQVal(miF,mtF,meF,mrF)
    if Q<0:
        Ethres=-Q*(mrF+meF)/(mrF+meF-miF)
        Emax=-Q*mrF/(mrF-miF)
        print "Ethres,Emax"
        print Ethres,Emax
        if Ethres<ELab<Emax:
            print "Possible second solution"
            thetaM=acos(sqrt(-(mrF+meF)*(mrF*Q+(mrF-miF)*ELab)/(miF*meF*ELab)))
            return thetaM
    return False

def solveNum(ang,veo,vRo,Vcm,meF,mrF):
    thEject=0
    dTh=0.2
    ang=radians(ang)
    tolerance=0.0001
    while True:
        thEject+=dTh
        veoy=veo*sin(thEject)
        veoz=veo*cos(thEject)
        vRoy=vRo*sin(pi-thEject)
        vRoz=vRo*cos(pi-thEject)
         
        #They actually have to be zero
        ### deltaPy=(veoy*meF-vRoy*mrF)*1.0/c**2
        ### deltaPz=(veoz*meF+vRoz*mrF)*1.0/c**2
        # print deltaPy,deltaPz
        if (veoz+Vcm)==0:
            print "No solution was found, div by zero"
            print "#####################################################"
            return False
        thEjectLab=atan(veoy/(veoz+Vcm))
        ELabEject=meF*(veoy**2+(veoz+Vcm)**2)/(2*c**2)
        theResLab=atan(vRoy/(vRoz+Vcm))
        ELabResid=mrF*(vRoy**2+(vRoz+Vcm)**2)/(2*c**2)

        diff=ang-thEjectLab
        if abs(diff)<tolerance:
            break
        if dTh>0 and diff<0 or dTh<0 and diff>0:
            dTh *= -1.0/2
        if thEject>=pi:
            print "No solution was found"
            print "#####################################################"
            return False

    return [degrees(thEjectLab),ELabEject,degrees(theResLab),\
            ELabResid]

#Fails for xtremeTest('H',2,'Ar',40)
#['F', 15, 'Ne', 27, -46.60144060000274]
# In "The final values for Ne are"
#When sReaction(key1,a1,key2,a2,e[0],e[1],e[2],e[3],50.0,30)
#Is used in the loop
def xtremeTest(key1,a1,key2,a2,E=10,ang=30):
    reactions=nReaction(key1,a1,key2,a2)
    for e in reactions:
        print "Reaction is: ",e
        react=sReaction(key1,a1,key2,a2,e[0],e[1],e[2],e[3],E,ang)
        if react==False:
            continue
        print "The normal solution is"
        print react[0]
        if react[1]==False and 'None' not in [key1,key2]:
            return
        if react[1]!=False:
                print "The excited levels are"
                for j in react[1]:
                    print j

def numberReact(key1,a1):
    for e in iDict:
        for i in iDict[e][1]:
            print e,i
            nR=nReaction(key1,a1,e,i)
            if nR==False:
                print 0
            else:
                print len(nR)

def getPopLevels(eName,iso,aE):
    levels=[]
    if not checkDictIso(eName,iso):
        return [1]
    for e in iDict[eName][1][iso][1]:
        lE=iDict[eName][1][iso][1][e][0]
        if lE>aE:
            return levels
        levels.append([e,lE])
    return levels

def checkDictIso(eName,iso):
    if len(iDict[eName][1][iso])<=1:
        return False
    else:
        return True


def getCoef(miF,mtF,meF,mrF,eject,aEject,res,aRes,ELab):
    Q=getQVal(miF,mtF,meF,mrF)
    Pi=sqrt(2*miF*ELab)/c
    Vcm=Pi*c**2/(miF+mtF)
    Etied=(Pi*c)**2/(2*(miF+mtF))
    Edisp=ELab-Etied
    Ef=Edisp+Q

    if Ef<0:
        print "Not enough energy for reaction"
        return False,False,False,False

    Po=sqrt(2*Ef*meF*mrF/(meF+mrF))/c
    veo=Po*c**2/meF
    vRo=Po*c**2/mrF
    return veo,vRo,Vcm,Ef

def getEMass(k,iso):
    eCoef=938.41
    return iDict[k][1][iso][0]*eCoef

def getLevelE(k,iso,level):
    if not checkDictIso(k,iso):
        return 0
    return iDict[k][1][iso][1][level][0]

#Still work to be done, assuming the nucleus only gets increased mass
#when the reaction occurs (no fission or gammas for now)
def exLevReact(popLevels,ang,miF,mtF,meF,mrF,eject,aEject,res,aRes,ELab):
    levList=[]
    for e in popLevels:
        if e[1] == False and e[0] != 1:
            print "Entered false for e[1] en exLevReact"
            continue
        veo,vRo,Vcm,Ef=getCoef(miF,mtF,meF,mrF+e[1],\
                                          eject,\
                                          aEject,\
                                          res,\
                                          aRes,\
                                          ELab)
        if not veo:
            return False

        Q=getQVal(miF,mtF,meF,mrF+e[1])
        numSol=solveNum(ang,veo,vRo,Vcm,meF,mrF)
        # print e,numSol
        levList.append([e,numSol])
    return levList
    

def getQVal(m1,m2,m3,m4):
    Q=(m1+m2-m3-m4)
    return Q
