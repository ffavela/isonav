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

def nRadius(A):
    #In fermis
    return 1.2*A**(1.0/3.0)
    
def coulombE(e1,a1,e2,a2):
    alpha=1/137.036 #fine structure
    hc=197.33 #MeV-fm
    z1=getPnum(e1)
    z2=getPnum(e2)
    rMin=nRadius(a1)+nRadius(a2)
    return z1*z2*alpha*hc/rMin

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
            # coulE=coulombE(eKey,aEject,rKey,aRes)
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


##Printing latex fiendly nReaction
def latexNReaction(key1,a1,key2,a2):
    reacList=nReaction(key1,a1,key2,a2)
    sa1=str(a1)
    sa2=str(a2)
    print """\\begin{eqnarray*} """
    
    print ' ^{'+sa1+'}\!'+key1+'+'+' ^{'+sa2+'}\!'+key2+'\longrightarrow&',
    maxVal=len(reacList)
    for r in reacList:
        if r==reacList[4]:
            fStr='MeV'
        else:
            fStr='MeV\\\\'

        r[1]=str(r[1])
        r[3]=str(r[3])
        r[4]=str(round(r[4],2))
     
        if r[0]=='None':
            print ' ^{'+r[3]+'}\!'+r[2]+'&Q='+r[4]+fStr
            continue

        print '& ^{'+r[1]+'}\!'+r[0]+'+'+' ^{'+r[3]+'}\!'+r[2]+'&Q='+r[4]+fStr
    print '\end{eqnarray*}'


#Not yet perfect, only uses Q
#Not any beta decays
def QDecay(key1,a1):
    decayCand=nReaction(key1,a1,'None',0)
    if decayCand==False:
        return False
    decays=[val for val in decayCand if val[4]>0]
    return decays

#Prints out all the possible neg Q's
def QStable(key1,a1):
    decayCand=nReaction(key1,a1,'None',0)
    if decayCand==False:
        return False
    decays=[val for val in decayCand if val[4]<0]
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

def sReaction(key1,a1,key2,a2,eject,aEject,res,aRes,ELab=2.9,ang=30):
    react=checkReaction(key1,a1,key2,a2,eject,aEject,res,aRes)
    if not checkArguments(ELab,react,eject,res):
        return False
    Q=react[4]
    miF,mtF,meF,mrF=getAllEMasses(key1,a1,key2,a2,eject,aEject,res,aRes)
    veo,vRo,Vcm,Ef=getCoef(miF,mtF,meF,mrF,eject,aEject,res,aRes,ELab)
    if veo==False:
        return False
    # print "Normal solution is"
    s1=solveNum(ang,veo,vRo,Vcm,meF,mrF)
    s2=solveNum(ang,vRo,veo,Vcm,mrF,meF)
    solution=[s1,s2]
    return solution

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
    if ang>pi/2:
        ang-=pi
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
        if (veoz+Vcm)==0 or (vRoz+Vcm)==0:
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
            # print "No solution was found"
            # print "#####################################################"
            return False

    return [degrees(thEjectLab),ELabEject,degrees(theResLab),\
            ELabResid]

def xTremeTest(key1,a1,key2,a2,E=10,ang=30):
    reactions=nReaction(key1,a1,key2,a2)
    for e in reactions:
        if 'None' in e:
            continue
        react=sReaction(key1,a1,key2,a2,e[0],e[1],e[2],e[3],E,ang)
        if react==False:
            break
        print e
        print react[0]
        print react[1]

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
def exLevReact(ang,miF,mtF,meF,mrF,eject,aEject,res,aRes,ELab,Ef,eVal=1):
    if eVal==1:
        k=res
        aVal=aRes
    else:
        k=eject
        aVal=aEject

    popLevels=getPopLevels(k,aVal,Ef)
    if len(popLevels)<=1:
        popLevels=[[1,0.0]]
    levList=[]
    for e in popLevels:
        # print e
        if e[1] == False and e[0] != 1:
            print "Entered false for e[1] en exLevReact"
            continue
        if eVal==1:
            mEject=meF
            mRes=mrF+e[1]
        else:
            mEject=meF+e[1]
            mRes=mrF
        veo,vRo,Vcm,Ef=getCoef(miF,mtF,mEject,mRes,\
                                          eject,\
                                          aEject,\
                                          res,\
                                          aRes,\
                                          ELab)
        if not veo:
            return False

        Q=getQVal(miF,mtF,mEject,mRes)
        numSol=solveNum(ang,veo,vRo,Vcm,mEject,mRes)
        # print e,numSol
        levList.append([e,numSol])
        if numSol==False:
            break
    return levList
    
def getQVal(m1,m2,m3,m4):
    Q=(m1+m2-m3-m4)
    return Q

def iso2String(k,iso,eVal=''):
    return eVal+str(iso)+k

def xReaction(key1,a1,key2,a2,eject,aEject,res,aRes,ELab=2.9,ang=30):
    react=checkReaction(key1,a1,key2,a2,eject,aEject,res,aRes)
    if not checkArguments(ELab,react,eject,res):
        return False
    Q=react[4]

    miF,mtF,meF,mrF=getAllEMasses(key1,a1,key2,a2,eject,aEject,res,aRes)
    veo,vRo,Vcm,Ef=getCoef(miF,mtF,meF,mrF,eject,aEject,res,aRes,ELab)
    if veo==False:
        return False
    lL=[]
    c=[iso2String(eject,aEject,'*'),iso2String(res,aRes,'')]
    lL.append([c,exLevReact(ang,miF,mtF,meF,mrF,eject,aEject,res,aRes,ELab,Ef,0)])

    c=[iso2String(eject,aEject,''),iso2String(res,aRes,'*')]
    lL.append([c,exLevReact(ang,miF,mtF,meF,mrF,eject,aEject,res,aRes,ELab,Ef,1)])

    c=[iso2String(res,aRes,'*'),iso2String(eject,aEject,'')]
    lL.append([c,exLevReact(ang,miF,mtF,mrF,meF,res,aRes,eject,aEject,ELab,Ef,0)])

    c=[iso2String(res,aRes,''),iso2String(eject,aEject,'*')]
    lL.append([c,exLevReact(ang,miF,mtF,mrF,meF,res,aRes,eject,aEject,ELab,Ef,1)])

    return lL

def pXReaction(xReact):
    for e in xReact:
        print e[0]
        for ee in e[1]:
            print ee

def xXTremeTest(key1,a1,key2,a2,E=10,ang=30):
    reactions=nReaction(key1,a1,key2,a2)
    rStuff=[]
    for e in reactions:
        # print e
        if 'None' in e:
            continue
        react=xReaction(key1,a1,key2,a2,e[0],e[1],e[2],e[3],E,ang)
        if react==False:
            break
        # print e
        # pXReaction(react)
        rStuff.append([e,react])
    return rStuff

def pXXTremeTest(XXList):
    for e in XXList:
        print e[0]
        for ee in e[1]:
            print ee[0]
            for states in ee[1]:
                print states

def checkArguments(ELab,react,eject,res):
    if ELab<=0:
        print "Lab energy has to be positive"
        return False

    if not react:
        return False

    if eject=='None' or res=='None':
        print "Reaction must have at least 2 final elements"
        return False

    return True

def getAllEMasses(key1,a1,key2,a2,eject,aEject,res,aRes):
    miF=getEMass(key1,a1)
    mtF=getEMass(key2,a2)

    meF=getEMass(eject,aEject)
    mrF=getEMass(res,aRes)
    return miF,mtF,meF,mrF

#Given an energy, beam energy, angle, a list of reactions and a
#tolerance it returns values to hint where it might be from
def fReact(E,bE,angle,rList,tol=140):
    for iR in rList:
        print "######################"
        print iR
        print "######################"
        XXList=xXTremeTest(iR[0],iR[1],iR[2],iR[3],bE,angle)
        # pXXTremeTest(XXList)
        pFReact(E,tol,XXList)

def pFReact(E,tol,XXList):
    for e in XXList:
        for ee in e[1]:
            for states in ee[1]:
                if states[1]==False:
                    continue
                if abs(states[1][1]-E)<=tol:
                    print e[0],ee[0],states

def findOE(Eang,ang,r):
    E=Eang
    Emax=2*Eang
    dE=0.01
    tolerance=0.0001
    while True:
        sR= sReaction(r[0],r[1],r[2],r[3],r[0],r[1],r[2],r[3],E,ang)
        diff=Eang-sR[0][1]
        if abs(diff)<tolerance:
            break
        if dE>0 and diff<0 or dE<0 and diff>0:
            dE*=-1.0/2
        if E>Emax:
            return False
        E+=dE
    return E
    
def rutherford0(z1,z2,E1,theta):
    hc=197.33 #MeV-fm
    alpha=1/137.036
    theta=radians(theta)
    dSigma=(z1*z2*alpha*hc/(4*E1))**2/sin(theta/2)**4
    # converting to mb
    dSigma*=10
    return dSigma

def rutherford1(s1,s2,E1,theta):
    z1=getPnum(s1)
    z2=getPnum(s2)
    return rutherford0(z1,z2,E1,theta)

def nEvents(Ni,aDens,dSigma,dOmega):
    return Ni*aDens*dSigma*dOmega
