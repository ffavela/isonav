from math import *
from loadingStuff import *
#important constant
# c=3*10**8
c=299792458 #in m/s
cfm=c*10**(15) #in fm/s
# cfm=1 #in fm/s

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

def getMass(key,a):
    return iDict[key][1][a][0]

def printElemList():
    i=0
    for e in listStuff:
        print i,e
        i+=1

def parseIso(s):
    sLen=len(s)
    x=''
    if sLen==0:
        return False
    if s[0]=="*":
        x="*"
        s=s[1:]
        sLen-=1
    index=0
    while s[index] in range(10):
        index+=1
    if index==0:
        isoNo=0
    else:
        isoNo=int(s[0:index+1])
    
#Center of mass velocity stuff
def comVel(k1,a1,k2,a2,E1):
    m1=getEMass(k1,a1)
    m2=getEMass(k2,a2)
    v1=sqrt(2*E1/m1)
    v2=0 #assuming it is still
    Vcom=(v1*m1+v2*m2)/(m1+m2)
    v1p=v1-Vcom
    v2p=v2-Vcom
    return v1p,v2p,Vcom

def comE(k1,a1,k2,a2,E1):
    vels=comVel(k1,a1,k2,a2,E1)
    me1=getEMass(k1,a1)
    me2=getEMass(k2,a2)
    #Alternative way
    # mu=me1*me2/(me1+me2)
    # rVel=vels[0]-vels[1]
    # print 1.0/2.0*mu*rVel**2
    E1com=vels[0]**2*me1/2
    E2com=vels[1]**2*me2/2
    Ecom=E1com+E2com
    return E1com,E2com,Ecom

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

def mirror(e,a):
    # if not checkDictIso(e,a):
    #     return False
    pNumber=getNnum(e,a)
    nNumber=getPnum(e)
    ma=pNumber+nNumber
    me=getKey(pNumber)
    return me,ma
    
    
def coulombE(e1,a1,e2,a2):
    alpha=1/137.036 #fine structure
    hbc=197.33 #MeV-fm
    z1=getPnum(e1)
    z2=getPnum(e2)
    rMin=nRadius(a1)+nRadius(a2)
    return z1*z2*alpha*hbc/rMin

def thresholdE(e1,a1,e2,a2,e3,a3,e4,a4):
    miF=getMass(e1,a1)
    mtF=getMass(e2,a2)
    meF=getMass(e3,a3)
    mrF=getMass(e4,a4)
    eCoef=938.41

    Q=getQVal(miF,mtF,meF,mrF)*eCoef
    if Q<=0:
        Ethres=-Q*(mrF+meF)/(mrF+meF-miF)
    else:
        Ethres=0
    # print miF,mtF,meF,mrF,Q
    return Ethres

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
    initialMass=getMass(key1,a1)+getMass(key2,a2)
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
            if 'None' in [key1,key2,eKey,rKey]:
                Ethres='None'
            else:
                Ethres=thresholdE(key1,a1,key2,a2,eKey,aEject,rKey,aRes)
            newVal=[eKey,aEject,rKey,aRes,Ethres,Q]
            newValP=[rKey,aRes,eKey,aEject,Ethres,Q]#Avoiding repetition
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
    ls.sort(key=lambda x: x[5],reverse=True)
    return ls

#Printing it nicely for a spreadsheet.
def tNReaction(key1,a1,key2,a2):
    rList=nReaction(key1,a1,key2,a2)
    for e in rList:
        if e[4]=='None':
            print str(e[1])+e[0]+'\t'+str(e[3])+e[2]+'\t',e[4],'\t',"{0:0.2f}".format(float(e[5]))
        else:
            print str(e[1])+e[0]+'\t'+str(e[3])+e[2]+'\t',"{0:0.2f}".format(float(e[4])),'\t',"{0:0.2f}".format(float(e[5]))

            # print str(e[1])+e[0]+'\t'+str(e[3])+e[2]+'\t',float(e[4]),'\t',float(e[5])

##Printing latex fiendly nReaction
def latexNReaction(key1,a1,key2,a2):
    reacList=nReaction(key1,a1,key2,a2)
    sa1=str(a1)
    sa2=str(a2)
    print """\\begin{eqnarray*} """
    
    print ' ^{'+sa1+'}\!'+key1+'+'+' ^{'+sa2+'}\!'+key2+'\longrightarrow&',
    maxVal=len(reacList)
    for r in reacList:
        if r==reacList[5]:
            fStr='MeV'
        else:
            fStr='MeV\\\\'

        r[1]=str(r[1])
        r[3]=str(r[3])
        r[5]=str(round(r[5],2))
     
        if r[0]=='None':
            print ' ^{'+r[3]+'}\!'+r[2]+'&Q='+r[5]+fStr
            continue

        print '& ^{'+r[1]+'}\!'+r[0]+'+'+' ^{'+r[3]+'}\!'+r[2]+'&Q='+r[5]+fStr
    print '\end{eqnarray*}'


#Not yet perfect, only uses Q
#Not any beta decays
def QDecay(key1,a1):
    decayCand=nReaction(key1,a1,'None',0)
    if decayCand==False:
        return False
    decays=[val[0:4]+[val[5]] for val in decayCand if val[5]>0]
    return decays

#Prints out all the possible neg Q's
def QStable(key1,a1):
    decayCand=nReaction(key1,a1,'None',0)
    if decayCand==False:
        return False
    decays=[val for val in decayCand if val[5]<0]
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
        #Excluding the threshold and the QValue
        if reactionStuffa==ret[:-2] or reactionStuffb==ret[:-2]:
            return ret
    print "Reaction is invalid"
    return False

def sReaction(key1,a1,key2,a2,eject,aEject,res,aRes,ELab=2.9,ang=30):
    react=checkReaction(key1,a1,key2,a2,eject,aEject,res,aRes)
    if not checkArguments(ELab,react,eject,res):
        return False
    Q=react[5]
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
    Q=react[5]

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

def tabXEject(key1,a1,key2,a2,eject,aEject,res,aRes,ELabs=[2.8,2.9],ang=30):
    react=checkReaction(key1,a1,key2,a2,eject,aEject,res,aRes)
    gList=[]
    for energy in ELabs:
        gList.append(xEject(xReaction(key1,a1,key2,a2,eject,aEject,res,aRes,\
                                      energy,ang)))
    return gList
    
class prettyfloat(float):
    def __repr__(self):
        return "%0.2f" % self

def pTabXEject(key1,a1,key2,a2,eject,aEject,res,aRes,ELabs=[2.8,2.9],ang=30):
    # ELabs=[1.41685, 1.4665065, 1.520496, 1.5788185, 1.641474, 1.7084625, 1.779784, 1.8554385, 1.935426, 2.0197465, 2.1084, 2.2013865, 2.298706, 2.4003585, 2.506344, 2.6166625, 2.731314, 2.8502985, 2.973616, 3.1012665, 3.23325, 3.3695665]
    # ELabs=[2.2013865,2.298706,2.4003585,2.506344,2.6166625,2.731314,2.87461536,2.973616,3.1012665,3.3695665]
    # ELabs=[2.1084,2.2013865,2.298706,2.4003585,2.506344,2.6166625,2.731314,2.87461536,2.973616,3.1012665,3.26016666,3.3695665]
    levE=tabXEject(key1,a1,key2,a2,eject,aEject,res,aRes,ELabs,ang)
    for l in levE:
        ll=map(prettyfloat, l)
        # print ll
        # print('\t'.join(map(str,ll)))
        print "%.2f\t "*len(l) % tuple(l)

def xEject(xReact,mCount=6):
    xList=[]
    count=0
    for e in xReact[1][1]:
        xList.append(e[1][1])
        if count>=mCount:
            break
        count+=1
    return xList
    # print xReact[1]

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

def xXTremeTestSame(key1,a1,key2,a2,E=10,ang=30):
    reactions=[[key1,a1,key2,a2,0,0]]
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

#It prints the CS in mb
def rutherford0(z1,z2,Ecm,theta):
    hbc=197.33 #MeV-fm
    alpha=1/137.036
    theta=radians(theta)
    dSigma=(z1*z2*alpha*hbc/(4*Ecm))**2/sin(theta/2)**4
    # converting to mb
    dSigma*=10
    return dSigma
#in mb
def rutherford1(s1,s2,Ecm,theta):
    z1=getPnum(s1)
    z2=getPnum(s2)
    return rutherford0(z1,z2,Ecm,theta)

##WARNING for now it only works for deuterons in Nitrogen
#in mb
def rutherfordLab0(s1,s2,Ecm,thetaL):
    """ Returns the rutherford value in the lab frame"""
    z1=getPnum(s1)
    z2=getPnum(s2)
    #This has to be fixed
    K=1.0/7.0
    #see m. cottereau and f. lefebvres recuel de problemes...
    theta=solveAng(thetaL,K)
    dSigmaL=rutherford0(z1,z2,Ecm,theta)*\
        (1+K**2+2*K*cos(theta))**(3.0/2.0)/(1+K*cos(theta))
    return dSigmaL

def solveAng(thetaL,ratio):
    """ Returns the CM angle """
    thetaL=radians(thetaL)
    tgThetaL=tan(thetaL)
    thetaCM=0
    def myFunct(thetaCM,KE):
        return sin(thetaCM)/(cos(thetaCM)+ratio)
    tolerance=0.0001
    dTh=0.05
    # i=0
    while True:
        fVal=myFunct(thetaCM,ratio)
        # if i>=20:
        #     break
        # print "fVal is:",fVal
        # i+=1
        diff=tgThetaL-fVal
        if abs(diff)<tolerance:
            break
        if dTh>0 and diff<0 or dTh<0 and diff>0:
            dTh *= -1.0/2
            # print "Sign switch"
        if thetaCM>=pi:
            # print "No solution was found"
            return False
        thetaCM+=dTh
    thetaL=degrees(atan(fVal))
    return degrees(thetaCM)
    # return thetaL


def nEvents(Ni,aDens,dSigma,dOmega):
    return Ni*aDens*dSigma*dOmega

def getdOmega(r,R):
    return pi*(r/R)**2

#Converts current into # of charges
def current2Part(current):
    C=6.2415093E18
    return C*current*10**(-6)

#Gets the product of #Projectiles*#Targets
#in part/mb
def getT(ps,ts,E,angle,Nr,dOmega):
    return Nr/(rutherfordLab0(ps,ts,E,angle)*dOmega)

def getdSigma(Nn,dOmega,T):
   return Nn/(dOmega*T) 

#Returns density in part/cm**2, T increases with time as well as nPart
#so time cancels out, just put the average current, and remember that
#there are 5mm collimators and that not all of the original beam gets to
#the jet.
def getDensityIncmSquare(T,current):
    #Current in micro Amperes
    nPart=current2Part(current)
    mBarn2cm2=1E-27
    return T/(mBarn2cm2*nPart)
    
#Binding Energy
def getBE(s,A):
    z=getPnum(s)
    em=getEMass(s,A)
    #proton mass
    pm=getEMass("H",1)
    #neutron mass
    nm=getEMass("n",1)
    return em-z*pm-(A-z)*nm

#Binding Energy per nucleon
def getBEperNucleon(s,A):
    return getBE(s,A)/A

#Using the liquid drop model for the binding energy
#Values taken from A. Das and T. Ferbel book
def getLDBE(s,A,a1=15.6,a2=16.8,a3=0.72,a4=23.3,a5=34):
    #All the coeficients are in MeV
    Z=getPnum(s)
    N=getNnum(s,A)
    if N%2==0 and Z%2==0:#Even even case
        a5*=-1 #Greater stability
    elif (A%2)==1:#Odd even case
        a5=0
    BE=-a1*A+a2*A**(2.0/3.0)+a3*Z**2/A**(1.0/3.0)+a4*(N-Z)**2/A+a5*A**(-3.0/4.0)
    return BE

#Binding energy per nucleon using LD
def getLDBEperNucleon(s,A):
    return getLDBE(s,A)/A

#Using the LD model to get the eMass
def getLDEMass(s,A):
    Z=getPnum(s)
    #proton mass
    pm=getEMass("H",1)
    #neutron mass
    nm=getEMass("n",1)
    return Z*pm+(A-Z)*nm+getLDBE(s,A)

#Using the LD model to get the mass
def getLDMass(s,A):
    eCoef=938.41
    return getLDEMass(s,A)/eCoef

#de Broglie wavelength in angstrom
def deBroglie(element,A,E):
    hc=1.23984193 #MeV-pm
    em=getEMass(element,A)
    p=sqrt(2*em*E) #a "c" from here goes to the hc
    return hc/p/100 # 1/100 to convert to angstrom

#reduced de Broglie wavelength in angstrom
def reducedDeBroglie(element,A,E):
    return deBroglie(element,A,E)/(2*pi)

#Compton wavelength
def comptonW(em):
    hc=1.23984193 #MeV-pm
    return hc/em*1000 #*1000 to convert to fm

#Reduced Compton wavelength
def rComptonW(em):
    hbc=197.33 #MeV-fm
    return hbc/em

#Hard sphere classical total CS
#All this was taken from Griffiths
def hardSphereCTCS(target,A):
    a=nRadius(A)
    return pi*a**2/100 #1/100 barn conversion.

#Hard sphere quantum total CS
#Note; this is an approximation from an expansion.
def hardSphereQTCS(target,A):
    a=nRadius(A)
    return 4*pi*a**2/100 #1/100 barn conversion.

#soft sphere differential CS
def softSphereDCS(sp,ap,st,at,V0=50):
    a=nRadius(at)
    em=getEMass(sp,ap)
    hbc=197.33 #MeV-fm
    return (2*em*V0*a**3/(3*hbc**2))**2

#soft sphere total CS
def softSphereTCS(sp,ap,st,at,V0=50):
    return 4*pi*softSphereDCS(sp,ap,st,at,V0)

#soft sphere using the second Born approximation
def softSphereDSBorn(sp,ap,st,at,V0=50):
    a=nRadius(at)
    em=getEMass(sp,ap)
    hbc=197.33 #MeV-fm
    firstC=2*em*V0*a**3/(3*hbc**2)
    secondC=1-4*em*V0*a**2/(5*hbc**2)
    return (firstC*secondC)**2

#soft sphere using the second Born approximation for total CS
def softSphereTSBorn(sp,ap,st,at,V0=50):
    return 4*pi*softSphereDSBorn(sp,ap,st,at)


#Using the Yukawa potential
def yukawaDCS(sp,ap,st,E,theta,beta,mu):
    hbc=197.33 #MeV-fm
    eMass=getEMass(sp,ap)
    theta=radians(theta)
    k=sqrt(2*eMass*E/hbc)
    kappa=2*k*sin(theta/2)
    return (-2*eMass*beta/(hbc**2*(mu**2+kappa**2)))**2
    
#Getting the total CS for the Yukawa potential, Griffiths 11.12 Note;
#this is still in testing
def yukawaTCS(sp,ap,st,E,theta,beta,mu):
    hbc=197.33 #MeV-fm
    eMass=getEMass(sp,ap)
    theta=radians(theta)
    k=sqrt(2*eMass*E/hbc)
    kappa=2*k*sin(theta/2)
    return pi*(4*eMass*beta/(mu*hbc))**2/((mu*kappa)**2+8*eMass*E)

#Using gamow factor according to krane eq. 8.17
def gamowAlpha(s1,a1):
    sEject="He"
    aEject=4
    decay=findDecay(s1,a1,sEject,aEject)
    if decay != 'None':
        Q=decay[4]
    else:
        return 'None'

    hbc=197.33 #MeV-fm
    alpha=1/137.036

    B=getB(s1,a1,sEject,aEject)
    em=getEMass(sEject,aEject) #Most probably alpha part mass
    z1=getPnum(s1)
    z2=getPnum(sEject)

    x=Q/B
    #Both equations should give the same... but they don't!!
    #See Krane pg 253, eq. 8.16
    # G=sqrt(2*em/Q)*alpha*z1*z2*(pi/2-2*x**2)
    G=sqrt(2*em/Q)*alpha*z1*z2*(acos(x)-sqrt(x*(1-x)))
    return G

#Gets the half life using the Gamow factor
def gamowHL(s1,a1):
    sEject="He"
    aEject=4
    decay=findDecay(s1,a1,sEject,aEject)
    # Q=6
    if decay != 'None':
        Q=decay[4]
    else:
        return 'None'

    ln2=0.693
    a=nRadius(a1)
    V0=35
    em=getEMass(s1,a1)
    G=gamowAlpha(s1,a1)
    tHalf=ln2*a/cfm*sqrt(em/(V0+Q))*e**(2*G)
    return tHalf


def findDecay(s1,a1,sEject,aEject):
    rList=QDecay(s1,a1)
    for e in rList:
        if sEject==e[0] and aEject==e[1]:
            return e
    #Take care of this case
    return 'None'

#For alpha decay is the barrier penetration energy for decay (in MeV),
#normally alpha
def getB(s1,a1,sEject,aEject):
    alpha=1/137.036 #fine structure
    hbc=197.33 #MeV-fm
    a=nRadius(a1)
    z1=getPnum(s1)
    z2=getPnum(sEject)
    return alpha*hbc*z1*z2/a

#This is still in testing
def stoppingPowerD(e1,e2,a2,E,I):
    z1=getPnum(e1)
    z2=getPnum(e2)
    A=getMass(e2,a2)
    #In MeV/cm
    return -z1**2*z2*log(2195*E/I)/(A*E)

#This is also still in testing    
def stoppingPowerI(e1,e2,a2,E,I,L):
    #L in microns (10**-4 cm)
    x=0
    L=L*10**(-4)
    dx=L/10
    while x<L or E<=0:
        E+=stoppingPowerD(e1,e2,a2,E,I)*dx
        x+=dx
    return E
        
    
