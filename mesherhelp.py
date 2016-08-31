import os

def getAnnouncesFromPath(path):
    mesher_root = os.path.join(path, "mesher/")
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

    start = min2d(announces)

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
