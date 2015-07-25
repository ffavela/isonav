"""Usage:
  isonavCLI.py <number> [-v] (-s|--symbol)
  isonavCLI.py <symbol> [-v] (-p|--protons)
  isonavCLI.py <iso> [-v] (-n|--neutrons)
  isonavCLI.py <iso> [-v] (-m|--mass) [--amu --liquidDrop]
  isonavCLI.py <iso> [-v] --mirror
  isonavCLI.py <iso> [-v] (-r | --radius)
  isonavCLI.py <iso> [-v] --Elab=val [--redDeBroglie] [--angstrom|--fm|--nm|--microns]
  isonavCLI.py <iso> [-v] --decay [--simple|--bp|--bm|--all] [--latex]
  isonavCLI.py <iso> [-v] (--BE | --BEperNucleon) [--liquidDrop]
  isonavCLI.py <iso1> <iso2> [-v] (--coulomb | --reactions)
  isonavCLI.py <iso1> <iso2> [-v] --Elab=val --angle=val [[--xTreme|-x] --latex]
  isonavCLI.py <iso1> <iso2> --Elab=val --reactE=val --tol=val
  isonavCLI.py <isop> <isot> <isoEject> <isoRes> [-v] (-q|--QVal) [--amu]
  isonavCLI.py <isop> <isot> <isoEject> <isoRes> [-v] --Elab=val --maxAng
  isonavCLI.py <isop> <isot> <isoEject> <isoRes> [-v] --Elab=val --angle=val [-x|--xTreme]
  isonavCLI.py -h | --version
  isonavCLI.py <"expression">
"""
from docopt import docopt
from argumentHandling import argHand
import sqlite3


if __name__ == '__main__':
    args = docopt(__doc__, version='v1.0')
    # print(args)
    argHand(args)

