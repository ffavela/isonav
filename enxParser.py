#   Copyright (C) 2016 Francisco Favela

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
    if len(stringLine)>=4:
        line=stringLine[3:].split()
    else:
        line=stringLine.split()
    # line=stringLine.split()
    if len(line)>=3 and isNumeric(line[0]) \
       and line[1]=="L" and isNumeric(line[2]):
        return line
    return False
