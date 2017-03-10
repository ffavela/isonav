#   Copyright (C) 2015, 2016, 2017 Francisco Favela

#   This file is part of isonav

#   isonav is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   isonav is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from math import *
from loadingStuff import *
from isoParser import *
import sqlite3

conn = sqlite3.connect(isoDatadb)
cursor = conn.cursor()

#important constant
# c=3*10**8
c=299792458 #in m/s
cfm=c*10**(15) #in fm/s
eCoef=931.4941 #amu to MeV convertion coef
hc=1.23984193 #MeV-pm
hbc=197.33 #MeV-fm
alpha=1/137.036 #fine structure
electEMass=0.5109989461 # mass of the electron in MeV
N_a=6.022140857e23 #mol^-1, Avogadro constant
# cfm=1 #in fm/s

#utility functions for nuclear physics reactions
def checkDictIso(iso):
    A,k=getIso(iso)
    if len(iDict[k][1][A])<=1:
        return False
    else:
        return True

def getKey(pNum):
    if 0<=pNum<len(listStuff):
        return listStuff[pNum]
    return False

def getPnum(iso):
    A,k=getIso(iso)
    if k=="None" or k=="0None":
        return 0
    if k not in listStuff:
        return False
    return listStuff.index(k)

def getNnum(iso):
    A,k=getIso(iso)
    return A-getPnum(k)

def getMass(iso):
    a,key=getIso(iso)
    return iDict[key][1][a][0]

def getNameFromSymbol(s):
    if s not in nameDict:
        return False
    return nameDict[s]

def printElemList():
    i=0
    for e in listStuff:
        print(i,e)
        i+=1

##This functions should be somewhat equivalent to getCoef but I'll leave
##it for now
#Center of mass velocity stuff
def getVelcm(iso1,iso2,E1):
    m1=getEMass(iso1)
    m2=getEMass(iso2)
    v1=sqrt(2.0*E1/m1)*c
    v2=0 #assuming it is still
    Vcm=(1.0*v1*m1+1.0*v2*m2)/(m1+m2)
    v1p=v1-Vcm
    v2p=v2-Vcm
    return v1p,v2p,Vcm

def getEcm(iso1,iso2,E1L):
    vels=getVelcm(iso1,iso2,E1L)
    mE1=getEMass(iso1)
    mE2=getEMass(iso2)
    #Alternative way
    # mu=mE1*mE2/(mE1+mE2)
    # rVel=vels[0]-vels[1]
    # print 1.0/2.0*mu*rVel**2
    E1cm=0.5*(vels[0]/c)**2*mE1
    E2cm=0.5*(vels[1]/c)**2*mE2
    Ecm=E1cm+E2cm
    return E1cm,E2cm,Ecm

def getEcmsFromECM(iso1,iso2,ECM):
    #For example, in a decay ECM=Q
    m1=getEMass(iso1)
    m2=getEMass(iso2)
    mu=1.0*m1*m2/(m1+m2)
    P=sqrt(2.0*mu*ECM)/c
    E1=0.5*(P*c)**2/m1
    E2=0.5*(P*c)**2/m2
    return E1,E2

def getAvailEnergy(iso1,iso2,isoEject,isoRes,E1L,E2L=0):
    E1cm,E2cm,Ecm=getEcm(iso1,iso2,E1L)
    Q=getIsoQVal(iso1,iso2,isoEject,isoRes)
    return Ecm+Q

#Just for testing
def getAllVs(iso1,iso2,isoE,isoR,E1L):
    v1cm,v2cm,Vcm=getVelcm(iso1,iso2,E1L)
    EcmAvail=getAvailEnergy(iso1,iso2,isoE,isoR,E1L)
    ejectE,resE=getEcmsFromECM(isoE,isoR,EcmAvail)
    print(ejectE,resE)
    vE=sqrt(2.0*ejectE/getEMass(isoE))*c
    vR=sqrt(2.0*resE/getEMass(isoR))*c

############################################

def checkIsoExistence(iso1,iso2):
    a1,key1=getIso(iso1)
    a2,key2=getIso(iso2)

    if key1 not in iDict or key2 not in iDict:
        print("Error: keys have to be in the dictionary")
        return False

    if a1 not in iDict[key1][1] or a2 not in iDict[key2][1]:
        print("Error: isotopes have to exist")
        return False
    return True

def checkIsoExist1(iso):
    a,key=getIso(iso)

    if key not in iDict:
        # print "Error: keys have to be in the dictionary"
        return False
    return True

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
    mE=getKey(pNumber)
    isoM=str(ma)+str(mE)
    return isoM

def coulombE(iso1,iso2):
    z1=getPnum(iso1)
    z2=getPnum(iso2)
    rMin=nRadius(iso1)+nRadius(iso2)
    return z1*z2*alpha*hbc/rMin

def thresholdE(iso1,iso2,iso3,iso4):
    mp=getMass(iso1)
    mt=getMass(iso2)
    mE=getMass(iso3)
    mR=getMass(iso4)

    Q=getQVal(mp,mt,mE,mR)*eCoef
    if Q<=0:
        Ethres=-Q*(mR+mE)/(mR+mE-mp)
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
            #Maybe use getMass or getQval here?
            finalMass=iDict[eKey][1][aEject][0]+iDict[rKey][1][aRes][0]
            Q=(initialMass-finalMass)*eCoef
            ejectIso=str(aEject)+eKey
            resIso=str(aRes)+rKey

            if 'None' in [key1,key2,eKey,rKey]:
                Ethres='None'
            else:
                Ethres=thresholdE(iso1,iso2,ejectIso,resIso)
                #Getting rid o the annoying -0.0, there must be a better way
                if Ethres==0:
                    Ethres=0.0
            newVal=[ejectIso,resIso,Ethres,Q]
            newValP=[resIso,ejectIso,Ethres,Q]#Avoiding repetition
            # if newVal not in reactionList and newValP not in reactionList:
            fList=[v[0] for v in reactionList]
            slist=[v[1] for v in reactionList]
            if ejectIso not in fList and ejectIso not in slist:
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
        print("Nuclei might be too big")
    if ls==False:
        print("An error ocurred")
        return False
    #Sort the list elements in terms of their
    #Q value
    ls.sort(key=lambda x: x[3],reverse=True)
    return ls


#Not yet perfect
#Not any beta decays
def QDecay(iso1):
    decayCand=nReaction(iso1,'0None')
    if decayCand==False:
        return False
    decays=[val[0:2]+[val[3]] for val in decayCand if val[3]>0]
    ndec=[]
    for d in decays:
        E1cm,E2cm=getEcmsFromECM(d[0],d[1],d[2])
        d=[d[0],d[1],E1cm,E2cm,d[2]]
        ndec.append(d)
    return ndec

#Not very elegant for now (Calls QDecay) But it was a quick and easy
#solution ;) For proton and neutron emission do emit="1H" or emit="1n"
#Note: only for the base state for now.
def emitDecay(iso,emit="4He"):
    qDecList=QDecay(iso)
    for e in qDecList:
        if emit in e[0:2]:
            return e

#This is the more careful solution###
def emitDecay2(iso,emit="4He",num=1):
    newIso=getNewIso(iso,emit,num)
    if not newIso:
        return False

    QVal=emitDecayQVal(iso,emit,num)
    if not QVal or QVal<0:
        return False

    nEmit=str(num)+"("+emit+")"
    return [nEmit,newIso,QVal]

def emitDecayQVal(iso,emit="4He",num=1):
    newIso=getNewIso(iso,emit,num)
    if not newIso:
        return False
    isoEMass=getEMass(iso)
    if not isoEMass:
        return False
    emitEMass=getEMass(emit)
    if not emitEMass:
        return False
    newIsoEMass=getEMass(newIso)
    if not newIsoEMass:
        return False

    QVal=getQVal(isoEMass,0,newIsoEMass,emitEMass*num)
    return QVal

def getNewIso(iso,emit="4He",num=1):
    isoN=getNnum(iso)
    isoP=getPnum(iso)

    emitN=getNnum(emit)
    emitP=getPnum(emit)

    newIsoN=isoN-emitN*num
    newIsoP=isoP-emitP*num

    #Still not sure about this condition, maybe neutron condition can be
    #loosened, check special cases such as deuteron
    if newIsoP<=0 or newIsoP<=0:
        return False

    newA=newIsoP+newIsoN
    newKey=getKey(newIsoP)
    if not newKey:
        return False

    newIso=str(newA)+newKey
    if not checkIsoExist1(newIso):
        return False

    return newIso


#Still working on this
# #Given an isotope, the ejectile nucleus, the Daughter and the available
# #energy (in CM, not Q), it returns all the possible combinations of
# #excitation modes.
# def xDecay(iso,isoE,isoD,ECM=0):
#     if iso != getCompound(isoE,isoD):
#         return False
#     exList=[0,0,0,0]
#     Q=getIsoQVal(iso,"0None",isoE,isoD,exList)
#     Eavail=ECM+Q
#     levsE=getPopLevels(isoE,Eavail)
#     levsD=getPopLevels(isoR,Eavail)

#Prints out all the possible neg Q's
def QStable(iso1):
    a1,key1=getIso(iso1)
    decayCand=nReaction(iso1,'0None')
    if decayCand==False:
        return False
    decays=[val for val in decayCand if val[3]<0]
    return decays

def checkReaction(iso1,iso2,isoEject,isoRes):
    a1,key1=getIso(iso1)
    a2,key2=getIso(iso2)
    aEject,eject=getIso(isoEject)
    aRes,res=getIso(isoRes)
    #Making sure that the cases 'n' are '1n' 'p' is '1H' etc
    if eject==None or res==None:
        print("Reaction is invalid")
        return False
    isoEject=str(aEject)+eject
    isoRes=str(aRes)+res
    if not checkIsoExistence(iso1,iso2):
        print("Entered first cond")
        return False

    if not checkIsoExistence(isoEject,isoRes):
        print("Entered second cond")
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
    print("Reaction is invalid")
    return False

def sReaction(iso1,iso2,isoEject,isoRes,ELab=2.9,ang=30):
    a1,key1=getIso(iso1)
    a2,key2=getIso(iso2)
    aEject,eject=getIso(isoEject)
    aRes,res=getIso(isoRes)

    react=checkReaction(iso1,iso2,isoEject,isoRes)
    if not checkArguments(ELab,react,eject,res):
        return False

    # vE,vR,Vcm,Ef=getCoef(iso1,iso2,isoEject,isoRes,ELab)
    # if vE==False:
    #     return False

    # s1=solveNum(ang,vE,vR,Vcm,isoEject,isoRes)
    # s2=solveNum(ang,vR,vE,Vcm,isoRes,isoEject)

    # s1=getEsAndAngs(ang,iso1,iso2,isoEject,isoRes,ELab)
    # s2=getEsAndAngs(ang,iso1,iso2,isoRes,isoEject,ELab)

    # potential BUG, the signs switch sometimes when comparing with the
    # solutions above
    s1=analyticSol(iso1,iso2,isoEject,isoRes,ELab,angle=ang)
    s2=analyticSol(iso1,iso2,isoRes,isoEject,ELab,angle=ang)

    solution=[s1,s2]
    return solution

#This is now deprecated
def checkSecSol(emp,emt,emE,emR,ELab):
    Q=getQVal(emp,emt,emE,emR)
    if Q<0:
        Ethres=-Q*(emR+emE)/(emR+emE-emp)
        Emax=-Q*emR/(emR-emp)
        print("Ethres,Emax")
        print(Ethres,Emax)
        if Ethres<ELab<Emax:
            print("Possible second solution")
            thetaM=acos(sqrt(-(emR+emE)*(emR*Q+(emR-emp)*ELab)/(emp*emE*ELab)))
            return thetaM
    return False

#This is now deprecated
def solveNum(ang,vE,vR,Vcm,isoE,isoR,exList=[0,0,0,0]):
    emE=getEMass(isoE)+exList[2]
    emR=getEMass(isoR)+exList[3]
    thEject=0
    dTh=0.2
    ang=radians(ang)
    if ang>pi/2:
        ang-=pi
    tolerance=0.0001
    while True:
        thEject+=dTh
        vEy=vE*sin(thEject)
        vEz=vE*cos(thEject)
        vRy=vR*sin(pi-thEject)
        vRz=vR*cos(pi-thEject)

        #They actually have to be zero
        ### deltaPy=(vEy*emE-vRy*emR)*1.0/c**2
        ### deltaPz=(vEz*emE+vRz*emR)*1.0/c**2
        # print deltaPy,deltaPz
        if (vEz+Vcm)==0 or (vRz+Vcm)==0:
            print("No solution was found, div by zero")
            print("#####################################################")
            return False
        thEjectLab=atan(1.0*vEy/(vEz+Vcm))
        ELabEject=emE*(1.0*vEy**2+(vEz+Vcm)**2)/(2*c**2)
        theResLab=atan(1.0*vRy/(vRz+Vcm))
        ELabResid=emR*(1.0*vRy**2+(vRz+Vcm)**2)/(2*c**2)

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
    l=[]
    for e in reactions:
        if 'None' in e:
            continue
        isoEject=e[0]
        isoRes=e[1]
        react1,react2=sReaction(iso1,iso2,isoEject,isoRes,E,ang)

        if react1[0]==[False,False,False,False]:
            break

        firstSols=[react1[0],react2[0]]
        secSols=[react1[1],react2[1]]
        l.append([e,firstSols,secSols])
    return l
#returns the corresponding fused element, along with the max populated
#level and the corresponding remaining energy
def fussionCase(iso1,iso2,E1L,E2L=0):
    isof=getCompound(iso1,iso2)
    if isof==False:
        return False
    Q=getIsoQVal(iso1,iso2,"0None",isof)
    E1cm,E2cm,Ecm=getEcm(iso1,iso2,E1L)
    ETotcm=Q+Ecm
    maxLev,maxLE=getCorrespLevE(isof,ETotcm)
    rKEcm=ETotcm-maxLE #residual KE

    vDump,vDump,Vcm=getVcms(iso1,iso2,iso1,iso2,E1L)
    EcmSys=0.5*(Vcm/c)**2*(getEMass(iso1)+getEMass(iso2))
    rKE=rKEcm+EcmSys

    return isof,maxLev,maxLE,rKE

def getCompound(iso1,iso2):
    a1,k1=getIso(iso1)
    a2,k2=getIso(iso2)

    p1=getPnum(iso1)
    p2=getPnum(iso2)

    pf=p1+p2
    af=a1+a2
    kf=getKey(pf)
    if kf==False:
        return False
    isof=str(af)+kf
    if getPnum(isof):
        return isof
    return False

def getCorrespLevE(iso,E):
    aVal,eName=getIso(iso)
    getMoreData(iso)
    if not checkDictIso(iso):
        return False
    lev,lEMax=0,0
    for e in iDict[eName][1][aVal][1]:
        lE=iDict[eName][1][aVal][1][e][0]
        if lE >= E:
            lev,lEMax=e-1,iDict[eName][1][aVal][1][e-1][0]
            break
    if E>0 and lev==0:
        print("#Energy over max level in db")
        lev,lEMax=e,iDict[eName][1][aVal][1][e][0]
    return lev,lEMax

def getLevelE(iso1,level):
    A,k=getIso(iso1)
    getMoreData(iso1)
    if not checkDictIso(iso1):
        return 0
    return iDict[k][1][A][1][level][0]

def getAllLevels(iso):
    A,k=getIso(iso)
    getMoreData(iso)
    if not checkDictIso(iso):
        return 0
    lList=[]
    for level in iDict[k][1][A][1]:
        lList.append([level,iDict[k][1][A][1][level][0]])
    return lList

def getPopLevels(iso1,aE):
    levels=[]
    iso,eName=getIso(iso1)

    getMoreData(iso1)
    if not checkDictIso(iso1):
        return [1]
    for e in iDict[eName][1][iso][1]:
        lE=iDict[eName][1][iso][1][e][0]
        if lE>aE:
            return levels
        levels.append([e,lE])
    return levels

#If the excitation data is needed then this loads it.
def getMoreData(iso,xFile=None):
    #Careful with neutrons and Nones
    A,k=getIso(iso)
    levDict={}
    if len(iDict[k][1][A])<2:
        if xFile == None:
            t=(iso,)
            cursor.execute('SELECT levNum,xEnergy,extra FROM isoLevels WHERE iso=?', t)
            #Creating subDictionary
            for exData in cursor.fetchall():
                if int(exData[0]) not in levDict:
                    levDict[exData[0]]=[float(exData[1]),myString2List(exData[2])]
                    #print("Debug in getMoreData",levDict[exData[0]])
                    iDict[k][1][A].append(levDict)
        else:
            with open(xFile) as myFileObj:
                lineLst=myFileObj.readlines()

            for a,b in zip(lineLst,range(len(lineLst))):
                levDict[b+1]=[float(a),[]]
                iDict[k][1][A].append(levDict)


#This is now deprecated
def getCoef(iso1,iso2,isoE,isoR,ELab,exList=[0,0,0,0]):
    emp,emt,emE,emR=getAllEMasses(iso1,iso2,isoE,isoR,exList)
    Q=getQVal(emp,emt,emE,emR)
    # Pi=sqrt(2*emp*ELab)/c
    # Vcm=Pi*c**2/(emp+emt)
    # EcmSys=(Pi*c)**2/(2.0*(emp+emt))
    v1=sqrt(2.0*ELab/emp)*c
    v2=0 #For future improvement
    Vcm=(1.0*emp*v1+1.0*emt*v2)/(emp+emt)
    EcmSys=0.5*(Vcm/c)**2*(emp+emt)
    #Available E in b4 collision
    Edisp=ELab-EcmSys
    Ef=Edisp+Q
    if Ef<0:
        print("Inside getCoef Ef = ", Ef)
        print("Not enough energy for reaction")
        return False,False,Vcm,Ef
    #Final momentum, in cm.
    muf=1.0*emE*emR/(emE+emR)
    Pf=sqrt(2.0*Ef*muf)/c
    vE=1.0*Pf*c**2/emE
    vR=1.0*Pf*c**2/emR
    return vE,vR,Vcm,Ef

def getEMass(iso1):
    if iso1 == "n":
        iso1="1n"
    A,k=getIso(iso1)
    vals=[i[0] for i in getIsotopes(iso1)]
    vals.append("p")
    vals.append("d")
    vals.append("t")
    vals.append("a")
    if iso1 not in vals:
        return False
    return iDict[k][1][A][0]*eCoef

#Still work to be done, assuming the nucleus only gets increased mass
#when the reaction occurs (no fission or gammas for now)
def exLevReact(ang,iso1,iso2,isoEject,isoRes,E1L,E2L,eVal=1):
    if eVal==1:
        isoEX1=isoRes
    else:
        isoEX1=isoEject
    Edisp=getAvailEnergy(iso1,iso2,isoEject,isoRes,E1L,E2L)
    popLevels=getPopLevels(isoEX1,Edisp)
    if len(popLevels)<=1:
        popLevels=[[1,0.0]]
    levList=[]
    #For sending the mass excitations into getCoef
    exList=[0,0,0,0]
    for e in popLevels:
        # print e
        if e[1] == False and e[0] != 1:
            #print("#Entered false for e[1] en exLevReact")
            continue
        if eVal==1:
            exList[3]=e[1]
        else:
            exList[2]=e[1]

        # numSol=getEsAndAngs(ang,iso1,iso2,isoEject,isoRes,ELab,E2L=0,\
        #                     exList=exList)

        numSol1,numSol2=analyticSol(iso1,iso2,isoEject,isoRes,\
                           E1L,E2L,angle=ang,exList=exList)

        if numSol1[0]==False:
            break
        levList.append([e,[numSol1,numSol2]])
    return levList

def getQVal(m1,m2,m3,m4):
    Q=(m1+m2-m3-m4)
    return Q

def getIsoQVal(iso1,iso2,iso3,iso4,exList=[0,0,0,0]):
    if not checkReaction(iso1,iso2,iso3,iso4):
        return False
    m1=getEMass(iso1)+exList[0]#Adding mas excitations
    m2=getEMass(iso2)+exList[1]
    m3=getEMass(iso3)+exList[2]
    m4=getEMass(iso4)+exList[3]
    Q=(m1+m2-m3-m4)
    return Q

def getIsoQValAMU(iso1,iso2,iso3,iso4):
    return getIsoQVal(iso1,iso2,iso3,iso4)/eCoef

def iso2String(k,iso,eVal=''):
    return eVal+str(iso)+k

def xReaction(iso1,iso2,isoEject,isoRes,ELab=2.9,ang=30,xf1=None,xf2=None):
    a1,key1=getIso(iso1)
    a2,key2=getIso(iso2)
    aEject,eject=getIso(isoEject)
    aRes,res=getIso(isoRes)

    react=checkReaction(iso1,iso2,isoEject,isoRes)
    if not checkArguments(ELab,react,eject,res):
        return False
    Q=react[3]

    # vE,vR,Vcm,Ef=getCoef(iso1,iso2,isoEject,isoRes,ELab)
    # if vE==False:
    #     return False
    lL=[]
    E1L=ELab
    #For now E2L=0
    E2L=0
    if xf1 != None:
        getMoreData(isoEject,xf1)

    if xf2 != None:
        getMoreData(isoRes,xf2)

    c=[iso2String(eject,aEject,'*'),iso2String(res,aRes,'')]
    # lL.append([c,exLevReact(ang,iso1,iso2,isoEject,isoRes,ELab,Ef,0)])
    exL1=exLevReact(ang,iso1,iso2,isoEject,isoRes,E1L,E2L,0)
    # exL1=[[val[0],val[1][0]] for val in exL1L]
    lL.append([c,exL1])

    c=[iso2String(eject,aEject,''),iso2String(res,aRes,'*')]
    # lL.append([c,exLevReact(ang,iso1,iso2,isoEject,isoRes,ELab,Ef,1)])
    exL2=exLevReact(ang,iso1,iso2,isoEject,isoRes,E1L,E2L,1)
    # exL2=[[val[0],val[1][0]] for val in exL2L]
    lL.append([c,exL2])

    c=[iso2String(res,aRes,'*'),iso2String(eject,aEject,'')]
    # lL.append([c,exLevReact(ang,iso1,iso2,isoRes,isoEject,ELab,Ef,0)])
    exL3=exLevReact(ang,iso1,iso2,isoRes,isoEject,E1L,E2L,0)
    # exL3=[[val[0],val[1][0]] for val in exL3L]
    lL.append([c,exL3])

    c=[iso2String(res,aRes,''),iso2String(eject,aEject,'*')]
    # lL.append([c,exLevReact(ang,iso1,iso2,isoRes,isoEject,ELab,Ef,1)])
    exL4=exLevReact(ang,iso1,iso2,isoRes,isoEject,E1L,E2L,1)
    # exL4=[[val[0],val[1][0]] for val in exL4L]
    lL.append([c,exL4])

    return lL

def xXTremeTest(iso1,iso2,E=10,ang=30):
    reactions=nReaction(iso1,iso2)
    rStuff=[]
    for e in reactions:
        if 'None' in e:
            continue

        isoEject=e[0]
        isoRes=e[1]

        reactL=xReaction(iso1,iso2,isoEject,isoRes,E,ang)
        react=[]

        for lr in reactL:
            exitReact=lr[0]
            for info in lr[1:]:
                firstSolEs=[[val[0],val[1][0]] for val in info]
                secSol=[[val[0],val[1][1]] for val in info]
                react.append([exitReact,firstSolEs,secSol])

        #Is this meaningful?
        if react==False:
            break

        rStuff.append([e,react])
    return rStuff

def checkArguments(ELab,react,eject,res):
    if ELab<=0:
        print("Lab energy has to be positive")
        return False

    if not react:
        return False

    if eject=='None' or res=='None':
        print("Reaction must have at least 2 final elements")
        return False

    return True

def getAllEMasses(iso1,iso2,isoEject,isoRes,exList=[0,0,0,0]):
    emp=getEMass(iso1)
    emt=getEMass(iso2)

    emE=getEMass(isoEject)
    emR=getEMass(isoRes)

    emp+=exList[0]
    emt+=exList[1]
    emE+=exList[2]
    emR+=exList[3]

    return emp,emt,emE,emR

#Given an energy, beam energy, angle, a list of reactions and a
#tolerance it returns values to hint where it might be from
def fReact(E,bE,angle,rList,tol=140):
    for iR in rList:
        print("######################")
        print(iR)
        print("######################")
        #Need to be upgraded for second sol from xXtremeTest
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
                    print(e[0],ee[0],states)

def findOE(Eang,ang,iso1,iso2):
    E=Eang
    Emax=2.0*Eang
    dE=0.01
    tolerance=0.00001
    while True:
        sRList=sReaction(iso1,iso2,iso1,iso2,E,ang)
        sR=sRList[0]
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
    theta=radians(theta)
    z1=getPnum(iso1)
    z2=getPnum(iso2)
    dSigma=(z1*z2*alpha*hbc/(4*Ecm))**2/sin(theta/2)**4
    # converting to mb
    dSigma*=10
    return dSigma

def rutherfordLab0(iso1,iso2,ELab,thetaL):
    """ Returns the rutherford value in the lab frame"""
    Ecm=getEcm(iso1,iso2,ELab)[2] #Taking the 3rd argument
    K=getMass(iso1)/getMass(iso2)
    #see m. cottereau and f. lefebvres recuel de problemes...
    thetaCM=solveAng(thetaL,K)
    dSigmaL=rutherford0(iso1,iso2,Ecm,thetaCM)*\
        (1+K**2+2*K*cos(thetaCM))**(3.0/2.0)/(1+K*cos(thetaCM))
    return dSigmaL

def solveAng(thetaL,ratio,direction="f"):
    """ Returns the CM angle """
    thetaL=radians(thetaL)
    tgThetaL=tan(thetaL)
    #"f" is for forward sol "b" for backward sol
    if direction=="f":
        thetaCM=0
        dTh=0.05
        sign=1
    else:
        thetaCM=pi
        dTh=-0.05
        sign=-1

    def myFunct(thetaCM,ratio):
        return sin(thetaCM)/(cos(thetaCM)+ratio)
    tolerance=0.0001
    # i=0
    while True:
        fVal=myFunct(thetaCM,ratio)
        # if i>=20:
        #     break
        # print "fVal is:",fVal
        # i+=1
        diff=sign*(tgThetaL-fVal)
        if abs(diff)<tolerance:
            break
        if dTh>0 and diff<0 or dTh<0 and diff>0:
            dTh *= -1.0/2
            # print "Sign switch"
        if sign==1 and thetaCM>=pi or sign==-1 and thetaCM<0:
            # print "No solution was found"
            return False
        thetaCM+=dTh
    thetaL=degrees(atan(fVal))
    return degrees(thetaCM)

def getAngs(iso1,iso2,isoE,isoR,E1L,exList,thetaL):
    vE,vR,Vcm,Ef=getCoef(iso1,iso2,isoE,isoR,E1L,exList)
    r=1.0*vE/Vcm
    ratio=1.0/r
    thetaCMf=solveAng(thetaL,ratio,"f")
    # For excited states it stays in this function
    #Commenting it for now
    # thetaCMb=solveAng(thetaL,ratio,"b")
    thetaCMb=False
    #No need to convert to radians in this case
    return thetaCMf,thetaCMb

#This is now deprecated
def getEsAndAngs(iso1,iso2,isoE,isoR,E1L,E2L=0,thetaL=0,\
                 exList=[0,0,0,0],direction="f"):
    angMax=getMaxAng(iso1,iso2,isoE,isoR,E1L,E2L,exList)[0]
    #Keeping angles in degrees
    if thetaL>angMax:
        print("Angle is too big, no solution found")
        return [False,False,False,False]

    #Getting the coefficients
    vE,vR,Vcm,Ef=getCoef(iso1,iso2,isoE,isoR,E1L,exList)
    #Getting the CM angles
    angs=getAngs(iso1,iso2,isoE,isoR,E1L,exList,thetaL)
    if direction=="f":
        thEjectCM=angs[0]
    else:
        thEjectCM=angs[1]

    thEjectCM=radians(thEjectCM)
    theResCM=pi-thEjectCM

    emE=getEMass(isoE)+exList[2]
    emR=getEMass(isoR)+exList[3]

    vEy=vE*sin(thEjectCM)
    vEz=vE*cos(thEjectCM)
    vRy=vR*sin(theResCM)
    vRz=vR*cos(theResCM)

    thEjectLab=atan(vEy/(vEz+Vcm))
    ELabEject=emE*(vEy**2+(vEz+Vcm)**2)/(2*c**2)
    theResLab=atan(vRy/(vRz+Vcm))
    ELabResid=emR*(vRy**2+(vRz+Vcm)**2)/(2*c**2)

    return [degrees(thEjectLab),ELabEject,degrees(theResLab),\
            ELabResid]

def getMaxAng(iso1,iso2,isoE,isoR,E1L,E2L=0,exList=[0,0,0,0]):
    emp,emt,emE,emR=getAllEMasses(iso1,iso2,isoE,isoR,exList)
    # v1=sqrt(2.0*E1L/emp)
    # v2=0 #Zero for now
    vE,vR,Vcm,Ef=getCoef(iso1,iso2,isoE,isoR,E1L,exList)
    if vE==False:
        print("Not enough energy to get angle")
        return False

    r1=1.0*vE/Vcm
    r2=1.0*vR/Vcm

    if r1>=1:
        maxAng1=pi
    else:
        maxAng1=atan(r1/sqrt(1.0-r1**2))

    if r2>=1:
        maxAng2=pi
    else:
        maxAng2=atan(r2/sqrt(1.0-r2**2))

    return [degrees(maxAng1),degrees(maxAng2)]

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
    return 1.0*Nr/(rutherfordLab0(ps,ts,E,angle)*dOmega)

def getdSigma(Nn,dOmega,T):
   return 1.0*Nn/(dOmega*T)

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
    nm=getEMass("1n")
    return em-z*pm-(A-z)*nm

#Binding Energy per nucleon
def getBEperNucleon(iso):
    A,k=getIso(iso)
    return 1.0*getBE(iso)/A

#Using the liquid drop model for the binding energy
#Values taken from A. Das and T. Ferbel book
def getLDBE(iso,a1=15.6,a2=16.8,a3=0.72,a4=23.3,a5=34):
    #All the coefficients are in MeV
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
    return 1.0*getLDBE(iso)/A

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
    return 1.0*getLDEMass(iso)/eCoef

#de Broglie wavelength in angstrom
def deBroglie(iso,E):
    # iso=str(A)+element
    em=getEMass(iso)
    p=sqrt(2.0*em*E) #a "c" from here goes to the hc
    return hc/p/100 # 1/100 to convert to angstrom

#reduced de Broglie wavelength in angstrom
def reducedDeBroglie(iso,E):
    return deBroglie(iso,E)/(2.0*pi)

#Compton wavelength
def comptonW(iso):
    em=getEMass(iso)
    return hc/em*1000 #*1000 to convert to fm

#Reduced Compton wavelength
def rComptonW(iso):
    em=getEMass(iso)
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
    return (2*em*V0*a**3/(3*hbc**2))**2

#soft sphere total CS
def softSphereTCS(isop,isot,V0=50):
    return 4*pi*softSphereDCS(isop,isot,V0)

#soft sphere using the second Born approximation
def softSphereDSBorn(isop,isot,V0=50):
    a=nRadius(isot)
    # iso=str(ap)+sp
    em=getEMass(isop)
    firstC=2*em*V0*a**3/(3*hbc**2)
    secondC=1-4*em*V0*a**2/(5*hbc**2)
    return (firstC*secondC)**2

#soft sphere using the second Born approximation for total CS
def softSphereTSBorn(isop,isot,V0=50):
    return 4*pi*softSphereDSBorn(isop,isot,V0)

#Using the Yukawa potential
def yukawaDCS(isop,isot,E,theta,beta,mu):
    # iso=str(ap)+sp
    eMass=getEMass(isop)
    theta=radians(theta)
    k=sqrt(2*eMass*E/hbc)
    kappa=2*k*sin(theta/2)
    return (-2*eMass*beta/(hbc**2*(mu**2+kappa**2)))**2

#Getting the total CS for the Yukawa potential, Griffiths 11.12 Note;
#this is still in testing
def yukawaTCS(isop,isot,E,theta,beta,mu):
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
    TAlpha=Q*(1.0-4.0/A)
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

    B=getB(iso1,isoEject)
    em=getEMass(isoEject) #Most probably alpha part mass
    z1=getPnum(iso1)
    z2=getPnum(isoEject)

    x=1.0*Q/B
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

#########################################################################
###### Testing analytic #################################################
#########################################################################

#def getVcms(v1L,v2L,m1,m2):
def getVcms(iso1,iso2,isoEject,isoRes,E1L,E2L=0,exList=[0,0,0,0]):
    #In case the isos are excited b4 reaction
    m1=getEMass(iso1)+exList[0]
    m2=getEMass(iso2)+exList[1]
    # print "m1,m2 = ", m1,m2
    # print "E1L,E2L = ",E1L,E2L
    v1L=sqrt(2.0*E1L/m1)*c
    v2L=sqrt(2.0*E2L/m2)*c

    Vcm=1.0*(v1L*m1+v2L*m2)/(1.0*m1+m2)
    Q=getIsoQVal(iso1,iso2,isoEject,isoRes)
    Q-=sum(exList)
    # print "Vcm,Q = ", Vcm,Q
    #abs is impotant, they are magnitudes!!
    v1cm=abs(v1L-Vcm)
    v2cm=abs(v2L-Vcm)

    E1cm=0.5*m1*(v1cm/c)**2
    E2cm=0.5*m2*(v2cm/c)**2
    Ecm=E1cm+E2cm+Q
    if Ecm<=0:
        return False,False,False
    # print "E1cm,E2cm,Ecm = ",E1cm,E2cm,Ecm
    vEcm,vRcm=getVcmsFromEcm(isoEject,isoRes,Ecm,exList[0:2])
    # print "v1cm,v2cm",v1cm,v2cm
    # print "vEcm,vRcm",vEcm,vRcm

    return vEcm,vRcm,Vcm

def getVcmsFromEcm(iso1,iso2,Ecm,redXL=[0,0]):
    m1=getEMass(iso1)+redXL[0]
    m2=getEMass(iso2)+redXL[1]
    if Ecm<=0:
        return False,False
    v1cm=sqrt(2.0*Ecm/(m1*(1+1.0*m1/m2)))*c
    v2cm=(1.0*m1)/m2*v1cm
    return v1cm,v2cm

def getEFromV(iso,v,xMass=0):
    m=getEMass(iso)+xMass
    return 0.5*m*(v/c)**2

#Testing the non numeric solution
def analyticSol(iso1,iso2,isoEject,isoRes,E1L,E2L=0,angle=0,exList=[0,0,0,0]):
    vEcm,vRcm,Vcm=getVcms(iso1,iso2,isoEject,isoRes,E1L,E2L,exList)
    if vEcm == False:
        return [[False,False,False,False],[]]
    maxAng=getMaxAngles(iso1,iso2,isoEject,isoRes,E1L,E2L,exList)[0]
    if maxAng=="NaN":
        return "NaN"
    if angle>=maxAng:
        return [[False,False,False,False],[]]
    # maxAng=radians(maxAng) #not sure about this
    # angLA1,Ea1,angLB1,Eb1=getEsAndAngs(iso1,iso2,isoEject,isoRes,E1L,E2L,angle,exList)
    sol1,sol2=analyticDetails(vEcm,vRcm,Vcm,angle,isoEject,isoRes)
    angLA1,Ea1,angLB1,Eb1=sol1
    retVal2=[]
    if sol2 != []:
        angLA2,Ea2,angLB2,Eb2=sol2
        retVal2=[degrees(angLA2),Ea2,degrees(angLB2),Eb2]
    retVal1=[degrees(angLA1),Ea1,degrees(angLB1),Eb1]
    return [retVal1,retVal2]

def analyticDetails(vEcm,vRcm,Vcm,angle,isoEject,isoRes):
    angle=radians(angle)
    kAng=tan(angle)
    k1=1.0*vEcm/Vcm
    discr=1-(1+kAng**2)*(1-k1**2)
    secSol=True
    if discr<0:
        # print "Angle maybe too large"
        return [[False,False,False,False],[]]
    if angle <= pi/2:
        vxa1=Vcm*(1+sqrt(discr))/(1+kAng**2)
    else: #angle >= pi/2
        #Using the backward solution for this case
        vxa1=Vcm*(1-sqrt(discr))/(1+kAng**2)
        secSol=False
    if Vcm<=vEcm:
        #There can only be one solution in this case.
        secSol=False

    #Ignoring the second solutions for now
    # vxa2=Vcm*(1-sqrt(discr))/(1+kAng**2)
    vya1=kAng*vxa1
    # vya2=kAng*vxa2
    va1=sqrt(vxa1**2+vya1**2)
    # va2=sqrt(vxa2**2+vya2**2)
    angLA1=atan(vya1/vxa1)
    # angLA2=atan(vya2/vxa2)

    #To get the angle and velocity of the corresponding particle, we
    #do the following 1.- Get the center of mass velocity of
    #particle "a".
    vxa1CM=vxa1-Vcm
    vya1CM=vya1
    # vxa2CM=vxa2-Vcm
    # vya2CM=vya2
    #2.- Get the slopes
    sa1=vya1CM/vxa1CM
    # sa2=vya2CM/vxa2CM
    #3.- The corresponding angles
    angA1=atan(sa1)
    # angA2=atan(sa2)
    # print "angA1,angA2 = ", degrees(angA1),degrees(angA2)
    angB1=angA1-pi
    # angB2=angA2-pi
    #4.- The corresponding center of mass velocity values
    vxb1CM=vRcm*cos(angB1)
    vyb1CM=vRcm*sin(angB1)
    # vxb2CM=vRcm*cos(angB2)
    # vyb2CM=vRcm*sin(angB2)
    #5.- The lab values
    vxb1=vxb1CM+Vcm
    vyb1=vyb1CM
    vb1=sqrt(vxb1**2+vyb1**2)
    # vxb2=vxb2CM+Vcm
    # vyb2=vyb2CM
    # vb2=sqrt(vxb2**2+vyb2**2)
    angLB1=atan(vyb1/vxb1)
    # angLB2=atan(vyb2/vxb2)
    Ea1=getEFromV(isoEject,va1)
    Eb1=getEFromV(isoRes,vb1)
    firstSolList=[angLA1,Ea1,angLB1,Eb1]

    secSolList=[]
    if secSol:
        #Calculating the second solutions here
        vxa2=Vcm*(1-sqrt(discr))/(1+kAng**2)
        vya2=kAng*vxa2
        va2=sqrt(vxa2**2+vya2**2)
        angLA2=atan(vya2/vxa2)

        #To get the angle and velocity of the corresponding particle, we
        #do the following 1.- Get the center of mass velocity of
        #particle "a".
        vxa2CM=vxa2-Vcm
        vya2CM=vya2

        #2.- Get the slopes
        sa2=vya2CM/vxa2CM
        #3.- The corresponding angles
        angA2=atan(sa2)
        # print "angA1,angA2 = ", degrees(angA1),degrees(angA2)
        angB2=angA2-pi
        #4.- The corresponding center of mass velocity values
        vxb2CM=vRcm*cos(angB2)
        vyb2CM=vRcm*sin(angB2)
        #5.- The lab values
        vxb2=vxb2CM+Vcm
        vyb2=vyb2CM
        vb2=sqrt(vxb2**2+vyb2**2)
        # print(vb2)
        angLB2=atan(vyb2/vxb2)
        Ea2=getEFromV(isoEject,va2)
        Eb2=getEFromV(isoRes,vb2)

        secSolList=[angLA2,Ea2,angLB2,Eb2]

    #Angle is in radians
    return [firstSolList,secSolList]

# def getMaxAngles(v1L,v2L,m1,m2):
def getMaxAngles(iso1,iso2,isoEject,isoRes,E1L,E2L=0,exList=[0,0,0,0]):
    vEcm,vRcm,Vcm=getVcms(iso1,iso2,isoEject,isoRes,E1L,E2L,exList)
    if Vcm == False:
        return ["NaN","NaN"]
    k1=1.0*vEcm/Vcm
    k2=1.0*vRcm/Vcm
    # print "k1,k2 = ",k1,k2
    if k1 != 1:
        discr1=k1**2/(1.0-k1**2)
        # print "discr1 = ",discr1
        if discr1<0: #Vcm < vEcm
            maxAng1=pi
        else:
            maxAng1=atan(sqrt(discr1))
    else:
        maxAng1=pi #Maybe it should be pi/2

    if k2 != 1:
        discr2=k2**2/(1.0-k2**2)
        # print "discr2 = ",discr2
        if discr2<0: #Vcm < vRcm
            maxAng2=pi
        else:
            maxAng2=atan(sqrt(discr2))
    else:
        maxAng2=pi #Maybe it should be pi/2

    return [degrees(maxAng1),degrees(maxAng2)]


def getIsotopes(s):
    a,key=getIso(s)
    l=[]
    if key not in iDict:
        return False
    for e in iDict[key][1]:
        isoVar=str(e)+key
        l+=[[isoVar,iDict[key][1][e][0]]]
    return l

# print "#Populating dictionary"
# iDict=populateDict()
iDict=fastPopulateDict()

def gamowE(iso1,iso2):
    #In MeV
    z1=getPnum(iso1)
    z2=getPnum(iso2)
    em1=getEMass(iso1)
    em2=getEMass(iso1)
    eMu=em1*em2/(em1+em2)
    GE=2*(pi*z1*z2*alpha)**2*eMu
    return GE

def gamowPeak(iso1,iso2,T):
    GE=gamowE(iso1,iso2)
    TE=temp2E(T)/10**6 #Converting to MeV
    GP=(TE**2*GE/4)**(1.0/3)
    return GP

def temp2E(T):
    #Energy given is in eV
    #Ta=300K, Ea=1/40eV
    Ta=300
    Ea=0.025
    TE=T/Ta*Ea
    return TE

#Bethe-Bloch energy loss stuff
def getBeta(iso,E):
    m=getEMass(iso)
    #The non relativistic version is:
    #v=sqrt(2.0*E/m)*c, and beta=v/c
    # beta=sqrt(2.0*E/m)
    #Using the relativistic version
    beta=sqrt(1-(1/(E/m+1))**2)
    return beta

def getTOF(iso,E,L):
    #Here L is in meters
    beta=getBeta(iso,E)
    v=c*beta
    #t is in seconds
    t=L/v
    return t

def getElectDensity(Z,A_r,rho):
    """Returns the electron density, in #e^-/cm^3"""
    #Properly is; n=(N_a*Z*rho)/(A*M_u), but M_u=1 g/mol
    n=(N_a*Z*rho)/A_r
    return n

def getBlochMeanExcE(Z):
    """Returns the Bloch approximation of the mean ionization potential in
    eV """
    I=10*Z
    return I

#Using this for now, this has to be improved through a database or a
#pickle file!!. Format will probably change. The list format (for now)
#is Z, A_r, rho(at solid state).
# materialDict={"silicon":[14,28.085,2.3290],
#               "gold":[79,196.966569,19.30],
#               "aluminum":[13,26.9815385,2.70],
#               "copper":[29,63.54,8.96]}

def checkMaterial(material,bloch=False,density=None):
    #Calls get material properties to fill the cache only once
    vals=getMaterialProperties(material,bloch,density)
    if vals[-1] == False:
        return False
    return True

#Global variable to avoid loading the pkl file over and over again.
materialDictCache={}

def getMaterialProperties(material,bloch=False,density=None):
    if material in materialDictCache:
        return materialDictCache[material]
    materialDict=getChemDictFromFile()
    if material not in materialDict:
        return False,False,False,False
    if bloch:
        Z=materialDict[material][0]
        materialDict[material][-1] = getBlochMeanExcE(Z)
    if density != None:
        materialDict[material][2]=density
    if materialDict[material][-1] == '-':
        return False,False,False,False
    materialDictCache[material]=materialDict[material]
    return materialDict[material]

def getBetheLoss(iso,E,material):
    """Gets the Bethe energy loss differential of an ion through a
    material, it includes soft and hard scattering.

    """
    beta=getBeta(iso,E)
    beta2=beta**2
    coefs=getCBbetaCoef(iso,material)
    if coefs == None:
        return None
    C_beta,B_beta = coefs
    #remember dE/dx is negative, it is the relativistic formula
    dEx=C_beta/beta2*(log((B_beta*beta2)/(1-beta2))-beta2)
    return dEx

CBDictCache={}

def getCBbetaCoef(iso, material):
    myString="[" + iso + "," + material + "]"
    if myString in CBDictCache:
        return CBDictCache[myString]
    Z,A_r,rho,I=getMaterialProperties(material)
    if rho == False:
        return None
    n=getElectDensity(Z,A_r,rho)
    #n has to be given in #e^-/fm^3
    n*=10**(-39)
    zNum=getPnum(iso)
    #"I" was given in eV so it has to be converted in MeV
    I*=10**(-6)
    C_beta=4*pi/electEMass*n*zNum**2*(hbc*alpha)**2
    C_beta*=10**(9) #Converting the units into MeV/mu^3
    B_beta=2*electEMass/I
    CBDictCache[myString]=[C_beta,B_beta]
    return CBDictCache[myString]

def integrateELoss(iso,E,material,thick):
    """Gets the final energy of an ion going through a material with a
    certain thickness.

    """
    partitionSize=10000
    dx=1.0*thick/partitionSize

    ##For the criteria of considering the particle has stopped##
    coefs=getCBbetaCoef(iso,material)
    if coefs == None:
        #No material was found
        return -2
    C_beta,B_beta = coefs
    ionMass=getEMass(iso)
    #e=2.71...
    EM=e*ionMass/(2*B_beta)
    dExMax=(C_beta*B_beta)/e
    fracCrit=0.01
    ##############
    for i in range(partitionSize):
        dEx=getBetheLoss(iso,E,material)
        if dEx == None:
            #No material was found
            return -2
        E-=dEx*dx
        if E<EM and dEx<=fracCrit*dExMax:
            #Particle has stopped
            return -1
    return E
#Note that the DeltaEs for alphas of 5.15, 5.48, 5.80 are 2.55, 2.41,
#2.29 for an 11 micron silicon detector (and I think with a 1 micron
#gold coating)

#Don't forget this?
#Leave it commented or else errors occur :(
# conn.close()
