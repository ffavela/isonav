#!/bin/bash

#Finds all the binary reactions that could produce a specific isotope

iso2Find=26Al #The isotope 2 find
achiE=10.0 #CM Energy achievable at our lab

pNum=$(isonav $iso2Find -p)
initVal=$(echo "$pNum-1"|bc)

function getIsotopes {
    iso=$(isonav $1 -i)
    echo $iso | tr " " "\n"
}

echo -e "#proj\ttarget\teje\tres\tthres\tQ\tcoulAft\tcoulb4"
for n in $(seq 0 118)
do
    s1=$(isonav $n -s)
    isos1=$(getIsotopes $s1)
    for m in $(seq $initVal 118)
    do
        s2=$(isonav $m -s)
        isos2=$(getIsotopes $s2)
        flagVar=0

        for iso1 in $isos1
        do
            for iso2 in $isos2
            do
                coulE=$(isonav $iso1 $iso2 --coulomb)
                [ $(echo "$coulE > $achiE" | bc) -eq 1 ] && continue
                flagVar=1 #At least one iso of s2 is under the barrier
                val=$(isonav $iso1 $iso2 --reactions | grep $iso2Find)
                if [ "$val" != "" ]
                then
                    Q=$(echo $val | cut -f4 -d' ')
                    [ $(echo "$Q > 0" | bc) -eq 0 ] && continue
                    coulEF=$(printf "%0.2f\n" $(bc -q <<< scale=2\;$coulE))
                    echo -e "$iso1\t$iso2\t$val\t$coulEF"
                fi
            done
        done
        if [ $flagVar = 0 ]
        then
            echo "No more reactions under the barrier"
            exit 0
        fi
    done
done
