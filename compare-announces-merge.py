#!/usr/bin/env python
import sys, os, csv, re, collections, numpy
from CSVObject import *
from plotter import *
from mesherhelp import *

import matplotlib.pyplot as plt
from pprint import pprint

colors = ["firebrick", "sienna", "orange", "gold", "olive", "sage", "mediumseagreen", "teal", "dodgerblue", "darkviolet", "deeppink"]
event_time = 150

paths = sys.argv[1:]
names = ["-".join(os.path.basename(os.path.normpath(path)).split("-")[:2]) for path in paths]

print("Experiment names: "+", ".join(names))
experiments = []
for path in paths:
    experiment = getAnnouncesFromPath(path)
    experiment_filtered = []
    for i in range(len(experiment)):
        node_announces = experiment[i]
        if i < len(experiment) / 2:
            experiment_filtered.append(node_announces)
        else:
            experiment_filtered.append([ann for ann in node_announces if ann > 150])
    experiments.append(experiment_filtered)

apses = [computeAnnouncesPerSecond(experiment)[1] for experiment in experiments]

# minimum der maximalen experiment zeiten
end = min([max2d(experiment) for experiment in experiments])

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.set_xlabel("time (s)")
ax1.set_ylabel("announces / second")

import matplotlib.patches as mpatches
patches = []
for i in range(len(names)):
    color = colors[i % len(colors)]
    line(ax1, apses[i], linewidth=1, alpha=0.7, color=color)
    patches.append(mpatches.Patch(color=color, label=names[i], alpha=0.7))
    i += 1

ax1.legend(patches, names, prop={'size': 10})
event(fig, event_time, "merge")

# ax1.set_ylim([-1, len(announces)])
ax1.set_xlim([0, end])
fig.tight_layout()
plt.savefig(os.path.basename(__file__).split(".")[0]+".pdf")
print("Plot is done.\n")
