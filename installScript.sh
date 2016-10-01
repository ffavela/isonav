#!/bin/bash
#Run the script as with sudo
RED='\033[0;31m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color
databaseName=data1p4p5
zipFile=$databaseName.zip
ggURLVal='https://drive.google.com/uc?export=download'
dataID='0B2znJ2THUGDiWU5BYkFIVUdkdFk'
dbURL="https://drive.google.com/open?id=0B2znJ2THUGDiWU5BYkFIVUdkdFk"

function downloadDatabase(){
    ggID=$dataID
    ggURL=$ggURLVal
    curl -LOJb /tmp/gcokie "${ggURL}&id=${ggID}"
}

if [ "$1" = "--uninstall" ]
then
    if [ -L /usr/local/bin/isonav ] || [ -f /usr/local/bin/isonav ]
    then 
	echo "Removing the isonav symlink"
	rm /usr/local/bin/isonav
    fi

    if [ -d /usr/share/isonav ]
    then
    echo "Removing the isonav files"
    rm -r /usr/share/isonav
    fi
    echo "isonav uninstall complete"
    exit 0
fi

if [ -d /usr/share/isonav ]
then
    echo "File /usr/share/isonav exists"
    echo "Removing it for new installation"
    rm -r /usr/share/isonav
fi

python -c "import docopt"
if [ $? -eq 1  ]
then
    printf "${RED}Error; install docopt first. Aborting${NC}\n"
    echo "For ubuntu execute"
    echo "sudo apt-get install python-docopt"
    echo "For arch:"
    echo "sudo pacman -S python-docopt"
    echo "For linux in general:"
    echo "pip install docopt==0.6.1"
    exit 1
fi

[ ! -d $databaseName ]&&[ -e $zipFile ]&& unzip $zipFile

[ -e $zipFile ]&&[ -d $databaseName ]&& echo "rm $zipFile to avoid errors"&&rm $zipFile

if [ ! -d $databaseName ]
then
    printf "${BLUE}Trying to download database from:${NC}\n"
    echo "$dbURL"
    downloadDatabase
    exitVal=$?
    if [ $exitVal -ne 0 ]
    then
	printf "${RED}Error downloading database from:${NC}\n"
	echo "$dbURL"
	printf "${BLUE}Do you have internet connection?:${NC}\n"
	printf "${GREEN}Perhaps google drive is blocked in${NC}\n"
	printf "${GREEN}your area or it is down.${NC}\n"
	printf "${BLUE}Please try again or download it manually from:${NC}\n"
	echo "$dbURL"
	echo "and uncompress it in this directory."
	exit 2
    fi
    unzip $zipFile && echo "removing $zipFile" && rm $zipFile
fi

mkdir /usr/share/isonav
[ $? -ne 0 ] && echo "Error; try running with sudo" && exit 3
chmod +x isonav.py
cp -r $databaseName /usr/share/isonav
cp isonav.py /usr/share/isonav
cp isoParser.py /usr/share/isonav
cp isonavBase.py /usr/share/isonav
cp loadingStuff.py /usr/share/isonav
cp enxParser.py /usr/share/isonav
cp outputFunctions.py /usr/share/isonav
cp argumentHandling.py /usr/share/isonav

chmod -R o=rx /usr/share/isonav

if [ -f /usr/local/bin/isonav ] || [ -L /usr/local/bin/isonav ]
then
    echo "/usr/local/bin/isonav exists"
    echo "Removing it for reinstall"
    rm /usr/local/bin/isonav
fi

ln -s /usr/share/isonav/isonav.py /usr/local/bin/isonav

echo "Installation complete"
echo "Run isonav to see a list of options"

exit 0
