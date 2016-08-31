#!/bin/bash

function plot {
    echo "Processing $1"
    ./announce-scatter.py $1
    #./load-netmon.py $1
    #./jitter-global.py $1
    #./jitter-local.py $1    
}

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <base of log paths>"
    exit
fi

for i in $1/*/ ; do
 plot $i &
done

wait

mkdir pdfs
mv *.pdf pdfs
echo "Done"
