#!/usr/bin/env python
"""Usage:
  isonav.py <number> [-v] (-s|--symbol)
  isonav.py <symbol> [-v] ([-p|--protons])
  isonav.py <iso> [-v] [-n|--neutrons] [[-i|--isotopes] [-m --amu]]
  isonav.py <iso> [-v] ([-m|--mass]|--compton) [--amu --liquidDrop]
  isonav.py <iso> [-v] --mirror
  isonav.py <iso> [-v] ([-r | --radius]|[(-l|--levels) [--limit=val]])
  isonav.py <iso> [-v] --Elab=val [--redDeBroglie] 
  isonav.py <iso> [-v] --decay
  isonav.py <iso> [-v] (--BE | --BEperNucleon) [--liquidDrop]
  isonav.py <iso1> <iso2> [-v] (--coulomb | --reactions [--latex] )
  isonav.py <iso1> <iso2> [-v] --fussion [--Elab=val]
  isonav.py <iso1> <iso2> [-v] --Elab=val --angle=val [[--xTreme|-x] --latex]
  isonav.py <iso1> <iso2> [-v] --scatE=val --angle=val 
  isonav.py <iso1> <iso2> --Elab=val --reactE=val --tol=val
  isonav.py <isop> <isot> <isoEject> <isoRes> [-v] (-q|--QVal) [--amu]
  isonav.py <isop> <isot> <isoEject> <isoRes> [-v] --Elab=val --maxAng
  isonav.py <isop> <isot> <isoEject> <isoRes> [-v] --Elab=val --angle=val [-x|--xTreme]
  isonav.py -h | --version
"""
from docopt import docopt
from argumentHandling import argHand
import sqlite3


if __name__ == '__main__':
    args = docopt(__doc__, version='v1.0')
    # print(args)
    argHand(args)
