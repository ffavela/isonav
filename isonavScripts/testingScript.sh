#!/bin/bash

#Just a series of tests, not very descriptive for now

echo "$ isonav"
isonav
echo ""
echo "$ isonav 22 -s"
isonav 22 -s
echo ""
echo "$ isonav Au --protons"
isonav Au --protons
echo ""
echo "$ isonav 195Au --neutrons"
isonav 195Au --neutrons
echo ""
echo "$ isonav Pb -i"
isonav Pb -i
echo ""
echo "$ isonav Pb -iv"
isonav Pb -iv
echo ""
echo "$ isonav Au -im --amu"
isonav Au -im --amu
echo ""
echo "$ isonav 22Ne --mass"
isonav 22Ne --mass
echo ""
echo "$ isonav 22Ne --mass --liquidDrop"
isonav 22Ne --mass --liquidDrop
echo ""
echo "$ isonav 22Ne --mirror"
isonav 22Ne --mirror
echo ""
echo "$ isonav 40Ca -r"
isonav 40Ca -r
echo ""
echo "$ isonav 12C --levels --limit=10"
isonav 12C --levels --limit=10
echo ""
echo "$ isonav 151Lu --pEmission"
isonav 151Lu --pEmission
echo ""
echo "$ isonav 13Be --nEmission"
isonav 13Be --nEmission
echo ""
echo "$ isonav 45Fe --pEmission --num=2"
isonav 45Fe --pEmission --num=2
isonav 12C --levels --limit=10
echo ""
echo "$ isonav 12C --Elab=2.0 --redDeBroglie"
isonav 12C --Elab=2.0 --redDeBroglie
echo ""
echo "$ isonav d 14N a 12C --Elab=3.0 --angle=35"
isonav d 14N a 12C --Elab=3.0 --angle=35
echo ""
echo "$ isonav d 14N a 12C --Elab=3.0 --angle=35 --xTreme"
isonav d 14N a 12C --Elab=3.0 --angle=35 --xTreme
echo ""
echo "$ isonav d 14N d 14N --Elab=5.5 --angle=25 --xTreme"
isonav d 14N d 14N --Elab=5.5 --angle=25 --xTreme
echo ""
echo "$ isonav d 14N --reactions"
isonav d 14N --reactions
echo ""
echo "$ isonav p 14N  --fussion"
isonav p 14N  --fussion
echo ""
echo "$ isonav p 14N --fussion --Elab=0.1 -v"
isonav p 14N --fussion --Elab=0.1 -v
echo ""
echo "$ isonav d 14N --Elab=3.0 --angle=35"
isonav d 14N --Elab=3.0 --angle=35
echo ""
echo "$ isonav d 14N --Elab=3.0 --angle=35 --xTreme"
isonav d 14N --Elab=3.0 --angle=35 --xTreme
echo ""
echo "$ isonav n --compton -v"
isonav n --compton -v
echo ""

