#!/bin/bash
#Simply list the elements of the database
#With proton number and symbol

for n in $(seq 0 118)
do
    s=$(isonav $n -s)
    echo $n $s
done

exit 0
