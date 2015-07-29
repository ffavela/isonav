from isonavBase import *
from outputFunctions import *
import sqlite3

def testVal(stuff):
    try:
        stuff=float(stuff)
    except:
        stuff=None
    return isinstance(stuff,float)

def argHand(args):
    if args["--symbol"] or args["-s"]:
        if args["-v"]:
            print "#Given a number it returns the periodic table symbol"
        number=args["<number>"]
        try:
            number=int(number)
        except:
            print "Error; <number> has to be an integer"
            return 5

        print getKey(number)
        return 0

    if args["--protons"] or args["-p"]:
        if args["-v"]:
            print "#Given an isotope or purely the symbol it returns the number of protons"
        symbol=args["<symbol>"]
        print getPnum(symbol)
        return 0
    if args["--neutrons"] or args["-n"]:
        if args["-v"]:
            print "Given an isotope it returns the number of neutrons"
        iso=args["<iso>"]
        print getNnum(iso)
        return 0

    if args["--isotopes"] or args["-i"]:
        if args["-v"]:
            print "Isotopes and masses, in MeV by default"
        flag=True
        mFlag=False
        if args["-m"]:
            mFlag=True
            if args["--amu"]:
                flag=False
        iso=args["<iso>"]
        pIsotopes(iso,mFlag,flag)
        return 0

    if args["--mirror"]:
        if args["-v"]:
            print "Given an isotope it returns the mirror isotope"
        iso=args["<iso>"]
        print mirror(iso)
        return 0

    if args["-r"]==True or args["--radius"]==True:
        if args["-v"]:
            print "#Returns the isotope's radius, in fermis, using r=1.2*A**(1.0/3)"
        iso=args["<iso>"]
        print nRadius(iso)
        return 0

    Elab=args['--Elab']
    if Elab != None and args["<iso>"] :
        Elab=float(Elab)
        iso=args["<iso>"]
        if args["-v"]==True:
            print "#Returns the deBroglie wavelength by default, in angstrom"
        if testVal(Elab):
            if args["--redDeBroglie"]:
                print reducedDeBroglie(iso,Elab)
            else:
                print deBroglie(iso,Elab)
            return 0
        print "Error; Elab needs a numerical value"
        return 2

    if args["-m"] or args["--mass"]:
        if args["-v"]==True:
            print "#Returns the mass in MeV or in amu if --amu is used"
        if args["--liquidDrop"]:
            if args["--amu"]==True:
                print getLDMass(args['<iso>'])
            else:
                print getLDEMass(args['<iso>'])
                return 0
        if args["--amu"]==True:
            print getMass(args['<iso>'])
        else:
            print getEMass(args['<iso>'])
        return 0

    if  args["--compton"]:
        if args["-v"]==True:
            print "#The compton wavelength in fm"
        print comptonW(args['<iso>'])
        return 0
            
    if args["--BE"] or args["--BEperNucleon"]:
        iso=args["<iso>"]
        if args["-v"]:
            print "#Given an isotope it provides its binding energy"
        if args["--BE"]:
            if args["--liquidDrop"]:
                print getLDBE(iso)
            else:
                print getBE(iso)
        elif args["--BEperNucleon"]:
            if args["--liquidDrop"]:
                print getLDBEperNucleon(iso)
            else:
                print getBEperNucleon(iso)
        return 0

    if args["--coulomb"] or args["--reactions"]:
        iso1=args["<iso1>"]
        iso2=args["<iso2>"]
        if args["-v"]:
            print "#Given two isotopes it returns the coulomb energy barrier"
            print "#Or the possible reactions."
        if args["--reactions"]:
            if args["-v"]==True:
                print "#Eject\tResidue\tThres\tQValue"
            if args["--latex"]==True:
                latexNReaction(iso1,iso2)
            else:
                tNReaction(iso1,iso2)
            return 0

        print coulombE(iso1,iso2)
        return 0

    if args["--decay"] and args["<iso>"]:
        iso=args["<iso>"]
        if args["-v"]:
            print "#Decay, splitting in two nucleons (no beta)"
            print "#res\tdaught\t\teRes\teDaugh\tQ"
        pDecay(iso)
        return 0

    if args["--fussion"]:
        iso1=args["<iso1>"]
        iso2=args["<iso2>"]
        
        Elab=args['--Elab']
        if Elab:
            Elab=float(Elab)
        else:
            Elab=0
        if args["-v"]:
            print "#Prints the fused element, if isotope exists."
            print "#Max populated level, and energy, and remaining KE in lab"
        pFussion(iso1,iso2,Elab)

    Elab=args['--Elab']
    if args["<iso1>"] and testVal(Elab):
        Elab=float(Elab)
        angle=args['--angle'] 
        if angle!=None and testVal(angle):
            angle=float(angle)
            if args["-v"]==True:
                print "#Energy at given angle for the ejectile and the residue"
            if not 0<=angle<=180:
                print "Error; 0<=angle<=180 has to be True "
                print "angle = ", angle
                return 55

            iso1=args["<iso1>"]
            iso2=args["<iso2>"]

            if args["--xTreme"]==True:
                if args["-v"]==True:
                    print "#Prints out angles and energies of the reactions"
                    print "#lev\tlevE\t\tEe\tang2L\tEr"
                pXXTremeTest(xXTremeTest(iso1,iso2,Elab,angle))
                return 0
                    
            # print xTremeTest(iso1,iso2,Elab,angle)
            pXTremeTest(iso1,iso2,Elab,angle)
            return 0

    scatE=args["--scatE"]    
    if scatE:
        if args["-v"]==True:
            print "#Gives the beam energy [MeV]"

        if not testVal(scatE):
            print "Error; scattered energy has to be a number"
            return 10 #Making this up as I go
        scatE=float(scatE)

        angle=args["--angle"]
        if not testVal(scatE):
            print "Error; scattered energy has to be a number"
            return 10
        angle=float(angle)
        if not 0<=angle<=180:
            print "Error; angle outside of 0<=angle<=180"
            return 11

        iso1=args["<iso1>"]
        iso2=args["<iso2>"]
        print findOE(scatE,angle,iso1,iso2)
        return 0

    if args["--reactE"]:
        pass #For now
            
    if args["--QVal"] or args["-q"]:
        isop=args["<isop>"]
        isot=args["<isot>"]
        isoE=args["<isoEject>"]
        isoR=args["<isoRes>"]
        if args["--amu"]:
            print getIsoQValAMU(isop,isot,isoE,isoR)
        else:
            print getIsoQVal(isop,isot,isoE,isoR)
        return 0


    if args["--maxAng"]:
        if args["-v"]:
            print "#Given a beam energy it outputs the maximum angle the exit particles have"
        Elab=args["--Elab"]
        if not testVal(Elab):
            print "Error; energy has to be a number"
            return 8
        Elab=float(Elab)
        isop=args["<isop>"]
        isot=args["<isot>"]
        isoE=args["<isoEject>"]
        isoR=args["<isoRes>"]

        print getMaxAngles(isop,isot,isoE,isoR,Elab)
        return 0

    if args["--angle"] and args["<isoRes>"]:
        if args["-v"]:
            print "#Prints the energies that'll reach the detector"
        Elab=args['--Elab']
        angle=args["--angle"]
        if testVal(Elab) and testVal(angle):
            Elab=float(Elab)
            angle=float(angle)
            if not 0<=angle<=180:
                print "Error; 0<=angle<=180 has to be True "
                print "angle = ",angle
                return 7
            isop=args["<isop>"]
            isot=args["<isot>"]
            isoE=args["<isoEject>"]
            isoR=args["<isoRes>"]
            if args["-x"] or args["--xTreme"]:
                pXReaction(xReaction(isop,isot,isoE,isoR,Elab,angle))
                return 0
            # sReact=sReaction(isop,isot,isoE,isoR,Elab,angle)
            pSReaction(isop,isot,isoE,isoR,Elab,angle)
            return 0

