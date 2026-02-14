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

import lib.isonavBase as iB  # type: ignore
import lib.outputFunctions as oF  # type: ignore
import lib.isoParser as iP  # type: ignore
import lib.loadingStuff as lS  # type: ignore
from operator import itemgetter


def getOrdMatList(matDict):
    newList = []
    for e in matDict:
        vl = matDict[e]
        newList.append([e, vl[0], vl[1], vl[2], vl[3]])
    sortList = sorted(newList, key=itemgetter(2))
    return sortList


def makeSureIso(iso):
    A, k = iP.getIso(iso)
    if A is None or k is None:
        return False
    return True


def testVal(stuff, strFlag="E"):
    if stuff is False:
        return False
    try:
        stuff = float(stuff)
    except:
        stuff = None
    val = isinstance(stuff, float) or isinstance(stuff, int)
    if val:
        if strFlag == "E" or strFlag == "T" or strFlag == "L":
            if not 0 <= stuff:
                return False
        if strFlag == "angle":
            if not 0 <= stuff <= 180:
                return False
        return True
    return False


commonVal = ["n", "p", "d", "t", "a"]


def argHand(args):
    verbose = args["-v"]
    Elab = args['--Elab']
    angle = args['--angle']
    scatE = args["--scatE"]
    iso = args["<iso>"]
    iso1 = args["<iso1>"]
    iso2 = args["<iso2>"]
    isop = args["<isop>"]
    isot = args["<isot>"]
    isoE = args["<isoEject>"]
    isoR = args["<isoRes>"]
    alpha = args["--alpha"]
    pEmit = args["--pEmission"]
    nEmit = args["--nEmission"]
    Emit = args["--Emission"]
    num = args["--num"]
    name = args["--name"]
    symbol = args["<symbol>"]
    T = args["--T"]
    ion = args["<ion>"]
    material = args["--material"]
    thick = args["--thickness"]
    ionRange = args["--range"]
    deltaE = args["--depositedE"]
    bloch = args["--bloch"]
    density = args["--density"]
    lsMat = args["--listMaterials"]
    xEje = args["--xEje"]
    xRes = args["--xRes"]
    xF1 = args["--xF1"]
    xF2 = args["--xF2"]
    L = args["--L4TOF"]
    redDeBroglie = args["--redDeBroglie"]
    deBroglieFlag = args["--deBroglie"] or redDeBroglie
    Ex = args["--Ex"]

    if iso:
        vals = [i[0] for i in iB.getIsotopes(iso)]

    if iso in commonVal:
        vals = commonVal

    if args["--symbol"] or args["-s"]:
        if verbose:
            print("#Given a number it returns the periodic table symbol")
        number = args["<number>"]
        try:
            number = int(number)
        except:
            print("Error; <number> has to be an integer")
            return 5

        print(iB.getKey(number))
        return 0

    if args["--protons"] or args["-p"]:
        if verbose:
            print("#Given an isotope or purely the symbol it returns the number of protons")
        print(iB.getPnum(symbol))
        return 0

    if name:
        if verbose:
            print("#Given an element symbol it prints out the name")
        oF.pName(symbol)
        return 0

    if args["--neutrons"] or args["-n"]:

        if not makeSureIso(iso):
            print("Not a valid isotope")
            return 1

        if verbose:
            print("Given an isotope it returns the number of neutrons")

        print(iB.getNnum(iso))
        return 0

    if args["--isotopes"] or args["-i"]:
        if verbose:
            print("Isotopes and masses, in MeV by default")
        flag = True
        mFlag = False
        if args["-m"]:
            mFlag = True
            if args["--amu"]:
                flag = False

        oF.pIsotopes(iso, mFlag, flag)
        return 0

    if args["--mirror"]:
        if verbose:
            print("Given an isotope it returns the mirror isotope")

        print(iB.mirror(iso))
        return 0

    if args["-r"] is True or args["--radius"] is True:
        if verbose:
            print("#Returns the isotope's radius, in fermis, using r=1.2*A**(1.0/3)")
        if not makeSureIso(iso):
            print("Not a valid isotope")
            return 1

        print(iB.nRadius(iso))
        return 0

    if args["-l"] is True or args["--levels"] is True:
        if verbose:
            print("#Returns the energy levels of the isotope, prints at most limit levels")
        if not makeSureIso(iso):
            print("Not a valid isotope")
            return 1

        if iso not in vals:
            print("Error; isotope not in database")
            return 999

        if args["--limit"]:
            limit = int(args["--limit"])
            oF.pLevels(iso, limit)
            return 0

        oF.pLevels(iso)
        return 0

    if Elab is not None and iso and deBroglieFlag:
        if verbose is True:
            print("#Returns the deBroglie wavelength by default, in angstrom")

        if not testVal(Elab, "E"):
            print("Error; energy has to be a positive number")
            return 777
        Elab = float(Elab)

        if not makeSureIso(iso):
            print("Not a valid isotope")
            return 1

        if testVal(Elab):
            if redDeBroglie:
                print(iB.reducedDeBroglie(iso, Elab))
            else:
                print(iB.deBroglie(iso, Elab))
            return 0
        print("Error; Elab needs a numerical value")
        return 2

    if L is not None and Elab is not None and iso:
        if verbose is True:
            print("Given an isotope, an energy in MeV & a length in cm")
            print("it returns the time of flight in ns.")
        if not testVal(L, "L"):
            print("Error; Length has to be a positive number")
            return 1029
        L = float(L)/100  # because input is in cm

        if not testVal(Elab, "E"):
            print("Error; energy has to be a positive number")
            return 1028
        Elab = float(Elab)

        tof = iB.getTOF(iso, Elab, L)
        tof *= 10**9  # because output is in ns
        print(tof)
        return 0

    if args["-m"] or args["--mass"]:
        if verbose is True:
            print("#Returns the mass in MeV or in amu if --amu is used")

        if not makeSureIso(iso):
            print("Not a valid isotope")
            return 1

        if args["--liquidDrop"]:
            if args["--amu"] is True:
                print(iB.getLDMass(args['<iso>']))
                return 0
            else:
                print(iB.getLDEMass(args['<iso>']))
                return 0

        if iso not in vals:
            print("Error; isotope not in database")
            return 999
        if args["--amu"] is True:
            print(iB.getMass(args['<iso>']))
        else:
            print(iB.getEMass(args['<iso>']))
        return 0

    if args["--compton"]:
        if verbose is True:
            print("#The compton wavelength in fm")
        if not makeSureIso(iso):
            print("Not a valid isotope")
            return 1

        if iso not in vals:
            print("Error; isotope not in database")
            return 999
        print(iB.comptonW(args['<iso>']))
        return 0

    if args["--BE"] or args["--BEperNucleon"]:
        if verbose:
            print("#Given an isotope it provides its binding energy")
        if not makeSureIso(iso):
            print("Not a valid isotope")
            return 1

        if args["--BE"]:
            if args["--liquidDrop"]:
                print(iB.getLDBE(iso))
            else:
                if iso not in vals:
                    print("Error; isotope not in database")
                    return 999
                print(iB.getBE(iso))
        elif args["--BEperNucleon"]:
            if args["--liquidDrop"]:
                print(iB.getLDBEperNucleon(iso))
            else:
                if iso not in vals:
                    print("Error; isotope not in database")
                    return 999
                print(iB.getBEperNucleon(iso))
        return 0

    if args["--coulomb"] or args["--reactions"]:
        if verbose:
            print("#Given two isotopes it returns the coulomb energy barrier")
            print("#Or the possible reactions.")
        if args["--reactions"]:
            if verbose is True:
                print("#Eject\tResidue\tThres\tQValue\tcoulombE")

            if not iB.checkIsoExistence(iso1, iso2):
                return 665

            if args["--latex"] is True:
                oF.latexNReaction(iso1, iso2)
            else:
                oF.tNReaction(iso1, iso2)
            return 0

        print(iB.coulombE(iso1, iso2))
        return 0

    if args["--gamowEnergy"] or args["--gamowPeak"]:
        if verbose:
            print("#Gamow functions, in MeV")

        if args["--gamowEnergy"]:
            print(iB.gamowE(iso1, iso2))
            return 0

        if args["--gamowPeak"]:
            if not testVal(T, "T"):
                print("Error; temperature has to be a positive number")
                return 8889

            T = float(T)
            print(iB.gamowPeak(iso1, iso2, T))
            return 0

    if args["--decay"] and iso:
        if verbose:
            print("#Decay, splitting in two nucleons (no beta)")
            print("#res\tdaught\t\teRes\teDaugh\tQ")
        if not makeSureIso(iso):
            print("Not a valid isotope")
            return 1
        if Ex:
            if not testVal(Ex, "E"):
                print("Error; Ex has to be a positive number")
                return 1119
            Ex = float(Ex)
        if Ex is None:
            Ex = 0.0
        oF.pDecay(iso, Ex=Ex)
        return 0

    if alpha or nEmit or pEmit:
        if num:
            num = int(num)
        else:
            num = 1

        if verbose:
            print("#Decay for the cases of alpha and proton or neutron emission")
            print("#By default num=1")
        if alpha:
            oF.pDecay(iso, "4He", num)
            return 0

        if nEmit:
            oF.pDecay(iso, "1n", num)
            return 0

        if pEmit:
            oF.pDecay(iso, "1H", num)
            return 0

    if Emit:
        if verbose:
            print("#eject\tdaughter\tQval[MeV]")
        # Adding the common abbreviations
        if Emit == "p":
            Emit = "1H"
        if Emit == "n":
            Emit = "1n"
        if Emit == "d":
            Emit = "2H"
        if Emit == "t":
            Emit = "3H"
        if Emit == "a":
            Emit = "4He"
        num = int(num)
        oF.pDecay2(iso, Emit, num)
        return 0

    if args["--fussion"]:
        if not iB.checkIsoExistence(iso1, iso2):
            return 665

        if Elab:
            if not testVal(Elab, "E"):
                print("Error; energy has to be a positive number")
                return 777
            Elab = float(Elab)
        else:
            Elab = 0
        if verbose:
            print("#Prints the fused element, if isotope exists.")
            print("#Max populated level, and energy, and remaining KE in lab")
        iso1, iso2 = oF.getRealIso(iso1), oF.getRealIso(iso2)
        oF.pFussion(iso1, iso2, Elab)

    if iso1 and Elab:
        if not testVal(Elab, "E"):
            print("Error; energy has to be a positive number")
            return 777

        Elab = float(Elab)

        if not iB.checkIsoExistence(iso1, iso2):
            return 665

        iso1, iso2 = oF.getRealIso(iso1), oF.getRealIso(iso2)
        if angle is not None:
            if verbose is True:
                print("#Energy at given angle for the ejectile and the residue")
            if not testVal(angle, "angle"):
                print("Error; 0<=angle<=180 has to be True ")
                return 888

            angle = float(angle)
            if angle == 0:
                print("Error, give a positive angle")
                return 222

            if args["--xTreme"] is True or args["-x"] is True:
                if verbose is True:
                    print("#Prints out angles and energies of the reactions")
                    print("#lev\tlevE\t\tEe\tang2L\tEr")
                oF.pXXTremeTest(iso1, iso2, Elab, angle)
                return 0

            # print xTremeTest(iso1,iso2,Elab,angle)
            oF.pXTremeTest(iso1, iso2, Elab, angle)
            return 0

    if scatE:
        if verbose is True:
            print("#Gives the beam energy [MeV]")

        if not iB.checkIsoExistence(iso1, iso2):
            return 665

        iso1, iso2 = oF.getRealIso(iso1), oF.getRealIso(iso2)
        if not testVal(scatE):
            print("Error; scattered energy has to be a number")
            return 10  # Making this up as I go
        scatE = float(scatE)

        if not testVal(angle, "angle"):
            print("Error; 0<=angle<=180 has to be True")
            return 888
        angle = float(angle)

        print(iB.findOE(scatE, angle, iso1, iso2))
        return 0

    if args["--QVal"] or args["-q"]:
        if args["--amu"]:
            print(iB.getIsoQValAMU(isop, isot, isoE, isoR))
        else:
            print(iB.getIsoQVal(isop, isot, isoE, isoR))
        return 0

    if args["--maxAng"]:
        if verbose:
            print("#Given a beam energy it outputs the maximum angle the exit particles have")
        if not testVal(Elab):
            print("Error; energy has to be a positive number")
            return 777
        Elab = float(Elab)
        if not iB.checkReaction(isop, isot, isoE, isoR):
            return 666
        a = iB.getMaxAngles(isop, isot, isoE, isoR, Elab)
        print(a[0], a[1])
        return 0
    # if angle means angle != 0 but there might be a problem here.
    if angle and args["<isoRes>"]:
        if verbose:
            print("#Prints the energies that'll reach the detector")
            print("If the --xF format is used then it takes the energy levels from")
            print("a single column txt file")

        if not testVal(Elab, "E"):
            print("Error; energy has to be a positive number")
            return 777

        if not testVal(angle, "angle"):
            print("Error; 0<=angle<=180 has to be True")
            return 888

        Elab = float(Elab)
        angle = float(angle)

        if not iB.checkReaction(isop, isot, isoE, isoR):
            return 666

        isop, isot = oF.getRealIso(isop), oF.getRealIso(isot)
        isoE, isoR = oF.getRealIso(isoE), oF.getRealIso(isoR)
        if args["-x"] or args["--xTreme"]:
            oF.pXReaction(isop, isot, isoE, isoR, Elab,
                          angle, xF1, xF2)
            return 0
        # sReact=sReaction(isop,isot,isoE,isoR,Elab,angle)

        if xEje is not None:
            if not testVal(xEje, "E"):
                print("Error; ejectile excitation energy has to be a positive number")
                return 798
            xEje = float(xEje)
        else:
            xEje = 0.0

        if xRes is not None:
            if not testVal(xRes, "E"):
                print("Error; residual excitation energy has to be a positive number")
                return 799
            xRes = float(xRes)
        else:
            xRes = 0.0

        exList = [0, 0, xEje, xRes]
        oF.pSReaction(isop, isot, isoE, isoR, Elab,
                      angle, exList)
        return 0

    if args["--material"] and Elab is not None:
        if verbose:
            print("Given the ion, it's energy, the material name and the material")
            print("thickness (in microns) it prints the final energy of the ion.")
            print("If the --depositedE flag is used, then the deposited energy in the")
            print("material is given (deltaE). Use the format for --listMaterials to")
            print("see a list of implemented materials. If --bloch flag is used then")
            print("the Bloch mean iotization potential is used even if it's")
            print("reported as '-'. Density values can also be overriden.")
        if not makeSureIso(ion):
            print("Ion has to be a valid isotope")
            return 1
        if not testVal(Elab, "E"):
            print("Error; ion energy has to be a positive number")
            return 12345
        E = float(Elab)
        if not ionRange:
            if not testVal(thick, "E"):
                print("Error; thickness has to be a positive number")
                return 12346
            thick = float(thick)
        # Note checkMaterial loads the proper I (and rho) to a global
        # dictionary so no need to put it as argument in other functions
        # ;-)
        if density is not None:
            density = float(density)
            if not testVal(density, "E"):
                print("Error; density has to be a positive number (g/cm^3)")
                return 12347

        if not iB.checkMaterial(material, bloch, density):
            print("Error; material not yet implemented :(")
            return 12347
        if deltaE is not False:
            eLoss = iB.integrateELoss(ion, E, material, thick)
            if eLoss == -1.0:
                val2Print = E
            else:
                val2Print = E - eLoss
        elif ionRange:
            val2Print = iB.getParticleRange(ion, E, material)
        else:
            val2Print = iB.integrateELoss(ion, E, material, thick)
        print("%.3f" % val2Print)
        return 0

    if lsMat:
        if verbose:
            print("#Prints a list of the implemented materials")
            print("#the Z, A_r,density (in gm/cm^3) and I (mean excitation")
            print("#potential in eV)\n")
            print("#Mat\tZ\tA_r\trho\t\tI")
        materialDict = lS.getChemDictFromFile()
        if material is not None:
            if not iB.checkMaterial(material):
                print("Error; material not yet implemented :(")
                return 4321

            stringStuff = [str(val) for val in materialDict[material]]
            # TODO: improve this printout
            finalString = material
            for s in stringStuff[0:-1]:
                finalString += '\t' + s
            finalString += '\t\t' + stringStuff[-1]
            print(finalString)
            return 0
        sortMatList = getOrdMatList(materialDict)
        for e in sortMatList:
            stringStuff = [str(val) for val in e]
            finalString = e[0]
            for s in stringStuff[1:-1]:
                finalString += '\t' + s
            finalString += '\t\t' + stringStuff[-1]
            print(finalString)
        return 0
