import numpy as np
import re

inputFile = open("advent-of-code-2022-inputs/input_22.txt", "r")
inputDat = inputFile.readlines()
inputFile.close()

instructions = [x for x in re.split('(\d+)', inputDat[-1][0:-1]) if x != '']

map = []
for l in inputDat[0:-2]:
    map.append([-1 if (x == ' ') else (0 if (x == '.') else 1) for x in list(l[0:-1])])
(numRows, numCols) = (len(map), 1)
for row in map:
    numCols = max(numCols, len(row))
for row in map:
    numAppend = numCols - len(row)
    if(numAppend > 0):
        row.extend([-1 for x in range(0, numAppend)])
map = np.array(map)

# traveling up/down is rows, left/right is columns
facings = [np.array([0, 1]), np.array([1, 0]), np.array([0, -1]), np.array([-1, 0])]

(currentPoint, currentFacing) = (np.array([0, [x for x in range(0, numCols) if (map[0, x] == 0)][0]]), 0)

print("Current Point: " + str(currentPoint) + ", facing: " + str(facings[currentFacing]))
for i in instructions:
    if(i.isdigit()): # walk forward
        steps = int(i)
        while(steps > 0):
            nextStep = np.array([(currentPoint[0] + facings[currentFacing][0]) % numRows, (currentPoint[1] + facings[currentFacing][1]) % numCols])
            while(map[nextStep[0], nextStep[1]] == -1):
                nextStep = np.array([(nextStep[0] + facings[currentFacing][0]) % numRows, (nextStep[1] + facings[currentFacing][1]) % numCols])

            if(map[nextStep[0], nextStep[1]] == 1): # hit a wall
                steps = 0
            elif(map[nextStep[0], nextStep[1]] == 0): # empty space, take a step
                currentPoint = nextStep
                steps -= 1
    else: # turn
        if(i == 'R'):
            currentFacing = (currentFacing + 1) % 4
        elif(i == 'L'):
            currentFacing = (currentFacing - 1) % 4
        else:
            print('instruction error')

print("Row: " + str(currentPoint[0] + 1) + ", Col: " + str(currentPoint[1] + 1) + ", Facing: " + str(currentFacing))
password = 1000*(currentPoint[0] + 1) + 4*(currentPoint[1] + 1) + currentFacing
print(password)
