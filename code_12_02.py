import numpy as np
import heapq, itertools

inputFile = open("advent-of-code-2022-inputs/input_12.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

class Grid():
    def __init__(self, heightMap):
        self.heightMap = heightMap
        self.span = heightMap.shape
        self.nodes = [[None for cc in range(self.span[1])] for rr in range(self.span[0])]
        self.initNodes()

    def initNodes(self):
        for rr in range(self.span[0]):
            for cc in range(self.span[1]):
                self.nodes[rr][cc] = Node((np.array([rr]), np.array([cc])), self.heightMap[rr, cc])
                
        for rr in range(self.span[0]):
            for cc in range(self.span[1]):
                for action in [[0, 1], [0, -1], [-1, 0], [1, 0]]:
                    if(((rr + action[0] >= 0) & (rr + action[0] < self.span[0])) & ((cc + action[1] >= 0) & (cc + action[1] < self.span[1]))):
                        self.nodes[rr][cc].addNeighbor(self.nodes[rr + action[0]][cc + action[1]])

    def getMinDistance(self, startNodes, endNode):
        distMap = np.full(self.span, np.inf)

        (openSet, closedSet) = (PriorityQueue(), set())

        for s in startNodes:
            distMap[s.location] = 0
            openSet.add(s, 0)

        while(openSet.smallest() is not endNode):
            checkNode = openSet.pop()
            closedSet.add(checkNode)
            for neighbor in checkNode.neighbors:
                cost = distMap[checkNode.location] + checkNode.moveCost(neighbor)
                if(cost < distMap[neighbor.location]):
                    if(neighbor in openSet.entry_finder):
                        openSet.remove(neighbor)
                    elif(neighbor in closedSet):
                        closedSet.remove(neighbor)
                if((neighbor not in openSet.entry_finder) & (neighbor not in closedSet)):
                    distMap[neighbor.location] = cost
                    neighbor.parent = checkNode
                    openSet.add(neighbor, distMap[neighbor.location] + neighbor.h(endNode))
        return(distMap[endNode.location])

class Node():
    def __init__(self, location, height):
        self.location = location
        self.height = height
        self.parent = None
        self.neighbors = []

    def h(self, goalNode): # manhattan distance
        return(np.abs(self.location[0] - goalNode.location[0]) + np.abs(self.location[1] - goalNode.location[1]))

    def moveCost(self, nextNode):
        cost = 1 if (self.height - nextNode.height >= -1) else np.inf
        return cost

    def addNeighbor(self, neighbor):
        self.neighbors.append(neighbor)

class PriorityQueue():
    def __init__(self):
        self.entries = []
        self.entry_finder = {}
        self.counter = itertools.count()

    def add(self, task, priority, count=None):
        if task in self.entry_finder:
            self.remove(task)
        if(count is None):
            count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.entries, entry)
    
    def remove(self, task):
        entry = self.entry_finder.pop(task)
        entry[-1] = None

    def pop(self):
        while self.entries:
            priority, count, task = heapq.heappop(self.entries)
            if(task is not None):
                del self.entry_finder[task]
                return task
        raise KeyError('pop from empty queue')

    def smallest(self):
        while self.entries:
            priority, count, task = heapq.heappop(self.entries)
            if(task is not None):
                heapq.heappush(self.entries, [priority, count, task])
                return task
        raise KeyError('retrieve from empty queue')

heightMap = np.array([[ord(a) - 97 for a in list(l.strip())] for l in inputDat])
(startLoc, endLoc) = (np.nonzero(heightMap == -14), np.nonzero(heightMap == -28))
(heightMap[startLoc], heightMap[endLoc]) = (0, 25)
grid = Grid(heightMap)

startLocs = np.argwhere(heightMap == 0)
endNode = grid.nodes[endLoc[0][0]][endLoc[1][0]]

startNodes = [grid.nodes[s[0]][s[1]] for s in startLocs]
minDist = grid.getMinDistance(startNodes, endNode)

print(minDist)
