#!/bin/bash

#For each element, print the isotope that has the most ways it could
#breakup and print out the maximum along with the corresponding isotope
#We are still limited by the current datababase

function isoBreak {
    c=$(isonav $1 --decay | wc -l)
    echo $c
}

function getSymbol {
    s=$(isonav $1 -s)
    echo $s
}

function getIsotopes {
    iso=$(isonav $1 -i)
    echo $iso | tr " " "\n"
}

function getIsoB {
    if [ $# -ne 1 ]
    then
	echo "Exactly one argument is needed"
	return 1
    fi
    maxW=0
    maxIso="NaN"
    for t in $(getIsotopes $1 -i)
    do
	w=$(isoBreak $t)

	if [ $w -ge $maxW ]
	then
	    maxW=$w
	    maxIso=$t
	fi

    done

    echo $maxIso $maxW
}

echo -e "#Z\tSymbol\tiso\tNumberOfBreakups"
for n in $(seq 0 118)
do
    s=$(isonav $n -s)
    maxV=$(getIsoB $s)
    maxV=$(echo $maxV | tr " " "\t")
    echo -e "$n\t$s\t$maxV"
done
