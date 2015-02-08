#Parses enx files

def enxParse(enxFile):
    f=open(enxFile,"r")
    lines=f.readlines()
    levelDict={}
    for e in lines:
        a=levelParseOne(e)
        if a != False and int(a[0]) not in levelDict:
            #a[0]=level, [float(a[2])/1000 energy in MeV and extra stuff
            levelDict[int(a[0])]=[float(a[2])/1000,a[3:]]
    # for l in levelDict:
    #     print l,levelDict[l]
    return levelDict
    # print levelDict

def isNumeric(string):
    try:
        float(string)
        return True
    except (ValueError, TypeError):
        return False

def levelParseOne(stringLine):
    line=stringLine.split()
    if len(line)>=3 and isNumeric(line[0]) \
       and line[1]=="L" and isNumeric(line[2]):
        return line
    return False
