#!/bin/bash

#Looks for all the most tightly bound nucleus

function getIsotopes {
    iso=$(isonav $1 -i)
    echo $iso | tr " " "\n"
}

echo -e "#iso\tBE per nucleus[MeV]"
min=0
max=-100

for n in $(seq 0 118)
do
    s=$(isonav $n -s)
    isos=$(getIsotopes $s)
    for v in $isos
    do
    	val=$(isonav $v --BEperNucleon)
	echo -e "$v\t$val"

	if [ $(echo "$val < $min" | bc) -eq 1 ]
	then 
	    min=$val
	    isoMin=$v
	fi

	if [ $(echo "$val > $max" | bc) -eq 1 ]
	then 
	    max=$val
	    isoMax=$v
	fi
    done
done

echo "The most tightly bound isotope is $isoMin BE=$min"
echo ""
echo "The most loosely bound isotope is $isoMax BE=$max"

