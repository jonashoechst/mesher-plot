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

jitter_groups="002 005 010 025 050 100 200 maxfirst minfirst rand_and_sweet random static step_and_rand step- unsteady"

for g in $jitter_groups; do
    ./jitter-global.py $1/*$g*/
    mv jitter-global.pdf pdfs/jitter-global-$g.pdf
done

echo
echo "Plotting announce groups"

announce_groups=$jitter_groups

for g in $announce_groups; do
    ./compare-announces.py $1/*$g*/
    mv compare-announces.pdf pdfs/compare-announces-$g.pdf
done



echo "Done"