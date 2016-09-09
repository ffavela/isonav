#!/bin/bash

#Looks for all the isotopes that could have triple proton emission but
#not 1 or 2

function getIsotopes {
    iso=$(isonav $1 -i)
    echo $iso | tr " " "\n"
}
counter=0
echo -e "#iso\teject\tdaughter\tQval"
for n in $(seq 0 118)
do
    s=$(isonav $n -s)
    isos=$(getIsotopes $s)
    for v in $isos
    do
	val1=$(isonav $v --pEmission --num=1)
    	val2=$(isonav $v --pEmission --num=2)
    	val3=$(isonav $v --pEmission --num=3)
	[ ! "$val1" = "" ] && continue #Only triple p emit
	[ ! "$val2" = "" ] && continue #Only triple p emit
    	[ ! "$val3" = "" ]&& echo -e "$v\t$val3"&&counter=$(echo "$counter +1" | bc)
    done
done

echo "There are $counter isos that could have 2 protons emission"
echo "but not one or 2 proton emission"
