#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <base of log paths>"
    exit
fi

for i in $1/*/ ; do
    ./announce-scatter.py $i &
    ./load-netmon.py $i &
done

wait

mkdir -p pdfs
mv *.pdf pdfs

echo
echo "Plotting jitter groups"

jitter_groups="n010 n025 n050 n100 maxfirst minfirst rand_and_sweet random static step_and_rand step unsteady"

for g in $jitter_groups; do
    ./jitter-global.py $1/*$g*/
    mv jitter-global.pdf pdfs/jitter-global-$g.pdf
done

echo "Done"