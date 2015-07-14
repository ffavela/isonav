from math import *
from loadingStuff import *
from isoParser import *

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

def getPnum(iso):
    A,k=getIso(iso)
    return iDict[k][0]
        
def getNnum(iso):
    A,k=getIso(iso)
    return A-getPnum(k)

def getMass(iso):
    a,key=getIso(iso)
    return iDict[key][1][a][0]

def printElemList():
    i=0
    for e in listStuff:
        print i,e
        i+=1

#Center of mass velocity stuff
def comVel(iso1,iso2,E1):
    m1=getEMass(iso1)
    m2=getEMass(iso2)
    v1=sqrt(2*E1/m1)
    v2=0 #assuming it is still
    Vcom=(v1*m1+v2*m2)/(m1+m2)
    v1p=v1-Vcom
    v2p=v2-Vcom
    return v1p,v2p,Vcom

def comE(iso1,iso2,E1):
    vels=comVel(iso1,iso2,E1)
    me1=getEMass(iso1)
    me2=getEMass(iso2)
    #Alternative way
    # mu=me1*me2/(me1+me2)
    # rVel=vels[0]-vels[1]
    # print 1.0/2.0*mu*rVel**2
    E1com=vels[0]**2*me1/2
    E2com=vels[1]**2*me2/2
    Ecom=E1com+E2com
    return E1com,E2com,Ecom

def checkIsoExistence(iso1,iso2):
    a1,key1=getIso(iso1)
    a2,key2=getIso(iso2)

    if key1 not in iDict or key2 not in iDict:
        print "Error: keys have to be in the dictionary"
        return False

    if a1 not in iDict[key1][1] or a2 not in iDict[key2][1]:
        print "Error: isotopes have to exist"
        return False
    return True

print "#Populating dictionary"
iDict=populateDict()

def nRadius(iso):
    #In fermis
    A,k=getIso(iso)
    return 1.2*A**(1.0/3.0)

def mirror(iso):
    # if not checkDictIso(e,a):
    #     return False
    pNumber=getNnum(iso)
    nNumber=getPnum(iso)
    ma=pNumber+nNumber
    me=getKey(pNumber)
    return me,ma
    
def coulombE(iso1,iso2):
    alpha=1/137.036 #fine structure
    hbc=197.33 #MeV-fm
    z1=getPnum(iso1)
    z2=getPnum(iso2)
    rMin=nRadius(iso1)+nRadius(iso2)
    return z1*z2*alpha*hbc/rMin

def thresholdE(iso1,iso2,iso3,iso4):
    mp=getMass(iso1)
    mt=getMass(iso2)
    me=getMass(iso3)
    mr=getMass(iso4)
    eCoef=938.41

    Q=getQVal(mp,mt,me,mr)*eCoef
    if Q<=0:
        Ethres=-Q*(mr+me)/(mr+me-mp)
    else:
        Ethres=0
    return Ethres

def reaction(iso1,iso2):
    #Think about meoizing
    a1,key1=getIso(iso1)
    a2,key2=getIso(iso2)
    isoExist=checkIsoExistence(iso1,iso2)
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
    initialMass=getMass(iso1)+getMass(iso2)
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
            ejectIso=str(aEject)+eKey
            resIso=str(aRes)+rKey

            if 'None' in [key1,key2,eKey,rKey]:
                Ethres='None'
            else:
                Ethres=thresholdE(iso1,iso2,ejectIso,resIso)
            newVal=[ejectIso,resIso,Ethres,Q]
            newValP=[resIso,ejectIso,Ethres,Q]#Avoiding repetition
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

def nReaction(iso1,iso2):
    ls=reaction(iso1,iso2)
    if ls==[]:
        print "Nuclei might be too big"
    if ls==False:
        print "An error ocurred"
        return False
    #Sort the list elements in terms of their 
    #Q value
    ls.sort(key=lambda x: x[3],reverse=True)
    return ls

#Printing it nicely for a spreadsheet.
def tNReaction(iso1,iso2):
    rList=nReaction(iso1,iso2)
    for e in rList:
        if e[2]=='None':
            print e[0]+'\t'+e[1]+'\t',e[2],'\t',"{0:0.2f}".format(float(e[3]))
        else:
            print e[0]+'\t'+e[1]+'\t',"{0:0.2f}".format(float(e[2])),'\t',"{0:0.2f}".format(float(e[3]))

            # print str(e[1])+e[0]+'\t'+str(e[3])+e[2]+'\t',float(e[4]),'\t',float(e[5])

##Printing latex fiendly nReaction
def latexNReaction(iso1,iso2):
    reacList=nReaction(iso1,iso2)
    a1,key1=getIso(iso1)
    a2,key2=getIso(iso2)
    sa1=str(a1)
    sa2=str(a2)
    print """\\begin{eqnarray*} """
    
    print ' ^{'+sa1+'}\!'+key1+'+'+' ^{'+sa2+'}\!'+key2+'\longrightarrow&',
    maxVal=len(reacList)
    for r in reacList:
        if r==reacList[3]:
            fStr='MeV'
        else:
            fStr='MeV\\\\'

        r[3]=str(round(r[3],2))
        aEject,kEject=getIso(r[0])
        aRes,kRes=getIso(r[1])
        aEject,aRes=str(aEject),str(aRes)
        if kEject==None:
            print ' ^{'+aRes+'}\!'+kRes+'&Q='+r[3]+fStr
            continue

        print '& ^{'+aEject+'}\!'+kEject+'+'+' ^{'+aRes+'}\!'+kRes+'&Q='+r[3]+fStr
    print '\end{eqnarray*}'


#Not yet perfect, only uses Q
#Not any beta decays
def QDecay(iso1):
    decayCand=nReaction(iso1,'0None')
    if decayCand==False:
        return False
    decays=[val[0:2]+[val[3]] for val in decayCand if val[3]>0]
    return decays

#Prints out all the possible neg Q's
def QStable(iso1):
    a1,key1=getIso(iso1)
    decayCand=nReaction(iso1,'0None')
    if decayCand==False:
        return False
    decays=[val for val in decayCand if val[3]<0]
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
            isoVal=str(iso)+k
            d=QDecay(isoVal)
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
            isoVal=str(iso)+k
            d=QStable(isoVal)
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

def checkReaction(iso1,iso2,isoEject,isoRes):
    a1,key1=getIso(iso1)
    a2,key2=getIso(iso2)
    aEject,eject=getIso(isoEject)
    aRes,res=getIso(isoRes)
    #Making sure that the cases 'n' are '1n' 'p' is '1H' etc
    isoEject=str(aEject)+eject
    isoRes=str(aRes)+res
    if not checkIsoExistence(iso1,iso2):
        print "Entered first cond"
        return False

    if not checkIsoExistence(isoEject,isoRes):
        print "Entered second cond"
        return False
    reactionStuffa=[eject,aEject,res,aRes]
    reactionStuffb=[res,aRes,eject,aEject]

    reactionStuffa=[isoEject,isoRes]
    reactionStuffb=[isoRes,isoEject]
    retList=nReaction(iso1,iso2)
    for ret in retList:
        #Excluding the threshold and the QValue
        if reactionStuffa==ret[:2] or reactionStuffb==ret[:2]:
            return ret
    print "Reaction is invalid"
    return False

def sReaction(iso1,iso2,isoEject,isoRes,ELab=2.9,ang=30):
    a1,key1=getIso(iso1)
    a2,key2=getIso(iso2)
    aEject,eject=getIso(isoEject)
    aRes,res=getIso(isoRes)

    react=checkReaction(iso1,iso2,isoEject,isoRes)
    if not checkArguments(ELab,react,eject,res):
        return False

    ve,vR,Vcm,Ef=getCoef(iso1,iso2,isoEject,isoRes,ELab)
    if ve==False:
        return False
    s1=solveNum(ang,ve,vR,Vcm,isoEject,isoRes)
    s2=solveNum(ang,vR,ve,Vcm,isoRes,isoEject)
    solution=[s1,s2]
    return solution

def checkSecSol(emp,emt,eme,emr,ELab):
    Q=getQVal(emp,emt,eme,emr)
    if Q<0:
        Ethres=-Q*(emr+eme)/(emr+eme-emp)
        Emax=-Q*emr/(emr-emp)
        print "Ethres,Emax"
        print Ethres,Emax
        if Ethres<ELab<Emax:
            print "Possible second solution"
            thetaM=acos(sqrt(-(emr+eme)*(emr*Q+(emr-emp)*ELab)/(emp*eme*ELab)))
            return thetaM
    return False

def solveNum(ang,ve,vR,Vcm,isoE,isoR,exList=[0,0,0,0]):
    eme=getEMass(isoE)+exList[2]
    emr=getEMass(isoR)+exList[3]
    thEject=0
    dTh=0.2
    ang=radians(ang)
    if ang>pi/2:
        ang-=pi
    tolerance=0.0001
    while True:
        thEject+=dTh
        vey=ve*sin(thEject)
        vez=ve*cos(thEject)
        vRy=vR*sin(pi-thEject)
        vRz=vR*cos(pi-thEject)
         
        #They actually have to be zero
        ### deltaPy=(vey*eme-vRy*emr)*1.0/c**2
        ### deltaPz=(vez*eme+vRz*emr)*1.0/c**2
        # print deltaPy,deltaPz
        if (vez+Vcm)==0 or (vRz+Vcm)==0:
            print "No solution was found, div by zero"
            print "#####################################################"
            return False
        thEjectLab=atan(vey/(vez+Vcm))
        ELabEject=eme*(vey**2+(vez+Vcm)**2)/(2*c**2)
        theResLab=atan(vRy/(vRz+Vcm))
        ELabResid=emr*(vRy**2+(vRz+Vcm)**2)/(2*c**2)

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


def xTremeTest(iso1,iso2,E=10,ang=30):
    reactions=nReaction(iso1,iso2)
    for e in reactions:
        if 'None' in e:
            continue
        isoEject=e[0]
        isoRes=e[1]
        react=sReaction(iso1,iso2,isoEject,isoRes,E,ang)
        if react==False:
            break
        print e
        print react[0]
        print react[1]

def numberReact(iso1):
    for e in iDict:
        for i in iDict[e][1]:
            print e,i
            iso2=str(i)+e
            nR=nReaction(iso1,iso2)
            if nR==False:
                print 0
            else:
                print len(nR)

def getPopLevels(iso1,aE):
    levels=[]
    iso,eName=getIso(iso1)
    if not checkDictIso(iso1):
        return [1]
    for e in iDict[eName][1][iso][1]:
        lE=iDict[eName][1][iso][1][e][0]
        if lE>aE:
            return levels
        levels.append([e,lE])
    return levels

def checkDictIso(iso):
    A,k=getIso(iso)
    if len(iDict[k][1][A])<=1:
        return False
    else:
        return True

def getCoef(iso1,iso2,isoE,isoR,ELab,exList=[0,0,0,0]):
    emp,emt,eme,emr=getAllEMasses(iso1,iso2,isoE,isoR)
    emp+=exList[0]
    emt+=exList[1]
    eme+=exList[2]
    emr+=exList[3]
    Q=getQVal(emp,emt,eme,emr)
    # Pi=sqrt(2*emp*ELab)/c
    # Vcm=Pi*c**2/(emp+emt)
    # EcmSys=(Pi*c)**2/(2.0*(emp+emt))
    v1=sqrt(2.0*ELab/emp)*c
    v2=0 #For future improvement
    Vcm=(emp*v1+emt*v2)/(emp+emt)
    iso1="d"
    iso2="14N"
    EcmSys=0.5*(Vcm/c)**2*(emp+emt)
    #Available E in b4 collision
    Edisp=ELab-EcmSys
    Ef=Edisp+Q
    if Ef<0:
        print "Not enough energy for reaction"
        return False,False,False,False
    #Momentum, in cm, going out
    muO=eme*emr/(eme+emr)
    Po=sqrt(2*Ef*muO)/c
    ve=Po*c**2/eme
    vR=Po*c**2/emr
    return ve,vR,Vcm,Ef

def getEMass(iso1):
    eCoef=938.41
    A,k=getIso(iso1)
    return iDict[k][1][A][0]*eCoef

def getLevelE(iso1,level):
    A,k=getIso(iso1)
    if not checkDictIso(iso1):
        return 0
    return iDict[k][1][A][1][level][0]

#Still work to be done, assuming the nucleus only gets increased mass
#when the reaction occurs (no fission or gammas for now)
# def exLevReact(ang,emp,emt,eme,emr,eject,aEject,res,aRes,ELab,Ef,eVal=1):
def exLevReact(ang,iso1,iso2,isoEject,isoRes,ELab,Ef,eVal=1):
    emp,emt,eme,emr=getAllEMasses(iso1,iso2,isoEject,isoRes)#Necessary?
    if eVal==1:
        isoE1=isoRes
    else:
        isoE1=isoEject
    popLevels=getPopLevels(isoE1,Ef)
    if len(popLevels)<=1:
        popLevels=[[1,0.0]]
    levList=[]
    #For sending the mass excitations into getCoef
    exList=[0,0,0,0]
    for e in popLevels:
        # print e
        if e[1] == False and e[0] != 1:
            print "Entered false for e[1] en exLevReact"
            continue
        if eVal==1:
            mEject=eme
            mRes=emr+e[1]
            exList[3]=e[1]
        else:
            mEject=eme+e[1]
            mRes=emr
            exList[2]=e[1]

        ve,vR,Vcm,Ef=getCoef(iso1,iso2,isoEject,isoRes,ELab,exList)
        if not ve:
            return False

        numSol=solveNum(ang,ve,vR,Vcm,isoEject,isoRes,exList)
        levList.append([e,numSol])
        if numSol==False:
            break
    return levList
    
def getQVal(m1,m2,m3,m4,exList=[0,0,0,0]):
    m1+=exList[0]
    m2+=exList[1]
    m3+=exList[2]
    m4+=exList[3]
    Q=(m1+m2-m3-m4)
    return Q

def getIsoQVal(iso1,iso2,iso3,iso4):
    # checkReaction(iso1,iso2,iso3,iso4)
    m1=getEMass(iso1)
    m2=getEMass(iso2)
    m3=getEMass(iso3)
    m4=getEMass(iso4)
    Q=(m1+m2-m3-m4)
    return Q

def iso2String(k,iso,eVal=''):
    return eVal+str(iso)+k

def xReaction(iso1,iso2,isoEject,isoRes,ELab=2.9,ang=30):
    a1,key1=getIso(iso1)
    a2,key2=getIso(iso2)
    aEject,eject=getIso(isoEject)
    aRes,res=getIso(isoRes)

    react=checkReaction(iso1,iso2,isoEject,isoRes)
    if not checkArguments(ELab,react,eject,res):
        return False
    Q=react[3]

    ve,vR,Vcm,Ef=getCoef(iso1,iso2,isoEject,isoRes,ELab)
    if ve==False:
        return False
    lL=[]
    c=[iso2String(eject,aEject,'*'),iso2String(res,aRes,'')]
    lL.append([c,exLevReact(ang,iso1,iso2,isoEject,isoRes,ELab,Ef,0)])

    c=[iso2String(eject,aEject,''),iso2String(res,aRes,'*')]
    lL.append([c,exLevReact(ang,iso1,iso2,isoEject,isoRes,ELab,Ef,1)])

    c=[iso2String(res,aRes,'*'),iso2String(eject,aEject,'')]
    lL.append([c,exLevReact(ang,iso1,iso2,isoRes,isoEject,ELab,Ef,0)])

    c=[iso2String(res,aRes,''),iso2String(eject,aEject,'*')]
    lL.append([c,exLevReact(ang,iso1,iso2,isoRes,isoEject,ELab,Ef,1)])

    return lL

def pXReaction(xReact):
    for e in xReact:
        print e[0]
        for ee in e[1]:
            print ee

def tabXEject(iso1,iso2,isoEject,isoRes,ELabs=[2.8,2.9],ang=30):
    a1,key1=getIso(iso1)
    a2,key2=getIso(iso2)
    aEject,eject=getIso(isoEject)
    aRes,res=getIso(isoRes)

    react=checkReaction(iso1,iso2,isoEject,isoRes)
    gList=[]
    for energy in ELabs:
        gList.append(xEject(xReaction(iso1,iso2,isoEject,isoRes,\
                                      energy,ang)))
    return gList
    
class prettyfloat(float):
    def __repr__(self):
        return "%0.2f" % self

def pTabXEject(iso1,iso2,isoEject,isoRes,ELabs=[2.8,2.9],ang=30):
    # ELabs=[1.41685, 1.4665065, 1.520496, 1.5788185, 1.641474, 1.7084625, 1.779784, 1.8554385, 1.935426, 2.0197465, 2.1084, 2.2013865, 2.298706, 2.4003585, 2.506344, 2.6166625, 2.731314, 2.8502985, 2.973616, 3.1012665, 3.23325, 3.3695665]
    # ELabs=[2.2013865,2.298706,2.4003585,2.506344,2.6166625,2.731314,2.87461536,2.973616,3.1012665,3.3695665]
    # ELabs=[2.1084,2.2013865,2.298706,2.4003585,2.506344,2.6166625,2.731314,2.87461536,2.973616,3.1012665,3.26016666,3.3695665]
    levE=tabXEject(iso1,iso2,isoEject,isoRes,ELabs=[2.8,2.9],ang=30)
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

def xXTremeTest(iso1,iso2,E=10,ang=30):
    reactions=nReaction(iso1,iso2)
    rStuff=[]
    for e in reactions:
        # print e
        if 'None' in e:
            continue

        isoEject=e[0]
        isoRes=e[1]

        react=xReaction(iso1,iso2,isoEject,isoRes,E,ang)
        if react==False:
            break

        rStuff.append([e,react])
    return rStuff

def pXXTremeTest(XXList):
    for e in XXList:
        print e[0]
        for ee in e[1]:
            print ee[0]
            for states in ee[1]:
                print states

def pSpecialXXTremeTest(XXList,reactStuff,lev):
    pass
    for e in XXList:
        print 
        # if e[0]==reactStuff:
        #     print e[1][0]

#Commenting this for now
# def xXTremeTestSame(key1,a1,key2,a2,E=10,ang=30):
#     iso1=str(a1)+key1
#     iso2=str(a2)+key2

#     reactions=[[key1,a1,key2,a2,0,0]]
#     rStuff=[]
#     for e in reactions:
#         # print e
#         if 'None' in e:
#             continue
#         isoEject=str(e[1])+e[0]
#         isoRes=str(e[3])+e[2]
#         react=sReaction(iso1,iso2,isoEject,isoRes,E,ang)
#         if react==False:
#             break
#         # print e
#         # pXReaction(react)
#         rStuff.append([e,react])
#     return rStuff


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

def getAllEMasses(iso1,iso2,isoEject,isoRes):
    emp=getEMass(iso1)
    emt=getEMass(iso2)

    eme=getEMass(isoEject)
    emr=getEMass(isoRes)
    return emp,emt,eme,emr

#Given an energy, beam energy, angle, a list of reactions and a
#tolerance it returns values to hint where it might be from
def fReact(E,bE,angle,rList,tol=140):
    for iR in rList:
        print "######################"
        print iR
        print "######################"
        XXList=xXTremeTest(iR[0],iR[1],bE,angle)
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

def findOE(Eang,ang,iso1,iso2):
    E=Eang
    Emax=2*Eang
    dE=0.01
    tolerance=0.0001
    while True:
        sR= sReaction(iso1,iso2,iso1,iso2,E,ang)
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
def rutherford0(iso1,iso2,Ecm,theta):
    hbc=197.33 #MeV-fm
    alpha=1/137.036
    theta=radians(theta)
    z1=getPnum(iso1)
    z2=getPnum(iso2)
    dSigma=(z1*z2*alpha*hbc/(4*Ecm))**2/sin(theta/2)**4
    # converting to mb
    dSigma*=10
    return dSigma

def rutherfordLab0(iso1,iso2,ELab,thetaL):
    """ Returns the rutherford value in the lab frame"""
    Ecm=comE(iso1,iso2,ELab)[2] #Taking the 3rd argument
    K=getMass(iso1)/getMass(iso2)
    #see m. cottereau and f. lefebvres recuel de problemes...
    theta=solveAng(thetaL,K)
    dSigmaL=rutherford0(iso1,iso2,Ecm,theta)*\
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

def getdSigma2(pIso,tIso,Nruth,Nnucl,ELab,angle):
    return 1.0*Nnucl/Nruth*rutherfordLab0(pIso,tIso,ELab,angle)

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
def getBE(iso):
    # iso=str(A)+s
    A,k=getIso(iso)
    z=getPnum(iso)
    em=getEMass(iso)
    #proton mass
    pm=getEMass("1H")
    #neutron mass
    nm=getEMass("n")
    return em-z*pm-(A-z)*nm

#Binding Energy per nucleon
def getBEperNucleon(iso):
    A,k=getIso(iso)
    return getBE(iso)/A

#Using the liquid drop model for the binding energy
#Values taken from A. Das and T. Ferbel book
def getLDBE(iso,a1=15.6,a2=16.8,a3=0.72,a4=23.3,a5=34):
    #All the coeficients are in MeV
    A,s=getIso(iso)
    Z=getPnum(s)
    N=getNnum(iso)
    if N%2==0 and Z%2==0:#Even even case
        a5*=-1 #Greater stability
    elif (A%2)==1:#Odd even case
        a5=0
    BE=-a1*A+a2*A**(2.0/3.0)+a3*Z**2/A**(1.0/3.0)+a4*(N-Z)**2/A+a5*A**(-3.0/4.0)
    return BE

#Binding energy per nucleon using LD
def getLDBEperNucleon(iso):
    A,s=getIso(iso)
    return getLDBE(iso)/A

#Using the LD model to get the eMass
def getLDEMass(iso):
    A,s=getIso(iso)
    Z=getPnum(iso)
    #proton mass
    pm=getEMass("1H")
    #neutron mass
    nm=getEMass("n")
    return Z*pm+(A-Z)*nm+getLDBE(iso)

#Using the LD model to get the mass
def getLDMass(iso):
    eCoef=938.41
    return getLDEMass(iso)/eCoef

#de Broglie wavelength in angstrom
def deBroglie(iso,E):
    hc=1.23984193 #MeV-pm
    # iso=str(A)+element
    em=getEMass(iso)
    p=sqrt(2*em*E) #a "c" from here goes to the hc
    return hc/p/100 # 1/100 to convert to angstrom

#reduced de Broglie wavelength in angstrom
def reducedDeBroglie(iso,E):
    return deBroglie(iso,E)/(2*pi)

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
def hardSphereCTCS(iso):
    a=nRadius(iso)
    return pi*a**2/100 #1/100 barn conversion.

#Hard sphere quantum total CS
#Note; this is an approximation from an expansion.
def hardSphereQTCS(iso):
    a=nRadius(iso)
    return 4*pi*a**2/100 #1/100 barn conversion.

#soft sphere differential CS
def softSphereDCS(isop,isot,V0=50):
    a=nRadius(isot)
    # iso=str(ap)+sp
    em=getEMass(isop)
    hbc=197.33 #MeV-fm
    return (2*em*V0*a**3/(3*hbc**2))**2

#soft sphere total CS
def softSphereTCS(isop,isot,V0=50):
    return 4*pi*softSphereDCS(isop,isot,V0)

#soft sphere using the second Born approximation
def softSphereDSBorn(isop,isot,V0=50):
    a=nRadius(isot)
    # iso=str(ap)+sp
    em=getEMass(isop)
    hbc=197.33 #MeV-fm
    firstC=2*em*V0*a**3/(3*hbc**2)
    secondC=1-4*em*V0*a**2/(5*hbc**2)
    return (firstC*secondC)**2

#soft sphere using the second Born approximation for total CS
def softSphereTSBorn(isop,isot,V0=50):
    return 4*pi*softSphereDSBorn(isop,isot,V0)


#Using the Yukawa potential
def yukawaDCS(isop,isot,E,theta,beta,mu):
    hbc=197.33 #MeV-fm
    # iso=str(ap)+sp
    eMass=getEMass(isop)
    theta=radians(theta)
    k=sqrt(2*eMass*E/hbc)
    kappa=2*k*sin(theta/2)
    return (-2*eMass*beta/(hbc**2*(mu**2+kappa**2)))**2
    
#Getting the total CS for the Yukawa potential, Griffiths 11.12 Note;
#this is still in testing
def yukawaTCS(isop,isot,E,theta,beta,mu):
    hbc=197.33 #MeV-fm
    # iso=str(ap)+sp
    eMass=getEMass(isop)
    theta=radians(theta)
    k=sqrt(2*eMass*E/hbc)
    kappa=2*k*sin(theta/2)
    return pi*(4*eMass*beta/(mu*hbc))**2/((mu*kappa)**2+8*eMass*E)

#Using krane pg 248 eq 8.72
def getTAlpha(radIso):
    A,k=getIso(radIso)
    daughterIso=str(A-4)+getKey(getPnum(k)-2)
    # print daughterIso
    Q=getIsoQVal('0None',radIso,'4He',daughterIso)
    TAlpha=Q*(1-4/A)
    return TAlpha

#Using gamow factor according to krane eq. 8.17
def gamowAlpha(iso1):
    isoEject="4He"
    # a1,s1=getIso(iso1)
    # aEject,sEject=getIso(isoEject)
    decay=findDecay(iso1,isoEject)
    if decay != 'None':
        Q=decay[2]
    else:
        return 'None'

    hbc=197.33 #MeV-fm
    alpha=1/137.036

    B=getB(iso1,isoEject)
    em=getEMass(isoEject) #Most probably alpha part mass
    z1=getPnum(iso1)
    z2=getPnum(isoEject)

    x=Q/B
    #Both equations should give the same... but they don't!!
    #See Krane pg 253, eq. 8.16
    G=sqrt(2*em/Q)*alpha*z1*z2*(pi/2-2*sqrt(x))
    # G=sqrt(2*em/Q)*alpha*z1*z2*(acos(x)-sqrt(x*(1-x)))
    return G

#Gets the half life using the Gamow factor. It sometimes matches
#experimental vals and sometimes it is way off!  TODO; add the option to
#change the QVal for example. Also include the hbc*l*(l+1)/emR**2 in the
#energy. And the possibility to change V0.
def gamowHL(iso1):
    isoEject="4He"
    a1,s1=getIso(iso1)
    decay=findDecay(iso1,isoEject)
    # Q=6
    if decay != 'None':
        Q=decay[2]
    else:
        return 'None'

    ln2=0.693
    a=nRadius(iso1)
    V0=35 #50
    em=getEMass(iso1)
    G=gamowAlpha(iso1)
    tHalf=ln2*a/cfm*sqrt(em/(V0+Q))*e**(2*G)
    return tHalf


def findDecay(iso1,ejectIso):
    rList=QDecay(iso1)
    # aEject,sEject=getIso(ejectIso)
    # for e in rList:
    #     if sEject==e[0] and aEject==e[1]:
    #         return e
    for e in rList:
        if ejectIso in e:
            return e
    #Take care of this case
    return 'None'

#For alpha decay is the barrier penetration energy for decay (in MeV),
#normally alpha
def getB(iso1,isoEject):
    alpha=1/137.036 #fine structure
    hbc=197.33 #MeV-fm
    a=nRadius(iso1)
    z1=getPnum(iso1)
    z2=getPnum(isoEject)
    return alpha*hbc*z1*z2/a

#This is still in testing
def stoppingPowerD(iso1,iso2,E,I):
    z1=getPnum(iso1)
    z2=getPnum(iso2)
    A=getMass(iso2)
    #In MeV/cm
    return -z1**2*z2*log(2195*E/I)/(A*E)

#This is also still in testing
def stoppingPowerI(iso1,iso2,E,I,L):
    #L in microns (10**-4 cm)
    x=0
    L=L*10**(-4)
    dx=L/10
    while x<L or E<=0:
        E+=stoppingPowerD(iso1,iso2,E,I)*dx
        x+=dx
    return E
