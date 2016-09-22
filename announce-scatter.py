#!/usr/bin/env python
import sys, os, csv, re, collections, numpy, random
from CSVObject import *
from plotter import *
from mesherhelp import *

import matplotlib.pyplot as plt
from pprint import pprint
random.seed(1)
scatter_jitter = 0.8

name = os.path.basename(os.path.normpath(sys.argv[1]))

print("Experiment name: "+name)

announces = getAnnouncesFromPath(sys.argv[1])
random.shuffle(announces)
end = max2d(announces)
x_values, aps = computeAnnouncesPerSecond(announces)

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.set_xlabel("time (s)")
ax1.set_ylabel("node announces", color="blue")

for i in range(len(announces)):
    # y_values = [i] * len(announces[i])
    y_values = [i + 1 - (scatter_jitter/2) + scatter_jitter * random.random() for _ in range(len(announces[i]))]
    plt.scatter(announces[i], y_values, marker="+", linewidth=0.2, color="blue")

ax2 = ax1.twinx()
ax2.set_ylabel("announces / second", color="orange", alpha=0.7)

weightedAvgLine(ax2, aps, linewidth=1.5, alpha=0.7, color="orange", weights=range(20))
# variableLine(ax2, x_values, aps, linewidth=1.5, alpha=0.7, color="orange")

ax1.set_ylim([0, len(announces)+1])
ax1.set_xlim([0, end])
ax2.set_ylim([0, max(aps)])
plt.savefig(os.path.basename(__file__).split(".")[0]+"-"+name+".pdf")
print("Plot is done.\n")
