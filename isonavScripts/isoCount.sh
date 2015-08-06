#!/bin/bash

#For each element in the database
#It prints the number of isotopes
#It prints at the end the max values

maxN=0
maxS="n"
maxIsoC=0

echo -e "#Z\tSymbol\tNum of isos"

for n in $(seq 0 118)
do
    s=$(isonav $n -s)
    isoCount=$(isonav $s -i | wc -l)
    echo -e "$n\t$s\t$isoCount"

    if [ $isoCount -ge $maxIsoC ]
    then
	maxN=$n
	maxS=$s
	maxIsoC=$isoCount
    fi
done

echo "The max values are:"
echo -e "$maxN\t$maxS\t$maxIsoC"

