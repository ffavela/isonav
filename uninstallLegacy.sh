#!/bin/bash
#Run the script as with sudo
RED='\033[0;31m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

if [ -L /usr/local/bin/isonav ] || [ -f /usr/local/bin/isonav ]
then
    echo "Removing the isonav symlink"
    rm /usr/local/bin/isonav
fi

if [ -d /usr/share/isonav ]
then
    echo "Removing the isonav files"
    rm -r /usr/share/isonav
    echo "isonav legacy uninstall complete"
    exit 0
fi

echo "No legacy install isonav present"
exit 1
