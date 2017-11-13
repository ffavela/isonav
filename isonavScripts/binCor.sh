#!/bin/bash

#A script for checking coincidences on the rings of CHIMERA

eLab=64.0 #in MeV
#Make sure reactions are valid!!!
isoP=4He
isoT=12C

isoE=4He
isoR=12C

material=C #For energy loss in the target
#Use isonav --listMaterials to see which ones are available.
thickness=0.44 #in microns
#Where in the target we think the reaction occurs, say halfway.
halfThick=$(echo "$thickness/2.0" | bc -l )

xRes=7.65 #Excitation of the residual particle.

thetaVals=(1.4 2.2 3.1 4.1 5.2 6.4 7.8 9.3 10.8 12.3 13.8 15.3 17.00
	  19.00 21.00 23.00 25.50 28.50 34 42 50 58 66 74 82 90 98 106
	  114 122 130 138 146 156.5 169.5)


theta_min=(1. 1.8 2.6 3.6 4.6 5.8 7.0 8.5 10. 11.5 13. 14.5
          16. 18. 20. 22. 24. 27.
          30. 38. 46. 54. 62. 70. 78. 86. 94. 102. 110.
          118. 126. 134. 142. 150. 163.)

theta_max=(1.8 2.6 3.6 4.6 5.8 7. 8.5 10. 11.5 13. 14.5
          16. 18. 20. 22. 24. 27. 30.
          38. 46. 54. 62. 70. 78. 86. 94. 102. 110.
          118. 126. 134. 142. 150. 163. 176.)

ring_tags=(1i 1e 2i 2e 3i 3e 4i 4e 5i 5e 6i 6e 7i 7e 8i 8e 9i 9e
	   S10 S11 S12 S13 S14 S15 S16 S17 S18 S19 S20 S21 S22 S23
	  S24 S25 S26)

#The distance from the sphere center to the detectors (cm)
det_dist=(350 350 300 300 250 250 210 210 180 180 160 160 140 140
          120 120 100 100 40 40 40 40 40 40 40 40 40 40 40 40
         40 40 40 40 40)

thickVar=230
thick_Si=(220 220 $thickVar $thickVar $thickVar
          $thickVar $thickVar $thickVar 275 275 275 275
          275 275 275 275 $thickVar $thickVar 305 305 305
          305 305 305 305 305 305 305 305 305 305 305 305
          305 305)

teles_num=(16 16 24 24 32 32 40 40 40 40 48 48 48 48 48 48 48 48
           32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 16 8)

delta_phi=(22.5 22.5 15 15 11.25 11.25 9 9 9 9 7.5 7.5 7.5
           7.5 7.5 7.5 7.5 7.5 11.25 11.25 11.25 11.25 11.25
           11.25 11.25 11.25 11.25 11.25 11.25 11.25 11.25
           11.25 11.25 22.5 45)

firstTelL=(0 16 32 56 80 112 144 184 224 264 304 352 400 448 496
       544 592 640 688 720 752 784 816 848 880 912 944 976
       1008 1040 1072 1104 1136 1168 1184)

lastTelL=(15 31 55 79 111 143 183 223 263 303 351 399 447 495
       543 591 639 687 719 751 783 815 847 879 911 943 975
      1007 1039 1071 1103 1135 1167 1183 1191)

#in cm^2
# S=(blach blah blah)

#Defining colors
RED='\033[0;31m'
NC='\033[0m' # No Color

function myHelp(){
    usage="${RED}usage:${NC} ./binCor [options]\n
           Does simple binary kinematics on CHIMERA\n
           says which rings are in coincidence\n
           Unless specified, only one option can be used\n
           at the same time.\n\n
           \t-h:\t\t\t shows this help\n\n
           \t-p:\t\t\t prints Chimera's table\n\n
           \t-E [--tof]:
           \t\t prints the energies of the particles after the\n
           \t\t\t\t reaction with target energy loss. If\n
           \t\t\t\t a -1.000 is printed then the particle\n
           \t\t\t\t did not exit the target.\n
           \t\t\t\t If --tof is used then it will calculate\n
           \t\t\t\t the time of flight (in ns) using the distances\n
           \t\t\t\t on the table.\n\n
           \t--dE [--depo]:\t\t same as the -E option but also\n
           \t\t\t\t includes the energy loss in the frontal\n
           \t\t\t\t  dE (Si). If --depo is used it prints the deposited\n
           \t\t\t\t energy on the Si.\n\n
           \t-A:\t\t\t prints the angles of the particles.\n\n
           \t--getN <ringId tN>:\t gets the global telescope\n
           \t\t\t\t number.\n\n
           \t--getChimAddr <gTN>:\t  gets the ring and local detector\n
           \t\t\t\t number within the ring\n\n
           \nmore options comming eventually"
    echo -e $usage
}

function argHandling() {
    if [ "$1" == "-h" ]
    then
	      myHelp
    elif [ "$1" == "-E" ]
    then
	#Dumb 4 now but eventually might prove useful
	printCoinRings $@
    elif [ "$1" == "--dE" ]
    then
	      printCoinRings $@
    elif [ "$1" == "-A" ]
    then
	      printCoinRings $@
    elif [ "$1" == "-p" ]
    then
        #Printing the table of chimera
        printChimTab
        exit 1
    elif [ "$1" == "--getN" ]
    then
        shift
        tNumParse $@
        getTNum $@
    elif [ "$1" == "--getChimAddr" ]
    then
        shift
        checkGTN $@
        getChimAddr $@
    else
	printCoinRings
    fi
}

function checkIfAnyEmpty(){
    expectedArgNum=3
    [ $# -ne $expectedArgNum ] && echo "empty"
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
 echo "###Reaction conditions###"
 echo "#$isoP $isoT => $isoE $isoR"
 echo "#xRes=$xRes, eLab=$eLab, material=$material, thickness=$thickness"
 echo "##########"
 baseHeadStr="#ejeRng\tresMin\tresMax"
 eHead=""

 if [ "$1" == "-E" ]
 then
     if [ "$2" == "--tof" ]
     then
         eHead="\teTof\teFTof\trTof\trFTof"
     else
         eHead="\tejeE\tejeFE\tresE\tresFE"
     fi
 fi

 if [ "$1" == "--dE" ]
 then
    if [ "$2" == "--depo" ]
    then
        echo "Entered --depo condition"
        eHead="\tejeE\tejeDE\tresE\tresDE"
    else
        eHead="\tejeE\tejeFE\tresE\tresFE"
    fi
 fi

 [ "$1" == "-A" ] && eHead="\tejeAng\tresMin\tresA\tresMax"
 headStr=$baseHeadStr$eHead

 echo -e "$headStr"

 let "maxIdx=${#thetaVals[*]}-1"
 #i is the ring number index -1 of the ejectile
 for i in $( seq 0 $maxIdx )
 do
     getStr2Print $i $@
 done
}

function getStr2Print() {
    i=$1
    shift #So we get the same arguments as b4
    thetaA=${thetaVals[i]}
    thetaAMin=${theta_min[i]}
    thetaAMax=${theta_max[i]}
    var=$(isonav  $isoP $isoT $isoE $isoR --Elab=$eLab\
                  --angle=$thetaA --xRes=$xRes)
    varMin=$(isonav $isoP $isoT $isoE $isoR --Elab=$eLab\
                    --angle=$thetaAMin --xRes=$xRes)
    varMax=$(isonav $isoP $isoT $isoE $isoR --Elab=$eLab\
                    --angle=$thetaAMax --xRes=$xRes)
    thetaRes=$(echo $var | cut -d' ' -f 4)
    thetaResMin=$(echo $varMin | cut -d' ' -f 4)
    thetaResMax=$(echo $varMax | cut -d' ' -f 4)

    emptyCheck=$(checkIfAnyEmpty $thetaRes $thetaResMin $thetaResMax)
    [ "$emptyCheck" == "empty" ] && return

    ejectE=$(echo $var | cut -d' ' -f 3)
    resE=$(echo $var | cut -d' ' -f 5)
    thetaRes=$(getAbs $thetaRes)
    thetaResMin=$(getAbs $thetaResMin)
    thetaResMax=$(getAbs $thetaResMax)

    realMin=$(awk -v a="$thetaResMin"\
                  -v b="$thetaResMax" 'BEGIN{print (a>b)?b:a}')

    realMax=$(awk -v a="$thetaResMin" -v\
                  b="$thetaResMax" 'BEGIN{print (a<b)?b:a}')

    minDIdx=$(getMinIxd $realMin)
    maxDIdx=$(getMaxIxd $realMax)
    let "aveRIdx=($minDIdx+$maxDIdx)/2"

    minDRingV=${theta_min[$minDIdx]}
    maxDRingV=${theta_max[$maxDIdx]}

    mainRing=${ring_tags[$i]}
    minRing=${ring_tags[$minDIdx]}
    maxRing=${ring_tags[$maxDIdx]}

    baseStr="$mainRing\t$minRing\t$maxRing"
    energyStr=""
    angleStr=""
    tofStr=""

    if [ "$1" == "--dE" ] || [ "$1" == "-E" ]
    then
	resHThick=$(echo "scale=10;$(getTan $thetaRes)*$halfThick"|bc)
	resFE=$(getFinalEnergy $isoR $resE  $material $resHThick)

	ejeHThick=$(echo "scale=10;$(getTan $thetaA)*$halfThick"|bc)
	ejeFE=$(getFinalEnergy $isoE $ejectE $material $resHThick)

	if [ "$1" == "-E" ] && [ "$2" == "--tof" ]
	then
	    eTof=$(getTof $isoE $ejectE ${det_dist[$i]})
	    rTof=$(getTof $isoR $resE ${det_dist[$aveRIdx]})

	    eFTof=$(getTof $isoE $ejeFE ${det_dist[$i]})
	    rFTof=$(getTof $isoE $resFE ${det_dist[$aveRIdx]})
	    tofStr="\t$eTof\t$eFTof\t$rTof\t$rFTof"
	fi

	detThick="${thick_Si[$i]}"
	if [ "$1" == "--dE" ]
	then
	    if  [ $( echo "$resFE>0" | bc) -eq 1 ]
	    then
		newResFE=$(getFinalEnergy $isoR $resFE Si $detThick)
	    else
		newResFE=$resFE
	    fi

	    if  [ $( echo "$ejeFE>0" | bc) -eq 1 ]
	    then
		newEjeFE=$(getFinalEnergy $isoE $ejeFE Si $detThick)
	    else
		newEjeFE=$ejeFE
	    fi

	    if [ "$2" == "--depo" ]
	    then
		resFE=$(depoE $resFE $newResFE )
		ejeFE=$(depoE $ejeFE $newEjeFE )
	    else
		resFE=$newResFE
		ejeFE=$newEjeFE
	    fi
	fi
	energyStr="\t$ejectE\t$ejeFE\t$resE\t$resFE"
	[ "$2" == "--tof" ] && energyStr=""
    fi

    if [ "$1" == "-A" ]
    then
	angleStr="\t$thetaA\t$realMin\t$thetaRes\t$realMax"
    fi

    str2Print=$baseStr$energyStr$tofStr$angleStr
    echo -e "$str2Print"
}

function printChimTab() {
    echo -en "#rings\tfTel\tlTel\tdistD\ttheta\t"
    echo -e "thickSi\tN_\tdeltaPhi"

    echo -e "#name\t\t\t[ns]\t[deg]\t[um]\t\t[deg]"
    for i in $( seq 0 34 )
    do
        strVar="${ring_tags[$i]}\t${firstTelL[$i]}\t${lastTelL[$i]}"
        strVar=$strVar"\t${det_dist[$i]}\t${thetaVals[$i]}"
        strVar=$strVar"\t${thick_Si[$i]}\t${teles_num[$i]}"
        strVar=$strVar"\t${delta_phi[$i]}"
        echo -e $strVar
    done
}

function depoE() {
    eB4=$1
    eAft=$2
    if [ $( echo "$eB4<0" | bc) -eq 1 ]
    then
        echo 0
    elif [ $( echo "$eAft<0" | bc) -eq 1 ]
    then
        echo $eB4
    else
        echo "scale=10; $eB4-$eAft" | bc
    fi
}

function tNumParse() {
    if [ $# != 2 ]
    then
        echo "ringId and tN are mandatory"
        exit 2
    fi
    ringIdx=$(getRingIdx $1)
    if [ "$ringIdx" == "" ]
    then
        echo -e "${RED}Error${NC} ring $1 not found"
        exit 3
    fi

    checkSubTel $ringIdx $2
}

function getTNum() {
    ringIdx=$(getRingIdx $1)
    initTNum=${firstTelL[$ringIdx]}
    let "tNum=$initTNum+$2"
    echo $tNum
}

function getRingIdx() {
    for i in $( seq 0 34 )
    do
        if [ "$1" == ${ring_tags[$i]} ]
        then
            echo $i
        fi
    done
}

function checkSubTel() {
    rIdx=$1
    subTel=$2
    if [ $subTel -ge ${teles_num[$rIdx]} ] || [ "$subTel" -lt 0 ]
    then
        echo "Not a valid telescope"
        exit 4
    fi
}

function checkGTN() {
    if [ "$#" -ne 1 ]
    then
        echo -e "${RED}Error: ${NC} the gTN is mandatory"
        exit 5
    fi

    gTN=$1
    if [ "$gTN" -lt 0 ] || [ "$gTN" -ge 1192 ]
    then
        errorStr="${RED}Error: ${NC} gTN (global
        telescope number)\n
        \thas to be an integer
        between 0 and 1191"
        echo -e $errorStr
        exit 6
    fi
}

function getChimAddr() {
    fTIdx=$(findFirstTelIdx $1)
    let "relT=$1-${firstTelL[$fTIdx]}"
    echo -e "${ring_tags[$fTIdx]}\t$relT"
}

function findFirstTelIdx() {
    oldTelIdx=0
    gTN=$1
    for i in $( seq 0 34 )
    do
        newTel=${firstTelL[$i]}
        if [ $gTN -lt "$newTel" ]
        then
            break
        fi
        oldTelIdx=$i
    done
    echo "$oldTelIdx"
}

function getTof() {
    iso4Tof=$1
    ene4Tof=$2
    L4Tof=$3
    if  [ $( echo "$ene4Tof>0" | bc) -eq 1 ]
    then
        myTof=$(isonav $iso4Tof\
                       --Elab=$ene4Tof --L4TOF=$L4Tof)
        printf "%.2f" $myTof
        return
    fi
    myTof="None"
    echo $myTof
}

argHandling $@

# getStr2Print 11
