import queue
import numpy as np

inputFile = open("advent-of-code-2022-inputs/input_24.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

map = []
for l in inputDat:
    map.append(list(l.strip()))
rowTotal = len(map)
colTotal = len(map[0])

startPos = [0, 1]
goalPos = [rowTotal - 1, colTotal - 2]
modFactor = np.lcm(rowTotal - 2, colTotal - 2)

def inMap(pos, map):
    return (((pos[0] >= 0) & (pos[1] >= 0)) & ((pos[0] < len(map)) & (pos[1] < len(map[0]))))

def notBlocked(pos, map, block):
        return map[pos[0]][pos[1]] != block

def noBlizzard(pos, map, time):
    (row, col, maxRow, maxCol) = (pos[0], pos[1], len(map) - 2, len(map[0]) - 2)
    return (((map[row][(col - time - 1) % maxCol + 1] != '>')
           & (map[row][(col + time - 1) % maxCol + 1] != '<'))
          & ((map[(row - time - 1) % maxRow + 1][col] != 'v')
           & (map[(row + time - 1) % maxRow + 1][col] != '^')))

def fastestCrossing(start, end, modFactor, startTime):
    actions = [[0, 1], [1, 0], [0, -1], [-1, 0], [0, 0]]
    pathQueue = queue.Queue()
    pathQueue.put((startTime, [start]))

    seen = set((startTime, tuple(start)))
    while(not pathQueue.empty()):
        (time, path) =  pathQueue.get()
        if(path[-1] != end):
            for action in actions:
                newPos = [path[-1][0] + action[0], path[-1][1] + action[1]]
                if(inMap(newPos, map)):
                    if(notBlocked(newPos, map, '#') & noBlizzard(newPos, map, time + 1)):
                        if(((time + 1) % modFactor, tuple(newPos)) not in seen):
                            seen.add(((time + 1) % modFactor, tuple(newPos)))
                            pathQueue.put((time + 1, path + [newPos]))
        else:
            bestTime = time
            break
    return bestTime

bestTime = fastestCrossing(startPos, goalPos, modFactor, 0)
bestTime = fastestCrossing(goalPos, startPos, modFactor, bestTime)
bestTime = fastestCrossing(startPos, goalPos, modFactor, bestTime)

print(bestTime)
