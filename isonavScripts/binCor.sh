#!/bin/bash

#A script for checking coincidences on the rings of CHIMERA

eLab=60.0 #in MeV
#Make sure reactions are valid!!!
isoP=a
isoT=12C

isoE=a
isoR=12C

material=C #For energy loss in the target
#Use isonav --listMaterials to see which ones are available.
thickness=0.44 #in microns
#Where in the target we think the reaction occurs, say halfway.
halfThick=$(echo "$thickness/2.0" | bc -l )

xRes=9.64 #Excitation of the residual particle.

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


#Defining colors
RED='\033[0;31m'
NC='\033[0m' # No Color

function myHelp(){
    usage="${RED}usage:${NC} ./binCor [options]\n
           Does simple binary kinematics on CHIMERA\n
           says which rings are in coincidence\n
           by default it shows this help\n
           Only one option can be used at the same time.\n
           \t-h:\t shows this help\n
           \t-E:\t prints the energies of the particles after the\n
           \t\treaction with target energy loss.\n
           \t-A:\tprints the angles of the particles.\n
           \t\tmore options coming eventually"
    echo -e $usage
}

function argHandling() {
    if [ "$1" == "-h" ]
    then
	myHelp
    elif [ "$1" == "-E" ]
    then
	#Dumb 4 now but eventually might prove useful
	printCoinRings $1
    elif [ "$1" == "-A" ]
    then
	printCoinRings $1
    else
	printCoinRings
    fi
}

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

function getFinalEnergy(){
    ion=$1
    ionE=$2
    material=$3
    thickness=$4

    finalE=$(isonav $ion --Elab=$ionE --material=$material --thickness=$thickness)
    echo $finalE
}

function getTan(){
    #Received values are in degrees
    angleDeg=$1
    pi=$(echo "scale=10; 4*a(1)" | bc -l)
    angleRad=$(echo "scale=10; $angleDeg/180*$pi" | bc)
    myTan=$(echo "s($angleRad)/c($angleRad)" | bc -l)
    echo $myTan
}

function printCoinRings(){
    #### ### for thetaA in "${thetaVals[@]}"

    baseHeadStr="ejeRing\tresMin\tresMax"
    eHead=""

    [ "$1" == "-E" ] && eHead="\tejeE\tejeFE\tresE\tresFE"
    [ "$1" == "-A" ] && eHead="\tejeAng\tresMin\tresA\tresMax"
    headStr=$baseHeadStr$eHead

    echo -e "$headStr"

    let "maxIdx=${#thetaVals[*]}-1"

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

	minDIdx=$(getMinIxd $realMin)
	maxDIdx=$(getMaxIxd $realMax)
	minDRingV=${theta_min[$minDIdx]}
	maxDRingV=${theta_max[$maxDIdx]}

	mainRing=${ring_tags[$i]}
	minRing=${ring_tags[$minDIdx]}
	maxRing=${ring_tags[$maxDIdx]}

	baseStr="$mainRing\t$minRing\t$maxRing"
	energyStr=""
	angleStr=""

	if [ "$1" == "-E" ]
	then
	    resHThick=$(echo "scale=10;$(getTan $thetaRes)*$halfThick" | bc )
	    resFE=$(getFinalEnergy $isoR $resE  $material $resHThick)

	    ejeHThick=$(echo "scale=10;$(getTan $thetaA)*$halfThick" | bc )
	    ejeFE=$(getFinalEnergy $isoE $ejectE  $material $resHThick)

	    energyStr="\t$ejectE\t$ejeFE\t$resE\t$resFE"
        fi

	if [ "$1" == "-A" ]
	then
	    angleStr="\t$thetaA\t$realMin\t$thetaRes\t$realMax"
	fi


	str2Print=$baseStr$energyStr$angleStr
	echo -e "$str2Print"
    done
}


argHandling $@
