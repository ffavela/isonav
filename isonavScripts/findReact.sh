#!/bin/bash

#Finds all the binary reactions that could produce a specific isotope

iso2Find=26Al #The isotope 2 find

pNum=$(isonav $iso2Find -p)

function getIsotopes {
    iso=$(isonav $1 -i)
    echo $iso | tr " " "\n"
}

echo -e "#proj\ttarget\teje\tres\tthres\tQ\tcoulomb"
for n in $(seq 0 118)
do
    s1=$(isonav $n -s)
    isos1=$(getIsotopes $s1)

    for m in $(seq $pNum 118)
    do
        s2=$(isonav $m -s)
        isos2=$(getIsotopes $s2)

        for iso1 in $isos1
        do
            for iso2 in $isos2
            do
                val=$(isonav $iso1 $iso2 --reactions | grep $iso2Find)
                if [ "$val" != "" ]
                then
                    echo -e "$iso1\t$iso2\t$val"
                fi
            done
        done

    done

done
