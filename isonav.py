#!/usr/bin/python3

#   Copyright (C) 2015-2026 Francisco Favela

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Usage:
  isonav <number> [-v] (-s|--symbol)
  isonav <symbol> [-v] ([-p|--protons])
  isonav <symbol> [-v] (--name)
  isonav <iso> [-v] [-n|--neutrons] [[-i|--isotopes] [-m --amu]]
  isonav <iso> [-v] ([-m|--mass]|--compton) [--amu --liquidDrop]
  isonav <iso> [-v] --mirror
  isonav <iso> [-v] ([-r | --radius]|[(-l|--levels) [--limit=val]])
  isonav <iso> [-v] --Elab=val (--deBroglie | --redDeBroglie)
  isonav <iso> [-v] --Elab=val --L4TOF=L
  isonav <iso> [-v] --decay [--Ex=val]
  isonav <iso> [-v] (--alpha | --nEmission | --pEmission ) [--num=val]
  isonav <iso> [-v] --Emission=val [--num=val]
  isonav <iso> [-v] (--BE | --BEperNucleon) [--liquidDrop]
  isonav <iso1> <iso2> [-v] (--coulomb | --reactions [--latex] )
  isonav <iso1> <iso2> [-v] (--gamowEnergy | --T=temp --gamowPeak )
  isonav <iso1> <iso2> [-v] --fussion [--Elab=val]
  isonav <iso1> <iso2> [-v] --Elab=val --angle=val [[--xTreme|-x] --latex]
  isonav <iso1> <iso2> [-v] --scatE=val --angle=val
  isonav <isop> <isot> <isoEject> <isoRes> [-v] (-q|--QVal) [--amu]
  isonav <isop> <isot> <isoEject> <isoRes> [-v] --Elab=val --maxAng
  isonav <isop> <isot> <isoEject> <isoRes> [-v] --Elab=val --angle=val ([--xEje=val] [--xRes=val])
  isonav <isop> <isot> <isoEject> <isoRes> [-v] --Elab=val --angle=val [(-x|--xTreme) [--xF1=xFileEject.txt] [--xF2=xFileRes.txt]]
  isonav <ion> [-v] --material=matName --Elab=val (--thickness=val [--depositedE] | --range) [--bloch] [--density=dens]
  isonav [-v] --listMaterials [--material=matName]
  isonav -h | --version
"""

from docopt import docopt
from argumentHandling import argHand
import sqlite3


if __name__ == '__main__':
    args = docopt(__doc__, version='v1.6.1')
    # print(args)
    argHand(args)
