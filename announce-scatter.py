#!/usr/bin/env python
import sys, os, csv, re, collections, numpy
from CSVObject import *
from plotter import *
from mesherhelp import *

import matplotlib.pyplot as plt
from pprint import pprint

name = os.path.basename(os.path.normpath(sys.argv[1]))

print("Experiment name: "+name)

announces = getAnnouncesFromPath(sys.argv[1])
end = max2d(announces)
x_values, aps = computeAnnouncesPerSecond(announces)

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.set_xlabel("time (s)")
ax1.set_ylabel("node_announce", color="blue")

for i in range(len(announces)):
    plt.scatter(announces[i], [i] * len(announces[i]), marker="+", linewidth=0.2, color="blue")

ax2 = ax1.twinx()
ax2.set_ylabel("announces / second", color="orange", alpha=0.7)
variableLine(ax2, x_values, aps, linewidth=1.5, alpha=0.7, color="orange")

ax1.set_ylim([-1, len(announces)])
ax1.set_xlim([0, end])
plt.savefig(os.path.basename(__file__).split(".")[0]+"-"+name+".pdf")
print("Plot is done.")
