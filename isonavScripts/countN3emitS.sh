#!/bin/bash

#Looks for all the isotopes that have 3 neutrons emission but not 1 or 2

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
	val1=$(isonav $v --nEmission --num=1)
	val2=$(isonav $v --nEmission --num=2)
    	val3=$(isonav $v --nEmission --num=3)
	[ ! "$val1" = "" ] && continue #Only triple
	[ ! "$val2" = "" ] && continue #Only triple
    	[ ! "$val3" = "" ]&& echo -e "$v\t$val3"&&counter=$(echo "$counter +1" | bc)
    done
done

echo "There are $counter isos that could have 3 neutrons emission"
echo "but not 1 or 2 neutrons emission"
