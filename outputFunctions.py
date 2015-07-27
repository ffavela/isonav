from isonavBase import *

def pSReaction(iso1,iso2,isoEject,isoRes,ELab=2.9,ang=30):
    react=sReaction(iso1,iso2,isoEject,isoRes,ELab,ang)
    if not react:
        print "Reaction is invalid"
        return 0
    fR=react[0][1:]
    sR=react[1][1:]
    stringFormat="%.3f\t"*(len(fR)-1)+"%.3f"
    print isoEject,"+",isoRes
    print stringFormat % tuple(fR)
    print ""
    print isoRes,"+",isoEject
    print stringFormat % tuple(sR)
    print ""

def pXReaction(xReact):
    for e in xReact:
        print e[0][0],'+',e[0][1]
        stringFormat="%d\t"+"%.3f\t\t"+"%.3f\t"*2+"%.3f"
        for ee in e[1]:
            level=ee[0][0]
            lE=ee[0][1]
            rest=ee[1][1:]
            tup=(level,lE, rest[0],rest[1],rest[2])
            print stringFormat % tuple(tup)
        print ""
            
def pXXTremeTest(XXList):
    stringFormat="%d\t%0.3f\t\t"+"%.3f\t"*2+"%.3f"
    for e in XXList:
        isoE=e[0][0]
        isoR=e[0][1]
        EThres=e[0][2]
        QVal=e[0][3]
        tup=(isoE,isoR,EThres,QVal)
        reaction=e[1]
        for ee in reaction:
            if len(ee[1])>0:
                isoE=ee[0][0]
                isoR=ee[0][1]
                print isoE+'\t'+isoR
                for states in ee[1]:
                    level=states[0][0]
                    levE=states[0][1]
                    ejectE=states[1][1]
                    resAng=states[1][2]
                    resE=states[1][3]
                    tup=(level,levE,ejectE,resAng,resE)
                    print stringFormat % tup
                print ""

    
def pXTremeTest(iso1,iso2,Elab,angle):
    val=xTremeTest(iso1,iso2,Elab,angle)
    stringFormat="%.3f\t%.3f\t%.3f"
    for v in val:
        isoE=v[0][0]
        isoR=v[0][1]
        ejectE=v[1][0][1]
        resAng=v[1][0][2]
        resE=v[1][0][3]
        tup=(ejectE,resAng,resE)
        print isoE,"\t",isoR
        print stringFormat % tuple(tup)
        ejectE=v[1][1][1]
        resAng=v[1][1][2]
        resE=v[1][1][3]
        tup=(ejectE,resAng,resE)
        print stringFormat % tuple(tup)
        print ""


#Printing it nicely for a spreadsheet.
def tNReaction(iso1,iso2):
    rList=nReaction(iso1,iso2)
    for e in rList:
        if e[2]=='None':
            print e[0]+'\t'+e[1]+'\t',e[2],'\t',"{0:0.2f}".format(float(e[3]))
        else:
            print e[0]+'\t'+e[1]+'\t',"{0:0.2f}".format(float(e[2])),'\t',"{0:0.2f}".format(float(e[3]))

##Printing latex fiendly nReaction
def latexNReaction(iso1,iso2):
    reacList=nReaction(iso1,iso2)
    a1,key1=getIso(iso1)
    a2,key2=getIso(iso2)
    sa1=str(a1)
    sa2=str(a2)
    print """\\begin{eqnarray*} """
    
    print ' ^{'+sa1+'}\!'+key1+'+'+' ^{'+sa2+'}\!'+key2+'\longrightarrow&',
    maxVal=len(reacList)
    for r in reacList:
        if r==reacList[3]:
            fStr='MeV'
        else:
            fStr='MeV\\\\'

        r[3]=str(round(r[3],2))
        aEject,kEject=getIso(r[0])
        aRes,kRes=getIso(r[1])
        aEject,aRes=str(aEject),str(aRes)
        if kEject==None:
            print ' ^{'+aRes+'}\!'+kRes+'&Q='+r[3]+fStr
            continue

        print '& ^{'+aEject+'}\!'+kEject+'+'+' ^{'+aRes+'}\!'+kRes+'&Q='+r[3]+fStr
    print '\end{eqnarray*}'


def pIsotopes(iso,flag=True):
    val=getIsotopes(iso)
    eCoef=1
    if flag:
        eCoef=938.41
    if val == False:
        print "Symbol not in database"
        return False
    stringFormat="%s\t%0.3f"
    for i in val:
        i[1]*=eCoef
        print stringFormat %tuple(i)

def pDecay(iso):
    dec=QDecay(iso)
    for d in dec:
        print "%s\t%s\t\t%.3f\t%.3f\t%.3f" % tuple(d)
