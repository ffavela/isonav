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

from isonavBase import *
from outputFunctions import *
from operator import itemgetter

def getOrdMatList(matDict):
    newList=[]
    for e in matDict:
        vl=matDict[e]
        newList.append([e,vl[0],vl[1],vl[2],vl[3]])
    sortList=sorted(newList,key=itemgetter(2))
    return sortList

def makeSureIso(iso):
    A,k=getIso(iso)
    if A == None or k == None:
        return False
    return True

def testVal(stuff,strFlag="E"):
    if stuff==False:
        return False
    try:
        stuff=float(stuff)
    except:
        stuff=None
    val=isinstance(stuff,float) or isinstance(stuff,int)
    if val:
        if strFlag=="E" or strFlag=="T":
            if not 0<=stuff:
                return False
        if strFlag=="angle":
            if not 0<=stuff<=180:
                return False
        return True
    return False

commonVal=["n","p","d","t","a"]

def argHand(args):
    verbose=args["-v"]
    Elab=args['--Elab']
    angle=args['--angle']
    scatE=args["--scatE"]
    iso=args["<iso>"]
    iso1=args["<iso1>"]
    iso2=args["<iso2>"]
    isop=args["<isop>"]
    isot=args["<isot>"]
    isoE=args["<isoEject>"]
    isoR=args["<isoRes>"]
    alpha=args["--alpha"]
    pEmit=args["--pEmission"]
    nEmit=args["--nEmission"]
    Emit=args["--Emission"]
    num=args["--num"]
    name=args["--name"]
    symbol=args["<symbol>"]
    T=args["--T"]
    ion=args["<ion>"]
    material=args["--material"]
    thick=args["--thickness"]
    deltaE=args["--depositedE"]
    bloch=args["--bloch"]
    density=args["--density"]
    lsMat=args["--listMaterials"]
    xF1=args["--xF1"]
    xF2=args["--xF2"]

    if iso:
        vals=[i[0] for i in getIsotopes(iso)]

    if iso in commonVal:
        vals=commonVal

    if args["--symbol"] or args["-s"]:
        if verbose:
            print("#Given a number it returns the periodic table symbol")
        number=args["<number>"]
        try:
            number=int(number)
        except:
            print("Error; <number> has to be an integer")
            return 5

        print(getKey(number))
        return 0

    if args["--protons"] or args["-p"]:
        if verbose:
            print("#Given an isotope or purely the symbol it returns the number of protons")
        print(getPnum(symbol))
        return 0

    if name:
        if verbose:
            print("#Given an element symbol it prints out the name")
        pName(symbol)
        return 0

    if args["--neutrons"] or args["-n"]:

        if not makeSureIso(iso):
            print("Not a valid isotope")
            return 1

        if verbose:
            print("Given an isotope it returns the number of neutrons")

        print(getNnum(iso))
        return 0

    if args["--isotopes"] or args["-i"]:
        if verbose:
            print("Isotopes and masses, in MeV by default")
        flag=True
        mFlag=False
        if args["-m"]:
            mFlag=True
            if args["--amu"]:
                flag=False

        pIsotopes(iso,mFlag,flag)
        return 0

    if args["--mirror"]:
        if verbose:
            print("Given an isotope it returns the mirror isotope")

        print(mirror(iso))
        return 0

    if args["-r"]==True or args["--radius"]==True:
        if verbose:
            print("#Returns the isotope's radius, in fermis, using r=1.2*A**(1.0/3)")
        if not makeSureIso(iso):
            print("Not a valid isotope")
            return 1

        print(nRadius(iso))
        return 0

    if args["-l"]==True or args["--levels"]==True:
        if verbose:
            print("#Returns the energy levels of the isotope, prints at most limit levels")
        if not makeSureIso(iso):
            print("Not a valid isotope")
            return 1

        if iso not in vals:
            print("Error; isotope not in database")
            return 999

        if args["--limit"]:
            limit=int(args["--limit"])
            pLevels(iso,limit)
            return 0

        pLevels(iso)
        return 0

    if Elab != None and iso :
        if verbose==True:
            print("#Returns the deBroglie wavelength by default, in angstrom")

        if not testVal(Elab,"E"):
            print("Error; energy has to be a positive number")
            return 777
        Elab=float(Elab)

        if not makeSureIso(iso):
            print("Not a valid isotope")
            return 1

        if testVal(Elab):
            if args["--redDeBroglie"]:
                print(reducedDeBroglie(iso,Elab))
            else:
                print(deBroglie(iso,Elab))
            return 0
        print("Error; Elab needs a numerical value")
        return 2

    if args["-m"] or args["--mass"]:
        if verbose==True:
            print("#Returns the mass in MeV or in amu if --amu is used")

        if not makeSureIso(iso):
            print("Not a valid isotope")
            return 1

        if args["--liquidDrop"]:
            if args["--amu"]==True:
                print(getLDMass(args['<iso>']))
                return 0
            else:
                print(getLDEMass(args['<iso>']))
                return 0

        if iso not in vals:
            print("Error; isotope not in database")
            return 999
        if args["--amu"]==True:
            print(getMass(args['<iso>']))
        else:
            print(getEMass(args['<iso>']))
        return 0

    if  args["--compton"]:
        if verbose==True:
            print("#The compton wavelength in fm")
        if not makeSureIso(iso):
            print("Not a valid isotope")
            return 1

        if iso not in vals:
            print("Error; isotope not in database")
            return 999
        print(comptonW(args['<iso>']))
        return 0
            
    if args["--BE"] or args["--BEperNucleon"]:
        if verbose:
            print("#Given an isotope it provides its binding energy")
        if not makeSureIso(iso):
            print("Not a valid isotope")
            return 1

        if args["--BE"]:
            if args["--liquidDrop"]:
                print(getLDBE(iso))
            else:
                if iso not in vals:
                    print("Error; isotope not in database")
                    return 999
                print(getBE(iso))
        elif args["--BEperNucleon"]:
            if args["--liquidDrop"]:
                print(getLDBEperNucleon(iso))
            else:
                if iso not in vals:
                    print("Error; isotope not in database")
                    return 999
                print(getBEperNucleon(iso))
        return 0

    if args["--coulomb"] or args["--reactions"]:
        if verbose:
            print("#Given two isotopes it returns the coulomb energy barrier")
            print("#Or the possible reactions.")
        if args["--reactions"]:
            if verbose==True:
                print("#Eject\tResidue\tThres\tQValue")

            if not checkIsoExistence(iso1,iso2):
                return 665

            if args["--latex"]==True:
                latexNReaction(iso1,iso2)
            else:
                tNReaction(iso1,iso2)
            return 0

        print(coulombE(iso1,iso2))
        return 0

    if args["--gamowEnergy"] or args["--gamowPeak"]:
        if verbose:
            print("#Gamow functions, in MeV")

        if args["--gamowEnergy"]:
            print(gamowE(iso1,iso2))
            return 0

        if args["--gamowPeak"]:
            if not testVal(T,"T"):
                print("Error; temperature has to be a positive number")
                return 8889

            T=float(T)
            print(gamowPeak(iso1,iso2,T))
            return 0

    if args["--decay"] and iso:
        if verbose:
            print("#Decay, splitting in two nucleons (no beta)")
            print("#res\tdaught\t\teRes\teDaugh\tQ")
        if not makeSureIso(iso):
            print("Not a valid isotope")
            return 1

        pDecay(iso)
        return 0

    if alpha or nEmit or pEmit:
        if num:
            num=int(num)
        else:
            num=1

        if verbose:
            print("#Decay for the cases of alpha and proton or neutron emission ")
            print("#By default num=1")
        if alpha:
            pDecay(iso,"4He",num)
            return 0

        if nEmit:
            pDecay(iso,"1n",num)
            return 0

        if pEmit:
            pDecay(iso,"1H",num)
            return 0

    if Emit:
        if verbose:
            print("#eject\tdaughter\tQval[MeV]")
        #Adding the common abbreviations
        if Emit=="p":
            Emit="1H"
        if Emit=="n":
            Emit="1n"
        if Emit=="d":
            Emit="2H"
        if Emit=="t":
            Emit="3H"
        if Emit=="a":
            Emit="4He"
        num=int(num)
        pDecay2(iso,Emit,num)
        return 0

    if args["--fussion"]:
        if not checkIsoExistence(iso1,iso2):
            return 665

        if Elab:
            if not testVal(Elab,"E"):
                print("Error; energy has to be a positive number")
                return 777
            Elab=float(Elab)
        else:
            Elab=0
        if verbose:
            print("#Prints the fused element, if isotope exists.")
            print("#Max populated level, and energy, and remaining KE in lab")
        pFussion(iso1,iso2,Elab)

    if iso1 and Elab:
        if not testVal(Elab,"E"):
            print("Error; energy has to be a positive number")
            return 777

        Elab=float(Elab)

        if not checkIsoExistence(iso1,iso2):
            return 665

        if angle!=None:
            if verbose==True:
                print("#Energy at given angle for the ejectile and the residue")
            if not testVal(angle,"angle"):
                print("Error; 0<=angle<=180 has to be True ")
                return 888

            angle=float(angle)
            if angle==0:
                print("Error, give a positive angle")
                return 222

            if args["--xTreme"]==True:
                if verbose==True:
                    print("#Prints out angles and energies of the reactions")
                    print("#lev\tlevE\t\tEe\tang2L\tEr")
                pXXTremeTest(iso1,iso2,Elab,angle)
                return 0
                    
            # print xTremeTest(iso1,iso2,Elab,angle)
            pXTremeTest(iso1,iso2,Elab,angle)
            return 0

    if scatE:
        if verbose==True:
            print("#Gives the beam energy [MeV]")

        if not checkIsoExistence(iso1,iso2):
            return 665

        if not testVal(scatE):
            print("Error; scattered energy has to be a number")
            return 10 #Making this up as I go
        scatE=float(scatE)

        if not testVal(angle,"angle"):
            print("Error; 0<=angle<=180 has to be True")
            return 888
        angle=float(angle)

        print(findOE(scatE,angle,iso1,iso2))
        return 0

    if args["--QVal"] or args["-q"]:
        if args["--amu"]:
            print(getIsoQValAMU(isop,isot,isoE,isoR))
        else:
            print(getIsoQVal(isop,isot,isoE,isoR))
        return 0


    if args["--maxAng"]:
        if verbose:
            print("#Given a beam energy it outputs the maximum angle the exit particles have")
        if not testVal(Elab):
            print("Error; energy has to be a positive number")
            return 777
        Elab=float(Elab)
        if not checkReaction(isop,isot,isoE,isoR):
            return 666
        a=getMaxAngles(isop,isot,isoE,isoR,Elab)
        print(a[0], a[1])
        return 0
    #if angle means angle!=0 but there might be a problem here.
    if angle and args["<isoRes>"]:
        if verbose:
            print("#Prints the energies that'll reach the detector")
            print("If the --xF format is used then it takes the energy levels from")
            print("a single column txt file")

        if not testVal(Elab,"E"):
            print("Error; energy has to be a positive number")
            return 777

        if not testVal(angle,"angle"):
            print("Error; 0<=angle<=180 has to be True")
            return 888

        Elab=float(Elab)
        angle=float(angle)

        if not checkReaction(isop,isot,isoE,isoR):
            return 666

        if args["-x"] or args["--xTreme"]:
            pXReaction(isop,isot,isoE,isoR,Elab,angle,xF1,xF2)
            return 0
        # sReact=sReaction(isop,isot,isoE,isoR,Elab,angle)
        pSReaction(isop,isot,isoE,isoR,Elab,angle)
        return 0

    if args["--material"] and Elab != None:
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
        if not testVal(Elab,"E"):
            print("Error; ion energy has to be a positive number")
            return 12345
        E=float(Elab)
        if not testVal(thick,"E"):
            print ("Error; thickness has to be a positive number")
            return 12346
        thick=float(thick)
        #Note checkMaterial loads the proper I (and rho) to a global
        #dictionary so no need to put it as argument in other functions
        #;-)
        if density != None:
            density=float(density)
            if not testVal(density,"E"):
                print("Error; density has to be a positive number (g/cm^3)")
                return 12347

        if not checkMaterial(material,bloch,density):
            print("Error; material not yet implemented :(")
            return 12347
        if deltaE != False:
            val2Print=E-integrateELoss(ion,E,material,thick)
        else:
            val2Print=integrateELoss(ion,E,material,thick)
        print("%.3f" % val2Print)
        return 0

    if lsMat:
        if verbose:
            print("#Prints a list of the implemented materials")
            print("#the Z, A_r,density (in gm/cm^3) and I (mean excitation")
            print("#potential in eV)\n")
            print("#Mat\tZ\tA_r\trho\t\tI")
        materialDict=getChemDictFromFile()
        if material != None:
            if not checkMaterial(material):
                print("Error; material not yet implemented :(")
                return 4321

            stringStuff=[str(val) for val in materialDict[material]]
            #TODO: improve this printout
            finalString=material
            for s in stringStuff[0:-1]:
                finalString+='\t'+s
            finalString+='\t\t'+stringStuff[-1]
            print(finalString)
            return 0
        sortMatList=getOrdMatList(materialDict)
        for e in sortMatList:
            stringStuff=[str(val) for val in e]
            finalString=e[0]
            for s in stringStuff[1:-1]:
                finalString+='\t'+s
            finalString+='\t\t'+stringStuff[-1]
            print(finalString)
        return 0
    
    if args["-d"] or args["--donate"]:
        if verbose:
            print("#Make a donation through bitcoin ;)")
            print("#The address belongs to Francisco Favela")

        flag=False
        if args["--QR"]:
            flag=True
        pDonation(flag)
        return 0
