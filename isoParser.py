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
        return int(s),None
    elif onlySymbol.match(s):
        #Maybe case not necessary
        return None,s
    return None,None

def myString2List(s):
    if len(s)<=2:
        return []
    c=s[2:-2].split("', '")
    return c
