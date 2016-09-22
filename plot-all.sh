#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <base of log paths>"
    exit
fi

pdf_path=`basename $1`
echo "Saving pdfs to $pdf_path"

for i in $1/*/ ; do
    ./announce-scatter.py $i &
    ./load-netmon.py $i &
done

wait

mkdir -p $pdf_path
mv *.pdf $pdf_path

echo
echo "Plotting jitter groups"

jitter_groups="002 005 010 025 050 100 200 MaxFirst- MinFirst- Random- RandomSweet- Static- Step- StepRand- Unsteady-"

for g in $jitter_groups; do
    ./jitter-global.py $1/*$g*/
    mv jitter-global.pdf $pdf_path/jitter-global-$g.pdf
done

echo
echo "Plotting announce groups"

announce_groups=$jitter_groups

for g in $announce_groups; do
    ./compare-announces.py $1/*$g*/
    mv compare-announces.pdf $pdf_path/compare-announces-$g.pdf
done



echo "Done"