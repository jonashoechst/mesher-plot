#!/usr/bin/env python
import sys, os, csv, re, collections, numpy
from CSVObject import *
from plotter import *
from mesherhelp import *

import matplotlib.pyplot as plt
from pprint import pprint

colors = ["firebrick", "sienna", "orange", "gold", "olive", "sage", "mediumseagreen", "teal", "dodgerblue", "darkviolet", "deeppink"]

paths = sys.argv[1:]
names = ["-".join(os.path.basename(os.path.normpath(path)).split("-")[1:2]) for path in paths]

print("Experiment names: "+", ".join(names))
experiments = [getAnnouncesFromPath(path) for path in paths]
apses = [computeAnnouncesPerSecond(experiment)[1] for experiment in experiments]

# minimum der maximalen experiment zeiten
end = min([max2d(experiment) for experiment in experiments])

fig = plt.figure(figsize=(4,3))
ax1 = fig.add_subplot(111)
ax1.set_xlabel("time (s)")
ax1.set_ylabel("announces / second")

import matplotlib.patches as mpatches
patches = []
for i in range(len(names)):
    color = colors[i % len(colors)]
    # line(ax1, apses[i], linewidth=1, alpha=0.7, color=color)
    # avgLine(ax1, apses[i], linewidth=1, alpha=0.7, color=color, avg=20)
    weightedAvgLine(ax1, apses[i], linewidth=1, alpha=0.7, color=color, weights=range(20))
    patches.append(mpatches.Patch(color=color, label=names[i], alpha=0.7))
    i += 1

ax1.legend(patches, names, prop={'size': 9})

ax1.set_yscale("log", nonposx='clip')
ax1.set_ylim([0.4, 105])
ax1.set_xlim([0, end])
fig.tight_layout()
plt.savefig(os.path.basename(__file__).split(".")[0]+".pdf")
print("Plot is done.\n")