#!/usr/bin/env python
import sys, os, csv, re, collections, numpy
from CSVObject import *
from plotter import *
from mesherhelp import *

import matplotlib.pyplot as plt
from pprint import pprint
from scipy.stats import gaussian_kde

paths = sys.argv[1:]
names = determineNames(paths)

print("Experiment names: "+", ".join(names))
experiments = [CSVObject(path+"/measurement.csv") for path in paths]


fig = plt.figure(1)
violinplot(fig, names, [ex.get_values("power") for ex in experiments])

ax1 = fig.add_subplot(111)
ax1.set_ylabel("time interval (s)")

fig.tight_layout()
ax1.set_ylim((1.44, 1.8))
plt.savefig(os.path.basename(__file__).split(".")[0]+".pdf")
print("Plot is done.\n")

sys.exit(0)