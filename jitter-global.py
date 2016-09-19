#!/usr/bin/env python
import sys, os, csv, re, collections, numpy
from CSVObject import *
from plotter import *
from mesherhelp import *

import matplotlib.pyplot as plt
from pprint import pprint

init_time_s = 20

paths = sys.argv[1:]
names = ["-".join(os.path.basename(os.path.normpath(path)).split("-")[:2]) for path in paths]

print("Experiment names: "+", ".join(names))

experiments = [sorted(flatten(getAnnouncesFromPath(path, offset=init_time_s))) for path in paths]
experimtens_dist = [[b-a for a, b in zip(exp[:-1], exp[1:])] for exp in experiments]


# fig = plt.figure(1, figsize=(10+len(names)/5, 10))
fig = plt.figure(1)
boxplot(fig, names, experimtens_dist)

ax1 = fig.add_subplot(111)
ax1.set_ylabel("time interval (s)")

# ax1.set_ylim([-0.01, 0.5])
# ax1.set_xlim([0, end-start])
fig.tight_layout()
plt.savefig(os.path.basename(__file__).split(".")[0]+".pdf")
print("Plot is done.\n")
