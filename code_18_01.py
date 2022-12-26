import numpy as np
import scipy.spatial.distance as dist

inputFile = open("advent-of-code-2022-inputs/input_18.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

points = []
for l in inputDat:
    points.append([int(x) for x in list(l.strip().split(','))])
points = np.array(points)

pointDists = dist.pdist(points, 'cityblock')
numAdjacent = sum(pointDists == 1)
totalSides = len(points)*6

print(totalSides - numAdjacent*2)
