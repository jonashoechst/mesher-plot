#!/usr/bin/env python
import sys, os, csv, re, collections, numpy
from CSVObject import *
from plotter import *
from mesherhelp import *

import matplotlib.pyplot as plt
from pprint import pprint
from scipy.stats import gaussian_kde

colors = ["firebrick", "sienna", "orange", "gold", "olive", "sage", "mediumseagreen", "teal", "dodgerblue", "darkviolet", "deeppink"]

init_time_s = 40

paths = sys.argv[1:]
names = ["-".join(os.path.basename(os.path.normpath(path)).split("-")[:2]) for path in paths]

print("Experiment names: "+", ".join(names))

experiments = [sorted(flatten(getAnnouncesFromPath(path, offset=init_time_s))) for path in paths]
experimtens_dist = [[b-a for a, b in zip(exp[:-1], exp[1:])] for exp in experiments]

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.set_xlabel("announce gap (s)")
ax1.set_ylabel("density")

import matplotlib.patches as mpatches
patches = []
xlim = [0, 5]

for i in range(len(names)):
    color = colors[i % len(colors)]

    density = gaussian_kde(experimtens_dist[i])
    xs = numpy.linspace(xlim[0], xlim[1],1000)
    density.covariance_factor = lambda : 0.2
    density._compute_covariance()
    
    factorAvgLine(ax1, density(xs), x=xs, linewidth=1, alpha=0.7, color=color, factor=1)
    patches.append(mpatches.Patch(color=color, label=names[i], alpha=0.7))

# ax1.set_yscale("log", nonposx='clip')
ax1.legend(patches, names, prop={'size': 9}, loc=1)
fig.tight_layout()
ax1.set_xlim(xlim)
plt.savefig(os.path.basename(__file__).split(".")[0]+".pdf")
print("Plot is done.\n")