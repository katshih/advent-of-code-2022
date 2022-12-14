import numpy as np

inputFile = open("advent-of-code-2022-inputs/input_14.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

class Cave():
    def __init__(self, paths, maxVals):
        self.floorDist = 2
        self.paths = paths
        (self.minX, self.maxX, self.minY, self.maxY) = maxVals
        self.minX -= 1000
        self.maxX += 1000
        self.maxY += self.floorDist
        self.grid = self.generateEmptyCave()

    def generateEmptyCave(self):
        grid = np.zeros((self.maxX - self.minX, self.maxY - self.minY))
        for path in self.paths:
            startPoint = path[0]
            for endPoint in path[1:]:
                (xStart, xEnd, yStart, yEnd) = (min(startPoint[0], endPoint[0]), max(startPoint[0], endPoint[0]), min(startPoint[1], endPoint[1]), max(startPoint[1], endPoint[1]))
                grid[xStart - self.minX:xEnd - self.minX + 1, yStart - self.minY:yEnd - self.minY + 1] = 1
                startPoint = endPoint
        grid[0:,-1] = 1
        return grid

    def prettyPrint(self):
        printVals = {0: '.', 1: '#', 2: 'o', 3: '+'}
        for row in self.grid.T:
            for el in row:
                print(printVals[el], end='')
            print('\n')
        print('\n')

    def pourSand(self, sandStart, maxGrains = np.inf):
        self.grid[sandStart[0] - self.minX, sandStart[1] - self.minY] = 3
        grains = 0
        blocked = False
        full = False

        while((not full) & (grains < maxGrains) & (not blocked)):
            grains = grains + 1
            activeGrainLoc = sandStart# + np.array([0, 1])
            atRest = False

            while(not atRest):
                nextPos = [activeGrainLoc + np.array([0, 1]), activeGrainLoc + np.array([-1, 1]), activeGrainLoc + np.array([1, 1])]
                lastGrainLoc = activeGrainLoc
                atRest = True
                for pos in nextPos:
                    if(((pos[0] < self.minX) | (pos[0] >= self.maxX)) | ((pos[1] < self.minY) | (pos[1] >= self.maxY))): # if it falls through, we're done
                        full = True
                        break
                    if(self.grid[pos[0] - self.minX, pos[1] - self.minY] == 0):
                        activeGrainLoc = pos
                        atRest = False
                        break
                self.grid[lastGrainLoc[0] - self.minX, lastGrainLoc[1] - self.minY] = 0
                if(full is False):
                    self.grid[activeGrainLoc[0] - self.minX, activeGrainLoc[1] - self.minY] = 2
                if(activeGrainLoc.all() == sandStart.all()):
                    blocked = True
        return grains, blocked


lines = []
(minX, maxX, minY, maxY) = (np.inf, -np.inf, np.inf, -np.inf)
for l in inputDat:
    indices = np.array([[int(i) for i in s.strip().split(',')] for s in l.strip().split('->')])
    (minX, maxX, minY, maxY) = (min(minX, min(indices[:,0])), max(maxX, max(indices[:,0])), min(minY, min(indices[:,1])), max(maxY, max(indices[:,1])))
    lines.append(indices)

sandStart = np.array([500, 0])
(minX, maxX, minY, maxY) = (min(minX, sandStart[0]), max(maxX, sandStart[0]) + 1, min(minY, sandStart[1]), max(maxY, sandStart[1]) + 1)

cave = Cave(lines, (minX, maxX, minY, maxY))
(grainNum, blocked) = cave.pourSand(sandStart)
cave.prettyPrint()

print(grainNum)
print(blocked)