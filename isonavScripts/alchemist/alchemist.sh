#!/bin/bash
#A script for checking coincidences on the rings of CHIMERA

#################### This part is for eventually
trap "exit 1" TERM # exiting the whole script through
export TOP_PID=$$  # the function calls
####################

########################################################################
########################################################################
## The configuration is now stored on an configuration file, use the ###
## --exampleConf option to create one and use it as an argument      ###
########################################################################
########################################################################

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
          275 275 275 275 $thickVar $thickVar 275 275 275
          275 275 275 275 275 275 275 275 275 275 275 275
          275 275)

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

dOmega=(0.133 0.209 0.247 0.326 0.373 0.458 0.549 0.660 0.756 0.870
     0.813 0.902 1.337 1.485 1.639 1.785 2.950 3.270 15.313 18.313 21.000
     23.250 25.063 26.375 27.125 27.438 27.125 26.375 25.063 23.250 21.00
     18.313 15.313 35.438 31.813)
#in cm^2
# S=(blach blah blah)

#Defining colors
RED='\033[0;31m'
NC='\033[0m' # No Color

function myHelp(){
    usage="${RED}usage:\n\t${NC}  $(basename $0) [eRing | gTN]\n
           \t $(basename $0) [miscOptions]\n
           \t $(basename $0) <confFile> [options] [eRing | gTN]\n\n
           \nMiscellaneous ($(basename $0) [miscOptions])\n\n
           \t-h:\t\t\t shows this help\n\n
           \t-p:\t\t\t prints Chimera's table\n\n
           \t--getN <ringId tN>:\t gets the global telescope\n
           \t\t\t\t number.\n\n
           \t--getChimAddr <gTN>:\t gets the ring and local detector\n
           \t\t\t\t number within the ring\n\n
           \t--getRing <gTN>:\t gets the ring from that telescope\n\n
           \t${RED}--exampleConf:\t\t creates an example configuration\n
           \t\t\t\t file named \"exampleConf.cor\"${NC}\n\n
           \t--getRTh <r1 t1 r2 t2>:\t Gets the theta relative angle\n
           \t\t\t\t between the detectors\n\n
           \nUsing the confFile ($(basename $0) <confFile> [options] [eRing | gTN])\n\n
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
           \t\t\t\t energy on the Si.\n\n\n
           \t--opp (gTN | ringId tN)\t gets the detectors of the\n
           \t\t\t\t residual particle in kinematic\n
           \t\t\t\t coincidence with the residual.\n\n
           \t-A:\t\t\t prints the angles of the particles.\n\n
           \nmore options comming eventually"
    echo -e $usage
}

function checkRingTagOrTel() {
    #Checking if it was a ring_tag or a telescope number, the
        myBoolTag=$(isTag $1)
        myBoolTel=$(isValidTel $1)
        if [ $myBoolTag = "true" ] || [ $myBoolTel = "true" ]
        then
            echo "true"
        else
            echo "false"
        fi
}

function argHandling() {
    if [ $# -eq 0 ] || [ "$1" == "-h" ]
    then
	      myHelp
	      exit 0
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
	      exit 0
    elif [ "$1" == "--getChimAddr" ]
    then
        shift
        checkGTN $@
        getChimAddr $@
	      exit 0
    elif [ "$1" == "--exampleConf" ]
    then
	      createExample
	      exit 0
    elif [ "$1" == "--getRing" ]
    then
        shift
        checkGTN $@
        getChimAddr $@ | cut -f1
	      exit 0
    elif [ "$1" == "--getRTh" ]
    then
	      shift
        python binCorComplementMain.py "--getRelTheta" $@
	      exit 0
    elif [ ! "$1" = "" ]
    then
        myBool=$(checkRingTagOrTel $@)
        if [ $myBool = "true" ]
        then
            myBoolTel=$(isValidTel $1)
            if [ $myBoolTel = "true" ]
            then
                getChimAddr $@
            else
                myRingIdx=$(getRingIdx $@)
                echo $myRingIdx
            fi
            exit 0
        fi
    fi

    #If it made if all the way here then the first argument was a
    #fileName
    if [ ! -e "$1" ]
    then
	      echo -e "${RED}error:\t${NC}filename $1 does not exist"
	      exit 0
    fi
    fileName="$1"
    source $fileName
    #Doing some basic parsing for the defined variables in the
    #configuration file, if anyone doesn't pass the test, then the
    #program does an error print and terminates inmediately
    checkIfPosFloat eLab $eLab
    checkIfPosFloat thickness $thickness
    checkIfPosFloat xRes $xRes

    #Add control for other variables here
    #Where in the target we think the reaction occurs, say halfway.
    halfThick=$(echo "$thickness/2.0" | bc -l )

    shift #shifting the arguments
    if [ "$1" == "-E" ]
    then
	      printCoinRings $@
	      exit 0
    elif [ "$1" == "--dE" ]
    then
	      printCoinRings $@
	      exit 0
    elif [ "$1" == "--opp" ]
    then
        getOpDet $@
	      exit 0
    elif [ "$1" == "--getOpR" ]
    then
        getOpRings $@
	      exit 0
    elif [ "$1" == "-A" ]
    then
	      printCoinRings $@
	      exit 0
    elif [ ! "$1" = "" ]
    then
        #Checking if it was a ring_tag or a telescope number, the
        #other cases will be catched by printCoinRings
        myBool=$(checkRingTagOrTel $@)
        if [ $myBool = "true" ]
        then
            printCoinRings $@
            exit 0
        fi
	      echo "error: option $1 not implemented. Maybe you mispelled."
	      exit 666
    else
	      printCoinRings
	      exit 0
    fi
}

function checkIfPosFloat() {
    varName=$1
    myNumber=$2

    #regular expression for positive floats
    re='^[0-9]+([.][0-9]+)?$'

    if [ "$myNumber" == "" ] || ! [[ $myNumber =~ $re ]]
    then
	echo -e  "${RED}error:\t${NC}$varName=$myNumber is not a positive float" >&2
	kill -s TERM $TOP_PID
    fi
}

function isTag() {
    thing=$1
    for rT in ${ring_tags[*]}
    do
        if [ "$rT"  = "$thing" ]
        then
            echo "true"
            return
        fi
    done
    echo "false"
}

function isInteger() {
    myNumber=$1
    re='^[0-9]+$'
    if ! [[ $myNumber =~ $re ]]
    then
        echo "false"
        return
    fi
    echo "true"
}

function isValidTel() {
    gTN=$1
    myBool=$(isInteger $gTN)
    if [ $myBool = "false" ]
    then
       echo false
       return
    fi
    if [ "$gTN" -lt 0 ] || [ "$gTN" -ge 1192 ]
    then
        echo "false"
    else
        echo "true"
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

function getMaxIdx(){
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

    denOp=""
    #overriding the Si density
    [ "$material" = "Si" ] && denOp="--density=2.368" #denOp="--density=2.265"
    finalE=$(isonav $ion --Elab=$ionE --material=$material --thickness=$thickness $denOp)
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
 baseHeadStr="#ejeRng\tresMin\tresMax"
 eHead=""

 myArgPos=1
 if [ "$1" == "-E" ]
 then
     let myArgPos=$myArgPos+1
     if [ "$2" == "--tof" ]
     then
         let myArgPos=$myArgPos+1
         eHead="\teTof\teFTof\trTof\trFTof"
     else
         eHead="\tejeE\tejeFE\tresE\tresFE"
     fi
 fi

 if [ "$1" == "--dE" ]
 then
     let myArgPos=$myArgPos+1
     if [ "$2" == "--depo" ]
     then
         let myArgPos=$myArgPos+1
         eHead="\tejeE\tejeDE\tresE\tresDE"
     else
         eHead="\tejeE\tejeFE\tresE\tresFE"
     fi
 fi

 [ "$1" == "-A" ] && let myArgPos=$myArgPos+1 && eHead="\tejeAng\tresMin\tresA\tresMax"
 headStr=$baseHeadStr$eHead

 let "maxIdx=${#thetaVals[*]}-1"

 eval "testArg=\${$myArgPos}"


 if [ ! $testArg = "" ]
 then
     myBoolTag=$(isTag $testArg)
     myBoolTel=$(isValidTel $testArg)
     if [ $myBoolTag = "true" ] || [ $myBoolTel = "true" ]
     then
         if [ $myBoolTel = "true" ]
         then
             myTag=$(getChimAddr $testArg | cut -f1)
         else
             myTag=$testArg
         fi
         myRingIdx=$(getRingIdx $myTag)
         printHeader
         echo -e "$headStr"
         getStr2Print $myRingIdx $@
         #Work more on this!!!!
         exit 0
     fi
     echo -e "${RED}Error: ${NC} $testArg is not a valid telescope or ring" >&2
     exit 333
 fi
 #i is the ring number index -1 of the ejectile
 printHeader
 echo -e "$headStr"
 for i in $( seq 0 $maxIdx )
 do
     getStr2Print $i $@
 done
}

function printHeader() {
    echo "###Reaction conditions###"
    echo "#$isoP $isoT => $isoE $isoR"
    echo "#xRes=$xRes, eLab=$eLab, material=$material, thickness=$thickness"
    echo "##########"
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
    if (( $(echo $ejectE == 0 | bc -l) ))
    then
        exit 96
    fi
    resE=$(echo $var | cut -d' ' -f 5)
    thetaRes=$(getAbs $thetaRes)
    thetaResMin=$(getAbs $thetaResMin)
    thetaResMax=$(getAbs $thetaResMax)

    realMin=$(awk -v a="$thetaResMin"\
                  -v b="$thetaResMax" 'BEGIN{print (a>b)?b:a}')

    realMax=$(awk -v a="$thetaResMin" -v\
                  b="$thetaResMax" 'BEGIN{print (a<b)?b:a}')

    minDIdx=$(getMinIxd $realMin)
    maxDIdx=$(getMaxIdx $realMax)
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
	    rFTof=$(getTof $isoR $resFE ${det_dist[$aveRIdx]})
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
    echo -e "thickSi\tN_\tdPhi\tdOmega"

    echo -e "#name\t\t\t[cm]\t[deg]\t[um]\t\t[deg]\t[msr]"
    for i in $( seq 0 34 )
    do
        strVar="${ring_tags[$i]}\t${firstTelL[$i]}\t${lastTelL[$i]}"
        strVar=$strVar"\t${det_dist[$i]}\t${thetaVals[$i]}"
        strVar=$strVar"\t${thick_Si[$i]}\t${teles_num[$i]}"
        strVar=$strVar"\t${delta_phi[$i]}"
        strVar=$strVar"\t${dOmega[$i]}"
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
        kill -s TERM $TOP_PID
    fi
    ringIdx=$(getRingIdx $1)
    if [ "$ringIdx" == "" ]
    then
        echo -e "${RED}Error${NC} ring $1 not found"
        kill -s TERM $TOP_PID
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
    echo "No ring_tag named $1 found" >&2
    kill -s TERM $TOP_PID
    exit 10
}

function checkSubTel() {
    rIdx=$1
    subTel=$2
    if [ "$subTel" == "" ]
    then
	echo -e "${RED}Error: ${NC} the tN is mandatory"
        kill -s TERM $TOP_PID
    fi

    if [ $subTel -ge ${teles_num[$rIdx]} ]\
	   || [ "$subTel" -lt 0 ]
    then
        echo "Not a valid telescope" >&2
        kill -s TERM $TOP_PID
        exit 4
    fi
}

function checkSubTelFromTag() {
    myTag=$1
    subTel=$2
    rIdx=$(getRingIdx $myTag)
    checkSubTel $rIdx $subTel
}

function someError() {
    if [ "$#" -ne 1 ]
    then
        echo -e "${RED}Error: ${NC} the gTN is mandatory">&2
        kill -s TERM $TOP_PID
        exit 5
    fi
}

function checkIfInRange() {
    gTN=$1
    if [ "$gTN" -lt 0 ] || [ "$gTN" -ge 1192 ]
    then
        errorStr="${RED}Error: ${NC} gTN (global
        telescope number)\n
        \thas to be an integer
        between 0 and 1191"
        echo -e $errorStr >&2
        kill -s TERM $TOP_PID
        exit 6
    fi
}

function checkGTN() {
    someError $@
    gTN=$1
    checkIfInRange $gTN
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

function getOpoInSameBase() {
    side1Num=$1
    totSideNum=$2
    let "side2Num=($side1Num+$totSideNum/2)%$totSideNum"
    echo $side2Num
}

function getOpoListInSameBase() {
    myListStr="$1"
    myList=($myListStr)
    baseNum="$2"
    myOpoList=()
    for i in ${myList[@]}
    do
	opo2i=$(getOpoInSameBase $i $baseNum)
	echo $i $opo2i
	myOpoList+=($opo2i)
    done
    echo "${myOpoList[@]}"
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

function getShift() {
    rTag=$1
    if [ $rTag == "S25" ]
    then
        echo "-5.625" # -11.25/2
    elif [ $rTag == "S26" ]
    then
        echo "-16.875" # -3/2*11.25
    else
        echo "0"
    fi
}

function getSidesInNewBase() {
    #Still needs the shift implementation!!!
    l=$1
    iBase=$2
    fBase=$3
    iShift=$4
    fShift=$5

    let "maxIdx=$fBase-1"

    DPhiA=$(echo "scale=3;360/$iBase" | bc)
    DPhiB=$(echo "scale=3;360/$fBase" | bc)

    initBaseAng1=$(echo "scale=3;$l*$DPhiA+($iShift)" | bc)
    initBaseAng2=$(echo "scale=3;($l+1)*$DPhiA+($iShift)" | bc)

    mySideArr=()
    for i in $(seq 0 $maxIdx)
    do
	finalBaseAng1=$(echo "scale=3;$i*$DPhiB+($fShift)" | bc)
	finalBaseAng2=$(echo "scale=3;($i+1)*$DPhiB+($fShift)" | bc)

	if [ $fBase -gt $iBase ]
	then
	    myCond1=$(isAngleInside  $finalBaseAng1 $initBaseAng1 $initBaseAng2)
	    myCond2=$(isAngleInside $finalBaseAng2 $initBaseAng1 $initBaseAng2)

	else
	    myCond1=$(isAngleInside $initBaseAng1 $finalBaseAng1 $finalBaseAng2)
	    myCond2=$(isAngleInside $initBaseAng2 $finalBaseAng1 $finalBaseAng2)
	fi

	if [ $myCond1 == "yes" ] || [ $myCond2 == "yes" ]
	then
	    mySideArr+=($i)
	fi
    done

    echo "${mySideArr[@]}"
}

function isAngleInRange() {
    range=$1
    angle1=$2
    angle2=$3

    diff=$(echo "scale=3;$angle1-($angle2)" | bc)

    myVal=$(echo "$diff % 360" | bc)
    #cheap way of doing absolute value
    myVal=${myVal#-}

    firstCond=$(echo "$myVal <= $range" | bc)
    mySecVal=$(echo "scale=3;360-$myVal" | bc)
    secCond=$(echo "$mySecVal <= $range" | bc)

    if [ $firstCond -eq 1 ] || [ $secCond -eq 1 ]
    then
	echo "yes"
    else
	echo "no"
    fi
}

function isAngleInside() {
    angle=$1
    initAng=$2
    finalAng=$3

    range=$(echo "$initAng-($finalAng)" | bc)
    #The absolute val trick
    range=${range#-}

    cond1=$(isAngleInRange $range $angle $initAng)
    cond2=$(isAngleInRange $range $angle $finalAng)

    if [ $cond1 == "yes" ] && [ $cond2 == "yes" ]
    then
	echo "yes"
    else
	echo "no"
    fi
}

function getOpRings (){
    shift
    rTag=$1
    ringIdx=$(getRingIdx $1)
    myIBase=${teles_num[$ringIdx]}
    myStr2Parse=$(getStr2Print $ringIdx)
    [ "$myStr2Parse" == "" ] &&\
        echo "No solution at ring $rTag" && exit 15
    initTag=$(echo -e "$myStr2Parse" | cut -f2)
    finTag=$(echo -e "$myStr2Parse" | cut -f3)

    iShift=$(getShift $rTag)

    initIdx=$(getRingIdx $initTag)
    finIdx=$(getRingIdx $finTag)
    for i in $(seq $initIdx $finIdx)
    do
        currentTag=${ring_tags[$i]}
        echo "$currentTag"
    done
}

function getOpDet (){
    shift
    isIntBool=$(isInteger $1)
    if [ $isIntBool = "true" ]
    then
	checkGTN $@
        chimAddr=$(getChimAddr $@)
	rTag=$(echo $chimAddr | cut -f1 -d" ")
	locTN=$(echo $chimAddr | cut -f2 -d" ")
    else
	rTag=$1
	locTN=$2
    fi
    ringIdx=$(getRingIdx $rTag)
    checkSubTelFromTag $rTag $locTN
    myIBase=${teles_num[$ringIdx]}
    myStr2Parse=$(getStr2Print $ringIdx)
    [ "$myStr2Parse" == "" ] &&\
        echo "No solution at ring $rTag" && exit 15
    initTag=$(echo -e "$myStr2Parse" | cut -f2)
    finTag=$(echo -e "$myStr2Parse" | cut -f3)

    iShift=$(getShift $rTag)

    initIdx=$(getRingIdx $initTag)
    finIdx=$(getRingIdx $finTag)

    for i in $(seq $initIdx $finIdx)
    do
        currentTag=${ring_tags[$i]}
        myFBase=${teles_num[$i]}
        fShift=$(getShift $currentTag)
        newBLStr=$(getSidesInNewBase\
                       $locTN $myIBase $myFBase\
                       $iShift $fShift)
        newBL=("$newBLStr")
        opValL=()
        for j in ${newBL[@]}
        do
            opVal=$(getOpoInSameBase $j $myFBase)
            opValL+=($opVal)
        done

	if [ $isIntBool = "true" ]
	then
	    for e in ${opValL[@]}
	    do
		getTNum $currentTag $e
	    done
	else
            echo -e "$currentTag\t${opValL[@]}"
	fi
    done
}


function createExample() {
    fileName="exampleConf.cor"
    echo "Creating example configuration in $fileName"
    # exampleConf="
    echo "#Remember not to leave spaces near the equal sign, IT IS BaSH!!">$fileName
    echo "" >>$fileName
    echo "eLab=64.0 #in MeV" >>$fileName
    echo "# Make sure reactions are valid!!!" >>$fileName
    echo "isoP=4He #The projectile" >>$fileName
    echo "isoT=12C #The target" >> $fileName
    echo "" >>$fileName
    echo "isoE=4He #The ejectile" >> $fileName
    echo "isoR=12C #The residual" >> $fileName
    echo "" >>$fileName
    echo "material=C #For energy loss in the target" >> $fileName
    echo "#Use isonav --listMaterials to see which ones are available." >>$fileName
    echo "" >>$fileName
    echo "thickness=0.44 #in microns, for the calculations we use half of this" >>$fileName
    echo "" >>$fileName
    echo "xRes=9.64 #Excitation of the residual particle." >>$fileName

    # echo -n -e $exampleConf > $fileName
    echo -e "\nNow run\n $ ./alchemist.sh $fileName\nto see the output"
}

argHandling $@
