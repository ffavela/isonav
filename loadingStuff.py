#   Copyright (C) 2015 Francisco Favela

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

from os import listdir
from os.path import isfile, join
import pickle
import os.path
import sys
from enxParser import *

if os.path.dirname(__file__) == "/usr/share/isonav":
    DATA_PATH = "/usr/share/isonav/data1p4"
# elif os.path.dirname(__file__) == ".":
else:
    # fileName=os.path.dirname(__file__)
    DATA_PATH ="./data1p4"
    print("#You do not have a working installation of isonav")
    print("#See the installation procedure in the README file")
    # sys.exit(1)

isoDictLoc=os.path.join(DATA_PATH, "isoDict.pkl")
isoMassesLoc=os.path.join(DATA_PATH, "isoMasses.txt")
isoDictMassLoc=os.path.join(DATA_PATH, "isoDictMass.pkl")
isoDatadb=os.path.join(DATA_PATH, "isoData.db")
isonavQR=os.path.join(DATA_PATH, "isonavQR.png")
wMLoc=os.path.join(DATA_PATH, "webMasses.txt")

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
           'Cn','Ed','Fl','Ef','Lv','Eh','Ei']

nameDict={'n':"neutron",'H':"Hydrogen","He":"Helium","Li":"Lithium",
          "Be":"Berillium","B":"Boron","C":"Carbon","N":"Nitrogen",
          "O":"Oxygen","F":"Fluorine","Ne":"Neon","Na":"Sodium",
          "Mg":"Magnesium","Al":"Aluminum","Si":"Silicon",
          "P":"Phosphorus","S":"Sulfur","Cl":"Chlorine","Ar":"Argon",
          "K":"Potassium","Ca":"Calcium","Sc":"Scandium",
          "Ti":"Titanium","V":"Vanadium","Cr":"Chromium",
          "Mn":"Manganese","Fe":"Iron","Co":"Cobalt","Ni":"Nickel",
          "Cu":"Copper","Zn":"Zinc","Ga":"Gallium","Ge":"Germanium",
          "As":"Arsenic","Se":"Selenium","Br":"Bromine","Kr":"Krypton",
          "Rb":"Rubidium","Sr":"Strontium","Y":"Yttrium","Zr":"Zirconium",
          "Nb":"Niobium","Mo":"Molybdenum","Tc":"Technetium",
          "Ru":"Ruthenium","Rh":"Rhodium","Pd":"Palladium","Ag":"Silver",
          "Cd":"Cadmium","In":"Indium","Sn":"Tin","Sb":"Antimony",
          "Te":"Tellurium","I":"Iodine","Xe":"Xenon","Cs":"Cesium",
          "Ba":"Barium","La":"Lanthanum","Ce":"Cerium","Pr":"Praseodymium",
          "Nd":"Neodymium","Pm":"Promethium","Sm":"Samarium",
          "Eu":"Europium","Gd":"Gadolinium","Tb":"Terbium","Dy":"Dysprosium",
          "Ho":"Holmium","Er":"Erbium","Tm":"Thulium","Yb":"Ytterbium",
          "Lu":"Lutetium","Hf":"Hafnium","Ta":"Tantalum","W":"Tungsten",
          "Re":"Rhenium","Os":"Osmium","Ir":"Iridium","Pt":"Platinum",
          "Au":"Gold","Hg":"Mercury","Tl":"Thallium","Pb":"Lead",
          "Bi":"Bismuth","Po":"Polonium","At":"Astatine","Rn":"Radon",
          "Fr":"Francium","Ra":"Radium","Ac":"Actinium","Th":"Thorium",
          "Pa":"Protactinium","U":"Uranium","Np":"Neptunium","Pu":"Plutonium",
          "Am":"Americium","Cm":"Curium","Bk":"Berkellium",
          "Cf":"Californium","Es":"Einsteinium","Fm":"Fermium","Md":"Mendelevium",
          "No":"Nobelium","Lr":"Lawrencium","Rf":"Rutherfordium",
          "Db":"Dubnium","Sg":"Seaborgium","Bh":"Bohrium","Hs":"Hassium",
          "Mt":"Meitnerium","Ds":"Darmstadtium","Rg":"Roentgenium",
          "Cn":"Copernicium","Ed":"Ununtrium","Fl":"Flerovium","Ef":"Ununpentium",
          "Lv":"Livermorium","Eh":"Ununseptium","Ei":"Ununoctium"}

# if not os.path.isfile(isoDictLoc):
#     lines = [line.strip().split() for line in open(isoMassesLoc)]

def populateDict1():
    lines = [line.strip().split() for line in open(isoMassesLoc)]
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
    lines = [line.strip().split() for line in open(isoMassesLoc)]
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
        print("#Dictionary file does not exist, creating it")
        iDict=populateDict1()
        iDict=populateDict2(iDict)
        pickle.dump(iDict,open(isoDictLoc,"wb"))
    return iDict

def fastPopulateDict():
    if os.path.isfile(isoDictMassLoc):
        # print "#Dictionary file exists, loading it"
        iDict = pickle.load(open(isoDictMassLoc, "rb" ))
    else:
        print("#Dictionary file does not exist, creating it")
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

def generateIsoMfromWebM():
    FILE = open(isoMassesLoc,"w")
    lines = [line.strip().split() for line in open(wMLoc)]
    for line in lines:
        #Omitting empty lines and beginning with #
        if len(line)>0 and line[0][0] != '#':
            massP2=line[-2]
            # if '#' in massP2:
            #     continue #Omitting this values
            newMassP2 = massP2.replace(".", "")
            newerMassP2 = newMassP2.replace("#", "")
            massP1= line[-3]
            mass=float(massP1+"."+newerMassP2)
            if line[4].isdigit():
                symbol=line[5]
                aVal=int(line[4])
                pVal=int(line[3])
            else:
                symbol=line[4]
                aVal=int(line[3])
                pVal=int(line[2])
            myString=str(pVal)+"\t\t"+str(aVal)+"\t"+str(mass)+"\n"
            print(myString)
            FILE.write(myString)
    FILE.close()
# print isoVal
# print len(isoVal)
