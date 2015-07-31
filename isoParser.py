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

import re
#Identifies isotopes and reactions from strings

#Simply to recognize the element isotope
isoRe=re.compile('\d+[A-Z][a-z]?')

aValRe=re.compile('\d+')

onlySymbol=re.compile('[A-Z][a-z]?')
#Returns isotope's "A" and symbol in a tuple if it has the form isoRe
#returns isotopes number if only number is specified. It returns the
#element's symbol if that was the only thing provided. Always in a
#tuple. It returns None,None in case none of the above matches.
def getIso(s):
    if isinstance(s,int):
        return s,None
    elif s=="a" or s=="alpha" or s=="Alpha":
        return 4,"He"
    elif s=="n" or s=="1n":
        return 1,"n"
    elif s=="p":#Isotopes of hydrogen
        return 1,"H"
    elif s=="D" or s=="d":
        return 2,"H"
    elif s=="T" or s=="t":
        return 3,"H"
    elif s=="None" or s=="0None":
        return 0,"None"

    m=isoRe.match(s)
    if m:
        isoVal=m.group()
        aValMatch=aValRe.match(isoVal)
        aVal=aValMatch.group()
        elementSymbol=s[aValMatch.end():]
        return int(aVal),elementSymbol
    elif aValRe.match(s):
        if s.isdigit():
            return int(s),None
        return None,None
    elif onlySymbol.match(s):
        #Maybe case not necessary
        return None,s
    return None,None

def myString2List(s):
    if len(s)<=2:
        return []
    c=s[2:-2].split("', '")
    return c
