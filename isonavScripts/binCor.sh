#!/bin/bash

#A script for checking coincidences on the rings of CHIMERA

eLab=60.0
#Make sure reactions are valid!!!
isoP=a
isoT=12C

isoE=a
isoR=12C

xRes=0.0

thetaVals=(1.4 2.2 3.1 4.1 5.2 6.4 7.8 9.3 10.8 12.3 13.8 15.3 17.00
	  19.00 21.00 23.00 25.50 28.50 34 42 50 58 66 74 82 90 98 106
	  114 122 130 138 146 156.5 169.5)


theta_min=(1. 1.8 2.6 3.6 4.6 5.8 7.0 8.5 10. 11.5 13. 14.5
          16. 18. 20. 22. 24. 27.
          30. 38. 46. 54. 62. 70. 78. 86. 94. 102. 110.
          118. 126. 134. 142. 150. 163. )

theta_max=(1.8 2.6 3.6 4.6 5.8 7. 8.5 10. 11.5 13. 14.5
          16. 18. 20. 22. 24. 27. 30.
          38. 46. 54. 62. 70. 78. 86. 94. 102. 110.
          118. 126. 134. 142. 150. 163. 176. )

ring_tags=(1i 1e 2i 2e 3i 3e 4i 4e 5i 5e 6i 6e 7i 7e 8i 8e 9i 9e
	   S10 S11 S12 S13 S14 S15 S16 S17 S18 S19 S20 S21 S22 S23
	  S24 S25 S26)


function getAbs(){
    #Dumb way of doing it
    echo $1 | tr -d '-'
}

function getMinIxd(){
    myMinIdx=0
    myMin=${theta_min[$myMinIdx]}
    myVar=$1
    lastVal=$myMinIdx

    let "maxIdx=${#thetaVals[*]}-1"
    for i in $( seq 0 $maxIdx )
    do
	if [ $( echo "$myVar<$myMin" | bc) -eq 1 ]
	then
	    let "lastVal=$lastVal-1"
	    echo $lastVal
	    return
	fi
	myMin=${theta_min[i]}
	lastVal=$i
    done
}

function getMaxIxd(){
    myMaxIdx=1
    myMax=${theta_min[$myMaxIdx]}
    myVar=$1
    lastVal=$myMaxIdx

    let "maxIdx=${#thetaVals[*]}-1"
    for i in $( seq 1 $maxIdx )
    do
	if [ $( echo "$myVar<$myMax" | bc) -eq 1 ]
	then
	    echo $lastVal
	    return
	fi
	myMax=${theta_max[i]}
	lastVal=$i
    done
}

# getMinIxd $1
# getMaxIxd $1

function printCoinRings(){
    #### ### for thetaA in "${thetaVals[@]}"

    let "maxIdx=${#thetaVals[*]}-1"

    echo -e "ejeRing\tresMin\tresMax"
    #i is the ring number index -1 of the ejectile

    for i in $( seq 0 $maxIdx )
    do
	thetaA=${thetaVals[i]}
	thetaAMin=${theta_min[i]}
	thetaAMax=${theta_max[i]}
	var=$(isonav  $isoP $isoT $isoE $isoR --Elab=$eLab --angle=$thetaA --xRes=$xRes)
	varMin=$(isonav $isoP $isoT $isoE $isoR --Elab=$eLab --angle=$thetaAMin --xRes=$xRes)
	varMax=$(isonav $isoP $isoT $isoE $isoR --Elab=$eLab --angle=$thetaAMax --xRes=$xRes)
	thetaRes=$(echo $var | cut -d' ' -f 4)
	thetaResMin=$(echo $varMin | cut -d' ' -f 4)
	thetaResMax=$(echo $varMax | cut -d' ' -f 4)

	ejectE=$(echo $var | cut -d' ' -f 3)
	resE=$(echo $var | cut -d' ' -f 5)
	thetaRes=$(getAbs $thetaRes)
	thetaResMin=$(getAbs $thetaResMin)
	thetaResMax=$(getAbs $thetaResMax)

	realMin=$(awk -v a="$thetaResMin" -v b="$thetaResMax" 'BEGIN{print (a>b)?b:a}')

	realMax=$(awk -v a="$thetaResMin" -v b="$thetaResMax" 'BEGIN{print (a<b)?b:a}')

	# echo -e "$i\t$thetaA\t$realMin\t$thetaRes\t$realMax"
	# echo "resE = $resE"
	minDIdx=$(getMinIxd $realMin)
	maxDIdx=$(getMaxIxd $realMax)
	minDRingV=${theta_min[$minDIdx]}
	maxDRingV=${theta_max[$maxDIdx]}
	# echo -e "$i\t$minDRingV\t$maxDRingV"
	#Puttig the correct ring numbers
	mainRing=${ring_tags[$i]}
	minRing=${ring_tags[$minDIdx]}
	maxRing=${ring_tags[$maxDIdx]}

	echo -e "$mainRing\t$minRing\t$maxRing"
    done
}

printCoinRings
