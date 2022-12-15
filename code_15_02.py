import re
import numpy as np
import scipy.spatial.distance as dist
import time

inputFile = open("advent-of-code-2022-inputs/input_15.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

sensor_beacon_pairs = []
for l in inputDat:
    sensor_beacon_pairs.append([int(s) for s in re.findall(r'-?\d+', l)])
(sensors, beacons) = (np.array([x[0:2] for x in sensor_beacon_pairs]), np.array([x[2:] for x in sensor_beacon_pairs]))
sensor_dists = np.diag(dist.cdist(sensors, beacons, 'cityblock'))

minV = 0
maxV = 4000000

sec = time.time()
testPoints = []
for sensor, d in zip(sensors, sensor_dists):
    peri = np.array([np.hstack((np.arange(sensor[0] - d - 1, sensor[0] + d + 2, 1),
                   np.arange(sensor[0] + d, sensor[0] - d - 1, -1))),
            np.hstack((np.arange(sensor[1], sensor[1] + d + 2, 1),
                   np.arange(sensor[1] + d, sensor[1] - d - 2, -1),
                   np.arange(sensor[1] - d, sensor[1], 1)))]).T
    peri = peri[np.argwhere(((peri[:, 0] >= minV) & (peri[:, 1] >= minV)) & ((peri[:, 0] <= maxV) & (peri[:, 1] <= maxV))), :]
    testPoints.append(peri)
testPoints = np.squeeze(np.unique(np.concatenate(testPoints), axis=0))
print(len(testPoints))
print(time.time() - sec)
sec = time.time()

lowVal = 0
jump = 1000000
for ii in range(jump, len(testPoints) + 1, jump):
    block = testPoints[lowVal:ii]
    testDists = dist.cdist(block, sensors, 'cityblock') # all distances from sensors, as (point, sensor)
    valid = block[np.nonzero(np.all(testDists > sensor_dists, axis = 1))]
    if(len(valid) > 0):
        print(valid)
        break
    lowVal = ii
print(time.time() - sec)
print(valid[0][0]*4000000 + valid[0][1])