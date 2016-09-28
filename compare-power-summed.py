#!/usr/bin/env python
import sys, os, csv, re, collections, numpy
from CSVObject import *
from plotter import *
from mesherhelp import *

import matplotlib.pyplot as plt
from pprint import pprint

colors = ["firebrick", "sienna", "orange", "gold", "olive", "sage", "mediumseagreen", "teal", "dodgerblue", "darkviolet", "deeppink"]

paths = sys.argv[1:]
names = ["-".join(os.path.basename(os.path.normpath(path)).split("-")[0:2]) for path in paths]

print("Experiment names: "+", ".join(names))
experiments = [CSVObject(path+"/measurement.csv") for path in paths]
pprint(experiments)

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.set_xlabel("time (s)")
ax1.set_ylabel("energy consumtion (Ws)")

import matplotlib.patches as mpatches
patches = []

end = 0

for i in range(len(names)):
    color = colors[i % len(colors)]
    
    start = experiments[i].get_values("timestamp_ms")[0] 
    x = [v-start for v in experiments[i].get_values("timestamp_ms")]
    data = experiments[i].get_values("power")
    print("avg(power {}) = {}".format(names[i], avg(data)))
    
    avg_power = 1.37910095889 #min(data)
    # Die werte werden in Watt gemessen. Um die Energie menge zu kalkulieren, muss durch das Messintervall geteilt werden (5 messungen / sekunde)
    summed = [sum([(val-avg_power)/5 for val in data[:j+1]]) for j in range(len(data))]
    if end == 0: end = x[-1]
    else: end = min(end, x[-1])
    
    factorAvgLine(ax1, summed, x=x, linewidth=1, alpha=0.7, color=color, factor=1)
    patches.append(mpatches.Patch(color=color, label=names[i], alpha=0.7))

ax1.legend(patches, names, prop={'size': 9}, loc=4)
fig.tight_layout()
# ax1.set_ylim([0.4, 105])
ax1.set_xlim([0, end])
plt.savefig(os.path.basename(__file__).split(".")[0]+".pdf")
print("Plot is done.\n")