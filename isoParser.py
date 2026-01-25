#   Copyright (C) 2015-2026 Francisco Favela

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
validSymbols=['n','H','He','Li','Be','B','C','N','O','F','Ne',
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

#Simply to recognize the element isotope
isoRe=re.compile(r'\d+[A-Z][a-z]?')

aValRe=re.compile(r'\d+')

onlySymbol=re.compile(r'[A-Z][a-z]?')
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
        if elementSymbol not in validSymbols:
            return None,None
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
