from os import listdir
from os.path import isfile, join


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
