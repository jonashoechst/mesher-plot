#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <base of log paths>"
    exit
fi

pdf_path=`basename $1`
echo "Saving pdfs to $pdf_path"

mkdir -p $pdf_path


for i in $1/*/ ; do
    ./power-announces.py $i &
    # ./load-netmon.py $i &
done

wait

mv *.pdf $pdf_path

echo
echo "Plotting jitter and announce groups"

jitter_groups="001 002 005 009 MaxFirst- MinFirst- Random- RandomSweet- Static- Static01- Static05- Step- StepRand- Unsteady-"

for g in $jitter_groups; do
    ./compare-power-summed.py $1/*$g*/ &
    ./compare-power-violin.py $1/*$g*/ &
    ./compare-power-histo.py $1/*$g*/ &
    ./compare-power.py $1/*$g*/ &
    wait
    mv compare-power-summed.pdf $pdf_path/compare-power-summed-$g.pdf
    mv compare-power-violin.pdf $pdf_path/compare-power-violin-$g.pdf
    mv compare-power-histo.pdf $pdf_path/compare-power-histo-$g.pdf
    mv compare-power.pdf $pdf_path/compare-power-$g.pdf
done


echo "Done"