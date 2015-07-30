#!/bin/bash
#Run the script as with sudo
RED='\033[0;31m'
NC='\033[0m' # No Color

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
    echo "For linux in general:"
    echo "pip install docopt==0.6.1"
    exit 1
fi

if [ ! -d data ]
then
    printf "${RED}Error; no data directory${NC}"
    echo "Download it from:"
    echo "https://mega.co.nz/#!3N9D1ZIR!5YrwRoVG24VPN7FlOI_jUX_LFvRT8VErUMTP434k-V0"
    echo "And uncompress it inside the repo's directory"
    exit 2
fi

mkdir /usr/share/isonav
[ $? -ne 0 ] && echo "Error; try running with sudo" && exit 3
chmod +x isonav.py
cp -r data /usr/share/isonav
cp isonav.py /usr/share/isonav
cp isoParser.py /usr/share/isonav
cp isonavBase.py /usr/share/isonav
cp loadingStuff.py /usr/share/isonav
cp enxParser.py /usr/share/isonav
cp outputFunctions.py /usr/share/isonav
cp argumentHandling.py /usr/share/isonav

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
