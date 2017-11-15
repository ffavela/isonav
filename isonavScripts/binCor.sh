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

thickVar=300
thick_Si=(220 220 $thickVar $thickVar $thickVar
          $thickVar $thickVar $thickVar 275 275 275 275
          275 275 275 275 $thickVar $thickVar 270 270 270
          270 270 270 270 270 270 270 270 270 270 270 270
          270 270)

teles_num=(16 16 24 24 32 32 40 40 40 40 48 48 48 48 48 48 48 48
           32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 16 8)

delta_phi=(22.5 22.5 15 15 11.25 11.25 9 9 9 9 7.5 7.5 7.5 7.5 7.5 7.5
           7.5 7.5 11.25 11.25 11.25 11.25 11.25 11.25 11.25 11.25
           11.25 11.25 11.25 11.25 11.25 11.25 11.25 22.5 45)

firstTelL=(0 16 32 56 80 112 144 184 224 264 304 352 400 448 496 544
	   592 640 688 720 752 784 816 848 880 912 944 976 1008 1040
	   1072 1104 1136 1168 1184)

lastTelL=(15 31 55 79 111 143 183 223 263 303 351 399 447 495 543 591
	  639 687 719 751 783 815 847 879 911 943 975 1007 1039 1071 1103
	  1135 1167 1183 1191)

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

    echo -e "#name\t\t\t[cm]\t[deg]\t[um]\t\t[deg]"
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
	    return
        fi
    done
    echo "No idx found"
    exit 10
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

function checkSubTelFromTag() {
    myTag=$1
    subTel=$2
    rIdx=$(getRingIdx $myTag)
    checkSubTel $rIdx $subTel
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

function convertTel2Less() {
    side1NumInit=$1
    initNumOfSides=$2
    finalNumOfSides=$3
    let "side1NumFinal=$side1NumInit/($initNumOfSides/$finalNumOfSides)"
    echo $side1NumFinal
}

function convert2More() {
    side1NumInit=$1
    initNumOfSides=$2
    finalNumOfSides=$3

    let "ratio=$finalNumOfSides/$initNumOfSides"
    let "lastVal=$ratio-1"
    side2FinalList=()
    for i in $(seq 0 $lastVal)
    do
	let "side2Final=$side1NumInit*$ratio+i"
	side2FinalList+=($side2Final)
    done
    echo "${side2FinalList[@]}"
}

function getOpoInSameBase() {
    side1Num=$1
    totSideNum=$2
    let "side2Num=($side1Num+$totSideNum/2)%$totSideNum"
    echo $side2Num
}

function getIdxs4Reaction() {
    ringTag=$1
    myRingIdx=$(getRingIdx $ringTag)
    myStr2Print=$(getStr2Print $myRingIdx)
    initTag=$(echo -e "$myStr2Print" | cut -f2)
    finalTag=$(echo -e "$myStr2Print" | cut -f3)
    myInitRingIdx=$(getRingIdx $initTag)
    myFinalRingIdx=$(getRingIdx $finalTag)
    # echo -e "$initTag\t$finalTag"
    echo -e "$myInitRingIdx\t$myFinalRingIdx"
}

function getFromIdxNumOfTelescopes() {
    rIdx=$1
    numOfTeles=${teles_num[$rIdx]}
    echo $numOfTeles
}

function getFromTagNumOfTelescopes() {
    tagName=$1
    rIdx=$(getRingIdx $tagName)
    getFromIdxNumOfTelescopes $rIdx
}

function myTestFunction() {
    rTag=$1
    rIdx=$(getRingIdx $rTag)
    subTel=$2
    checkSubTel $rIdx $subTel
    minMaxIdx=$(getIdxs4Reaction $rTag)
    minIdx=$(echo -e "$minMaxIdx" | cut -f1)
    maxIdx=$(echo -e "$minMaxIdx" | cut -f2)
    initNumOfSides=$(getFromIdxNumOfTelescopes $rIdx)
    echo $initNumOfSides
    for i in $( seq $minIdx $maxIdx )
    do
	numOfTeles=$(getFromIdxNumOfTelescopes $i)
	echo -e "i=$i\t$numOfTeles"
	if [ $numOfTeles -eq $initNumOfSides ]
	then
	    echo "equal"
	    echo "calling some function"
	    echo $subtel
	elif [  $numOfTeles -lt $initNumOfSides ]
	then
	    echo "less"
	    echo "Doing the other function stuff"
	    echo "numOfTeles=$numOfTeles"
	    convertTel2Less $subTel $initNumOfSides $numOfTeles
	elif [ $numOfTeles -gt $initNumOfSides ]
	then
	    echo "greater"
	    echo "Doing the greater function case"
	    echo "echoing my more var"
	    echo "numOfTeles = $numOfTeles and initNumOfSides $initNumOfSides"
	    convert2More $subTel $initNumOfSides $numOfTeles
	fi
    done
}

function getSidesInNewBase() {
    l=$1
    iBase=$2
    fBase=$3

    DPhiI=$(echo "scale=3;360/$iBase" | bc)
    DPhiF=$(echo "scale=3;360/$fBase" | bc)
    echo $DPhiI $DPhiF

    iBase1=$(echo "scale=3;$l*$DPhiI" | bc)
    iBase2=$(echo "scale=3;($l+1)*$DPhiI" | bc)

    echo -e "The initial base angular values\n"
    echo $iBase1 $iBase2
    echo "######################"
    let "maxIdx=$fBase-1"

    echo $maxIdx

    mySideArr=()
    for i in $(seq 0 $maxIdx)
    do
	fBase1=$(echo "scale=3;$i*$DPhiF" | bc)
	fBase2=$(echo "scale=3;($i+1)*$DPhiF" | bc)
	echo $fBase1 $fBase2
	# echo "Checking cond either $fBase1<=$iBase1<$fBase2 or $fBase1<=$iBase2<$fBase2"
	if [ $(echo "$fBase1<=$iBase1 && $iBase1<=$fBase2" | bc) -eq 1 ] ||\
	       [ $(echo "$fBase1<=$iBase2 && $iBase2<=$fBase2" | bc) -eq 1 ]
	then
	    echo "Inside cond either $fBase1<=$iBase1<=$fBase2 or $fBase1<=$iBase2<=$fBase2"
	    echo "Is true"
	    mySideArr+=($i)
	fi
    done
    echo "The corresponding sides in base $fBase are:"
    echo "${mySideArr[@]}"
}


argHandling $@

# getSidesInNewBase 23 24 10

# getStr2Print 2

# getRingIdx 8e

# getIdxs4Reaction 1i

# getFromTagNumOfTelescopes S10

# echo "Doing myTestFunction"
# myTestFunction 7e 37

# convertTel2Less 5 16 8
# convertTel2Less 15 16 8
# convertTel2Less 37 48 32

# getOpoInSameBase 3 8
# convert2More 3 4 16
