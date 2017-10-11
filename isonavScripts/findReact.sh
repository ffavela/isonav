#!/bin/bash

#Finds all the binary reactions that could produce a specific isotope

iso2Find=26Al #The isotope 2 find
achiE=10.0 #CM Energy achievable at our lab
maxPro=14
maxTar=30
minQ=-2.5

pNum=$(isonav $iso2Find -p)
initVal=$(echo "$pNum-1"|bc)

function getIsotopes {
    iso=$(isonav $1 -i)
    echo $iso | tr " " "\n"
}

isoPro=("1n" "1H" "2H" "3He" "4He" "6Li" "7Li")

echo -e "#proj\ttarget\teje\tres\tthres\tQ\tcoulAft\tcoulb4"

for iso1 in "${isoPro[@]}"
do
    for m in $(seq $initVal $maxTar)
    do
        s2=$(isonav $m -s)
        isos2=$(getIsotopes $s2)

        for iso2 in $isos2
        do
            coulE=$(isonav $iso1 $iso2 --coulomb)
            [ $(echo "$coulE > $achiE" | bc) -eq 1 ] && continue
            flagVar=1 #At least one iso of s2 is under the barrier
            val=$(isonav $iso1 $iso2 --reactions | grep $iso2Find)
            if [ "$val" != "" ]
            then
                Q=$(echo $val | cut -f4 -d' ')
                exitCoul=$(echo $val | cut -f5 -d' ')
                [ $(echo "$Q > $minQ" | bc) -eq 0 ] && continue
                coulEF=$(printf "%0.2f\n" $(bc -q <<< scale=2\;$coulE))
                echo -e "$iso1\t$iso2\t$val\t$coulEF"
            fi
        done
    done
done
