import re
import numpy as np
import scipy.spatial.distance as dist

inputFile = open("advent-of-code-2022-inputs/input_15.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

target_line = 2000000

sensor_beacon_pairs = []
for l in inputDat:
    sensor_beacon_pairs.append([int(s) for s in re.findall(r'-?\d+', l)])
(sensors, beacons) = (np.array([x[0:2] for x in sensor_beacon_pairs]), np.array([x[2:] for x in sensor_beacon_pairs]))
sensor_dists = np.diag(dist.cdist(sensors, beacons, 'cityblock'))
(minX, maxX, minY, maxY) = (int(min(min(sensors[:,0] - sensor_dists), min(beacons[:,0]))), 
                            int(max(max(sensors[:,0] + sensor_dists), max(beacons[:,0]))),
                            int(min(min(sensors[:,1] - sensor_dists), min(beacons[:,1]))),
                            int(max(max(sensors[:,1] + sensor_dists), max(beacons[:,1]))))

target_points = np.array([[x, target_line] for x in range(minX, maxX + 1)]) # all points on the target line
target_dists = dist.cdist(target_points, sensors, 'cityblock') # all distances from sensors, as (point, sensor)
line_beacons = np.unique([b for b in beacons if(b[1] == target_line)], axis = 0)

invalid_points = np.sum(np.any(target_dists <= sensor_dists, axis = 1)) - len(line_beacons)
print(invalid_points)