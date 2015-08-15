#!/bin/bash

#Looks for all the isotopes that could have double proton emission

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
    	val=$(isonav $v --pEmission --num=2)
    	[ ! "$val" = "" ]&& echo -e "$v\t$val"&&counter=$(echo "$counter +1" | bc)
    done
done

echo "There are $counter isos that could have 2 proton emission"
