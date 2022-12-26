import numpy as np
import scipy.spatial.distance as dist
import queue

inputFile = open("advent-of-code-2022-inputs/input_18.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

points = []
for l in inputDat:
    points.append([int(x) for x in list(l.strip().split(','))])
(xMin, yMin, zMin) = (min([point[0] for point in points]) - 1, min([point[1] for point in points]) - 1, min([point[2] for point in points]) - 1)
(xMax, yMax, zMax) = (max([point[0] for point in points]) + 1, max([point[1] for point in points]) + 1, max([point[2] for point in points]) + 1)
print("Cube is x = (" + str(xMin) + ", " + str(xMax) + "); y = (" + str(yMin) + ", " + str(yMax) + "); z = (" + str(zMin) + ", " + str(zMax) + ")")
boundVals = (xMin, xMax, yMin, yMax, zMin, zMax)

def getNeighbors(pt, boundVals):
    (xMin, xMax, yMin, yMax, zMin, zMax) = boundVals
    steps = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
    neighbors = []
    for s in steps:
        newPt = [pt[0] + s[0], pt[1] + s[1], pt[2] + s[2]]
        if((((newPt[0] >= xMin) & (newPt[0] <= xMax)) & ((newPt[1] >= yMin) & (newPt[1] <= yMax))) & ((newPt[2] >= zMin) & (newPt[2] <= zMax))):
            neighbors.append(newPt)
    return neighbors

airParticles = []
airQueue = queue.Queue()
airQueue.put([xMin, yMin, zMin])

while(not airQueue.empty()):
    test = airQueue.get()
    if((test not in points) & (test not in airParticles)):
        airParticles.append(test)
        neighbors = getNeighbors(test, boundVals)
        for n in neighbors:
            airQueue.put(n)

airParticles = np.array(airParticles)

pointDists = dist.pdist(airParticles, 'cityblock')
numAdjacent = sum(pointDists == 1)
totalSides = len(airParticles)*6
exteriorSides = 2*((xMax - xMin + 1)*(yMax - yMin + 1) + (yMax - yMin + 1)*(zMax - zMin + 1) + (zMax - zMin + 1)*(xMax - xMin + 1))

print(totalSides - numAdjacent*2 - exteriorSides)
