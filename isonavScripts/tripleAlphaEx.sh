#!/bin/bash

#Simulates the deposited energy of a triple alpha source in a 11 micron
#silicon detector with a 1.2 micron gold coating.

#All in MeV's
E1=5.15
E2=5.48
E3=5.8

silThick=11.5
goldThick=1.4

echo "Calculating energy loss from a triple alpha source through"
echo "a silicon detector with thickness $silThick microns and a gold"
echo "and a gold coating of $goldThick microns."

E1i=$(isonav a --material=Si --thick=$silThick --Elab=$E1)
dE1i=$(isonav a --material=Si --thick=$silThick --Elab=$E1 --depo)

E2i=$(isonav a --material=Si --thick=$silThick --Elab=$E2)
dE2i=$(isonav a --material=Si --thick=$silThick --Elab=$E2 --depo)

E3i=$(isonav a --material=Si --thick=$silThick --Elab=$E3)
dE3i=$(isonav a --material=Si --thick=$silThick --Elab=$E3 --depo)

E1f=$(isonav a --material=Au --thick=$goldThick --Elab=$E1i)
dE1f=$(isonav a --material=Au --thick=$goldThick --Elab=$E1i --depo)

E2f=$(isonav a --material=Au --thick=$goldThick --Elab=$E2i)
dE2f=$(isonav a --material=Au --thick=$goldThick --Elab=$E2i --depo)

E3f=$(isonav a --material=Au --thick=$goldThick --Elab=$E3i)
dE3f=$(isonav a --material=Au --thick=$goldThick --Elab=$E3i --depo)

tdE1=$(echo "scale=2; $dE1i+$dE1f" | bc -l)
tdE2=$(echo "scale=2; $dE2i+$dE2f" | bc -l)
tdE3=$(echo "scale=2; $dE3i+$dE3f" | bc -l)

echo -e "Alpha_E\tDeltaE\texp DeltaE"
echo -e "$E1\t$tdE1\t2.55"
echo -e "$E2\t$tdE2\t2.41"
echo -e "$E3\t$tdE3\t2.29"
