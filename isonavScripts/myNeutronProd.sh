#!/bin/bash

#Prints out the corresponding neutron reaction from deuterons on
#different gases

# gasArray[0]="d"
# gasArray[1]="t"
# gasArray[2]="14N"
# gasArray[3]="20Ne"
# gasArray[4]="21Ne"
# gasArray[5]="22Ne"
# gasArray[6]="40Ar"
# gasArray[7]="80Kr"

#Better way
gasArray=(d t 14N 20Ne 21Ne 22Ne 40Ar 80Kr)

for i in ${gasArray[@]}
do
    imp=$(isonav d $i --reactions | grep 1n | cut -f2,3,4)
    coul0=$(isonav d $i --coulomb)
    coul1=$(printf "%.2f\n" $coul0)
    echo -e "$i\t$imp\t$coul1"
done
