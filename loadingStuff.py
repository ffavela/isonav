from os import listdir
from os.path import isfile, join
import pickle
import os.path
import sys
from enxParser import *

if os.path.dirname(__file__) == "/usr/share/isonav":
    DATA_PATH = "/usr/share/isonav/data"
# elif os.path.dirname(__file__) == ".":
else:
    fileName=os.path.dirname(__file__)
    DATA_PATH = fileName+"/data"
    print "#You do not have a working installation of isonav"
    print "#See the installation procedure in the README file"
    # sys.exit(1)

isoDictLoc=os.path.join(DATA_PATH, "isoDict.pkl")
isoMassesLoc=os.path.join(DATA_PATH, "isoMasses.txt")
isoDictMassLoc=os.path.join(DATA_PATH, "isoDictMass.pkl")
isoDatadb=os.path.join(DATA_PATH, "isoData.db")

#Isotope dictionary
iDict={}
listStuff=['n','H','He','Li','Be','B','C','N','O','F','Ne',
           'Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca',
           'Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn',
           'Ga','Ge','As','Se','Br','Kr','Rb','Sr','Y','Zr',
           'Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn',
           'Sb','Te','I','Xe','Cs','Ba','La','Ce','Pr','Nd',
           'Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb',
           'Lu','Hf','Ta','W','Re','Os',
           'Ir','Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn',
           'Fr','Ra','Ac','Th','Pa','U','Np','Pu','Am','Cm',
           'Bk','Cf','Es','Fm','Md','No','Lr',
           'Rf','Db','Sg','Bh','Hs','Mt','Ds','Rg',
           'Cn','Uut','Fl','Uup','Lv','Uus','Uuo']

if  os.path.isfile(isoDictLoc):
    lines = [line.strip().split() for line in open(isoMassesLoc)]

def populateDict1():
    listLen=len(listStuff)
    #iDict[e][0]==proton number
    iDict['None']=[0,{0:[0]}]
    for i in range(listLen):
        iDict[listStuff[i]]=[i,{}]
        for j in lines:
            if i == int(j[0]):
                iDict[listStuff[i]][1][int(j[1])]=[float(j[2])]
    return iDict

def populateDict2(iDict):
    listLen=len(listStuff)
    #iDict[e][0]==proton number
    enxList=putIsoData()
    for i in range(listLen):
        for j in lines:
            if i == int(j[0]):
                fName=getFileName(enxList,listStuff[i],int(j[1]))
                if not fName:
                    # iDict[listStuff[i]][1][int(j[1])].append([])
                    continue
                fName="excitedData/"+fName
                pDPart=enxParse(fName)
                iDict[listStuff[i]][1][int(j[1])].append(pDPart)
                # if j <=3:
                #     print iDict[listStuff[i]][1][int(j[1])]
    return iDict

def getFileName(aList,key,iso):
    for e in aList:
        if e[0]==key and e[1]==iso:
            return e[2]
    return False

def populateDict():
    if os.path.isfile(isoDictLoc):
        # print "#Dictionary file exists, loading it"
        iDict = pickle.load(open(isoDictLoc, "rb" ))
    else:
        print "#Dictionary file does not exist, creating it"
        iDict=populateDict1()
        iDict=populateDict2(iDict)
        pickle.dump(iDict,open(isoDictLoc,"wb"))
    return iDict

def fastPopulateDict():
    if os.path.isfile(isoDictMassLoc):
        # print "#Dictionary file exists, loading it"
        iDict = pickle.load(open(isoDictMassLoc, "rb" ))
    else:
        print "#Dictionary file does not exist, creating it"
        iDict=populateDict1()
        pickle.dump(iDict,open(isoDictMassLoc,"wb"))
    return iDict
    
def putIsoData():
    isoVal=getIsoVal()
    filterList=[]
    for e in isoVal:
        #Ignoring weird enx files
        if '_' not in e[0] and not e[0].isdigit():
            boolVal=e[1] in iDict[e[0]][1]
            if boolVal:
                # print e, boolVal
                filterList+=[e]
    return filterList

def index(string,char):
    """Finds the index of the first char that is found"""
    for i in range(len(string)):
        if string[i]==char:
            return i
    return -1

def getIsoVal():
    return [[f[3:index(f,'.')],int(f[0:3]),f] for f in listdir('excitedData')\
            if isfile(join('excitedData',f))] 

# print isoVal
# print len(isoVal)
