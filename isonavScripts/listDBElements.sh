#!/bin/bash

#Prints out the name of each element, along with proton # and symbol

for n in $(seq 0 118)
do
    s=$(isonav $n -s)
    name=$(isonav $s --name)
    echo -e "$n\t$s\t$name"
done

exit 0
