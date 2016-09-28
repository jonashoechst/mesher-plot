#!/usr/bin/env python
import sys, os, csv, re, collections, numpy
from CSVObject import *
from plotter import *
from mesherhelp import *

import matplotlib.pyplot as plt
from pprint import pprint
from scipy.stats import gaussian_kde

colors = ["firebrick", "sienna", "orange", "gold", "olive", "sage", "mediumseagreen", "teal", "dodgerblue", "darkviolet", "deeppink"]

paths = sys.argv[1:]
names = ["-".join(os.path.basename(os.path.normpath(path)).split("-")[0:2]) for path in paths]

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





pprint(experiments)

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.set_xlabel("power consumption (W)")
ax1.set_ylabel("density")

import matplotlib.patches as mpatches
patches = []
xlim = [1.35, 2]
end = 0

for i in range(len(names)):
    color = colors[i % len(colors)]
    
    start = experiments[i].get_values("timestamp_ms")[0] 
    x = [float(v-start)/1000 for v in experiments[i].get_values("timestamp_ms")]
    data = experiments[i].get_values("power")

    density = gaussian_kde(data)
    xs = numpy.linspace(xlim[0], xlim[1],1000)
    density.covariance_factor = lambda : 0.05
    density._compute_covariance()
    
    factorAvgLine(ax1, density(xs), x=xs, linewidth=1, alpha=0.7, color=color, factor=1)
    patches.append(mpatches.Patch(color=color, label=names[i], alpha=0.7))

# ax1.set_yscale("log", nonposx='clip')
ax1.legend(patches, names, prop={'size': 9}, loc=1)
fig.tight_layout()
ax1.set_xlim(xlim)
plt.savefig(os.path.basename(__file__).split(".")[0]+".pdf")
print("Plot is done.\n")