#!/bin/bash

#Simulates the deposited energy of a triple alpha source in a 11 micron
#silicon detector with a 1.2 micron gold coating.

#All in MeV's
E1=5.15
E2=5.48
E3=5.8

silThick=11
goldThick=1.15

E1i=$(isonav a --material=silicon --thick=$silThick --Elab=$E1)
dE1i=$(isonav a --material=silicon --thick=$silThick --Elab=$E1 --depo)

E2i=$(isonav a --material=silicon --thick=$silThick --Elab=$E2)
dE2i=$(isonav a --material=silicon --thick=$silThick --Elab=$E2 --depo)

E3i=$(isonav a --material=silicon --thick=$silThick --Elab=$E3)
dE3i=$(isonav a --material=silicon --thick=$silThick --Elab=$E3 --depo)

E1f=$(isonav a --material=gold --thick=$goldThick --Elab=$E1i)
dE1f=$(isonav a --material=gold --thick=$goldThick --Elab=$E1i --depo)

E2f=$(isonav a --material=gold --thick=$goldThick --Elab=$E2i)
dE2f=$(isonav a --material=gold --thick=$goldThick --Elab=$E2i --depo)

E3f=$(isonav a --material=gold --thick=$goldThick --Elab=$E3i)
dE3f=$(isonav a --material=gold --thick=$goldThick --Elab=$E3i --depo)

tdE1=$(echo "scale=2; $dE1i+$dE1f" | bc -l)
tdE2=$(echo "scale=2; $dE2i+$dE2f" | bc -l)
tdE3=$(echo "scale=2; $dE3i+$dE3f" | bc -l)

echo "The deposited energy for the $E1 MeV alpha is $tdE1 the expected is 2.55"
echo "The deposited energy for the $E2 MeV alpha is $tdE2 the expected is 2.41"
echo "The deposited energy for the $E3 MeV alpha is $tdE3 the expected is 2.29"
