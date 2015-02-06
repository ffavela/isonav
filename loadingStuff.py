from os import listdir
from os.path import isfile, join

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

lines = [line.strip().split() for line in open('isoMasses.txt')]
def populateDict():
    listLen=len(listStuff)
    #iDict[e][0]==proton number
    iDict['None']=[0,{0:[0]}]
    # counter=0
    for i in range(listLen):
        iDict[listStuff[i]]=[i,{}]
        # counter+=1
        # if counter >=5:
        #     break
        for j in lines:
            if i == int(j[0]):
                iDict[listStuff[i]][1][int(j[1])]=[float(j[2])]
                # print iDict[listStuff[i]][1][int(j[1])]
                # iDict[listStuff[i]][1][int(j[1])]+=[float(j[2])]
    return iDict


def index(string,char):
    """Finds the index of the first char that is found"""
    for i in range(len(string)):
        if string[i]==char:
            return i
    return -1

def getIsoVal():
    return [[f[3:index(f,'.')],int(f[0:3])] for f in listdir('excitedData')\
            if isfile(join('excitedData',f))] 

# print isoVal
# print len(isoVal)
