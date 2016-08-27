#!/usr/bin/env python
import sys, os, csv, re, collections, numpy
from CSVObject import *
from plotter import *

name = os.path.basename(os.path.normpath(sys.argv[1]))
print("\nExperiment name: "+name)

netmons = csvs_from_folder(os.path.join(sys.argv[1], "netmon/"))

print("Read "+str(len(netmons))+" netmon files.")

MBIT = 8/(1024.0**2) # bytes * 8 / 1024^2

### TCP / UDP
tcp = [netmon.get_values_normalized("size_pkt", netmons[0].rows[0][0]/1000, netmons[0].rows[-1][0]/1000, value_factor=MBIT) for netmon in netmons]
udp = [netmon.get_values_normalized("size_pkt", netmons[0].rows[0][0]/1000, netmons[0].rows[-1][0]/1000, value_factor=MBIT) for netmon in netmons]
# traf = [netmon.get_values_normalized("size_pkt", timestamp_start, timestamp_end, value_factor=MBIT) for netmon in netmons]

# sum of serval_udp / tcp sizes
traf = [None] * len(tcp)
for i in range(len(tcp)):
    traf[i] = [x + y for x, y in zip(tcp[i], udp[i])]

# get max tcp_values at given time t
tcp_max = []
for t in range(0, len(tcp[0])):
    tcp_max.append(max([tcp_values[t] for tcp_values in tcp]))

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.set_xlabel("time (s)")

# configure first plot
ax1.set_ylabel("transfer rate (Mbit/s)", color="#00AA00", alpha=0.5)
stackedArea(ax1, traf, basecolor="#00AA%0.2X", linewidth=0.0)

plt.axis('tight')
ax2 = ax1.twinx()

ax1.set_ylim([0, 1])
ax2.set_ylim([0, 1])
plt.savefig(os.path.basename(__file__).split(".")[0]+"-"+name+".pdf")
print("Plot is done.")
