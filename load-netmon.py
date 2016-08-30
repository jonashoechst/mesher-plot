#!/usr/bin/env python
import sys, os, csv, re, collections, numpy
from CSVObject import *
from plotter import *

BIT = 8.0
KBIT = BIT/1024.0
MBIT = KBIT/1024.0
GBIT = MBIT/1024.0

name = os.path.basename(os.path.normpath(sys.argv[1]))
print("\nExperiment name: "+name)

netmon = CSVObject(os.path.join(sys.argv[1], "netmon-hub.csv"))

### TCP / UDP
ip = netmon.get_values_normalized("size_ip", netmon.rows[0][0]/1000, netmon.rows[-1][0]/1000, value_factor=MBIT)

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.set_xlabel("time (s)")

# configure first plot
ax1.set_ylabel("transfer rate (Mbit/s)", color="#00AA00", alpha=0.5)
stackedArea(ax1, [ip], basecolor="#00AA%0.2X", linewidth=0.0)

plt.axis('tight')
ax2 = ax1.twinx()

ax1.set_ylim([0, 0.1])
ax2.set_ylim([0, 0.1])
plt.savefig(os.path.basename(__file__).split(".")[0]+"-"+name+".pdf")
print("Plot is done.")
