#!/bin/bash

#For each element in the database
#It prints the number of isotopes
#It prints at the end the max values

maxN=0
maxS$="n"
maxIsoC=0

for n in $(seq 0 118)
do
    s=$(isonav $n -s)
    isoCount=$(isonav $s -i | wc -l)
    echo $n $s $isoCount

    if [ $isoCount -ge $maxIsoC ]
    then
	maxN=$n
	maxS=$s
	maxIsoC=$isoCount
    fi
done

echo "The max values are:"
echo $maxN $maxS $maxIsoC

