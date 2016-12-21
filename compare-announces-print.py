#!/usr/bin/env python
import sys, os, csv, re, collections, numpy
from CSVObject import *
from plotter import *
from mesherhelp import *

from pprint import pprint

paths = sys.argv[1:]
names = determineNames(paths)

print("Experiment names: "+", ".join(names))
experiments = [getAnnouncesFromPath(path, subpath="", offset=50) for path in paths]
apses = [computeAnnouncesPerSecond(experiment)[1] for experiment in experiments]

counts = [sum([len(node_ann) for node_ann in exp]) for exp in experiments]

for i in range(len(names)):
    print(names[i])

for i in range(len(names)):
    print(counts[i])
