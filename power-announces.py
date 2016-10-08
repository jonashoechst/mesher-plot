#!/usr/bin/env python
import sys, os, csv, re, collections, numpy
from CSVObject import *
from plotter import *
from mesherhelp import *

import matplotlib.pyplot as plt
from pprint import pprint

def getSutAnnouncesFromPath(path):
    mesher_root = path
    logs = []

    for root, dirs, files in os.walk(mesher_root):
        for filename in files:
            if not ("sut" in filename or "10.0.10.2" in filename): continue
            logfile = open(root + filename)
            logs.append([l.split("\n")[0] for l in logfile.readlines()])
            logfile.close()

    ids = []
    announces = []

    for log in logs:
        ids.append(log[0].split(" ")[-1])
        
        tmp = []
        for logline in log:
            if "ANNOUNCE" in logline and logline.split(",")[2] == ids[-1]:
                tmp.append(float(logline.split(",")[0])/1000)
        announces.append(tmp)

    start = 0# min2d(announces) + offset

    return announces

path = sys.argv[1]
name = "-".join(os.path.basename(os.path.normpath(path)).split("-")[:2])

print("Experiment name: "+name)
experiment = CSVObject(path+"/measurement.csv")
announces = getSutAnnouncesFromPath(path)
announces_sut = announces[0]

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.set_xlabel("time (s)")
ax1.set_ylabel("power consumption (W)")

color = colors[0]

start = experiment.get_values("timestamp_ms")[0]
end = experiment.get_values("timestamp_ms")[-1]

x = [float(v-start) for v in experiment.get_values("timestamp_ms")]
data = experiment.get_values("power")

factorAvgLine(ax1, data, x=x, linewidth=1, alpha=0.7, color=color, factor=1)

for a in announces_sut:
    event(fig, a-start, "")


fig.tight_layout()
# ax1.set_ylim([0.4, 105])
ax1.set_xlim([0, end-start])
plt.savefig(os.path.basename(__file__).split(".")[0]+"-"+name+".pdf")
print("Plot is done.\n")