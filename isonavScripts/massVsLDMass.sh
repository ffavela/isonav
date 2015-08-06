#!/bin/bash

# Prints all the masses of the isotopes and also the LD model mass it
# also prints the mass difference, the min diff, the max diff and the
# average

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

minD=1000
isoMin="n"

maxD=0
isoMax="n"

counter=0
avg=0

echo -e "#iso\tmass[MeV]\tLDmass[MeV]\tmassDiff"
for n in $(seq 0 118)
do
    s=$(isonav $n -s)
    isos=$(getIsotopes $s)
    for v in $isos
    do
	m=$(isonav $v -m)
	ldM=$(isonav $v -m --liquidDrop )
	diff=$(echo $m-$ldM | bc)
	echo -e "$v\t$m\t$ldM\t$diff"

	counter=$(echo "$counter +1" | bc)
	avg=$(echo "$avg + $diff" | bc)

	# ${diff#-} is like absolute value
	if [ $(echo "${diff#-} < $minD" | bc) -eq 1 ]
	then 
	    minD=${diff#-}
	    isoMin=$v
	fi

	if [ $(echo "${diff#-} > $maxD" | bc) -eq 1 ]
	then 
	    maxD=${diff#-}
	    isoMax=$v
	fi
    done
done

avg=$(echo "scale=3; $avg/$counter" | bc)

echo ""

echo "Min difference when $isoMin $minD"
echo "Max difference when $isoMax $maxD"
echo "The average difference is $avg"
