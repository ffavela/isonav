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

from isonavBase import *


def pSReaction(iso1, iso2, isoEject, isoRes, ELab=2.9, ang=30,
               exList=[0, 0, 0, 0]):
    react1, react2 = sReaction(iso1, iso2, isoEject, isoRes,
                               ELab, ang, exList)
    if not react1:
        print("Reaction is invalid")
        return 0

    fR1 = react1[0][1:]
    sR1 = react2[0][1:]  # switching the ejectile and the residue
    stringFormat = "%.3f\t" * (3-1) + "%.3f"
    if fR1[1] is not False:
        print(isoEject + '\t' + isoRes)
        print(stringFormat % tuple(fR1))
        print("")
    # The second solution
    if react2 != []:
        fR2 = react1[1][1:]
        sR2 = react2[1][1:]
        if fR2 != []:
            if fR1[1] is False:
                print(isoEject + '\t' + isoRes)

            print(stringFormat % tuple(fR2))
            print("")

    if sR1 != [False, False, False]:
        print(isoRes + '\t' + isoEject)
        print(stringFormat % tuple(sR1))
        print("")
    if sR2 != []:
        if sR1 == []:
            print(isoRes + '\t' + isoEject)
            print("\n")
        print(stringFormat % tuple(sR2))
        print("")


def pXReaction(isop, isot, isoE, isoR, Elab,
               angle, xF1, xF2):
    xReactL = xReaction(isop, isot, isoE, isoR,
                        Elab, angle, xF1, xF2)
    xReactF = []
    xReactSDict = {}
    for lr in xReactL:
        exitReact = lr[0]
        exitRString = exitReact[0] + '\t' + exitReact[1]
        if exitRString not in xReactSDict:
            xReactSDict[exitRString] = []
        for info in lr[1:]:
            firstSolEs = [[val[0], val[1][0]] for val in info]
            secSolEs = [[val[0], val[1][1]] for val in info]
            xReactSDict[exitRString].append(secSolEs)
        xReactF.append([exitReact, firstSolEs])

    stringFormat = "%d\t" + "%.3f\t\t" + "%.3f\t" * 2 + "%.3f"

    for e in xReactF:
        if e[1] == []:
            continue
        stringValue = e[0][0] + '\t' + e[0][1]
        print(stringValue)
        for ee in e[1]:
            level = ee[0][0]
            lE = ee[0][1]
            rest = ee[1][1:]
            tup = (level, lE, rest[0], rest[1], rest[2])
            print(stringFormat % tuple(tup))
        print("")
        if stringValue in xReactSDict:
            for E in xReactSDict[stringValue]:
                secSolBool = False
                for ee in E:
                    if ee[1] == []:
                        continue
                    secSolBool = True
                    level = ee[0][0]
                    lE = ee[0][1]
                    rest = ee[1][1:]
                    tup = (level, lE, rest[0], rest[1], rest[2])
                    print(stringFormat % tuple(tup))
                if secSolBool:
                    print("")


def pXXTremeTest(iso1, iso2, Elab, angle):
    XXList = xXTremeTest(iso1, iso2, Elab, angle)
    stringFormat = "%d\t%0.3f\t\t" + "%.3f\t" * 2 + "%.3f"
    for e in XXList:
        isoE = e[0][0]
        isoR = e[0][1]
        EThres = e[0][2]
        QVal = e[0][3]
        tup = (isoE, isoR, EThres, QVal)
        reaction = e[1]
        for ee in reaction:
            if len(ee[1]) > 0:
                isoE = ee[0][0]
                isoR = ee[0][1]
                print(isoE + '\t' + isoR)
                for states in ee[1]:
                    level = states[0][0]
                    levE = states[0][1]
                    ejectE = states[1][1]
                    resAng = states[1][2]
                    resE = states[1][3]
                    tup = (level, levE, ejectE, resAng, resE)
                    print(stringFormat % tup)
                print("")
                secStateBool = False
                for secStates in ee[2]:
                    if secStates[1] != []:
                        secStateBool = True
                        level = secStates[0][0]
                        levE = secStates[0][1]
                        ejectE = secStates[1][1]
                        resAng = secStates[1][2]
                        resE = secStates[1][3]
                        tup = (level, levE, ejectE, resAng,
                               resE)
                        print(stringFormat % tup)
                if secStateBool:
                    print("")


def pXTremeTest(iso1, iso2, Elab, angle):
    rawVal = xTremeTest(iso1, iso2, Elab, angle)
    dictSecSol = {}
    for rV in rawVal:
        stringEntry = rV[0][0]+"\t"+rV[0][1]
        if stringEntry not in dictSecSol:
            dictSecSol[stringEntry] = rV[2]

    stringFormat = "%.3f\t%.3f\t%.3f"
    stringFormat2 = "%s\t%s"
    for v in rawVal:
        isoE = v[0][0]
        isoR = v[0][1]
        ejectE = v[1][0][1]
        resAng = v[1][0][2]
        resE = v[1][0][3]
        tup = (ejectE, resAng, resE)
        isosString1 = isoE + '\t' + isoR
        if tup != (False, False, False):
            print(isosString1)
            print(stringFormat % tuple(tup))
            print("")
            if dictSecSol[isosString1][0] != []:
                vv = dictSecSol[isosString1][0]
                ejectE = vv[1]
                resAng = vv[2]
                resE = vv[3]
                tup = (ejectE, resAng, resE)
                print(stringFormat % tuple(tup))
                print("")
        ejectE = v[1][1][1]
        resAng = v[1][1][2]
        resE = v[1][1][3]
        tup = (ejectE, resAng, resE)
        isosString2 = isoR+'\t'+isoE
        if tup != (False, False, False):
            print(isosString2)
            print(stringFormat % tuple(tup))
            print("")
            if dictSecSol[isosString1][1] != []:
                vv = dictSecSol[isosString1][1]
                ejectE = vv[1]
                resAng = vv[2]
                resE = vv[3]
                tup = (ejectE, resAng, resE)
                print(stringFormat % tuple(tup))
                print("")


# Printing it nicely for a spreadsheet.
def tNReaction(iso1, iso2):
    rList = nReaction(iso1, iso2)
    for e in rList:
        if e[2] == 'None':
            string1 = str(e[0])+'\t'+str(e[1])+'\t'+str(e[2])+'\t'
            print(string1+"{0:0.2f}".format(float(e[3]))+"\tNone")
        else:
            string2 = e[0]+'\t'+e[1]+'\t'+"{0:0.2f}".format(float(e[2]))
            string3 = '\t'+"{0:0.2f}".format(float(e[3]))
            coulE = coulombE(e[0], e[1])
            string4 = '\t'+"{0:0.2f}".format(float(coulE))
            print(string2+string3+string4)


# Printing latex friendly nReaction
# Add the coulomb E functionality also here
def latexNReaction(iso1, iso2):
    reacList = nReaction(iso1, iso2)
    a1, key1 = getIso(iso1)
    a2, key2 = getIso(iso2)
    sa1 = str(a1)
    sa2 = str(a2)
    print("""\\begin{eqnarray*} """)

    print('{}^{' + sa1 + '}\\mathrm{' + key1 + '}+' + '{}^{' + sa2 +
          '}\\mathrm{' + key2 + '}\\longrightarrow ')
    # maxVal = len(reacList)
    for r in reacList:
        if r == reacList[3]:
            fStr = '\\:\\rm{MeV}'
        else:
            fStr = '\\:\\rm{MeV}\\\\'

        r[3] = str(round(r[3], 2))
        aEject, kEject = getIso(r[0])
        aRes, kRes = getIso(r[1])
        aEject, aRes = str(aEject), str(aRes)
        if kEject is None:
            print('{}^{' + aRes + '}' + kRes + '&\\:Q=' + r[3] + fStr)
            continue

        print('& {}^{' + aEject + '}\\mathrm{' + kEject + '}+' +
              ' {}^{' + aRes + '}\\mathrm{' + kRes + '}&\\:Q=' + r[3] + fStr)
    print('\\end{eqnarray*}')


def pIsotopes(iso, mFlag=False, flag=True):
    val = getIsotopes(iso)
    eCoef = 1
    if mFlag:
        if flag:
            eCoef = 931.4941
        if val is False:
            print("Symbol not in database")
            return False
        for i in val:
            i[1] *= eCoef
            print(str(i[0])+"\t"+str(i[1]))
        return 0
    for i in val:
        print(i[0])
    return 0


def pDecay(iso, emit="", num=1, Ex=0.0):
    if emit == "":
        dec = QDecay(iso, Ex)
        for d in dec:
            print("%s\t%s\t\t%.3f\t%.3f\t%.3f" % tuple(d))
    else:
        dec = emitDecay2(iso, emit, num)
        if dec is None or dec is False:
            return 1
        print("%s\t%s\t\t%.3f" % tuple(dec))


def pDecay2(iso, emit, num=1):
    dec = emitDecay2(iso, emit, num)
    if dec is None or dec is False:
        return 1
    print("%s\t%s\t\t%.3f" % tuple(dec))


def pFussion(iso1, iso2, Elab):
    l = fussionCase(iso1, iso2, Elab)
    stringFormat = "%s\t%d\t%.3f\t%.3f"
    print(stringFormat % tuple(l))


simpleDict = {"n": "1n", "p": "1H", "d": "2H", "t": "3H", "a": "4He"}


def getRealIso(myIso):
    if myIso in simpleDict:
        myIso = simpleDict[myIso]
    return myIso


def pLevels(iso, limit="NaN"):
    iso = getRealIso(iso)
    levs = getAllLevels(iso)
    if limit == "NaN":
        for l in levs:
            print(str(l[0])+'\t'+str(l[1]))
        return 0
    counter = 0
    for l in levs:
        counter += 1
        if counter > limit:
            break
        print(str(l[0])+'\t'+str(l[1]))
    return 0


def pName(s):
    eName = getNameFromSymbol(s)
    if eName is not False:
        print(eName)
