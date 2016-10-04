import os

colors = ["firebrick", "sienna", "orange", "gold", "olive", "sage", "mediumseagreen", "teal", "dodgerblue", "darkviolet", "deeppink"]

def getAnnouncesFromPath(path, offset=0, subpath="mesher/"):
    mesher_root = os.path.join(path, subpath)
    logs = []

    for root, dirs, files in os.walk(mesher_root):
        for filename in files:
            logfile = open(root + filename)
            logs.append([l.split("\n")[0] for l in logfile.readlines()])
            logfile.close()

    ids = []
    announces = []

    for log in logs:
        ids.append(log[1].split(" ")[-1])
        tmp = []
        for logline in log:
            if "ANNOUNCE" in logline and logline.split(",")[2] == ids[-1]:
                tmp.append(float(logline.split(",")[0])/1000)
        announces.append(tmp)

    start = min2d(announces) + offset

    return [[announce-start for announce in announce_list] for announce_list in announces]

def min2d(arr2d):
    return min([min(arr) for arr in arr2d])

def max2d(arr2d):
    return max([max(arr) for arr in arr2d])

def flatten(arr2d):
    return sum(arr2d, [])

def mean(values):
    return sorted(values)[(len(values)+1)/2]

def avg(values):
    return sum(values) / len(values)

def computeAnnouncesPerSecond(announces, discreteness=1):
    duration = max2d(announces)
    count = int(duration / discreteness + discreteness + 1)
    x_values = [discreteness * (i) for i in range(count)]
    aps = [0] * count
    for nodeAnnounces in announces:
        for announce in nodeAnnounces:
            aps[int(announce / discreteness) + 1] += 1
    return (x_values, aps)

def splitExperiment(experiment, event_time=160):
    experiment_filtered = []
    for i in range(len(experiment)):
        node_announces = experiment[i]
        if i < len(experiment) / 2: experiment_filtered.append(node_announces)
        else: experiment_filtered.append([ann for ann in node_announces if ann < event_time])
    return experiment_filtered

def mergeExperiment(experiment, event_time=160):
    experiment_filtered = []
    for i in range(len(experiment)):
        node_announces = experiment[i]
        if i < len(experiment) / 2: experiment_filtered.append(node_announces)
        else: experiment_filtered.append([ann for ann in node_announces if ann > event_time])
    return experiment_filtered
    
def determineNames(paths):
    name_parts = [os.path.basename(os.path.normpath(path)).split("-")[:2] for path in paths]
    
    parts0 = zip(*name_parts)[0]
    parts1 = zip(*name_parts)[1]
    if all(x == parts0[0] for x in parts0): return list(parts1)
    if all(x == parts1[0] for x in parts1): return list(parts0)
    
    return ["-".join(part) for part in name_parts]
    