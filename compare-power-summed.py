#!/usr/bin/env python
import sys, os, csv, re, collections, numpy
from CSVObject import *
from plotter import *
from mesherhelp import *

import matplotlib.pyplot as plt
from pprint import pprint

paths = sys.argv[1:]
names = determineNames(paths)

print("Experiment names: "+", ".join(names))
experiments = [CSVObject(path+"/measurement.csv") for path in paths]

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.set_xlabel("time (s)")
ax1.set_ylabel("energy consumption (Wh)")

import matplotlib.patches as mpatches
patches = []

global_end = 0

for i in range(len(names)):
    color = colors[i % len(colors)]
    
    start = experiments[i].get_values("timestamp_ms")[0]
    end = experiments[i].get_values("timestamp_ms")[-1] 
    x = [v-start for v in experiments[i].get_values("timestamp_ms")]
    data = experiments[i].get_values("power")
    
    avg_power = 1.37910095889
    # avg_power *= 0

    duration = end - start
    frequency = duration / len(x)
    
    summed = [sum([v-avg_power for v in data[:j+1]]) / (3600 / frequency) for j in range(len(x))]
    if global_end == 0: end = x[-1]
    else: global_end = max(end, x[-1])
    
    factorAvgLine(ax1, summed, x=x, linewidth=1, alpha=0.7, color=color, factor=1)
    patches.append(mpatches.Patch(color=color, label=names[i], alpha=0.7))

ax1.legend(patches, names, prop={'size': 9}, loc=2)
fig.tight_layout()
# ax1.set_ylim([0.4, 105])
ax1.set_xlim([0, end])
plt.savefig(os.path.basename(__file__).split(".")[0]+".pdf")
print("Plot is done.\n")