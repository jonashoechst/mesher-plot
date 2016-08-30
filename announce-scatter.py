#!/usr/bin/env python
import sys, os, csv, re, collections, numpy
from CSVObject import *
from plotter import *

import matplotlib.pyplot as plt
from pprint import pprint

name = os.path.basename(os.path.normpath(sys.argv[1]))

print("Experiment name: "+name)

mesher_root = os.path.join(sys.argv[1], "mesher/")
logs = []

for root, dirs, files in os.walk(mesher_root):
    for filename in files:
        logfile = open(root + filename)
        logs.append([l.split("\n")[0] for l in logfile.readlines()])
        logfile.close()

# pprint(logs)
ids = []
announces = []

for log in logs:
    ids.append(log[1].split(" ")[-1])
    tmp = []
    for line in log:
        if "ANNOUNCE" in line and line.split(",")[2] == ids[-1]:
            tmp.append(float(line.split(",")[0])/1000)
    announces.append(tmp)

start = min([min(timestamps) for timestamps in announces])
end = max([max(timestamps) for timestamps in announces])
# print("Start: {}; end: {}".format(start, end))

fig = plt.figure()
ax1 = fig.add_subplot(111)

for i in range(len(announces)):
    # announces[i] = [announce-start for announce in announces[i]]
    plt.scatter([announce-start for announce in announces[i]], [i] * len(announces[i]), marker="+")


ax1.set_ylim([-1, len(announces)])
ax1.set_xlim([0, end-start])
plt.savefig(os.path.basename(__file__).split(".")[0]+"-"+name+".pdf")
print("Plot is done.")
