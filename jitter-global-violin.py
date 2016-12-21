#!/usr/bin/env python
import sys, os, csv, re, collections, numpy
from CSVObject import *
from plotter import *
from mesherhelp import *

import matplotlib.pyplot as plt
from pprint import pprint

init_time_s = 40

paths = sys.argv[1:]
names = determineNames(paths)

print("Experiment names: "+", ".join(names))

experiments = [sorted(flatten(getAnnouncesFromPath(path, offset=init_time_s))) for path in paths]
experimtens_dist = [[b-a for a, b in zip(exp[:-1], exp[1:])] for exp in experiments]

fig = plt.figure(1, figsize=(8, 3))
violinplot(fig, names, experimtens_dist)

ax1 = fig.add_subplot(111)
ax1.set_ylabel("announce gaps (s)")

fig.tight_layout()
plt.savefig(os.path.basename(__file__).split(".")[0]+".pdf")
print("Plot is done.\n")
