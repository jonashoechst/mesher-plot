#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <base of log paths>"
    exit
fi

pdf_path=`basename $1`
echo "Saving pdfs to $pdf_path"
mkdir -p $pdf_path

echo "Plotting announce groups"

announce_groups="002 005 010 025 050 100 200 MaxFirst- MinFirst- Random- RandomSweet- Static- Step- StepRand- Unsteady-"

for g in $announce_groups; do
    ./compare-announces-split.py $1/*$g*/
    mv compare-announces-split.pdf $pdf_path/compare-announces-$g.pdf
done



echo "Done"